# GitHub Issues - Các chức năng đã sửa

## Issue 1: Cải thiện hiển thị ảnh sản phẩm trên trang chủ

**Tên:** Cải thiện hiển thị ảnh sản phẩm trên trang chủ — ưu tiên ảnh `is_primary`

**Chi tiết:**
- **Mô tả:** Trang chủ (`Views/Home/index.html`) hiện tại ưu tiên `product.image_url` trước ảnh có `is_primary=True`. Cần đổi logic để ưu tiên ảnh `is_primary=True` (primary image) thay vì `image_url`.
- **Vị trí:** `Views/Home/index.html` (dòng 1443, 1501)
- **Thay đổi:** Sửa thứ tự ưu tiên ảnh — `is_primary` -> `image_url` -> `product_images[0]` -> `no-image.png`
- **File liên quan:** `Views/Home/index.html`
- **Trạng thái:** Đã sửa trong commit `2454775`

---

## Issue 2: Thêm Modal chọn Option sản phẩm trên trang chủ (Product Option Modal)

**Tên:** Thêm Modal chọn Option (màu sắc, dung lượng) trên trang chủ

**Chi tiết:**
- **Mô tả:** Thêm modal popup cho phép người dùng chọn màu sắc và dung lượng trước khi thêm vào giỏ hàng ngay tại trang chủ. Modal hỗ trợ:
  - Chọn màu sắc với dot màu preview
  - Chọn dung lượng (storage)
  - Tăng/giảm số lượng
  - Cập nhật giá và ảnh theo variant được chọn
  - Fallback hiển thị nếu sản phẩm không có variant
- **Vị trí:** `Views/Home/index.html` (phần `<!-- ===== MODAL: Chọn Option Sản phẩm ===== -->`)
- **API endpoint:** `GET /Products/{product_id}/variants` trả về danh sách variants + images
- **File mới:** `Controllers/ProductsController.py` — thêm endpoint `/variants`
- **File liên quan:** `Views/Home/index.html`, `Controllers/ProductsController.py`
- **Trạng thái:** Đã sửa trong commit `2454775`

---

## Issue 3: Modal sửa Option sản phẩm trong trang giỏ hàng

**Tên:** Thêm chức năng sửa option (màu/dung lượng) sản phẩm trong giỏ hàng

**Chi tiết:**
- **Mô tả:** Thêm nút "Sửa option" (icon edit) trên mỗi sản phẩm trong giỏ hàng. Khi click sẽ mở modal cho phép:
  - Xem option hiện tại của sản phẩm
  - Đổi màu sắc hoặc dung lượng (variant)
  - Thay đổi số lượng
  - Cập nhật giá và ảnh theo variant mới
- **Vị trí:** `Views/Cart/index.html` — thêm nút edit + modal `ev-overlay`
- **API endpoints:**
  - `GET /Cart/update-variant-data/{item_id}` — lấy thông tin variant + product của cart item
  - `POST /Cart/update-variant/{item_id}` — cập nhật variant và số lượng
- **File mới:** `Controllers/CartController.py`, `Services/CartService.py`
- **File liên quan:** `Views/Cart/index.html`, `Controllers/CartController.py`, `Services/CartService.py`
- **Trạng thái:** Đã sửa trong commit `2454775`

---

## Issue 4: Thêm cảnh báo lỗi khi checkout không hợp lệ

**Tên:** Thêm error alert khi validation checkout thất bại

**Chi tiết:**
- **Mô tả:** Thêm hộp cảnh báo (error alert box) trên trang giỏ hàng hiển thị thông báo lỗi khi người dùng thực hiện checkout không hợp lệ (ví dụ: chưa chọn option sản phẩm). Error được đọc từ URL query param `?error=...`.
- **Vị trí:** `Views/Cart/index.html` (phần `<!-- ===== ERROR ALERT (from checkout validation) ===== -->`)
- **Hành vi:** Alert tự động scroll vào giữa màn hình, có nút đóng thủ công
- **File liên quan:** `Views/Cart/index.html`
- **Trạng thái:** Đã sửa trong commit `2454775`

---

## Issue 5: Cải thiện hiển thị ảnh & logic chọn variant trên trang chi tiết sản phẩm

**Tên:** Cải thiện hiển thị ảnh và logic chọn variant trên trang chi tiết sản phẩm

**Chi tiết:**
- **Mô tả:** Cải thiện trang chi tiết sản phẩm (`Views/Products/detail.html`):
  - Fix logic hiển thị color/storage — group unique values thay vì lặp theo variant
  - Hiển thị label màu/dung lượng đã chọn (`selected-color`, `selected-storage`)
  - Xây dựng `fullVariantMap` lookup map cho việc match variant chính xác khi chọn cả color + storage
  - Fix auto-select variant on load — chọn cả color lẫn storage
  - Sửa ảnh sản phẩm liên quan (related products) ưu tiên `is_primary`
- **Vị trí:** `Views/Products/detail.html` (dòng 208-376)
- **File liên quan:** `Views/Products/detail.html`
- **Trạng thái:** Đã sửa trong commit `2454775`

---

## Issue 6: Thêm debug logging cho việc debug hypotheses (ProductImage / variant)

**Tên:** Thêm hệ thống debug logging để theo dõi ProductImage và variant rendering

**Chi tiết:**
- **Mô tả:** Thêm `_debug_log()` function trong `AdminController`, `HomeController`, và `ProductService` để ghi log debug phục vụ hypothesis testing về ProductImage. Log ghi vào file `debug-ed9600.log` với các hypothesis IDs: H1, H2, H3, H4, H_STAR.
  - `H1` — Cache hit/miss cho featured và new products
  - `H2` — Featured/New products loaded from DB (image counts, is_primary flags)
  - `H3` — ProductImage saved to DB after upload
  - `H4` — Product updated via admin
  - `H_STAR` — Star toggle (is_primary) state changes
- **Vị trí:** `Controllers/AdminController.py`, `Controllers/HomeController.py`, `Services/ProductService.py`
- **File liên quan:** `Controllers/AdminController.py`, `Controllers/HomeController.py`, `Services/ProductService.py`
- **Trạng thái:** Đã sửa trong commit `2454775`
