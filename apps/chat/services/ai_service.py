"""
AI Service - Ket hop Ollama + OpenRouter + Groq (FREE TIER) + RAG Knowledge Base
Uu tien: Ollama (local) -> OpenRouter -> Groq -> Gemini -> Rule-based
RAG: Tu dong lay kien thuc tu KnowledgeChunk, Product, FAQ, Policy
"""
import os
import re
import logging
import json
import time
from typing import Dict, List, Tuple, Optional
from django.conf import settings
from django.db.models import Q

from .rule_based import FAQSystem
from .product_recommender import ProductRecommender

logger = logging.getLogger(__name__)

# Try to import KnowledgeChunk
try:
    from apps.chat.models import KnowledgeChunk
    HAS_KNOWLEDGE_CHUNK = True
except ImportError:
    HAS_KNOWLEDGE_CHUNK = False


# ============================================================================
# CẤU HÌNH - Ưu tiên từ .env
# ============================================================================

# Ollama Settings (Local - FREE!)
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.2')
OLLAMA_TIMEOUT = int(os.getenv('OLLAMA_TIMEOUT', '120'))

# OpenRouter Settings (Free Tier - $5 credit)
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', 'google/gemini-2.0-flash')  # FREE model!

# Groq Settings (Rất nhiều Free Credits!)
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.2-3b-vision')  # Miễn phí!

# Gemini (Backup)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# Priority: Ollama > OpenRouter > Groq > Gemini > Rule-based
AI_PROVIDER_PRIORITY = os.getenv('AI_PROVIDER_PRIORITY', 'ollama,openrouter,groq,gemini').split(',')


# ============================================================================
# CLASSES CHO TỪNG PROVIDER
# ============================================================================

class OllamaProvider:
    """Provider Ollama - Chạy local, hoàn toàn FREE!"""

    def __init__(self):
        self.base_url = OLLAMA_BASE_URL
        self.model = OLLAMA_MODEL
        self.timeout = OLLAMA_TIMEOUT

    def is_available(self) -> bool:
        """Kiểm tra Ollama có đang chạy không."""
        try:
            import requests
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m.get('name', '') for m in models]
                logger.info(f"Ollama available. Models: {model_names}")
                return True
            return False
        except Exception as e:
            logger.debug(f"Ollama not available: {e}")
            return False

    def generate(self, prompt: str, context: str = '') -> Optional[str]:
        """Gọi Ollama API."""
        try:
            import requests

            full_prompt = f"""Bạn là trợ lý AI thân thiện của TechStore - cửa hàng bán đồ công nghệ uy tín.
Hãy trả lời ngắn gọn, thân thiện bằng tiếng Việt (dưới 200 từ).
Luôn hỏi thêm nếu cần để tư vấn chính xác.

{context}

Khách hàng hỏi: {prompt}

Hãy trả lời ngắn gọn, đúng trọng tâm:"""

            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 500  # Giới hạn độ dài
                }
            }

            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            return None

        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return None

    def get_name(self) -> str:
        return f"Ollama ({self.model})"


