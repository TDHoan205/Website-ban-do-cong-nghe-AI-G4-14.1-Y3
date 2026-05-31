# CHƯƠNG III: KẾT QUẢ THỰC NGHIỆM CHƯƠNG TRÌNH

## 3.1. Mô tả kết quả kiểm thử các chức năng chương trình

### 3.1.1. Môi trường và cách thức kiểm thử

**Môi trường chạy thử:**
- Hệ điều hành: Windows 10/11
- Python: 3.10+
- Web Framework: FastAPI (Uvicorn)
- Database: SQL Server Express (`DESKTOP-1TM8FSO`)
- Database name: `TechShopWebsite2`
- Trình duyệt: Chrome / Edge (DevTools)

**Cấu hình kết nối Database** (`Data/database.py`):
```python
SQL_SERVER_CONFIG = {
    "server": os.getenv("DB_SERVER", "DESKTOP-1TM8FSO"),  # Tên SQL Server
    "database": "TechShopWebsite2",                        # Tên database
    "driver": "ODBC Driver 17 for SQL Server",
    "trusted_connection": "yes",                           # Windows Authentication
    # Nếu dùng SQL Authentication, bỏ comment và điền username/password
}
```

**Hình thức kiểm thử:**
1. **Kiểm thử thủ công trên trình duyệt** — theo từng trang/chức năng, đúng luồng người dùng (happy path + edge cases).
2. **Kiểm thử hỗ trợ bằng script nhanh:**

| Script | Mục đích |
|--------|-----------|
| `test_run.py` | Kiểm tra import các module, kết nối DB, truy vấn accounts |
| `test_auth.py` | Kiểm tra thông tin tài khoản trong DB (username, hash, role) |

Chạy script:
```bash
python test_run.py
python test_auth.py
```

---

### 3.1.2. Hai mẫu dữ liệu đầu vào dùng để kiểm thử

**Mẫu 1 — Tài khoản Khách hàng (Customer):**

| Thuộc tính | Giá trị |
|------------|---------|
| Username | `customer01` |
| Password | `customer123` |
| Role | Customer |
| Thao tác tiêu biểu | Tìm kiếm "laptop", chat "Tư vấn laptop", giỏ hàng thêm 1–2 sản phẩm, đổi số lượng, đổi màu/dung lượng variant |

**Mẫu 2 — Tài khoản Quản trị (Admin):**

| Thuộc tính | Giá trị |
|------------|---------|
| Username | `admin` |
| Password | `admin123` |
| Role | Admin |
| Thao tác tiêu biểu | Tạo danh mục mới (Phụ kiện), tạo/sửa sản phẩm (Tai nghe ABC, giá 790.000, tồn 20, Đang bán), duyệt đơn hàng |

> **Ghi chú:** Thông tin tài khoản mẫu được mô tả đầy đủ trong `README.md` (mục "Tài khoản mặc định").

---

### 3.1.3. Kết quả kiểm thử theo bảng ca kiểm thử (Test case)

---

#### A. Module Đăng nhập / Đăng ký / Đăng xuất (Authentication)

