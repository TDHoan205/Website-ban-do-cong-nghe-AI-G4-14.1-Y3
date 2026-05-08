"""
FAQ Knowledge Base - Hệ thống trả lời câu hỏi thường gặp.
"""
import re
from typing import Optional, Dict, List, Tuple


FAQ_ANSWERS: Dict[str, Dict] = {
    'shipping': {
        'keywords': ['giao hàng', 'vận chuyển', 'ship', 'nhận hàng', 'phí ship', 'free ship', 'giao trong'],
        'answer': (
            "📦 **Thông tin giao hàng:**\n\n"
            "• Nội thành Hà Nội: 1-2 ngày\n"
            "• Tỉnh khác: 3-5 ngày\n"
            "• Miễn phí vận chuyển cho đơn từ **500.000đ**\n"
            "• Phí 30.000đ cho đơn dưới 500.000đ\n\n"
            "📍 Giao hàng toàn quốc, kiểm tra hàng trước khi thanh toán!"
        ),
    },
    'return': {
        'keywords': ['đổi trả', 'trả hàng', 'hoàn tiền', 'đổi', 'trả', 'không ưng'],
        'answer': (
            "🔄 **Chính sách đổi trả:**\n\n"
            "• Đổi trả trong **7 ngày** (kể từ ngày nhận hàng)\n"
            "• Sản phẩm còn nguyên vẹn, đầy đủ phụ kiện, chưa qua sử dụng\n"
            "• Có hóa đơn mua hàng hoặc xác nhận đơn hàng\n"
            "• Phụ kiện đi kèm phải còn đầy đủ, nguyên seal\n\n"
            "📞 Liên hệ hotline **1800.6601** (Nhánh 1) để được hỗ trợ đổi trả nhanh nhất!"
        ),
    },
    'payment': {
        'keywords': ['thanh toán', 'cod', 'chuyển khoản', 'momo', 'zalopay', 'visa', 'mastercard', 'thẻ'],
        'answer': (
            "💳 **Phương thức thanh toán:**\n\n"
            "• **COD** - Thanh toán khi nhận hàng (phí thu hộ 15.000đ)\n"
            "• **Chuyển khoản** ngân hàng (không phí)\n"
            "• **Ví điện tử**: Momo, ZaloPay, VNPay\n"
            "• **Thẻ**: Visa, Mastercard, JCB\n\n"
            "✅ Thanh toán online được **giảm thêm 50.000đ** cho đơn từ 1.000.000đ!"
        ),
    },
    'warranty': {
        'keywords': ['bảo hành', 'bh', 'warranty', 'hư', 'lỗi', 'hỏng', 'bảo hành'],
        'answer': (
            "🛡️ **Chính sách bảo hành:**\n\n"
            "• **Điện thoại**: Bảo hành 12-24 tháng (tùy hãng)\n"
            "• **Laptop**: Bảo hành 12-36 tháng (tùy hãng)\n"
            "• **Phụ kiện**: Bảo hành 6-12 tháng\n"
            "• Bảo hành chính hãng tại trung tâm bảo hành ủy quyền\n"
            "• **GIỮ HÓA ĐƠN** để được bảo hành đầy đủ\n\n"
            "📞 Hỗ trợ bảo hành: **1800.6601** (Nhánh 2)"
        ),
    },
    'contact': {
        'keywords': ['liên hệ', 'hotline', 'số điện thoại', 'email', 'địa chỉ', 'cửa hàng', 'shop'],
        'answer': (
            "📞 **Liên hệ TechStore:**\n\n"
            "• **Hotline**: 1800.6601 (8h-22h, 24/7 online)\n"
            "• **Email**: TechStore@gmail.com\n"
            "• **Địa chỉ**: Đường Trịnh Văn Bô, Nam Từ Liêm, Hà Nội\n"
            "• **Website**: techstore.com\n\n"
            "💬 Chat trực tuyến 24/7 hoặc ghé showroom để trải nghiệm sản phẩm!"
        ),
    },
    'working_hours': {
        'keywords': ['giờ làm', 'mấy giờ', 'giờ mở', 'giờ đóng', 'thời gian mở'],
        'answer': (
            "🕐 **Giờ làm việc:**\n\n"
            "• **Showroom**: 8h00 - 22h00 (Tất cả các ngày)\n"
            "• **Online**: 24/7 (Luôn có nhân viên hỗ trợ)\n"
            "• **Hotline**: 8h00 - 22h00\n\n"
            "📍 Ngoài giờ, bạn có thể đặt hàng online - chúng tôi sẽ giao ngay khi mở cửa!"
        ),
    },
    'promotion': {
        'keywords': ['khuyến mãi', 'giảm giá', 'sale', ' voucher', 'coupon', 'ưu đãi', 'flash sale'],
        'answer': (
            "🎁 **Khuyến mãi hiện có:**\n\n"
            "• **Giảm 10-30%** cho các sản phẩm laptop\n"
            "• **Giảm 5-15%** cho điện thoại flagship\n"
            "• **Miễn phí vận chuyển** đơn từ 500.000đ\n"
            "• **Giảm thêm 50.000đ** khi thanh toán online\n"
            "• **Trả góp 0%** qua thẻ tín dụng\n\n"
            "🔔 Theo dõi website và fanpage để cập nhật khuyến mãi mới nhất nhé!"
        ),
    },
    'installment': {
        'keywords': ['trả góp', 'installment', 'trả chậm', 'kỳ hạn', 'lãi xuất'],
        'answer': (
            "💰 **Trả góp - Mua trước trả sau:**\n\n"
            "• **Trả góp 0%** qua thẻ tín dụng (Visa, Mastercard)\n"
            "• Trả góp qua công ty tài chính: 6-12 tháng\n"
            "• Chỉ cần CMND + GPLX, duyệt trong 15 phút\n"
            "• Trả trước tối thiểu **10-20%** giá trị sản phẩm\n\n"
            "📞 Đăng ký trả góp: **1800.6601** (Nhánh 3)"
        ),
    },
    'auth_check': {
        'keywords': ['tài khoản', 'đăng nhập', 'đăng ký', 'quên mật khẩu', 'reset'],
        'answer': (
            "🔐 **Tài khoản TechStore:**\n\n"
            "• Đăng ký tài khoản để theo dõi đơn hàng, tích điểm\n"
            "• Quên mật khẩu: Nhấn 'Quên mật khẩu' tại trang đăng nhập\n"
            "• Đăng nhập bằng email hoặc số điện thoại\n"
            "• Tài khoản được bảo mật theo tiêu chuẩn quốc tế\n\n"
            "📝 Nếu gặp vấn đề đăng nhập, liên hệ **1800.6601** (Nhánh 4) để được hỗ trợ."
        ),
    },
}


