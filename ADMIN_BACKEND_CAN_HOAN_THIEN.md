# Ke Hoach Hoan Thien Backend Trang Admin

Tai lieu nay tong hop cac viec can chinh de hoan thien backend trang admin theo dung database hien tai trong `SQL/schema.sql`. Muc tieu la tang do on dinh cua API admin, tranh loi 500, giu lich su giao dich va khong thay doi cau truc SQL.

## Nguyen Tac Chung

- Khong sua `SQL/schema.sql`.
- Uu tien backend truoc frontend.
- Moi API admin phai validate du lieu dau vao truoc khi ghi DB.
- Moi thao tac ghi DB nen co `try/except IntegrityError`, `rollback()` khi loi va tra JSON ro rang.
- Khong xoa cung du lieu da lien quan den lich su giao dich, gio hang, chat hoac thong bao.
- Neu model/bang co cot `updated_at`, nen cap nhat khi sua du lieu.

## Tinh Trang Hien Tai

Backend admin hien da on dinh hon truoc o cac luong chinh:

- Product create/update da validate gia, ton kho, danh muc, nha cung cap.
- Product create/update da dong bo `Products.stock_quantity` voi bang `Inventory`.
- Product delete khong xoa cung neu da co `OrderItems` hoac `CartItems`; thay vao do chuyen `is_available = False`.
- Account delete khong xoa cung neu da co du lieu lien quan; thay vao do chuyen `is_active = False`.
- Order cancel da hoan kho va dong bo lai `Inventory`.
- Category, Supplier, Variant, ProductImages da duoc bo sung validation va `IntegrityError + rollback`.
- Upload anh da kiem tra `content_type` va duoi file hop le.

Tuy nhien, backend admin van chua hoan toan dong deu tren toan bo CRUD va van con mot so diem nen lam tiep.

## Cac Hang Muc Da Hoan Thanh

### 1. Validation Chung

Da co helper dung chung:

- `_to_int(...)`
- `_to_decimal(...)`
- `_validate_role(...)`
- `_validate_product_refs(...)`
- `_validate_email_optional(...)`
- `_validate_phone_optional(...)`
- `_is_allowed_image_extension(...)`

Muc tieu da dat duoc:

- Giam nguy co form sai du lieu gay loi 500.
- Chuan hoa validate cho product, account, category, supplier, variant, product image.

### 2. Category API

Da hoan thanh:

- Validate `display_order`.
- Bọc create/update/delete bang `IntegrityError + rollback`.
- Update co cap nhat `updated_at`.
- Delete uu tien soft-hide bang `is_active = False`.

### 3. Supplier API

Da hoan thanh:

- Validate `name`, `email`, `phone`.
- Bọc create/update/delete bang `IntegrityError + rollback`.
- Update co cap nhat `updated_at`.
- Delete uu tien soft-hide neu da co san pham lien quan.

### 4. Variant API

Da hoan thanh:

- Khong con parse truc tiep `int(...)`/`float(...)` cho cac field chinh.
- Validate `product_id`, `price`, `original_price`, `stock_quantity`, `display_order`.
- Delete khong xoa cung neu variant da nam trong `CartItems` hoac `OrderItems`.
- Truong hop co rang buoc, variant se duoc chuyen `is_active = False`.

### 5. ProductImages API

Da hoan thanh:

- Validate `product_id`, `variant_id`, `display_order`.
- Kiem tra variant co thuoc dung product hay khong.
- Dat anh chinh khong con anh huong sang san pham khac.
- Bọc create/update/delete bang `IntegrityError + rollback`.
- Upload anh da kiem tra `content_type` va duoi file `.jpg`, `.jpeg`, `.png`, `.webp`.

### 6. Order Delete

Da hoan thanh:

- `DELETE /Admin/API/Orders/{order_id}` khong xoa cung don hang nua.
- Neu don chua `Cancelled`, API se chuyen don sang `Cancelled` va hoan kho.
- Neu don da `Cancelled`, API tra loi khong ho tro xoa cung lich su giao dich.

## Cac Hang Muc Con Lai Nen Lam

### 1. Chuan Hoa Response Loi Toan Bo Admin API

Trang thai hien tai:

- Nhieu endpoint da tra JSON loi ro rang.
- Tuy nhien chua co lop xu ly dung chung cho toan bo admin API.

Can lam tiep:

- Thong nhat mau response loi cho tat ca endpoint admin.
- Duy tri quy uoc:
  - `400`: du lieu gui len khong hop le
  - `401`: chua dang nhap
  - `403`: khong du quyen
  - `404`: khong tim thay ban ghi
  - `409`: xung dot du lieu hoac rang buoc khoa ngoai
  - `500`: loi bat ngo

Mau response nen dung:

```json
{
  "success": false,
  "error": "Thong bao loi de admin hieu va sua"
}
```

### 2. Cac Diem Con Lai Nen Lam

Nhung diem con lai chu yeu la tinh dong deu va cau truc:

- Chuan hoa response loi cho toan bo admin API bang mot cach viet thong nhat hon nua.
- Can nhac cap nhat `updated_at` cho nhung luong khac neu sau nay mo rong model.
- Tiep tuc tach logic nghiep vu ra khoi `AdminController.py` de de bao tri hon.

### 3. Tach Bot Logic Khoi AdminController

Day la viec nen lam sau khi API da on:

- `AdminProductService`
- `AdminOrderService`
- `AdminAccountService`
- `AdminCatalogService`

Loi ich:

- Controller ngan hon.
- De test hon.
- De chia viec trong nhom hon.

## Checklist Hoan Thanh

- [x] Category API co validate va rollback day du.
- [x] Supplier API co validate va rollback day du.
- [x] Variant API khong con `int(...)`/`float(...)` truc tiep tren form input.
- [x] Variant delete khong xoa cung neu da co `CartItems` hoac `OrderItems`.
- [x] ProductImages API validate dung product/variant/display_order.
- [x] Dat anh chinh khong anh huong sang san pham khac.
- [x] Upload anh co kiem tra content type, duoi file va loi upload co ban.
- [x] Order delete khong xoa cung lich su giao dich.
- [ ] Tat ca API admin tra JSON loi thong nhat.
- [x] Cac luong update chinh da duoc cap nhat `updated_at` dong deu hon.
- [x] Xoa file anh tren filesystem khi xoa `ProductImage`.
- [x] Bọc thao tac ghi file bang `try/except OSError`.
- [x] Khong sua `SQL/schema.sql`.

## Ket Luan

Backend admin hien da on o cac luong chinh nhu product, account va order, va da duoc bo sung bao ve cho category, supplier, variant va product image. Phan viec con lai tap trung vao viec chuan hoa response loi, dong deu `updated_at`, va xu ly file anh tren filesystem. Sau khi cac diem nay duoc lam xong, backend admin se dat muc hoan thien tot de frontend admin goi API an toan hon va giam nguy co loi 500.