| STT | ID | Tên Test Case | Dữ liệu kiểm thử | Kết quả mong đợi |
|:---:|:---:|---------------|-------------------|-------------------|
| 1 | TC-A01 | Đăng nhập Admin hợp lệ | Username: `admin` / Password: `admin123` | Vào Dashboard quản trị (`/Admin/Dashboard`), hiển thị avatar/admin trên header |
| 2 | TC-A02 | Đăng nhập Customer hợp lệ | Username: `customer01` / Password: `customer123` | Vào trang chủ (`/`), hiển thị tên user và badge giỏ hàng trên header |
| 3 | TC-A03 | Đăng nhập sai mật khẩu | Username: `admin` / Password: `sai123` | Hiển thị thông báo lỗi "Sai thông tin đăng nhập", không chuyển trang |
| 4 | TC-A04 | Đăng nhập sai username | Username: `khongtontai` / Password: `admin123` | Hiển thị thông báo lỗi "Sai thông tin đăng nhập", không chuyển trang |
| 5 | TC-A05 | Bỏ trống thông tin đăng nhập | Để trống cả hai trường | Yêu cầu nhập đầy đủ thông tin, không gửi request |
| 6 | TC-A06 | Đăng ký tài khoản mới | Username: `newuser01`, Email: `newuser01@mail.com`, Password: `user123456`, Full name: `Nguyen Van Moi` | Tạo tài khoản thành công, chuyển về trang đăng nhập |
| 7 | TC-A07 | Đăng ký trùng username | Username: `admin` (đã tồn tại) | Báo lỗi "Tên đăng nhập đã tồn tại" |
| 8 | TC-A08 | Đăng ký mật khẩu quá ngắn | Password: `123` (< 6 ký tự) | Báo lỗi yêu cầu mật khẩu tối thiểu 6 ký tự |
| 9 | TC-A09 | Đăng xuất | Nhấn nút "Đăng xuất" từ header | Xóa cookie `access_token`, chuyển về trang chủ, header hiển thị nút "Đăng nhập / Đăng ký", badge giỏ hàng reset về 0 |
| 10 | TC-A10 | Truy cập trang Admin khi chưa đăng nhập | Không có cookie, truy cập `/Admin/Dashboard` | Chuyển hướng về trang đăng nhập quản trị (`/Auth/Login`) |

**Kết quả ghi nhận:** Tất cả 10 test case đều **Đạt** — Authentication hoạt động đúng theo thiết kế.

---

#### B. Module Cửa hàng & Giỏ hàng

| STT | ID | Tên Test Case | Dữ liệu kiểm thử | Kết quả mong đợi |
|:---:|:---:|---------------|-------------------|-------------------|
| 11 | TC-B01 | Xem trang chủ | Truy cập `/` | Hiển thị sản phẩm nổi bật (is_hot), sản phẩm mới (is_new), danh mục sản phẩm |
| 12 | TC-B02 | Tìm kiếm sản phẩm | Từ khóa: `laptop` | Hiển thị các sản phẩm có tên chứa "laptop" (MacBook, Dell XPS, ASUS ROG...) |
| 13 | TC-B03 | Lọc theo danh mục | Chọn danh mục: "Laptop & Macbook" | Chỉ hiển thị sản phẩm thuộc danh mục Laptop, có phân trang nếu nhiều kết quả |
| 14 | TC-B04 | Lọc theo khoảng giá | Min: 5.000.000 / Max: 20.000.000 VNĐ | Hiển thị sản phẩm trong khoảng giá đã chọn |
| 15 | TC-B05 | Sắp xếp theo "Mới nhất" | Sắp xếp: `is_new` | Danh sách ưu tiên sản phẩm mới nhất |
| 16 | TC-B06 | Sắp xếp theo "Hot" | Sắp xếp: `is_hot` | Danh sách ưu tiên sản phẩm hot nhất |
| 17 | TC-B07 | Xem chi tiết sản phẩm có variant | Sản phẩm: iPhone 15 Pro Max | Hiển thị gallery ảnh, mô tả, thông số kỹ thuật (JSON specifications), chip màu (Titan Tự nhiên, Titan Đen...), chip dung lượng (256GB, 512GB...), giá và tồn kho thay đổi khi chọn variant |
| 18 | TC-B08 | Xem chi tiết sản phẩm không có variant | Sản phẩm: AirPods Pro 2 | Hiển thị thông tin sản phẩm đơn lẻ, không có chip variant |
| 19 | TC-B09 | Thêm vào giỏ khi chưa đăng nhập | Sản phẩm: iPhone 15 Pro Max, chưa login | AJAX trả về 401, hiển thị toast yêu cầu đăng nhập |
| 20 | TC-B10 | Thêm sản phẩm vào giỏ (đã đăng nhập) | Sản phẩm: iPhone 15 Pro Max, quantity: 1 | Thêm thành công, badge giỏ hàng trên header tăng, toast xác nhận |
| 21 | TC-B11 | Thêm trùng sản phẩm đã có trong giỏ | Thêm cùng sản phẩm lần 2, quantity: 1 | Tăng số lượng của dòng hiện có, không tạo dòng mới, tổng tiền cập nhật |
| 22 | TC-B12 | Thêm vượt quá tồn kho | Thêm số lượng lớn hơn `stock_quantity` | Backend trả về lỗi, toast "Không đủ hàng trong kho" |
| 23 | TC-B13 | Cập nhật số lượng trong giỏ | Thay đổi số lượng từ 1 → 3 | Tổng tiền cập nhật chính xác theo số lượng mới × đơn giá |
| 24 | TC-B14 | Xóa sản phẩm khỏi giỏ | Nhấn nút xóa (biểu tượng thùng rác) | Dòng sản phẩm biến mất, tổng tiền cập nhật, badge giỏ hàng giảm |
| 25 | TC-B15 | Xóa toàn bộ giỏ hàng | Nhấn "Xóa toàn bộ giỏ hàng" | Giỏ hàng trống, tổng tiền = 0, badge reset về 0 |

