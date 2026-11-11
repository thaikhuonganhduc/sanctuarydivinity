# -*- coding: utf-8 -*-
"""PHẦN B - CHƯƠNG 6. THIẾT KẾ CƠ SỞ DỮ LIỆU"""
from docx_helpers import C

# Thực thể: (tên, mô tả, nơi lưu thực tế, [(thuộc tính, kiểu, mô tả, ràng buộc), ...])
ENTITIES = [
    ("USER", "Tài khoản thành viên", "localStorage: sanctuary_users", [
        ("email", "VARCHAR(254)", "Email đăng nhập, đã chuẩn hoá chữ thường", "PK"),
        ("name", "VARCHAR(100)", "Họ tên thành viên", "NOT NULL, ≥ 2 ký tự"),
        ("phone", "VARCHAR(20)", "Số điện thoại", "NULL, 8 - 15 chữ số"),
        ("address", "VARCHAR(200)", "Địa chỉ giao hàng mặc định", "NULL, ≥ 5 ký tự nếu có"),
        ("city", "VARCHAR(100)", "Thành phố", "NULL"),
        ("country", "VARCHAR(60)", "Nước", "NULL, thuộc danh sách vùng hỗ trợ"),
        ("salt", "CHAR(32)", "Chuỗi ngẫu nhiên 16 byte (hex) dùng khi băm mật khẩu", "NOT NULL"),
        ("password_hash", "CHAR(64)", "SHA-256(salt + mật khẩu), dạng hex", "NOT NULL"),
        ("created_at", "TIMESTAMP", "Thời điểm tạo tài khoản", "NOT NULL"),
    ]),
    ("ATHLETE_CODE", "Mã truy cập kiêm mã giảm giá của athlete", "data/access.json; localStorage: sanctuary_athletes", [
        ("code", "VARCHAR(30)", "Mã truy cập (chữ in hoa, số, gạch ngang)", "PK, 4 - 30 ký tự, không trùng"),
        ("name", "VARCHAR(100)", "Tên athlete sở hữu mã", "NOT NULL"),
        ("active", "BOOLEAN", "Mã đang bật hay tắt", "NOT NULL, mặc định TRUE"),
    ]),
    ("ORDER", "Đơn hàng", "localStorage: sanctuary_orders", [
        ("order_number", "VARCHAR(20)", "Mã đơn “SD-” + thời gian (cơ số 36)", "PK"),
        ("user_email", "VARCHAR(254)", "Tài khoản đặt đơn; trống với khách vãng lai", "FK → USER, NULL"),
        ("discount_code", "VARCHAR(30)", "Mã athlete đã dùng", "FK → ATHLETE_CODE, NULL"),
        ("ship_country", "VARCHAR(60)", "Nước nhận hàng", "FK → COUNTRY, NOT NULL"),
        ("order_date", "TIMESTAMP", "Thời điểm đặt", "NOT NULL"),
        ("status", "VARCHAR(12)", "Trạng thái đơn", "Processing | Shipped | Delivered | Cancelled"),
        ("payment", "VARCHAR(12)", "Phương thức thanh toán", "card | paypal | applepay | googlepay"),
        ("currency", "CHAR(3)", "Tiền tệ khách đang xem khi đặt", "Mã ISO 4217"),
        ("total_usd", "DECIMAL(10,2)", "Tổng tiền quy về USD (sau giảm, gồm ship, thuế)", "≥ 0"),
        ("stock_deducted", "BOOLEAN", "Đơn đã trừ kho hay chưa (để hoàn kho khi huỷ)", "NOT NULL"),
        ("ship_name, ship_email, ship_phone", "VARCHAR", "Người nhận (chép từ form thanh toán)", "NOT NULL"),
        ("ship_address, ship_city", "VARCHAR", "Địa chỉ giao hàng", "NOT NULL"),
    ]),
    ("ORDER_ITEM", "Dòng hàng trong đơn", "Mảng items trong mỗi ORDER", [
        ("order_number + line_no", "VARCHAR + INT", "Định danh dòng", "PK"),
        ("product_id", "VARCHAR(10)", "Sản phẩm", "FK → PRODUCT"),
        ("color_name", "VARCHAR(40)", "Màu đã chọn", "NOT NULL"),
        ("size", "VARCHAR(10)", "Size đã chọn", "NOT NULL"),
        ("qty", "INT", "Số lượng", "≥ 1"),
    ]),
    ("CART_ITEM", "Dòng hàng trong giỏ", "localStorage: sanctuary_cart", [
        ("product_id + color + size", "VARCHAR", "Bộ ba định danh dòng giỏ", "PK"),
        ("product_id", "VARCHAR(10)", "Sản phẩm", "FK → PRODUCT"),
        ("qty", "INT", "Số lượng", "≥ 1, tổng theo sản phẩm ≤ stock"),
    ]),
    ("PRODUCT", "Sản phẩm", "data/products.json + sanctuary_custom_products (ghi đè: sanctuary_product_overrides)", [
        ("product_id", "VARCHAR(10)", "Mã sản phẩm (p01..., c... do quản trị viên thêm)", "PK"),
        ("category", "VARCHAR(20)", "Loại sản phẩm", "FK → CATEGORY_WEIGHT"),
        ("name", "VARCHAR(150)", "Tên sản phẩm", "NOT NULL, không trùng"),
        ("gender", "VARCHAR(6)", "Dòng sản phẩm", "him | her | unisex"),
        ("price_usd", "DECIMAL(8,2)", "Giá niêm yết", "> 0"),
        ("stock", "INT", "Số lượng tồn kho", "≥ 0"),
        ("featured", "BOOLEAN", "Sản phẩm nổi bật", "Mặc định FALSE"),
        ("tag", "VARCHAR(20)", "Nhãn hiển thị (ví dụ New)", "NULL"),
        ("material, weight, fit, care", "VARCHAR", "Thông số: chất liệu, định lượng vải, kiểu dáng, cách giặt", "NULL"),
        ("description", "TEXT", "Mô tả", "NULL"),
        ("source", "VARCHAR(300)", "Liên kết tham khảo dữ liệu mẫu", "NULL"),
        ("hidden", "BOOLEAN", "Ẩn khỏi cửa hàng (ghi đè của quản trị viên)", "Mặc định FALSE"),
        ("deleted", "BOOLEAN", "Đã xoá mềm", "Mặc định FALSE"),
    ]),
    ("PRODUCT_COLOR", "Màu của sản phẩm", "Mảng colors trong PRODUCT", [
        ("color_id", "INT", "Định danh màu", "PK"),
        ("product_id", "VARCHAR(10)", "Sản phẩm", "FK → PRODUCT"),
        ("name", "VARCHAR(40)", "Tên màu (Void Black, Nightmare...)", "NOT NULL"),
        ("hex", "CHAR(7)", "Mã màu hiển thị ô màu", "Dạng #RRGGBB"),
        ("available", "BOOLEAN", "Màu còn bán", "Mặc định TRUE"),
    ]),
    ("COLOR_IMAGE", "Ảnh theo màu", "Mảng images trong PRODUCT_COLOR", [
        ("image_id", "INT", "Định danh ảnh", "PK"),
        ("color_id", "INT", "Màu", "FK → PRODUCT_COLOR"),
        ("path", "VARCHAR / TEXT", "Đường dẫn ảnh .webp hoặc data URL (ảnh quản trị viên tải lên)", "NOT NULL"),
        ("sort_order", "INT", "Thứ tự trong slideshow", "≥ 0"),
    ]),
    ("PRODUCT_SIZE", "Size đang bán", "Mảng sizes trong PRODUCT", [
        ("product_id + size", "VARCHAR", "Định danh", "PK"),
        ("size", "VARCHAR(10)", "XXS, XS, S, M, L, XL, XXL hoặc One size", "NOT NULL"),
    ]),
    ("PRODUCT_FEATURE", "Đặc điểm nổi bật", "Mảng features trong PRODUCT", [
        ("feature_id", "INT", "Định danh", "PK"),
        ("product_id", "VARCHAR(10)", "Sản phẩm", "FK → PRODUCT"),
        ("text", "VARCHAR(300)", "Nội dung đặc điểm", "NOT NULL"),
    ]),
    ("SIZE_CHART_ROW", "Một dòng bảng size", "data/size-chart.json", [
        ("gender + size", "VARCHAR", "Định danh (him/her + size)", "PK"),
        ("chest_min_cm, chest_max_cm", "DECIMAL(5,1)", "Khoảng vòng ngực của size", "NULL ở size đầu/cuối"),
        ("waist_cm", "DECIMAL(5,1)[2]", "Vòng eo P25 - P75", "NOT NULL"),
        ("height_cm", "DECIMAL(5,1)[2]", "Chiều cao P25 - P75", "NOT NULL"),
        ("weight_kg", "DECIMAL(5,1)[2]", "Cân nặng P25 - P75", "NOT NULL"),
        ("people", "INT", "Số người trong mẫu thuộc size", "≥ 0"),
    ]),
    ("SHIPPING_ZONE", "Vùng giao hàng", "data/shipping.xml: <zone>", [
        ("zone_id", "VARCHAR(20)", "Mã vùng (domestic, asia...)", "PK"),
        ("base_usd", "DECIMAL(6,2)", "Phí gốc", "≥ 0"),
        ("per_kg_usd", "DECIMAL(6,2)", "Giá mỗi kg", "≥ 0"),
    ]),
    ("COUNTRY", "Nước nhận hàng", "data/shipping.xml: <country>", [
        ("country_name", "VARCHAR(60)", "Tên nước", "PK"),
        ("zone_id", "VARCHAR(20)", "Vùng giao hàng", "FK → SHIPPING_ZONE"),
        ("tax_label", "VARCHAR(20)", "Tên thuế (VAT, GST, Sales tax...)", "NOT NULL"),
        ("tax_pct", "DECIMAL(5,2)", "Thuế suất", "0 - 100"),
        ("duty_pct", "DECIMAL(5,2)", "Thuế nhập khẩu theo % giá hàng", "0 - 100"),
        ("duty_per_item_usd", "DECIMAL(6,2)", "Thuế nhập khẩu cố định mỗi món", "≥ 0"),
    ]),
    ("CATEGORY_WEIGHT", "Khối lượng theo loại", "data/shipping.xml: <category>", [
        ("category", "VARCHAR(20)", "Loại sản phẩm", "PK"),
        ("weight_kg", "DECIMAL(4,2)", "Khối lượng ước tính 1 món", "> 0"),
    ]),
    ("MESSAGE", "Tin nhắn liên hệ", "localStorage: sanctuary_messages", [
        ("message_date", "TIMESTAMP", "Thời điểm gửi (dùng làm định danh)", "PK"),
        ("name", "VARCHAR(100)", "Người gửi", "NOT NULL"),
        ("email", "VARCHAR(254)", "Email người gửi", "NOT NULL, đúng định dạng"),
        ("topic", "VARCHAR(40)", "Chủ đề", "Thuộc danh sách chủ đề"),
        ("message", "VARCHAR(1000)", "Nội dung", "NOT NULL, ≤ 1.000 ký tự"),
        ("read", "BOOLEAN", "Đã đọc", "Mặc định FALSE"),
    ]),
    ("REVIEW", "Đánh giá (gộp theo người viết)", "data/reviews.json", [
        ("review_id", "VARCHAR(10)", "Mã đánh giá (r001...)", "PK"),
        ("reviewer_name", "VARCHAR(100)", "Tên người viết", "NOT NULL"),
        ("rating", "DECIMAL(2,1)", "Điểm trung bình các mục", "1,0 - 5,0"),
        ("verified", "BOOLEAN", "Người mua đã xác minh", "NOT NULL"),
        ("lang", "CHAR(2)", "Ngôn ngữ", "NOT NULL"),
    ]),
    ("REVIEW_ENTRY", "Một mục đánh giá cho một sản phẩm", "Mảng entries trong REVIEW", [
        ("entry_id", "INT", "Định danh", "PK"),
        ("review_id", "VARCHAR(10)", "Đánh giá cha", "FK → REVIEW"),
        ("rating", "DECIMAL(2,1)", "Điểm", "1,0 - 5,0"),
        ("text", "TEXT", "Nội dung", "NOT NULL"),
        ("product_name", "VARCHAR(150)", "Tên sản phẩm được đánh giá (so khớp tên, không phải FK)", "NULL"),
    ]),
    ("REVIEW_IMAGE", "Ảnh kèm đánh giá", "Mảng images trong REVIEW", [
        ("image_id", "INT", "Định danh", "PK"),
        ("review_id", "VARCHAR(10)", "Đánh giá", "FK → REVIEW"),
        ("path", "VARCHAR(200)", "Đường dẫn ảnh (thử .webp rồi .jpg)", "NOT NULL"),
    ]),
]


