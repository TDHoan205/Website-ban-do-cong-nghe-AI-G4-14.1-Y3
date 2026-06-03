"""
RAG Engine - Orchestrator cho RAG Pipeline
Flow: detect intent → vector search (ưu tiên) → fallback keyword search → call Groq
"""
import re
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from Services.AI.GroqService import get_groq_service
from Services.AI.KnowledgeService import KnowledgeService
from Services.AI.EmbeddingService import get_embedding_service
from Services.AI.VectorStore import VectorStore

# Stop words tiếng Việt
STOP_WORDS = {
    "là", "của", "và", "hay", "hoặc", "cho", "với", "này", "đó",
    "thì", "được", "có", "không", "bạn", "tôi", "mình", "cái",
    "một", "những", "các", "nào", "gì", "sao", "thế", "bao",
    "ở", "từ", "đến", "về", "trong", "ngoài", "trên", "dưới",
    "rất", "lắm", "quá", "nhất", "nhé", "ạ", "nha", "hả",
    "the", "a", "an", "is", "are", "what", "how", "which",
    # Từ giao tiếp bổ sung
    "tư", "vấn", "cần", "tìm", "kiếm", "giúp", "hỗ", "trợ", "xem",
    "hỏi", "xin", "chào", "hello", "hi", "alo", "ad", "admin",
    "shop", "cửa", "hàng", "sản", "phẩm", "muốn", "mua", "bán",
    "lấy", "đặt", "ngay", "luôn", "chốt", "thêm", "vào", "giỏ",
}

# Từ cần loại khi tìm sản phẩm theo buy intent
BUY_STRIP_WORDS = {
    # Tiếng Việt (có dấu)
    "muốn", "mua", "cần", "cho", "tôi", "mình", "lấy", "đặt",
    "ngay", "luôn", "chốt", "thêm", "vào", "giỏ", "hàng",
    "chiếc", "cái", "máy", "một", "order", "điện", "thoại",
    # Tiếng Việt (không dấu — khách hay gõ tắt)
    "muon", "can", "lay", "dat", "them", "vao", "gio",
    "chiec", "mot", "dien", "thoai", "luu", "luon", "chot",
    # Tiếng Anh
    "add", "cart", "buy", "want", "need", "please", "get", "want",
}