class FAQSystem:
    def __init__(self):
        self.faqs = FAQ_ANSWERS

    def find_matching_faq(self, message: str) -> Tuple[Optional[str], str]:
        """Tìm FAQ phù hợp nhất với tin nhắn."""
        msg_lower = message.lower().strip()

        best_match = None
        best_score = 0

        for faq_key, faq_data in self.faqs.items():
            score = 0
            for keyword in faq_data.get('keywords', []):
                keyword_lower = keyword.lower()
                if keyword_lower in msg_lower:
                    score += 1
                if re.search(r'\b' + re.escape(keyword_lower) + r'\b', msg_lower):
                    score += 2

            if score > best_score:
                best_score = score
                best_match = faq_key

        if best_score >= 1:
            return best_match, self.faqs[best_match]['answer']

        return None, ""

    def get_response(self, message: str, intent: str = None) -> str:
        """Lấy phản hồi FAQ cho tin nhắn."""
        if intent:
            intent_to_faq = {
                'shipping': 'shipping',
                'return_policy': 'return',
                'payment': 'payment',
                'contact': 'contact',
            }
            if intent in intent_to_faq:
                return self.faqs.get(intent_to_faq[intent], {}).get('answer', '')

        faq_key, faq_answer = self.find_matching_faq(message)
        if faq_answer:
            return faq_answer

        return ""