class OpenRouterProvider:
    """Provider OpenRouter - Cloud với Free Tier"""

    FREE_MODELS = [
        'google/gemini-2.0-flash',  # Miễn phí!
        'anthropic/claude-3.5-haiku',
        'meta-llama/llama-3.2-3b-instruct',
        'deepseek/deepseek-chat-v3',
    ]

    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.model = OPENROUTER_MODEL

    def is_available(self) -> bool:
        """Kiểm tra API key có hợp lệ không."""
        return bool(self.api_key and len(self.api_key) > 10)

    def generate(self, prompt: str, context: str = '') -> Optional[str]:
        """Gọi OpenRouter API."""
        if not self.is_available():
            return None

        try:
            import requests

            full_prompt = f"""Bạn là trợ lý AI thân thiện của TechStore - cửa hàng bán đồ công nghệ uy tín.
Hãy trả lời ngắn gọn, thân thiện bằng tiếng Việt (dưới 200 từ).
Luôn hỏi thêm nếu cần để tư vấn chính xác.

{context}

Khách hàng hỏi: {prompt}

Hãy trả lời ngắn gọn, đúng trọng tâm:"""

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://techstore.com",
                "X-Title": "TechStore Chatbot",
            }

            payload = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": full_prompt}
                ],
                "max_tokens": 500,
                "temperature": 0.7,
            }

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content'].strip()
            else:
                logger.error(f"OpenRouter error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"OpenRouter error: {e}")
            return None

    def get_name(self) -> str:
        return f"OpenRouter ({self.model})"


class GroqProvider:
    """Provider Groq - Rất nhiều free credits! (14,400 req/phút)"""

    FREE_MODELS = [
        'llama-3.2-3b-vision',  # Miễn phí!
        'llama-3.1-8b-instant',
        'mixtral-8x7b-32768',
    ]

    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.model = GROQ_MODEL

    def is_available(self) -> bool:
        """Kiểm tra API key."""
        return bool(self.api_key and len(self.api_key) > 10)

    def generate(self, prompt: str, context: str = '') -> Optional[str]:
        """Gọi Groq API."""
        if not self.is_available():
            return None

        try:
            import requests

            full_prompt = f"""Bạn là trợ lý AI thân thiện của TechStore - cửa hàng bán đồ công nghệ uy tín.
Hãy trả lời ngắn gọn, thân thiện bằng tiếng Việt (dưới 200 từ).
Luôn hỏi thêm nếu cần để tư vấn chính xác.

{context}

Khách hàng hỏi: {prompt}

Hãy trả lời ngắn gọn, đúng trọng tâm:"""

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": full_prompt}
                ],
                "max_tokens": 500,
                "temperature": 0.7,
            }

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content'].strip()
            else:
                logger.error(f"Groq error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"Groq error: {e}")
            return None

    def get_name(self) -> str:
        return f"Groq ({self.model})"


class GeminiProvider:
    """Provider Gemini - Backup option"""

    def __init__(self):
        self.api_key = GEMINI_API_KEY or settings.GEMINI_API_KEY

    def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 10)

    def generate(self, prompt: str, context: str = '') -> Optional[str]:
        """Gọi Gemini API (dùng google.genai package mới)."""
        if not self.is_available():
            return None

        try:
            from google import genai

            client = genai.Client(api_key=self.api_key)

            full_prompt = f"""{context}

Khách hàng hỏi: {prompt}

Hãy trả lời ngắn gọn (dưới 200 từ), thân thiện, đúng trọng tâm bằng tiếng Việt."""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=full_prompt
            )
            return response.text.strip()

        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return None

    def get_name(self) -> str:
        return "Gemini"


# ============================================================================
# MAIN AI SERVICE CLASS
# ============================================================================

