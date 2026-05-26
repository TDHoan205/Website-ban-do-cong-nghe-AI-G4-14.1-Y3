# Checklist Hoan Thien Trang Admin

Muc tieu cua file nay la giup ra soat admin theo huong:

- khong bi `404` khi mo tung trang
- khong co dead link
- menu trai hien day du o moi trang
- widget chat va trang chat admin hoat dong on dinh
- cac hanh dong CRUD co route dung va giao dien mo ta dung nghiep vu

## 1. Route HTML admin phai ton tai day du

Can dam bao cac trang sau mo duoc:

- `/Admin/Dashboard`
- `/Admin/Products`
- `/Admin/Products/{product_id}/edit`
- `/Admin/Categories`
- `/Admin/Suppliers`
- `/Admin/Orders`
- `/Admin/Orders/{order_id}`
- `/Admin/Accounts`
- `/Admin/Chats`
- `/Admin/Statistics`
- `/Admin/Chatbot`

Trang thai hien tai:

- Da bo sung route `/Admin/Statistics`.
- Da bo sung route `/Admin/Chatbot`.

## 2. Khong duoc con link sai route trong template admin

Can loai bo cac link co nguy co gay `404` hoac hanh vi sai:

- `/Admin/Login` trong khi route dung la `/Auth/Admin`
- `/Statistics` neu muc dich la mo trang HTML admin
- `/Admin/Profile` neu route that la `/Auth/Profile`
- `href="#"` chi de mo chuc nang nhung khong co JS xu ly that

Trang thai hien tai:

- Da doi menu `Thong ke` sang `/Admin/Statistics`.
- Da doi menu `AI Chatbot` sang `/Admin/Chatbot`.
- Da sua redirect sai `/Admin/Login` ve `/Auth/Admin`.
- Da thay cac link `data-admin-panel="/Admin/Profile"` bang `/Auth/Profile` o cac trang da ra soat.
- Da bo cac link `data-admin-panel="/Admin/Chatbot?embed=1"` o cac trang da ra soat va thay bang route that `/Admin/Chatbot`.

## 3. Sidebar admin phai dong deu o moi trang

Moi trang admin nen co day du 3 nhom:

- `Quản lý`
- `Phân tích`
- `Hệ thống`

Trong do:

- `Phân tích` phai co `Thống kê`
- `Hệ thống` phai co `Tài khoản`, `AI Chatbot`, `Lịch sử Chat`, `Xem website`

Trang thai hien tai:

- Da bo sung lai `Phân tích` va `Thống kê` tren cac trang admin chinh.
- Van can tiep tuc ra soat neu con them file admin khac duoc sinh them sau nay.

## 4. AI Chatbot phai hoat dong theo 2 lop

- Widget chat noi phai hien tren moi trang admin.
- Menu `AI Chatbot` phai mo trang lon `/Admin/Chatbot`.

Trang thai hien tai:

- Da gan script `wwwroot/js/admin-chat-widget.js` vao cac trang admin chinh.
- Da tao trang lon `Views/Admin/chatbot.html`.

## 5. Khong duoc mo ta sai nghiep vu tren UI

Can dam bao text tren giao dien khop voi backend that:

- `Order delete` hien tai khong xoa cung, ma chuyen `Cancelled`
- `Account delete` co the tro thanh khoa tai khoan neu co du lieu lien quan
- `Product delete` co the tro thanh an san pham neu co rang buoc

Trang thai hien tai:

- Da sua text va confirm cua `Order detail` va `Orders`.
- Da sua confirm cua `Accounts`.

## 6. Kiem tra file JS/CSS duoc nhung vao admin

Khong duoc goi file khong ton tai vi de gay `404`:

- `wwwroot/js/admin-chat-widget.js`
- `wwwroot/js/admin-panel.js` neu con dung

Trang thai hien tai:

- `admin-chat-widget.js` ton tai va dang duoc dung.
- `admin-panel.js` da duoc bo bo o cac trang da chuyen sang route that.

## 7. Viec con lai nen lam tiep

- Chuan hoa response loi cho toan bo admin API.
- Rà them toan bo `Views/Admin` neu co them file moi hoac file chua doc ky.
- Tiep tuc tach bot logic khoi `AdminController.py` neu muon de bao tri hon.