**Kết quả ghi nhận:** Tất cả 15 test case đều **Đạt**.

---

#### C. Module Thanh toán & Đơn hàng

| STT | ID | Tên Test Case | Dữ liệu kiểm thử | Kết quả mong đợi |
|:---:|:---:|---------------|-------------------|-------------------|
| 26 | TC-C01 | Checkout khi chưa chọn variant | Giỏ có sản phẩm có variant nhưng chưa chọn color/storage | Điều hướng về giỏ hàng, toast yêu cầu chọn đầy đủ option |
| 27 | TC-C02 | Checkout khi đã chọn đủ variant | Giỏ hàng có đủ variant (color + storage) | Vào được trang checkout (`/Checkout/`), hiển thị form thông tin giao hàng, tổng tiền đã tính 10% VAT |
| 28 | TC-C03 | Checkout khi giỏ trống | Giỏ hàng = 0, truy cập `/Checkout/` | Chuyển về trang giỏ hàng, thông báo giỏ trống |
| 29 | TC-C04 | Thanh toán thiếu thông tin giao hàng | Bỏ trống SĐT hoặc địa chỉ | Không cho tạo đơn, báo lỗi yêu cầu nhập đầy đủ |
| 30 | TC-C05 | Tạo thanh toán QR banking | Điền đầy đủ, nhấn "Tiến hành đặt hàng" | Hiển thị trang QR với: mã đơn (DH...), mã QR VietQR, số tài khoản, nội dung CK = mã đơn, hạn 30 phút |
| 31 | TC-C06 | Xác nhận thanh toán (giả lập) | Nhấn "Tôi đã thanh toán" | Tạo đơn trong `Orders`, giỏ hàng xóa, badge reset về 0, chuyển `/Checkout/Success/` |
| 32 | TC-C07 | Thanh toán trùng lặp | Nhấn "Tôi đã thanh toán" 2 lần cùng mã QR | Lần 2 không tạo đơn mới, trả về đơn đã tạo |
| 33 | TC-C08 | Xem danh sách đơn hàng (khách) | Đăng nhập customer, truy cập `/Orders/` | Chỉ hiển thị đơn của tài khoản đó: mã đơn, ngày đặt, trạng thái, tổng tiền |
| 34 | TC-C09 | Xem chi tiết đơn hàng | Click vào một đơn | Hiển thị đầy đủ: thông tin người nhận, danh sách sản phẩm, số lượng, đơn giá, tổng tiền, trạng thái |
| 35 | TC-C10 | Hủy đơn hàng | Nhấn "Hủy đơn" trên đơn chưa giao | Trạng thái → Cancelled, tồn kho sản phẩm được hoàn lại |

**Kết quả ghi nhận:** Tất cả 10 test case đều **Đạt**.

---

#### D. Module Quản trị (Admin)

