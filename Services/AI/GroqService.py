"""
Groq LLM Service - Gọi Groq API cho AI Chatbot
Singleton pattern để tái sử dụng client, tối ưu hiệu suất.
"""
import os
import time
import threading
from typing import List, Dict, Optional
# pyrefly: ignore [missing-import]
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# System prompt siết chặt — KHÔNG bịa, chỉ dựa vào context
SYSTEM_PROMPT = """Bạn là trợ lý AI của Tech Store - cửa hàng bán đồ công nghệ.

NHIỆM VỤ:
1. Tư vấn sản phẩm công nghệ (điện thoại, laptop, tablet, phụ kiện)
2. So sánh sản phẩm, giá cả
3. Tra cứu đơn hàng
4. Trả lời chính sách bảo hành, đổi trả

QUY TẮC BẮT BUỘC:
- Trả lời bằng tiếng Việt, ngắn gọn, thân thiện
- CHỈ trả lời dựa trên [THÔNG TIN TỪ CỬA HÀNG] được cung cấp bên dưới
- Nếu KHÔNG có thông tin trong context → NÓI RÕ: "Hiện tại mình chưa có thông tin về sản phẩm này trong hệ thống. Bạn có thể xem thêm tại trang Sản phẩm của cửa hàng nhé!"
- TUYỆT ĐỐI KHÔNG bịa giá, thông số, tên sản phẩm không có trong context
- TUYỆT ĐỐI KHÔNG đưa ra thông tin sản phẩm từ kiến thức riêng — chỉ dùng data cửa hàng cung cấp
- Giá hiển thị: 25,990,000₫
- Dùng emoji vừa phải 😊
- Trả lời tối đa 150 từ, trừ khi so sánh nhiều sản phẩm
"""


# Singleton GroqService — chỉ tạo 1 client duy nhất
_groq_instance = None
_groq_lock = threading.Lock()


def get_groq_service():
    """Lấy singleton GroqService instance"""
    global _groq_instance
    if _groq_instance is None:
        with _groq_lock:
            if _groq_instance is None:
                _groq_instance = GroqService()
    return _groq_instance


class GroqService:
    """Service gọi Groq API — singleton, tái sử dụng client"""

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY", "")
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.client = None
        self._init_client()

    def _init_client(self):
        """Khởi tạo Groq client"""
        if self.api_key and self.api_key != "gsk_your_key_here":
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                print(f"[GroqService] Error initializing client: {e}")
                self.client = None

    def is_available(self) -> bool:
        """Kiểm tra Groq API có sẵn sàng không"""
        return self.client is not None

    def chat(
        self,
        user_message: str,
        context: str = "",
        conversation_history: List[Dict[str, str]] = None,
        max_tokens: int = 512,
        temperature: float = 0.3,
    ) -> str:
        """
        Gọi Groq API để sinh phản hồi.
        - max_tokens=512: đủ cho câu trả lời ngắn gọn, giảm latency
        - temperature=0.3: ít sáng tạo → ít bịa, bám sát context
        """
        if not self.is_available():
            return self._fallback_response(user_message)

        messages = self._build_messages(user_message, context, conversation_history)

        # Retry tối đa 2 lần (3 attempts), backoff nhanh
        for attempt in range(3):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=0.85,
                    stop=None,
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"[GroqService] Attempt {attempt + 1} failed: {e}")
                if attempt < 2:
                    time.sleep(0.5 * (attempt + 1))
                continue

        return self._fallback_response(user_message)

    def _build_messages(
        self,
        user_message: str,
        context: str = "",
        conversation_history: List[Dict[str, str]] = None,
    ) -> List[Dict[str, str]]:
        """Xây dựng messages array — giới hạn history để tiết kiệm tokens"""
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        # Chỉ giữ 6 tin nhắn gần nhất (3 cặp user-bot) — tiết kiệm tokens
        if conversation_history:
            recent = conversation_history[-6:]
            for msg in recent:
                role = "user" if msg.get("sender") == "user" else "assistant"
                content = msg.get("content", "")
                # Cắt ngắn tin nhắn cũ quá dài
                if len(content) > 300:
                    content = content[:300] + "..."
                messages.append({"role": role, "content": content})

        # Augment user message với context
        if context:
            augmented_message = (
                f"[THÔNG TIN TỪ CỬA HÀNG]\n{context}\n\n"
                f"[CÂU HỎI CỦA KHÁCH HÀNG]\n{user_message}\n\n"
                f"Hãy trả lời CHỈ dựa trên thông tin ở trên. Nếu không có dữ liệu liên quan, hãy nói rõ."
            )
        else:
            augmented_message = (
                f"[THÔNG TIN TỪ CỬA HÀNG]\nKhông tìm thấy dữ liệu liên quan trong hệ thống.\n\n"
                f"[CÂU HỎI CỦA KHÁCH HÀNG]\n{user_message}\n\n"
                f"KHÔNG có thông tin sản phẩm trong hệ thống. Hãy trả lời phù hợp, KHÔNG bịa thông tin sản phẩm."
            )

        messages.append({"role": "user", "content": augmented_message})
        return messages

    def _fallback_response(self, user_message: str) -> str:
        """Phản hồi khi API không khả dụng"""
        return (
            "Xin lỗi, hệ thống AI đang bận. Vui lòng thử lại sau hoặc "
            "liên hệ hotline 0386-267-692 để được hỗ trợ trực tiếp! 🙏"
        )