class AIService:
    """
    AI Service chính - Tự động chọn provider tốt nhất.
    Priority: Ollama > OpenRouter > Groq > Gemini > Rule-based
    """

    def __init__(self):
        # Initialize providers
        self.providers = {
            'ollama': OllamaProvider(),
            'openrouter': OpenRouterProvider(),
            'groq': GroqProvider(),
            'gemini': GeminiProvider(),
        }

        # Initialize rule-based systems
        self.faq = FAQSystem()
        self.recommender = ProductRecommender()

        # Cache
        self._provider_status = {}
        self._init_status()

    def _init_status(self):
        """Kiểm tra trạng thái các provider."""
        logger.info("=" * 50)
        logger.info("KIỂM TRA TRẠNG THÁI AI PROVIDERS:")
        logger.info("=" * 50)

        for name, provider in self.providers.items():
            status = "✓" if provider.is_available() else "✗"
            logger.info(f"  [{status}] {provider.get_name()}")

        logger.info("=" * 50)

    def detect_intent(self, message: str) -> Tuple[str, float]:
        """Nhận diện intent từ tin nhắn."""
        msg_lower = message.lower().strip()

        intent_scores = {}

        # Định nghĩa intent patterns
        intents = {
            'greeting': {
                'keywords': [r'chào', r'xin chào', r'hello', r'hi', r'hey', r'alo', r'ở đây', r'có ai'],
                'weight': 1,
            },
            'thanks': {
                'keywords': [r'cảm ơn', r'cám ơn', r'thanks', r'tks'],
                'weight': 1,
            },
            'product_inquiry': {
                'keywords': [r'tìm', r'mua', r'xem', r'so sánh', r'điện thoại', r'laptop', r'máy', r'sản phẩm', r'có bán', r'cần mua', r'tư vấn', r'gợi ý', r'nên mua', r'chọn'],
                'weight': 2,
            },
            'price_inquiry': {
                'keywords': [r'giá', r'bao nhiêu', r'rẻ', r'đắt', r'khuyến mãi', r'giảm', r'sale'],
                'weight': 2,
            },
            'order_status': {
                'keywords': [r'đơn hàng', r'theo dõi', r'giao hàng', r'vận chuyển', r'đã đặt', r'order', r'tình trạng'],
                'weight': 2,
            },
            'return_policy': {
                'keywords': [r'đổi', r'trả', r'bảo hành', r'hoàn tiền', r'warranty'],
                'weight': 1,
            },
            'payment': {
                'keywords': [r'thanh toán', r'chuyển khoản', r'cod', r'momo', r'visa', r'thẻ', r'tiền mặt'],
                'weight': 1,
            },
            'shipping': {
                'keywords': [r'giao hàng', r'ship', r'vận chuyển', r'nhận hàng', r'phí ship', r'free ship'],
                'weight': 1,
            },
            'contact': {
                'keywords': [r'liên hệ', r'hotline', r'số điện thoại', r'email', r'địa chỉ', r'cửa hàng'],
                'weight': 1,
            },
            'complaint': {
                'keywords': [r'kém', r'chán', r'không hài lòng', r'phàn nàn', r'tệ', r'sai', r'lỗi', r'không', r'chưa'],
                'weight': 2,
            },
        }

        for intent, config in intents.items():
            score = 0
            for kw in config['keywords']:
                if re.search(kw, msg_lower):
                    score += config['weight']
            if score > 0:
                intent_scores[intent] = score

        if not intent_scores:
            return 'unknown', 0.0

        best_intent = max(intent_scores, key=intent_scores.get)
        confidence = min(sum(intent_scores.values()) / 4.0, 1.0)
        return best_intent, confidence

    def search_knowledge(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Tim kiem kien thuc trong RAG knowledge base.
        Su dung keyword matching thay vi vector search (de don gian, khong can embeddings).
        """
        if not HAS_KNOWLEDGE_CHUNK:
            return []

        try:
            query_lower = query.lower()
            query_words = re.findall(r'\w+', query_lower)

            all_chunks = KnowledgeChunk.objects.filter(is_active=True)

            scored_chunks = []
            for chunk in all_chunks:
                content_lower = chunk.content.lower()
                score = 0

                for word in query_words:
                    if len(word) < 2:
                        continue
                    if word in content_lower:
                        score += 2
                    if word in chunk.category.lower():
                        score += 3

                intent_keywords = {
                    'giao hang': ['giao hang', 'ship', 'van chuyen', 'nhan hang'],
                    'thanh toan': ['thanh toan', 'cod', 'chuyen khoan', 'vnpay', 'momo'],
                    'doi tra': ['doi tra', 'hoan tien', 'bao hanh', 'warranty'],
                    'san pham': ['san pham', 'mua', 'gia', 'chat luong'],
                    'ho tro': ['ho tro', 'hotline', 'lien he', 'email'],
                    'dat hang': ['dat hang', 'order', 'mua hang'],
                }

                for category, keywords in intent_keywords.items():
                    if any(kw in query_lower for kw in keywords):
                        if any(kw in content_lower for kw in keywords):
                            score += 5
                            break

                if score > 0:
                    scored_chunks.append({
                        'chunk': chunk,
                        'score': score,
                        'content': chunk.content,
                        'source': chunk.source_type,
                    })

            scored_chunks.sort(key=lambda x: x['score'], reverse=True)
            return scored_chunks[:top_k]
        except Exception as e:
            logger.error(f"Knowledge search error: {e}")
            return []

    def build_context(self, message: str, intent: str) -> str:
        """Xay dung context cho AI tu RAG knowledge base + san pham lien quan."""
        context_lines = [
            "Thong tin cua hang TechStore:",
            "- TechStore - Cu hang ban do cong nghe uy tin",
            "- Hotline: 0123-456-789",
            "- Dia chi: 123 Duong ABC, Quan 1, TP.HCM",
            "- Gio lam viec: 8h-22h (24/7 online)",
        ]

        if HAS_KNOWLEDGE_CHUNK:
            knowledge = self.search_knowledge(message, top_k=5)
            if knowledge:
                context_lines.append("\nKien thuc co the thuong gap:")
                seen_categories = set()
                for item in knowledge:
                    cat = item['chunk'].category
                    if cat and cat not in seen_categories:
                        seen_categories.add(cat)
                        context_lines.append(f"- [{item['source']}] {item['content'][:200]}")

        products = self.recommender.get_recommendations(message, top_k=3)
        if products:
            context_lines.append("\nSan pham lien quan:")
            for p in products:
                price = p.get('price', 0) or 0
                price_str = f"{price:,.0f}".replace(",", ".") if price else "Lien he"
                context_lines.append(f"- {p.get('name')}: {price_str}d ({p.get('category', '')})")

        return "\n".join(context_lines)

    def generate_with_provider(self, prompt: str, provider_name: str, context: str = '') -> Tuple[Optional[str], str]:
        """Gọi một provider cụ thể."""
        provider = self.providers.get(provider_name)
        if not provider or not provider.is_available():
            return None, provider_name

        result = provider.generate(prompt, context)
        return result, provider_name

    def generate_response(self, message: str) -> Tuple[str, str, List[Dict], bool]:
        """
        Tạo phản hồi AI - Tự động chọn provider tốt nhất.
        Trả về: (message, intent, products, should_escalate)
        """
        intent, confidence = self.detect_intent(message)
        products = self.recommender.get_recommendations(message, top_k=3)

        # 1. Thử FAQ rule-based trước (nhanh nhất, free)
        faq_response = self.faq.get_response(message, intent)
        if faq_response and intent in ['shipping', 'return_policy', 'payment', 'contact', 'warranty', 'promotion', 'installment', 'working_hours']:
            logger.info(f"Using FAQ for intent: {intent}")
            return faq_response, intent, products, False

        # 2. Thử các AI provider theo thứ tự ưu tiên
        context = self.build_context(message, intent)

        for provider_name in AI_PROVIDER_PRIORITY:
            provider_name = provider_name.strip()
            if provider_name not in self.providers:
                continue

            logger.info(f"Trying provider: {provider_name}")
            result, used_provider = self.generate_with_provider(message, provider_name, context)

            if result:
                logger.info(f"Success with: {used_provider}")
                return result, intent, products, False

        # 3. Fallback: rule-based response
        logger.info("Using rule-based fallback")
        return self._get_default_response(intent), intent, products, False

    def _get_default_response(self, intent: str) -> str:
        """Phản hồi mặc định theo intent."""
        defaults = {
            'product_inquiry': "Bạn đang quan tâm đến sản phẩm nào ạ? TechStore có đa dạng laptop, điện thoại, tablet và phụ kiện công nghệ. Hãy cho mình biết thêm chi tiết để được tư vấn tốt nhất nhé!",
            'price_inquiry': "TechStore luôn có giá tốt nhất thị trường! Bạn có thể cho mình biết sản phẩm cụ thể để kiểm tra giá và khuyến mãi hiện có không?",
            'order_status': "Bạn có thể cung cấp mã đơn hàng để mình kiểm tra tình trạng không? Hoặc đăng nhập tài khoản để xem lịch sử đặt hàng.",
            'unknown': "Mình chưa hiểu rõ ý bạn lắm. Bạn có thể diễn đạt lại được không? Hoặc nhấn vào 'Gặp quản trị viên' để được hỗ trợ trực tiếp nhé!",
        }
        return defaults.get(intent, "Bạn cần mình hỗ trợ gì thêm không? TechStore luôn sẵn sàng giúp đỡ bạn!")

    def get_status(self) -> Dict:
        """Lấy trạng thái các provider."""
        return {
            name: {
                'available': provider.is_available(),
                'name': provider.get_name(),
            }
            for name, provider in self.providers.items()
        }


# Singleton instance
ai_service = AIService()