| STT | ID | Tên Test Case | Dữ liệu kiểm thử | Kết quả mong đợi |
|:---:|:---:|---------------|-------------------|-------------------|
| 36 | TC-D01 | Truy cập Admin khi chưa đăng nhập | Không đăng nhập, truy cập `/Admin/Dashboard` | Chuyển hướng về `/Auth/Login` hoặc HTTP 403 |
| 37 | TC-D02 | Truy cập Admin khi đăng nhập Customer | Đăng nhập `customer01`, truy cập `/Admin/Dashboard` | Bị từ chối, chuyển về trang chủ |
| 38 | TC-D03 | Truy cập Admin khi đăng nhập Admin | Đăng nhập `admin`, truy cập `/Admin/Dashboard` | Vào được Dashboard, hiển thị menu quản trị đầy đủ |
| 39 | TC-D04 | Xem Dashboard thống kê | Dashboard Admin | Hiển thị tổng sản phẩm, khách, đơn hàng, doanh thu, biểu đồ doanh thu tuần, top sp bán chạy |
| 40 | TC-D05 | Xem danh sách sản phẩm (Admin) | Truy cập `/Admin/Products/` | Bảng: tên, giá, tồn kho, trạng thái, ảnh; có tìm kiếm, phân trang |
| 41 | TC-D06 | Thêm sản phẩm mới | Tên: "Tai nghe XYZ", Giá: 790.000, Tồn: 20, Danh mục: Phụ kiện | Sản phẩm được tạo trong DB, hiển thị trong danh sách, đồng bộ vào `Inventory` |
| 42 | TC-D07 | Sửa sản phẩm | Đổi giá từ 790.000 → 890.000 | Giá mới được lưu, cập nhật ngay trên danh sách |
| 43 | TC-D08 | Xóa sản phẩm (chưa có đơn) | Nhấn Xóa → Xác nhận (sp chưa có đơn hàng) | Sản phẩm xóa khỏi DB và danh sách |
| 44 | TC-D09 | Xóa sản phẩm (đã có đơn hàng) | Nhấn Xóa (sp đã từng được đặt) | Soft-delete: `is_available = False`, không hiển thị ở cửa hàng, đơn cũ còn nguyên |
| 45 | TC-D10 | Thêm / sửa / xóa biến thể (variant) | Thêm variant: màu Đỏ, 128GB, giá 24.990.000 | Variant mới hiển thị trong chi tiết sản phẩm, khách chọn được |
| 46 | TC-D11 | Upload ảnh sản phẩm | Upload file `.jpg` qua form Admin | Ảnh lưu vào `wwwroot/uploads/products/`, đường dẫn lưu vào `ProductImages` |
| 47 | TC-D12 | Xem danh sách đơn hàng (Admin) | Truy cập `/Admin/Orders/` | Bảng đầy đủ: mã đơn, khách hàng, tổng tiền, trạng thái, ngày đặt; có tìm kiếm, lọc theo trạng thái |
| 48 | TC-D13 | Đổi trạng thái đơn hàng | Đổi từ "Pending" → "Shipped" | Trạng thái lưu thành công, tạo notification cho khách |
| 49 | TC-D14 | Hủy đơn hàng (Admin) | Nhấn hủy từ trang quản trị | Trạng thái → Cancelled, tồn kho hoàn lại |
| 50 | TC-D15 | Xem danh sách tài khoản | Truy cập `/Admin/Accounts/` | Bảng: username, email, role, trạng thái; có tìm kiếm, phân trang |
| 51 | TC-D16 | Tạo tài khoản mới (Admin) | Username: `staff02`, Role: Staff, Password: `staff123` | Tài khoản tạo trong `Accounts` và `Employees` |
| 52 | TC-D17 | Xóa tài khoản có đơn hàng | Nhấn Xóa (tài khoản đã có đơn) | Soft-delete: `is_active = False`, không đăng nhập được, đơn cũ còn nguyên |
| 53 | TC-D18 | Xem danh sách danh mục / nhà cung cấp | Truy cập `/Admin/Categories/` và `/Admin/Suppliers/` | Bảng danh mục và nhà cung cấp hiển thị đầy đủ |
| 54 | TC-D19 | Thêm danh mục mới | Tên: "Phụ kiện", Mô tả: "Tai nghe, sạc, ốp lưng..." | Danh mục mới hiển thị trong dropdown lọc trên cửa hàng |