def build(R, ctx):
    D = ctx["diag"]
    R.chapter(6, "THIẾT KẾ CƠ SỞ DỮ LIỆU")
    R.p("Website không có cơ sở dữ liệu thật vì không có máy chủ ứng dụng. Tuy vậy, nhóm vẫn thiết kế **mô hình dữ liệu logic** "
        "như một cơ sở dữ liệu quan hệ: dữ liệu đang nằm trong các file JSON, XML và localStorage được chuẩn hoá thành 18 thực "
        "thể, xác định thuộc tính, khoá và quan hệ. Mô hình này vừa giúp lập trình nhất quán, vừa là bản thiết kế sẵn sàng khi "
        "nâng cấp lên máy chủ và cơ sở dữ liệu thật.")
    R.h3("6.1. Nhận diện, mô tả và xác định thuộc tính các thực thể")
    R.table(["STT", "Thực thể", "Mô tả", "Nơi lưu thực tế"],
            [(str(i), e[0], e[1], e[2]) for i, e in enumerate(ENTITIES, 1)],
            widths=[1.2, 3.6, 5.2, 7.0], caption="Bảng nhận diện các thực thể", size=11, center_cols=(0,))
    R.h3("6.2. Mối quan hệ giữa các thực thể")
    R.table(["Quan hệ", "Bản số", "Giải thích"], [
        ("USER - ORDER", "0..1 - 0..n", "Một tài khoản có nhiều đơn; đơn khách vãng lai không gắn tài khoản"),
        ("ATHLETE_CODE - ORDER", "0..1 - 0..n", "Một mã dùng cho nhiều đơn; đơn có thể không dùng mã"),
        ("ORDER - ORDER_ITEM", "1 - 1..n", "Mỗi đơn có ít nhất một dòng hàng"),
        ("PRODUCT - ORDER_ITEM", "1 - 0..n", "Một sản phẩm nằm trong nhiều đơn"),
        ("PRODUCT - CART_ITEM", "1 - 0..n", "Giỏ hàng lưu theo sản phẩm + màu + size"),
        ("PRODUCT - PRODUCT_COLOR", "1 - 1..n", "Mỗi sản phẩm có ít nhất một màu"),
        ("PRODUCT_COLOR - COLOR_IMAGE", "1 - 1..n", "Mỗi màu có ít nhất một ảnh"),
        ("PRODUCT - PRODUCT_SIZE", "1 - 1..n", "Mỗi sản phẩm bán ít nhất một size"),
        ("PRODUCT - PRODUCT_FEATURE", "1 - 0..n", "Sản phẩm có thể có nhiều đặc điểm nổi bật"),
        ("CATEGORY_WEIGHT - PRODUCT", "1 - 0..n", "Khối lượng ước tính theo loại, dùng để tính cước"),
        ("SHIPPING_ZONE - COUNTRY", "1 - 1..n", "Mỗi vùng gồm nhiều nước"),
        ("COUNTRY - ORDER", "1 - 0..n", "Phí ship, thuế tính theo nước nhận của đơn"),
        ("REVIEW - REVIEW_ENTRY", "1 - 1..n", "Một người đánh giá nhiều sản phẩm"),
        ("REVIEW - REVIEW_IMAGE", "1 - 0..n", "Đánh giá có thể kèm nhiều ảnh"),
        ("PRODUCT_SIZE ··· SIZE_CHART_ROW", "tra cứu", "Bảng size tra theo size + giới tính, không phải khoá ngoại"),
    ], widths=[5.6, 2.6, 8.8], caption="Mối quan hệ giữa các thực thể", size=11, center_cols=(1,))
    R.h3("6.3. Sơ đồ quan hệ thực thể (ERD)")
    R.p(R.next_fig() + " là sơ đồ ERD theo ký pháp chân chim. Thực thể màu xanh dương là dữ liệu gốc trong thư mục `data/`, đọc "
        "bằng `fetch`/`XMLHttpRequest`; màu xanh lá là dữ liệu sinh ra khi dùng web, lưu trong localStorage. Dòng chữ nghiêng "
        "dưới tên thực thể ghi nơi lưu thật; nét đứt là tra cứu bằng giá trị, không phải khoá ngoại.")
    R.figure(D / "02-erd-p1.png", "Sơ đồ quan hệ thực thể (ERD)", width=17)
    R.h3("6.4. Định nghĩa kiểu dữ liệu")
    R.p("Kiểu dữ liệu ghi theo cách khai báo của cơ sở dữ liệu quan hệ (để dùng khi nâng cấp); cột Ràng buộc ghi các điều kiện "
        "mà mã nguồn hiện đang kiểm tra (`js/storage.js`, `js/form-validate.js`, `js/admin.js`).")
    for name, desc, store, attrs in ENTITIES:
        R.table(["Tên thuộc tính", "Kiểu dữ liệu", "Mô tả", "Ràng buộc"], attrs, widths=[4.0, 3.2, 6.0, 3.8],
                caption="BẢNG " + name, size=11, align_cells=C)
    R.h3("6.5. Dữ liệu mẫu minh hoạ")
    R.p("Các đoạn dưới đây là bản ghi thật trong dữ liệu của website (một số mảng ảnh được rút gọn), giúp đối chiếu thiết kế "
        "logic ở mục 6.4 với cách lưu thực tế.")
    R.code("""{
  "id": "p12",
  "name": "Essential Embroidery Cuff Beanie",
  "category": "accessories",
  "gender": "unisex",
  "price": 40.0,
  "currency": "USD",
  "colors": [
    { "name": "Heavenly Pink", "hex": "#f0b6c8", "available": true,
      "images": ["assets/products/mens-embroidery-cuff-beanie-heavenly-pink-.../01.webp", "..."] },
    { "name": "Void Black", "hex": "#0a0a0a", "available": true, "images": ["..."] }
  ],
  "sizes": ["One size"],
  "featured": false,
  "stock": 70,
  "specs": { "fit": "Cuffed fit, one size fits all", "care": "Machine wash cold, hang dry." },
  "features": ["Premium ribbed knit", "Embroidered SANCTUARY logo", "Cuffed fit, one size fits all"]
}""", caption="Một sản phẩm trong data/products.json (thực thể PRODUCT, PRODUCT_COLOR, COLOR_IMAGE, PRODUCT_SIZE, PRODUCT_FEATURE):")
    R.code("""{
  "number": "SD-MWB50U4A",
  "date": "2026-11-11T05:02:14.000Z",
  "items": [ { "id": "p04", "color": "Nightmare", "size": "M", "qty": 2 },
             { "id": "p12", "color": "Void Black", "size": "One size", "qty": 1 } ],
  "currency": "VND",
  "customer": { "name": "Minh Tran", "email": "minh.tran@example.com", "phone": "0903456789",
                "address": "45 Le Loi Street", "city": "Ho Chi Minh City", "country": "Vietnam" },
  "payment": "card",
  "discountCode": "SANCTUARY-DEMO",
  "totalUsd": 182.57,
  "status": "Processing",
  "stockDeducted": true,
  "userEmail": "minh.tran@example.com"
}""", caption="Một đơn hàng trong localStorage sanctuary_orders (thực thể ORDER, ORDER_ITEM; số liệu minh hoạ):")
    R.code("""<country name="Japan" zone="asia">
  <tax label="Consumption tax">10</tax>
  <duty pct="0" perItemUsd="0"/>
</country>
<zone id="asia" base="12" perKg="5"/>
<category id="compression" kg="0.25"/>""", caption="Trích data/shipping.xml (thực thể COUNTRY, SHIPPING_ZONE, CATEGORY_WEIGHT):")
    R.code("""{ "influencers": [ { "name": "Demo Creator", "code": "SANCTUARY-DEMO", "active": true } ] }""",
           caption="Nội dung data/access.json (thực thể ATHLETE_CODE):")
    R.p("Với đơn mẫu trên (giao trong Việt Nam): tạm tính 2 × 71 + 40 = 182 USD, giảm 10% còn 163,80 USD; khối lượng 0,15 + "
        "2 × 0,25 + 0,40 = 1,05 kg, làm tròn lên 1,5 kg, phí ship 3 + 1,5 × 1,5 = 5,25 USD; không có thuế nhập khẩu; VAT 8% × "
        "(163,80 + 5,25) = 13,52 USD; tổng 182,57 USD, đúng như cách tính ở lưu đồ mục 3.9.3.")
    R.p("Đơn hàng lưu thêm `currency` (tiền khách đang xem) nhưng tổng tiền luôn quy về USD (`totalUsd`) để doanh thu ở trang "
        "quản trị cộng được với nhau; trường `stockDeducted` cho biết đơn đã trừ kho, nhờ đó khi huỷ đơn hệ thống biết có cần "
        "hoàn kho hay không.")

    R.h3("6.6. Đối chiếu, so sánh giữa cơ sở dữ liệu trên lý thuyết và trên thực tế")
    R.ps(
        "Vì dữ liệu thực tế nằm trong file JSON/XML và localStorage (chỉ lưu chuỗi theo khoá), cách lưu có nhiều điểm khác với "
        "mô hình quan hệ ở trên. Nhóm chủ động chọn các cách này để phù hợp web tĩnh, đồng thời dùng mã nguồn để mô phỏng các "
        "tính chất quan trọng của cơ sở dữ liệu như ràng buộc, transaction và xoá mềm.")
    R.table(["Lý thuyết (CSDL quan hệ)", "Thực tế trên web", "Lý do"], [
        ("Mỗi thực thể là một bảng riêng", "Màu, ảnh, size, đặc điểm lồng bên trong từng sản phẩm của products.json", "Đọc một lần là đủ, không cần JOIN"),
        ("ORDER_ITEM là bảng riêng", "Nằm trong mảng items của từng đơn", "Đơn và dòng hàng luôn đọc/ghi cùng nhau"),
        ("Thông tin giao hàng tham chiếu USER", "Đơn chép lại tên, địa chỉ vào customer", "Sửa hồ sơ sau này không đổi đơn cũ; khách vãng lai không có USER"),
        ("UPDATE từng dòng", "Đọc cả danh sách → sửa → ghi đè cả khoá localStorage", "localStorage chỉ lưu chuỗi theo khoá"),
        ("Transaction", "writeAll() ghi nhiều khoá, lỗi giữa chừng thì trả lại giá trị cũ", "Mô phỏng tính nguyên tử"),
        ("UPDATE bảng PRODUCT", "Lưu phần thay đổi vào sanctuary_product_overrides rồi đè lên dữ liệu gốc khi đọc", "Trình duyệt không ghi được file JSON"),
        ("DELETE", "Đánh dấu deleted: true (xoá mềm)", "Đơn cũ vẫn tra được tên sản phẩm; khôi phục được"),
        ("Ràng buộc khoá ngoại", "Không có ràng buộc tự động; mã nguồn tự kiểm tra (giỏ bỏ món bị xoá, hết màu)", "localStorage không có ràng buộc"),
        ("Kiểm tra kiểu khi ghi", "Kiểm tra khi đọc: isValidOrder, isValidUser... bỏ qua bản ghi sai", "Dữ liệu có thể bị sửa tay bằng công cụ trình duyệt"),
        ("Dữ liệu dùng chung mọi máy", "localStorage riêng từng trình duyệt", "Giới hạn của web không có máy chủ"),
    ], widths=[4.6, 7.0, 5.4], caption="So sánh mô hình dữ liệu lý thuyết và cách lưu thực tế", size=11)
    R.table(["Trạng thái", "Ý nghĩa nghiệp vụ", "Lý thuyết (ORDER.status)", "Thực tế trên web"], [
        ("Processing", "Đơn mới đặt, đang chuẩn bị", "status = 'processing'; tồn kho giữ chỗ", "Gán khi đặt hàng; tồn kho đã trừ (stockDeducted = true)"),
        ("Shipped", "Đã giao cho đơn vị vận chuyển", "status = 'shipped'", "Quản trị viên chọn trong bảng Orders"),
        ("Delivered", "Khách đã nhận hàng", "status = 'delivered'", "Quản trị viên chọn; khách thấy ở trang Account"),
        ("Cancelled", "Đơn bị huỷ", "status = 'cancelled'; hoàn tồn kho bằng trigger", "Mã nguồn cộng lại kho khi chuyển sang Cancelled; doanh thu không tính đơn này"),
    ], widths=[2.6, 4.0, 4.8, 5.6], caption="So sánh cách định nghĩa trạng thái đơn hàng giữa lý thuyết và thực tế", size=11)
    R.table(["Khoá localStorage / sessionStorage", "Thực thể tương ứng", "Kiểu lưu"], [
        ("sanctuary_cart", "CART_ITEM", "Mảng JSON"), ("sanctuary_orders", "ORDER, ORDER_ITEM", "Mảng JSON"),
        ("sanctuary_users", "USER", "Mảng JSON"), ("sanctuary_session", "Phiên đăng nhập (email)", "Chuỗi"),
        ("sanctuary_messages", "MESSAGE", "Mảng JSON"), ("sanctuary_athletes", "ATHLETE_CODE (bản đã sửa)", "Mảng JSON"),
        ("sanctuary_product_overrides", "PRODUCT (giá, kho, ẩn, xoá)", "Object JSON theo mã sản phẩm"),
        ("sanctuary_custom_products", "PRODUCT do quản trị viên thêm", "Mảng JSON"),
        ("sanctuary_currency, sanctuary_rates", "Tiền tệ đã chọn, tỷ giá lưu tạm", "Chuỗi, object JSON"),
        ("sanctuary_launch_override", "Ngày ra mắt do quản trị viên đặt", "Số (timestamp)"),
        ("sanctuary_role, sanctuary_source (sessionStorage)", "Vai trò, athlete giới thiệu", "Chuỗi"),
    ], widths=[6.6, 5.6, 4.8], caption="Các khoá lưu trữ trên trình duyệt", size=11)