class RAGEngine:
    """RAG Pipeline orchestrator — vector search + keyword fallback"""

    def __init__(self, db: Session):
        self.db = db
        self.groq = get_groq_service()
        self.knowledge = KnowledgeService(db)
        self.embedder = get_embedding_service()
        self.vector_store = VectorStore(db)

    def get_response(
        self,
        user_message: str,
        conversation_history: List[Dict] = None,
        account_id: int = None,
    ) -> Dict:
        """Xử lý tin nhắn → response + metadata"""
        # 1. Detect intent
        intent = self._detect_intent(user_message)

        # 2. Retrieve context (vector-first, keyword fallback)
        context = self._retrieve_context(user_message, intent, account_id)

        # 3. Max tokens theo intent
        max_tokens = 512
        if intent in ("product_compare", "category_browse"):
            max_tokens = 768

        # 4. Call Groq LLM
        response = self.groq.chat(
            user_message=user_message,
            context=context,
            conversation_history=conversation_history,
            max_tokens=max_tokens,
        )

        # 5. Lấy product_ids nếu có intent mua hàng hoặc sản phẩm
        product_ids = []
        buy_products = []
        if intent in ("buy_intent", "product_query", "price_query"):
            buy_products = self._get_buy_products(user_message, intent)
            product_ids = self._extract_product_ids(buy_products)

        return {
            "response": response,
            "intent": intent,
            "product_ids": product_ids,
            "buy_products": buy_products,  # [{id, name, price}, ...]
        }

    # ─────────────── VECTOR SEARCH ───────────────

    def _vector_search(self, message: str, top_k: int = 5) -> str:
        """
        Embed query → cosine search → trả context text.
        Trả "" nếu embeddings không khả dụng hoặc không tìm thấy.
        """
        if not self.embedder.is_available():
            return ""

        try:
            query_vec = self.embedder.embed_query(message)
            if not query_vec:
                return ""

            results = self.vector_store.search(
                query_embedding=query_vec,
                top_k=top_k,
                threshold=0.35,
            )
            if not results:
                return ""

            # Format kết quả thành context
            lines = [f"=== TÌM THẤY {len(results)} KẾT QUẢ LIÊN QUAN ===\n"]
            for i, r in enumerate(results, 1):
                sim_pct = int(r["similarity"] * 100)
                lines.append(f"{i}. [{sim_pct}%] {r['content']}")
            return "\n".join(lines)

        except Exception as e:
            print(f"[RAGEngine] Vector search error: {e}")
            return ""

    # ─────────────── INTENT DETECTION ───────────────

    def _detect_intent(self, message: str) -> str:
        """Phân loại intent bằng keyword matching"""
        msg = message.lower()
        msg_stripped = msg.strip()

        # ── FIX #3: Exact match greeting — thoát nhanh, tránh false positive ──
        EXACT_GREETINGS = {
            "hi", "hello", "helo", "hey", "alo", "chào", "xin chào",
            "hi!", "hello!", "chào bạn", "xin chào bạn",
        }
        if msg_stripped in EXACT_GREETINGS:
            return "greeting"

        # Order lookup (ưu tiên cao)
        order_patterns = [
            r"đơn\s*hàng", r"đơn\s*#?\d+", r"mã\s*đơn", r"tra\s*cứu\s*đơn",
            r"kiểm\s*tra\s*đơn", r"trạng\s*thái\s*đơn", r"order",
            r"tracking", r"giao\s*hàng\s*đến\s*đâu",
        ]
        for pat in order_patterns:
            if re.search(pat, msg):
                return "order_lookup"

        compare_kws = ["so sánh", "compare", "vs", "nên mua", "chọn cái nào", "khác gì"]
        if any(kw in msg for kw in compare_kws):
            return "product_compare"

        HAS_PRICE_RE = r"\d+\s*(?:triệu|trieu|tr\b|củ|cu\b|lít|lit\b|nghìn|ngàn|k\b)"
        # FIX #3b: Bỏ "muốn mua"/"cần mua" khỏi price_kws — chuyển sang product_kws
        price_kws_strict = [
            "giá", "bao nhiêu", "price", "cost", "rẻ", "đắt",
            "tầm giá", "khoảng giá", "budget", "tầm tiền", "trong khoảng", "dưới",
        ]
        if re.search(HAS_PRICE_RE, msg) or any(kw in msg for kw in price_kws_strict):
            return "price_query"

        deal_kws = ["giảm giá", "khuyến mãi", "sale", "deal", "hot", "nổi bật", "bán chạy"]
        if any(kw in msg for kw in deal_kws):
            return "deals"

        cat_kws = ["danh mục", "loại", "category", "có gì", "bán gì", "có những"]
        if any(kw in msg for kw in cat_kws):
            return "category_browse"

        # ── BUY INTENT — ưu tiên trước product_query ──
        buy_kws = [
            "mua ngay", "cho mình mua", "cho tôi mua", "tôi muốn mua", "mình muốn mua",
            "tôi cần mua", "mình cần mua", "đặt hàng", "tôi lấy", "mình lấy",
            "mua cái", "mua chiếc", "mua máy", "mua điện thoại", "order ngay",
            "thêm vào giỏ", "add to cart", "muốn đặt", "mình đặt", "tôi đặt",
            "mua luôn", "chốt đơn", "mua cái này", "lấy cái này",
        ]
        if any(kw in msg for kw in buy_kws):
            return "buy_intent"

        product_kws = [
            "iphone", "samsung", "laptop", "macbook", "airpods", "ipad",
            "tablet", "tai nghe", "sạc", "ốp lưng", "chuột", "bàn phím",
            "màn hình", "điện thoại", "phone", "tư vấn", "gợi ý", "recommend",
            "tìm", "search", "sản phẩm", "mua",
            "oppo", "xiaomi", "vivo", "dell", "asus", "acer", "hp", "lenovo",
            "apple", "galaxy",
        ]
        if any(kw in msg for kw in product_kws):
            return "product_query"

        greet_kws = [
            "xin chào", "hello", "helo", "hela", "hola", "hi ", "hi!", "chào", "hey",
            "alo", "good morning", "good afternoon",
        ]
        if any(kw in msg for kw in greet_kws):
            return "greeting"

        policy_kws = ["bảo hành", "đổi trả", "hoàn tiền", "chính sách", "ship", "vận chuyển", "thanh toán", "trả góp"]
        if any(kw in msg for kw in policy_kws):
            return "policy"

        return "general"

    def _clean_search_query(self, message: str) -> str:
        """Lọc stop words"""
        words = message.lower().split()
        filtered = [w for w in words if w not in STOP_WORDS and len(w) > 1]
        return " ".join(filtered) if filtered else message.lower()

    # ─────────────── CONTEXT RETRIEVAL ───────────────

    def _retrieve_context(self, message: str, intent: str, account_id: int = None) -> str:
        """
        Truy vấn context — ƯU TIÊN vector search, fallback keyword search.
        Với order_lookup/policy: dùng logic đặc biệt, không cần vector.
        """
        if intent == "order_lookup":
            return self._handle_order_lookup(message, account_id)
        if intent == "policy":
            return self._get_policy_context()

        vector_context = self._vector_search(message, top_k=5)
        keyword_context = self._keyword_search(message, intent)

        # FIX #6: Merge + dedup trước khi gửi LLM — tiết kiệm tokens
        merged = "\n\n".join(filter(None, [vector_context, keyword_context]))
        return self._dedup_context(merged)

    def _dedup_context(self, context: str) -> str:
        """FIX #6: Loại bỏ dòng trùng lặp trong context — tiết kiệm tokens"""
        if not context:
            return context
        seen: set = set()
        lines = []
        for line in context.split("\n"):
            key = line.strip()
            if key and key in seen:
                continue
            seen.add(key)
            lines.append(line)
        return "\n".join(lines)

    def _keyword_search(self, message: str, intent: str) -> str:
        """Keyword search truyền thống — fallback khi vector search không đủ"""
        context_parts = []

        if intent == "product_compare":
            context_parts.append(self._handle_compare(message))

        elif intent == "price_query":
            context_parts.append(self._handle_price_query(message))

        elif intent == "deals":
            products = self.knowledge.get_deal_products(5)
            if not products:
                products = self.knowledge.get_hot_products(5)
            context_parts.append(self.knowledge.build_product_context(products))

        elif intent == "category_browse":
            categories = self.knowledge.get_all_categories()
            if categories:
                cat_text = "=== DANH MỤC SẢN PHẨM ===\n"
                for c in categories:
                    cat_text += f"- {c['name']}"
                    if c["description"]:
                        cat_text += f": {c['description']}"
                    cat_text += "\n"
                context_parts.append(cat_text)
            clean_q = self._clean_search_query(message)
            products = self.knowledge.search_products(clean_q, 5)
            if not products:
                products = self.knowledge.search_products_any(clean_q, 5)
            if products:
                context_parts.append(self.knowledge.build_product_context(products))

        elif intent == "buy_intent":
            product_q = self._extract_product_name_from_buy(message)
            products = self.knowledge.search_products(product_q, 3) if product_q else []
            if not products:
                products = self.knowledge.search_products_any(product_q or message, limit=3)
            if products:
                context_parts.append(self.knowledge.build_product_context(products))

        elif intent == "product_query":
            clean_q = self._clean_search_query(message)
            products = self.knowledge.search_products(clean_q, 5)
            if not products:
                products = self.knowledge.search_products_any(clean_q, 5)
            if products:
                context_parts.append(self.knowledge.build_product_context(products))

        elif intent == "greeting":
            hot = self.knowledge.get_hot_products(3)
            if not hot:
                # Fallback: lấy bất kỳ sản phẩm nào đang có
                hot = self.knowledge.get_price_range(limit=3)
            if hot:
                context_parts.append("=== SẢN PHẨM NỔI BẬT CỦA CỬA HÀNG ===\n"
                              + self.knowledge.build_product_context(hot))

        else:
            # General
            clean_q = self._clean_search_query(message)
            if len(clean_q) > 2:
                products = self.knowledge.search_products(clean_q, 3)
                if not products:
                    products = self.knowledge.search_products_any(clean_q, 3)
                if products:
                    context_parts.append(self.knowledge.build_product_context(products))

        return "\n\n".join(filter(None, context_parts))

    # ─────────────── BUY INTENT HELPERS ───────────────

    def _get_buy_products(self, message: str, intent: str) -> List[Dict]:
        """
        Tìm sản phẩm liên quan đến ý định mua.
        Bước 1: Strip buy-intent keywords khỏi message → lấy tên sản phẩm
        Bước 2: Tìm bằng từng keyword riêng lẻ (OR logic) nếu AND không có kết quả
        """
        # Bước 1: Tách tên sản phẩm khỏi câu mua hàng
        product_query = self._extract_product_name_from_buy(message)

        products = []

        # Bước 2: Tìm với query sạch (AND các keyword sản phẩm)
        if product_query and len(product_query.strip()) > 1:
            products = self.knowledge.search_products(product_query, 3)

        # Bước 3: Nếu AND không ra → tìm từng keyword riêng lẻ (OR fallback)
        if not products:
            products = self.knowledge.search_products_any(
                product_query or message, limit=3
            )

        return products[:3]

    def _extract_product_name_from_buy(self, message: str) -> str:
        """
        Loại bỏ các từ mua-bán khỏi message, giữ lại tên sản phẩm.
        Ví dụ: "tôi muốn mua iPhone 15 Pro Max" → "iphone 15 pro max"
        """
        all_strip = STOP_WORDS | BUY_STRIP_WORDS
        words = message.lower().split()
        filtered = [
            w for w in words
            if w not in all_strip and len(w) > 1
        ]
        return " ".join(filtered)

    def _extract_product_ids(self, products: List[Dict]) -> List[int]:
        """Trích xuất product_id từ danh sách dict sản phẩm"""
        return [p["id"] for p in products if p.get("id")]

    # ─────────────── HANDLERS ───────────────

    def _handle_order_lookup(self, message: str, account_id: int = None) -> str:
        match = re.search(r"#?(\d+)", message)
        if match:
            order_id = int(match.group(1))
            order_data = self.knowledge.lookup_order(order_id)
            if order_data:
                return self.knowledge.build_order_context(order_data)
            return f"Không tìm thấy đơn hàng #{order_id} trong hệ thống."

        if account_id:
            orders = self.knowledge.lookup_orders_by_account(account_id, 5)
            if orders:
                lines = ["=== ĐƠN HÀNG GẦN ĐÂY ===\n"]
                for o in orders:
                    lines.append(f"- Đơn #{o['order_id']} | {o['status']} | {o['total_amount']:,.0f}₫ | {o['order_date']}")
                return "\n".join(lines)

        return "Vui lòng cung cấp mã đơn hàng (ví dụ: #12345) để tra cứu."

    def _handle_compare(self, message: str) -> str:
        msg = message.lower()
        for kw in ["so sánh", "compare", "và", "vs", "with", "hay"]:
            msg = msg.replace(kw, "|")
        names = [n.strip() for n in msg.split("|") if n.strip() and len(n.strip()) > 2]

        if len(names) >= 2:
            products = self.knowledge.compare_products(names[:3])
            if products:
                return self.knowledge.build_product_context(products)

        clean_q = self._clean_search_query(message)
        products = self.knowledge.search_products(clean_q, 5)
        if products:
            return self.knowledge.build_product_context(products)
        return ""

    def _handle_price_query(self, message: str) -> str:
        msg = message.lower()

        # ── Phát hiện category từ câu hỏi — map sang keyword tìm DB ──
        # DB categories: "Điện thoại di động", "Laptop & Macbook", "Máy tính bảng", "Phụ kiện"
        CATEGORY_MAP = [
            ("di động",       ["điện thoại", "phone", "iphone", "samsung", "xiaomi", "oppo", "vivo", "realme", "di động"]),
            ("laptop",        ["laptop", "máy tính xách tay", "macbook", "dell", "asus", "hp", "lenovo", "acer"]),
            ("máy tính bảng", ["máy tính bảng", "tablet", "ipad"]),
            ("phụ kiện",      ["tai nghe", "airpods", "earphone", "headphone", "sạc", "ốp lưng", "cáp", "chuột", "bàn phím", "phụ kiện"]),
        ]
        detected_cat = None
        for db_keyword, triggers in CATEGORY_MAP:
            if any(kw in msg for kw in triggers):
                detected_cat = db_keyword
                break

        # ── Pattern 1: Dạng khoảng "X-Y triệu" hoặc "X đến Y triệu" ──
        UNIT = r"(?:triệu|trieu|tr(?![a-z])|củ|cu|lít|lit)"
        RANGE_RE = r"(\d+(?:[.,]\d+)?)\s*[-–~đến tới to]+\s*(\d+(?:[.,]\d+)?)\s*" + UNIT
        range_match = re.search(RANGE_RE, msg)
        if range_match:
            lo = float(range_match.group(1).replace(",", ".")) * 1_000_000
            hi = float(range_match.group(2).replace(",", ".")) * 1_000_000
            # Tìm theo category + khoảng giá trước
            if detected_cat:
                products = self.knowledge.get_price_range_by_category(
                    category_keyword=detected_cat, min_price=min(lo, hi), max_price=max(lo, hi), limit=5
                )
                if products:
                    return self.knowledge.build_product_context(products)
            # Fallback: tìm theo giá không filter category
            products = self.knowledge.get_price_range(min(lo, hi), max(lo, hi), 8)
            if products:
                return self.knowledge.build_product_context(products)

        # ── Pattern 2: Từng số riêng lẻ có đơn vị ──
        MILLION_RE = r"(\d+(?:[.,]\d+)?)\s*(?:triệu|trieu|tr(?![a-z])|củ|cu|lít|lit)"
        THOUSAND_RE = r"(\d+(?:[.,]\d+)?)\s*(?:nghìn|nghìn đồng|ngàn|k(?![a-z]))"
        mil_matches = re.findall(MILLION_RE, msg)
        tho_matches = re.findall(THOUSAND_RE, msg)

        prices = [float(n.replace(",", ".")) * 1_000_000 for n in mil_matches] + \
                 [float(n.replace(",", ".")) * 1_000 for n in tho_matches]

        if prices:
            if len(prices) >= 2:
                mn, mx = min(prices), max(prices)
            else:
                mn, mx = None, prices[0] * 1.2
            if detected_cat:
                products = self.knowledge.get_price_range_by_category(
                    category_keyword=detected_cat, min_price=mn, max_price=mx, limit=5
                )
                if products:
                    return self.knowledge.build_product_context(products)
            products = self.knowledge.get_price_range(mn, mx, 8)
            if products:
                return self.knowledge.build_product_context(products)

        clean_q = self._clean_search_query(message)
        products = self.knowledge.search_products(clean_q, 5)
        if not products:
            products = self.knowledge.search_products_any(clean_q, 5)
        if products:
            return self.knowledge.build_product_context(products)
        return ""

    def _get_policy_context(self) -> str:
        # Thử vector search cho FAQs chính sách trước
        faq_context = self._vector_search("chính sách bảo hành đổi trả vận chuyển", top_k=3)

        base = """=== CHÍNH SÁCH CỬA HÀNG TECH STORE ===

🔄 Đổi trả: 7 ngày đổi trả miễn phí nếu sản phẩm lỗi do nhà sản xuất
🛡️ Bảo hành: 12-24 tháng tùy sản phẩm, bảo hành chính hãng
🚚 Vận chuyển: Miễn phí ship đơn từ 500,000₫. Ship toàn quốc 2-5 ngày
💳 Thanh toán: COD, chuyển khoản, thẻ tín dụng, ví điện tử
📱 Trả góp: Hỗ trợ trả góp 0% qua thẻ tín dụng
📞 Hotline: 0123-456-789 (8h-22h hàng ngày)"""

        if faq_context:
            return base + "\n\n" + faq_context
        return base