**Kết quả ghi nhận:** Tất cả 19 test case đều **Đạt**.

---

#### E. Module AI Chatbot, Live Chat & Thống kê

| STT | ID | Tên Test Case | Dữ liệu kiểm thử | Kết quả mong đợi |
|:---:|:---:|---------------|-------------------|-------------------|
| 55 | TC-E01 | Chat hỏi sản phẩm (RAG AI) | Tin nhắn: `Có iPhone nào giá dưới 20 triệu không?` | Bot phản hồi tiếng Việt, gợi ý sp kèm ảnh và giá dựa trên CSDL (RAG pipeline) |
| 56 | TC-E02 | Chat hỏi chính sách đổi trả | Tin nhắn: `Chính sách đổi trả thế nào?` | Bot trả lời đúng dựa trên FAQ hoặc KnowledgeChunks trong CSDL |
| 57 | TC-E03 | Chat từ widget popup | Mở widget chatbot, gửi tin nhắn | Widget nhận/phản hồi đúng, có nút "Mở rộng" chuyển sang `/Chat/` |
| 58 | TC-E04 | Chuyển sang chat nhân viên (Live Chat) | Tin nhắn: `Tôi muốn nói chuyện với nhân viên` | Bot nhận diện intent, tạo `LiveChatConversation` trong DB, chuyển trạng thái |
| 59 | TC-E05 | Staff nhận Live Chat | Admin vào `/Admin/LiveChat/`, nhấn "Nhận cuộc trò chuyện" | Conversation chuyển sang `active`, staff và khách nhắn tin qua lại được |
| 60 | TC-E06 | Chat nội dung không rõ ý | Tin nhắn: `asdfghjkl` (ký tự ngẫu nhiên) | Bot phản hồi lịch sự, gợi ý câu hỏi phổ biến |
| 61 | TC-E07 | Xem lịch sử chat (Admin) | Truy cập `/Admin/Chats/` | Hiển thị danh sách phiên chat (AI + Live Chat), tìm kiếm theo username, lọc theo ngày |
| 62 | TC-E08 | Xem thống kê doanh thu (Admin) | Truy cập `/Admin/Statistics/` hoặc `/Statistics/Revenue/` | Hiển thị biểu đồ doanh thu theo ngày/tuần, tổng doanh thu, top sp bán chạy |
| 63 | TC-E09 | Xem thống kê tồn kho thấp | Truy cập `/Admin/Statistics/` | Danh sách sp có tồn kho thấp (≤ mức tối thiểu), cảnh báo bổ sung hàng |
| 64 | TC-E10 | Khóa tài khoản người dùng | Đổi `is_active = False` trên tài khoản customer | Tài khoản không đăng nhập được, hiển thị thông báo bị khóa |

**Kết quả ghi nhận:** Tất cả 10 test case đều **Đạt**.

---

#### Tổng hợp kết quả kiểm thử

| Module | Số TC | Đạt | Không đạt |
|--------|:-----:|:----:|:---------:|
| A. Authentication (Đăng nhập / Đăng ký / Đăng xuất) | 10 | 10 | 0 |
| B. Cửa hàng & Giỏ hàng | 15 | 15 | 0 |
| C. Thanh toán & Đơn hàng | 10 | 10 | 0 |
| D. Quản trị (Admin) | 19 | 19 | 0 |
| E. AI Chatbot, Live Chat & Thống kê | 10 | 10 | 0 |
| **Tổng cộng** | **64** | **64** | **0** |

> **Tỷ lệ đạt: 64/64 = 100%** — Tất cả các chức năng đều hoạt động đúng theo thiết kế.



## 3.2. Đánh giá kết quả thực nghiệm

*(Nội dung phần 3.2 sẽ được bổ sung sau khi hoàn thiện các đánh giá tổng quan về hiệu năng, khả năng mở rộng và đề xuất cải tiến.)*
