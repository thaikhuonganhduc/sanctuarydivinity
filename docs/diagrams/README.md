# Sơ đồ phân tích thiết kế – SANCTUARY

Các sơ đồ trong thư mục này mô tả **đúng chức năng đang có trong code** (không phải chức năng dự kiến).

**Cách mở và sửa:** vào [app.diagrams.net](https://app.diagrams.net) → *File → Open from → Device* → chọn file `.drawio`.
Kéo chỉnh xong thì *File → Export as → PNG* để dán vào báo cáo.
Hoặc cài extension **Draw.io Integration** trong VS Code để mở thẳng file.

**Tạo lại từ code:** mỗi file được sinh bởi một script trong `tools/` (dùng thư viện nhỏ `tools/drawio.py`):

```
python tools/diagram_usecase.py
```

Lưu ý: chạy lại script sẽ **ghi đè** những chỉnh sửa đã làm trong draw.io. Nếu đã chỉnh tay thì sửa tiếp trong draw.io, không chạy lại script.

| File | Nội dung |
|---|---|
| `01-usecase.drawio` | Sơ đồ Use Case tổng quan (3 tác nhân, 24 use case) |
| `02-erd.drawio` | Sơ đồ quan hệ thực thể (ERD): mô hình dữ liệu logic, 18 thực thể |
| `03-dfd.drawio` | Sơ đồ luồng dữ liệu (DFD): trang 1 mức ngữ cảnh, trang 2 mức 0 |
| `04-bpmn.drawio` | Sơ đồ quy trình nghiệp vụ (BPMN): mỗi quy trình 1 trang |
| `05-flowchart.drawio` | Lưu đồ giải thuật (5 trang): kiểm tra mã cổng, gợi ý size, tính tổng tiền, đặt hàng, thuật toán Luhn (`tools/diagram_flowchart.py`) |
| `06-architecture.drawio` | Kiến trúc client/server và sơ đồ trang (sitemap) (`tools/diagram_architecture.py`) |

Ảnh PNG của mọi trang sơ đồ nằm trong `png/` (xuất bằng draw.io desktop, tỉ lệ 2x):

```
"%LOCALAPPDATA%\Programs\draw.io\draw.io.exe" -x -f png -s 2 -b 20 -p 1 -o png/05-flowchart-p1.png 05-flowchart.drawio
```

---

## 1. Sơ đồ Use Case (`01-usecase.drawio`)

### Tác nhân

| Tác nhân | Mô tả |
|---|---|
| **Khách** | Người đã nhập đúng **mã athlete** ở trang cổng (`index.html`). Xem và mua hàng được mà không cần tài khoản (đơn khách vãng lai). |
| **Thành viên** | Khách có tài khoản. **Kế thừa** mọi chức năng của Khách (mũi tên tam giác rỗng), thêm các chức năng tài khoản. |
| **Admin** | Người nhập đúng **mã admin** ở trang cổng (so sánh bằng hash SHA-256). Chỉ vào được `pages/admin.html`. |

### Quan hệ giữa các use case

- **«extend»** (mũi tên nét đứt, chỉ từ use case mở rộng về use case gốc): chức năng *có thể* xảy ra thêm, không bắt buộc.
  - UC04 *Xem bảng size, gợi ý size* mở rộng UC03 *Xem chi tiết sản phẩm*: khách chỉ dùng khi muốn.
  - UC08 *Áp mã giảm giá* mở rộng UC07 *Đặt hàng*: đặt hàng không cần mã.

### Bảng mô tả use case

| Mã | Tên | Tác nhân | Mô tả ngắn | File code chính |
|---|---|---|---|---|
| UC01 | Vào web bằng mã athlete | Khách | Nhập mã ở trang cổng; đúng mã đang bật thì vào trang chủ, sai thì báo lỗi | `js/gate.js`, `js/athletes.js` |
| UC02 | Xem, lọc và sắp xếp sản phẩm | Khách | Xem 3 khu (nam, nữ, phụ kiện); lọc theo size, màu; sắp xếp theo giá trong menu Armory | `js/shop.js` |
| UC03 | Xem chi tiết sản phẩm | Khách | Popup: ảnh theo màu, chọn màu, size, số lượng, xem tồn kho, mô tả, review liên quan | `js/product-popup.js` |
| UC04 | Xem bảng size, gợi ý size | Khách | Bảng size (cm/kg hoặc in/lb) và gợi ý size từ chiều cao, cân nặng (dữ liệu ANSUR II) | `js/product-popup.js`, `js/size-finder.js` |
| UC05 | Xem và lọc đánh giá | Khách | Popup Reviews: lọc theo số sao, dòng nam/nữ, loại sản phẩm; xem ảnh | `js/reviews.js` |
| UC06 | Quản lý giỏ hàng | Khách | Thêm, đổi số lượng, xoá món; không vượt tồn kho; lưu trong localStorage | `js/cart.js`, `js/cart-page.js` |
| UC07 | Đặt hàng (thanh toán) | Khách | Điền form giao hàng + thanh toán (kiểm tra bằng JS), tính ship/thuế, lưu đơn và trừ kho | `js/cart-page.js`, `js/shipping.js` |
| UC08 | Áp mã giảm giá athlete | Khách | Nhập mã athlete đang bật để giảm 10% | `js/cart-page.js` |
| UC09 | Đổi tiền tệ hiển thị | Khách | Chọn vùng ở footer; giá đổi theo tỷ giá lấy từ API (có lưu tạm) | `js/currency.js` |
| UC10 | Gửi tin nhắn liên hệ | Khách | Form trang Info, kiểm tra bằng JS, lưu vào localStorage cho admin đọc | `js/contact.js` |
| UC11 | Đăng ký tài khoản | Khách | Tên, email, mật khẩu; mật khẩu lưu dạng hash SHA-256 + salt | `js/auth.js`, `js/auth-ui.js` |
| UC12 | Đăng nhập / đăng xuất | Thành viên | Đăng nhập bằng email + mật khẩu | `js/auth.js`, `js/auth-ui.js` |
| UC13 | Sửa hồ sơ, địa chỉ | Thành viên | Sửa tên, SĐT, địa chỉ; checkout tự điền từ hồ sơ | `js/account-page.js` |
| UC14 | Đổi mật khẩu | Thành viên | Nhập mật khẩu cũ + mới | `js/account-page.js`, `js/auth.js` |
| UC15 | Xem lịch sử đơn hàng | Thành viên | Danh sách đơn đã đặt và trạng thái do admin cập nhật | `js/account-page.js` |
| UC16 | Vào trang quản trị | Admin | Nhập mã admin ở trang cổng; trang admin chặn người không phải admin | `js/gate.js`, `js/guard.js` |
| UC17 | Xem tổng quan | Admin | Doanh thu, số đơn, giá trị đơn trung bình, hàng sắp hết, bán chạy | `js/admin.js` |
| UC18 | Quản lý đơn hàng | Admin | Tìm, lọc, xem chi tiết, đổi trạng thái; huỷ đơn thì hoàn kho | `js/admin.js` |
| UC19 | Quản lý sản phẩm | Admin | Thêm (có ảnh), sửa giá, tồn kho, nổi bật, ẩn/hiện, xoá, khôi phục | `js/admin.js`, `js/products.js` |
| UC20 | Xem khách hàng | Admin | Danh sách tài khoản, số đơn, tổng chi tiêu | `js/admin.js` |
| UC21 | Quản lý tin nhắn | Admin | Đọc, đánh dấu đã đọc, trả lời qua email, xoá | `js/admin.js` |
| UC22 | Quản lý mã athlete | Admin | Thêm mã (có gợi ý), bật/tắt, copy, xoá, reset về `access.json` | `js/admin.js`, `js/athletes.js` |
| UC23 | Đặt ngày ra mắt | Admin | Đổi mốc đếm ngược ở trang cổng (giờ Việt Nam) | `js/admin.js`, `js/countdown.js` |
| UC24 | Sao lưu / khôi phục dữ liệu | Admin | Xuất file JSON, kiểm tra rồi khôi phục, xoá dữ liệu, tạo dữ liệu mẫu | `js/admin.js` |

---

## 2. Sơ đồ quan hệ thực thể – ERD (`02-erd.drawio`)

Web **không có cơ sở dữ liệu thật** (không có backend). ERD này là **mô hình dữ liệu logic**: dữ liệu đang nằm
trong file JSON và localStorage được chuẩn hoá thành các bảng giống một CSDL quan hệ, để thấy rõ thực thể và quan hệ.

- **Xanh dương:** dữ liệu gốc trong file JSON (`data/`), đọc bằng `fetch` (AJAX).
- **Xanh lá:** dữ liệu sinh ra khi dùng web, lưu trong `localStorage` của trình duyệt.
- Dòng chữ nghiêng dưới tên thực thể ghi **nơi lưu thật**, ví dụ `localStorage: sanctuary_orders`.

### Ký hiệu chân chim (crow's foot)

| Ký hiệu ở đầu đường nối | Nghĩa |
|---|---|
| `\|\|` | một và chỉ một |
| `o\|` | không hoặc một |
| `\|<` | một hoặc nhiều |
| `o<` | không hoặc nhiều |
| Nét đứt | tra cứu bằng giá trị, **không phải** khoá ngoại |

### Các quan hệ chính

| Quan hệ | Bản số | Giải thích |
|---|---|---|
| USER – ORDER | 0..1 – 0..n | Một tài khoản có nhiều đơn; đơn của **khách vãng lai** không gắn tài khoản (`user_email` trống) |
| ATHLETE_CODE – ORDER | 0..1 – 0..n | Một mã dùng cho nhiều đơn; đơn có thể không dùng mã |
| ORDER – ORDER_ITEM | 1 – 1..n | Mỗi đơn có ít nhất 1 món |
| PRODUCT – ORDER_ITEM | 1 – 0..n | Một sản phẩm nằm trong nhiều đơn |
| PRODUCT – CART_ITEM | 1 – 0..n | Giỏ hàng lưu theo sản phẩm + màu + size |
| PRODUCT – PRODUCT_COLOR – COLOR_IMAGE | 1 – 1..n – 1..n | Mỗi sản phẩm có nhiều màu, mỗi màu có nhiều ảnh |
| PRODUCT – PRODUCT_SIZE | 1 – 1..n | Size đang bán (XXS–XXL hoặc One size) |
| SHIPPING_ZONE – COUNTRY – ORDER | 1 – 1..n – 0..n | Phí ship tính theo vùng của nước nhận hàng |
| CATEGORY_WEIGHT – PRODUCT | 1 – 0..n | Cân nặng ước tính theo loại, dùng để tính phí ship |
| REVIEW – REVIEW_ENTRY, REVIEW_IMAGE | 1 – 1..n, 0..n | Một người đánh giá nhiều sản phẩm, kèm ảnh |
| PRODUCT_SIZE ··· SIZE_CHART_ROW | tra cứu | Bảng size tra theo size + giới tính |

### Đối chiếu: mô hình lý thuyết và cách web lưu thật

| Lý thuyết (CSDL quan hệ) | Thực tế trên web | Lý do |
|---|---|---|
| Mỗi thực thể là 1 bảng riêng | PRODUCT_COLOR, COLOR_IMAGE, PRODUCT_SIZE, PRODUCT_FEATURE **lồng bên trong** mỗi sản phẩm của `products.json` | JSON lồng nhau đọc 1 lần là có đủ, không cần JOIN |
| ORDER_ITEM là bảng riêng | Nằm trong mảng `items` của từng đơn | Đơn và món luôn được đọc/ghi cùng nhau |
| Thông tin giao hàng tham chiếu USER | Đơn **chép lại** tên, địa chỉ vào `customer` | Khách sửa hồ sơ sau này không làm đổi đơn cũ; khách vãng lai không có USER |
| UPDATE từng dòng | Đọc cả danh sách → sửa → **ghi đè cả key** localStorage | localStorage chỉ lưu chuỗi theo key |
| Transaction (ghi đơn + trừ kho cùng lúc) | `writeAll()` trong `js/storage.js`: ghi nhiều key, lỗi giữa chừng thì **trả lại giá trị cũ** | Mô phỏng tính nguyên tử (atomic) |
| UPDATE bảng PRODUCT | Không sửa được file JSON từ trình duyệt → lưu phần thay đổi vào `sanctuary_product_overrides`, rồi **đè lên** dữ liệu gốc khi đọc | Web tĩnh, không có server để ghi file |
| DELETE sản phẩm | Đánh dấu `deleted: true` (xoá mềm) | Đơn hàng cũ vẫn tra được tên sản phẩm |
| Khoá ngoại có ràng buộc | Không có ràng buộc tự động; code tự kiểm tra (vd: giỏ hàng bỏ món đã bị xoá hoặc hết màu) | localStorage không có ràng buộc |
| Kiểm tra kiểu dữ liệu khi ghi | Kiểm tra **khi đọc**: `isValidOrder`, `isValidUser`... trong `js/storage.js` bỏ qua bản ghi sai cấu trúc | Dữ liệu localStorage có thể bị sửa tay (F12) |
| Dữ liệu dùng chung mọi máy | localStorage **riêng từng trình duyệt** | Giới hạn của web không có backend; hướng phát triển: thêm server + CSDL |

---

## 3. Sơ đồ luồng dữ liệu – DFD (`03-dfd.drawio`, 2 trang)

Ký hiệu **Gane-Sarson**:

| Hình | Ý nghĩa |
|---|---|
| Chữ nhật bo góc (vàng), có số | Tiến trình: nơi dữ liệu được xử lý |
| Chữ nhật (xanh) | Tác nhân ngoài: người hoặc hệ thống bên ngoài gửi / nhận dữ liệu |
| Chữ nhật hở 1 đầu, có mã D | Kho dữ liệu |
| Mũi tên có nhãn | Luồng dữ liệu. Vào kho = ghi; ra khỏi kho = đọc; 2 đầu = đọc và ghi |

### Trang 1: DFD mức ngữ cảnh

Cả website là **1 tiến trình (số 0)**, trao đổi dữ liệu với 3 tác nhân ngoài:

- **Khách hàng** (gồm Khách và Thành viên): gửi mã athlete, lựa chọn sản phẩm, giỏ hàng, thông tin giao hàng, tin nhắn; nhận lại sản phẩm, gợi ý size, tổng tiền, xác nhận đơn.
- **Admin:** gửi mã admin và các thao tác quản trị; nhận lại doanh thu, danh sách đơn, khách, tin nhắn, file backup.
- **Dịch vụ tỷ giá** (`open.er-api.com`): tác nhân ngoài duy nhất là hệ thống; web gọi API này để đổi giá USD sang tiền tệ khác (`js/currency.js`).

### Trang 2: DFD mức 0

| Tiến trình | Việc làm | Kho đọc | Kho ghi | File code |
|---|---|---|---|---|
| 1.0 Xác thực truy cập | Kiểm tra mã admin (so hash) rồi mã athlete đang bật | D3 | (vai trò lưu trong sessionStorage) | `js/gate.js` |
| 2.0 Duyệt, lọc sản phẩm và đánh giá | Hiện sản phẩm, lọc size/màu, sắp xếp, popup, bảng size, gợi ý size, đánh giá, đổi tiền | D1, D2, D5, D10 | D10 (lưu tạm tỷ giá 1 giờ) | `js/shop.js`, `js/product-popup.js`, `js/reviews.js`, `js/currency.js` |
| 3.0 Quản lý giỏ hàng | Thêm, sửa số lượng, xoá; không vượt tồn kho | D1, D6 | D6 | `js/cart.js`, `js/cart-page.js` |
| 4.0 Đặt hàng | Kiểm tra form, kiểm tra lại giỏ, áp mã, tính ship/thuế, lưu đơn + trừ kho | D1, D3, D4, D6, D8 | D7, D1, D6 | `js/cart-page.js`, `js/shipping.js` |
| 5.0 Quản lý tài khoản | Đăng ký, đăng nhập, sửa hồ sơ, đổi mật khẩu, xem lịch sử đơn | D7, D8 | D8 | `js/auth.js`, `js/account-page.js` |
| 6.0 Gửi liên hệ | Kiểm tra form rồi lưu tin nhắn | – | D9 | `js/contact.js` |
| 7.0 Quản trị cửa hàng | Đơn hàng, sản phẩm, khách, tin nhắn, mã athlete, ngày ra mắt, backup | D1, D3, D7, D8, D9 | D1, D3, D7, D9 | `js/admin.js` |

### Kho dữ liệu

| Mã | Kho | Nơi lưu thật |
|---|---|---|
| D1 | Sản phẩm | `data/products.json` (gốc, chỉ đọc) + `sanctuary_product_overrides` + `sanctuary_custom_products` |
| D2 | Đánh giá | `data/reviews.json` |
| D3 | Mã athlete | `data/access.json` hoặc `sanctuary_athletes` (khi admin đã sửa) |
| D4 | Phí ship, thuế | `data/shipping.xml` |
| D5 | Bảng size | `data/size-chart.json` |
| D6 | Giỏ hàng | `sanctuary_cart` |
| D7 | Đơn hàng | `sanctuary_orders` |
| D8 | Tài khoản | `sanctuary_users`, `sanctuary_session` |
| D9 | Tin nhắn | `sanctuary_messages` |
| D10 | Tỷ giá | `sanctuary_rates` (lưu tạm kết quả API) |

Ghi chú: để sơ đồ dễ đọc, luồng giữa tác nhân và tiến trình vẽ thành **1 mũi tên 2 đầu**, nhãn ghi dạng *"dữ liệu gửi vào / dữ liệu nhận lại"*.

---

## 4. Sơ đồ quy trình nghiệp vụ – BPMN (`04-bpmn.drawio`)

Mỗi quy trình nằm ở **1 trang** (tab ở dưới cùng cửa sổ draw.io). Mỗi trang có 1 **pool** (tên quy trình),
chia thành các **lane** theo người / bộ phận thực hiện.

| Ký hiệu | Ý nghĩa |
|---|---|
| Vòng tròn xanh | Sự kiện bắt đầu |
| Vòng tròn đỏ viền đậm | Sự kiện kết thúc (có dấu tia sét = kết thúc do lỗi) |
| Hình chữ nhật bo góc | Công việc (task) |
| Hình thoi có dấu X | Cổng rẽ nhánh loại trừ (exclusive gateway): chỉ đi 1 nhánh Có / Không |
| Hình trụ | Kho dữ liệu (data store), nối bằng nét đứt: đọc / ghi |
| Mũi tên liền | Luồng tuần tự (sequence flow) |

### Danh sách quy trình

| Trang | Quy trình | Lane | Điểm cần nói khi vấn đáp | File code |
|---|---|---|---|---|
| 1 | Vào web qua cổng | Người dùng, Website | Kiểm tra mã admin trước (so **hash** SHA-256), rồi mới tới mã athlete; mã trống / sai đều quay lại bước nhập | `js/gate.js`, `js/athletes.js` |
| 2 | Đăng ký | Khách, Website | Kiểm tra form → kiểm tra trùng email → tạo **salt** + băm mật khẩu → lưu → đăng nhập luôn | `js/auth-ui.js`, `js/auth.js` |
| 3 | Đăng nhập | Thành viên, Website | Băm lại mật khẩu vừa nhập với salt đã lưu rồi so hash; sai email hay sai mật khẩu đều **báo chung 1 câu** | `js/auth-ui.js`, `js/auth.js` |
| 4 | Thêm vào giỏ | Khách, Website | Kiểm tra size → màu còn bán → **số còn thêm được = tồn kho − số đã có trong giỏ** → lưu giỏ | `js/product-popup.js`, `js/cart.js` |
| 5 | Đặt hàng | Khách, Website | Mã athlete tuỳ chọn; kiểm tra form (thẻ: Luhn, hạn, CVC); **kiểm tra lại giỏ** ngay lúc đặt; lưu đơn + trừ kho **cùng lúc** (`writeAll`) | `js/cart-page.js`, `js/shipping.js` |
| 6 | Admin xử lý đơn | Admin, Website, Khách | Huỷ đơn thì **cộng lại kho**, mở lại đơn đã huỷ thì trừ kho lần nữa; lỗi lưu thì trả ô chọn về trạng thái cũ | `js/admin.js` |
| 7 | Liên hệ | Khách, Website, Admin | 2 phần: khách gửi (kiểm tra form, lưu, báo đã gửi) và admin xử lý (đọc, trả lời qua mailto, xoá) | `js/contact.js`, `js/admin.js` |
| 8 | Admin thêm sản phẩm | Admin, Website | Kiểm tra loại + dung lượng ảnh; **thu nhỏ ảnh bằng canvas** trước khi lưu (localStorage ~5 MB); kiểm tra trùng tên | `js/admin.js` |

### Gợi ý chia việc

Mỗi thành viên nhận 1–2 sơ đồ, mở bằng draw.io, chỉnh bố cục cho đẹp, xuất PNG dán vào báo cáo và **tự commit**
phần mình làm (ví dụ `docs: polish BPMN checkout diagram`). Như vậy lịch sử Git có bằng chứng phân công.

