# -*- coding: utf-8 -*-
"""Chương 3. Phương pháp thực hiện (quy trình, đặc tả hệ thống, sơ đồ giải thuật, dữ liệu, công cụ, cách đánh giá)."""


def build(R, ctx):
    D = ctx["diag"]
    sc = ctx["size_chart"]
    R.h1("CHƯƠNG 3. PHƯƠNG PHÁP THỰC HIỆN", chapter=3)

    # ---------- 3.1 Quy trình ----------
    R.h2("3.1. Quy trình triển khai")
    R.p("Nhóm triển khai đồ án theo bảy bước, tương ứng các giai đoạn trong kế hoạch ở mục 1.6. Các bước 4 - 6 lặp lại "
        "nhiều vòng, mỗi vòng thêm một nhóm chức năng.")
    R.table(["Bước", "Nội dung", "Kết quả"], [
        ("1. Khảo sát", "Phân tích breathedivinity.com và yêu cầu học phần", "Danh sách chức năng, phạm vi"),
        ("2. Phân tích", "Xác định tác nhân, yêu cầu chức năng và phi chức năng", "Bảng yêu cầu (mục 3.2)"),
        ("3. Thiết kế", "Kiến trúc, sơ đồ trang, Use case, ERD, DFD, BPMN, lưu đồ, nhận diện thương hiệu", "Bộ sơ đồ (mục 3.3, 3.4)"),
        ("4. Chuẩn bị dữ liệu", "Thu thập dữ liệu mẫu, xử lý ảnh, tính bảng size", "Các file trong data/ và assets/"),
        ("5. Lập trình", "HTML semantic → CSS mobile-first → JavaScript theo từng mô-đun", "Mã nguồn, commit theo tính năng"),
        ("6. Kiểm thử", "Kiểm thử chức năng, đo Lighthouse, W3C, sửa lỗi", "Bảng kết quả (mục 4.7)"),
        ("7. Triển khai", "Đẩy lên GitHub, Vercel tự triển khai; cài thử WooCommerce", "Website online, bản cài thử"),
    ], widths=[3.2, 7.8, 5.0], caption="Các bước triển khai đồ án")

    # ---------- 3.2 Yêu cầu ----------
    R.h2("3.2. Phân tích yêu cầu")
    R.h3("3.2.1. Tác nhân")
    R.p("Hệ thống có ba tác nhân. **Khách** là người đã nhập đúng mã athlete ở trang cổng, mua được hàng mà không cần "
        "tài khoản. **Thành viên** là khách có tài khoản, kế thừa mọi chức năng của khách và có thêm chức năng tài khoản. "
        "**Quản trị viên** nhập mã admin ở trang cổng và chỉ vào được trang quản trị. Ngoài ra web gọi một hệ thống bên "
        "ngoài là dịch vụ tỷ giá open.er-api.com.")
    R.h3("3.2.2. Yêu cầu chức năng")
    R.table(["Nhóm", "Yêu cầu chức năng", "Tác nhân"], [
        ("Truy cập", "Trang cổng có đếm ngược tới ngày ra mắt; vào web bằng mã athlete; chặn trang khi chưa qua cổng", "Khách"),
        ("Sản phẩm", "Xem theo 3 khu (nam, nữ, phụ kiện) và nhóm; lọc theo size, màu; sắp xếp theo giá; đổi tiền tệ", "Khách"),
        ("Chi tiết", "Popup ảnh theo màu, chọn size, số lượng, xem tồn kho, bảng size, gợi ý size, đánh giá liên quan", "Khách"),
        ("Đánh giá", "Xem đánh giá có ảnh; lọc theo số sao, dòng nam/nữ, loại sản phẩm", "Khách"),
        ("Giỏ hàng", "Thêm, đổi số lượng, xoá; không vượt tồn kho; lưu khi tắt trình duyệt; gợi ý sản phẩm khác", "Khách"),
        ("Thanh toán", "Form giao hàng và thẻ có kiểm tra; mã giảm giá 10%; tính phí ship, thuế theo nước; lưu đơn, trừ kho", "Khách"),
        ("Tài khoản", "Đăng ký, đăng nhập, sửa hồ sơ, đổi mật khẩu, xem lịch sử và trạng thái đơn", "Thành viên"),
        ("Thông tin", "Form liên hệ; chính sách giao hàng, đổi trả, điều khoản, quyền riêng tư; bản đồ; giới thiệu thương hiệu", "Khách"),
        ("Quản trị", "Tổng quan doanh thu; đơn hàng; sản phẩm; khách hàng; tin nhắn; mã athlete; ngày ra mắt; sao lưu", "Quản trị viên"),
    ], widths=[2.6, 10.6, 2.8], caption="Yêu cầu chức năng theo nhóm", size=11)
    R.h3("3.2.3. Yêu cầu phi chức năng")
    R.table(["Loại", "Yêu cầu"], [
        ("Giao diện", "Tông đen, chữ trắng, điểm nhấn đỏ; chữ gothic cho tiêu đề; ảnh sản phẩm lớn; ghi chú “student project, not a real store” ở chân trang"),
        ("Đáp ứng", "Dùng tốt trên điện thoại (390 px), máy tính bảng (820 px), máy tính (1440 px)"),
        ("Hiệu năng", "Ảnh WebP, video nén, tải lười (lazy loading); LCP trên máy tính ≤ 2,5 s"),
        ("Khả năng truy cập", "HTML semantic, nhãn cho ô nhập, điều khiển bằng bàn phím, điểm Lighthouse Accessibility ≥ 90"),
        ("Bảo mật (mô phỏng)", "Không lưu mật khẩu chữ thô; mã admin chỉ lưu dạng băm; ghi dữ liệu người dùng bằng textContent"),
        ("Bền vững dữ liệu", "Đọc localStorage có kiểm tra cấu trúc; ghi đơn hàng và tồn kho cùng lúc; có sao lưu, khôi phục"),
        ("Dễ bảo trì", "JavaScript chia mô-đun, CSS chia file theo vai trò, comment tiếng Việt ở đoạn quan trọng"),
        ("Triển khai", "Chạy bằng Live Server trên máy; chạy online trên Vercel, không cần máy chủ ứng dụng"),
    ], widths=[3.6, 12.4], caption="Yêu cầu phi chức năng", size=11)

    # ---------- 3.3 Đặc tả ----------
    R.h2("3.3. Mô hình đề xuất và đặc tả hệ thống")
    R.h3("3.3.1. Kiến trúc hệ thống")
    R.p(R.next_fig() + " mô tả kiến trúc client/server của SANCTUARY. Máy chủ Vercel chỉ phục vụ file tĩnh qua HTTPS và "
        "CDN; không có CSDL hay mã chạy phía máy chủ. Trình duyệt tải trang HTML, CSS, JavaScript, rồi JavaScript đọc dữ "
        "liệu JSON bằng `fetch`, XML bằng `XMLHttpRequest`, gọi API tỷ giá, và lưu trạng thái trong Web Storage. Máy của "
        "nhóm phát triển đẩy mã lên GitHub; Vercel tự triển khai lại sau mỗi commit.")
    R.figure(D / "06-architecture-p1.png", "Kiến trúc hệ thống SANCTUARY", width=16)
    R.h3("3.3.2. Sơ đồ trang")
    R.p("Từ trang cổng, mã athlete dẫn vào trang chủ, mã admin dẫn vào trang quản trị (" + R.next_fig() + "). Trang chủ "
        "gom cả cửa hàng và các popup để khách không phải chuyển trang khi duyệt sản phẩm; trang Info dùng tab chuyển "
        "bằng địa chỉ `#mục` để chia sẻ được đường dẫn tới từng chính sách.")
    R.figure(D / "06-architecture-p2.png", "Sơ đồ trang (sitemap) của website", width=16)

    R.h3("3.3.3. Sơ đồ Use case")
    R.p(R.next_fig() + " là sơ đồ Use case tổng quan gồm 3 tác nhân và 24 use case. Thành viên kế thừa toàn bộ use case "
        "của khách (quan hệ tổng quát hoá). Hai quan hệ «extend»: xem bảng size, gợi ý size (UC04) mở rộng xem chi tiết "
        "sản phẩm (UC03); áp mã giảm giá (UC08) mở rộng đặt hàng (UC07), vì khách có thể đặt hàng mà không cần mã.")
    R.figure(D / "01-usecase-p1.png", "Sơ đồ Use case tổng quan", width=14.5)
    R.table(["Mã", "Use case", "Tác nhân", "File mã nguồn chính"], [
        ("UC01", "Vào web bằng mã athlete", "Khách", "js/gate.js, js/athletes.js"),
        ("UC02", "Xem, lọc và sắp xếp sản phẩm", "Khách", "js/shop.js"),
        ("UC03, UC04", "Xem chi tiết; bảng size, gợi ý size", "Khách", "js/product-popup.js, js/size-finder.js"),
        ("UC05", "Xem và lọc đánh giá", "Khách", "js/reviews.js"),
        ("UC06", "Quản lý giỏ hàng", "Khách", "js/cart.js, js/cart-page.js"),
        ("UC07, UC08", "Đặt hàng; áp mã giảm giá", "Khách", "js/cart-page.js, js/shipping.js"),
        ("UC09, UC10", "Đổi tiền tệ; gửi liên hệ", "Khách", "js/currency.js, js/contact.js"),
        ("UC11 - UC15", "Đăng ký, đăng nhập, sửa hồ sơ, đổi mật khẩu, xem lịch sử đơn", "Thành viên", "js/auth.js, js/account-page.js"),
        ("UC16 - UC24", "Vào trang quản trị, tổng quan, đơn hàng, sản phẩm, khách, tin nhắn, mã athlete, ngày ra mắt, sao lưu", "Quản trị viên", "js/admin.js, js/guard.js"),
    ], widths=[2.3, 6.6, 2.6, 4.5], caption="Tóm tắt use case và file mã nguồn tương ứng", size=11)

    R.h3("3.3.4. Sơ đồ quan hệ thực thể (ERD)")
    R.p("Website không có CSDL thật, nên ERD ở " + R.next_fig() + " là **mô hình dữ liệu logic**: dữ liệu đang nằm trong "
        "các file JSON/XML và localStorage được chuẩn hoá thành 18 thực thể như một CSDL quan hệ, để thấy rõ thực thể và "
        "quan hệ. Thực thể màu xanh dương là dữ liệu gốc trong thư mục `data/`, màu xanh lá là dữ liệu sinh ra khi dùng "
        "web (lưu trong localStorage).")
    R.figure(D / "02-erd-p1.png", "Sơ đồ quan hệ thực thể (mô hình dữ liệu logic)", width=16)
    R.table(["Mô hình lý thuyết", "Cách SANCTUARY lưu thật", "Lý do"], [
        ("Mỗi thực thể là một bảng", "Màu, ảnh, size lồng trong từng sản phẩm của products.json", "Đọc một lần là đủ, không cần JOIN"),
        ("ORDER_ITEM là bảng riêng", "Nằm trong mảng items của từng đơn", "Đơn và món luôn đọc/ghi cùng nhau"),
        ("Giao hàng tham chiếu USER", "Đơn chép lại tên, địa chỉ vào customer", "Sửa hồ sơ sau không làm đổi đơn cũ"),
        ("Transaction", "writeAll() ghi nhiều khoá, lỗi giữa chừng thì trả lại giá trị cũ", "Mô phỏng tính nguyên tử"),
        ("UPDATE bảng PRODUCT", "Lưu phần thay đổi vào sanctuary_product_overrides rồi đè lên dữ liệu gốc", "Trình duyệt không ghi được file"),
        ("DELETE", "Đánh dấu deleted: true (xoá mềm)", "Đơn cũ vẫn tra được tên sản phẩm"),
        ("Ràng buộc kiểu dữ liệu", "Kiểm tra khi đọc: isValidOrder, isValidUser trong js/storage.js", "Dữ liệu có thể bị sửa tay"),
    ], widths=[4.0, 7.0, 5.0], caption="Đối chiếu mô hình dữ liệu lý thuyết và cách lưu thực tế", size=11)

    R.h3("3.3.5. Sơ đồ luồng dữ liệu (DFD)")
    R.p("DFD dùng ký pháp Gane-Sarson. Ở mức ngữ cảnh (" + R.next_fig() + "), cả website là một tiến trình trao đổi dữ liệu "
        "với ba tác nhân ngoài: khách hàng, quản trị viên và dịch vụ tỷ giá. Ở mức 0, hệ thống tách thành 7 tiến trình "
        "và 10 kho dữ liệu.")
    R.figure(D / "03-dfd-p1.png", "DFD mức ngữ cảnh", width=14)
    R.figure(D / "03-dfd-p2.png", "DFD mức 0", width=16)
    R.table(["Tiến trình", "Việc xử lý", "Kho đọc", "Kho ghi"], [
        ("1.0 Xác thực truy cập", "So mã admin (băm SHA-256), rồi mã athlete đang bật", "D3", "sessionStorage"),
        ("2.0 Duyệt, lọc sản phẩm", "Lọc, sắp xếp, popup, bảng size, gợi ý size, đánh giá, đổi tiền", "D1, D2, D5, D10", "D10"),
        ("3.0 Quản lý giỏ hàng", "Thêm, sửa số lượng, xoá; không vượt tồn kho", "D1, D6", "D6"),
        ("4.0 Đặt hàng", "Kiểm tra form, áp mã, tính ship/thuế, lưu đơn, trừ kho", "D1, D3, D4, D6, D8", "D1, D6, D7"),
        ("5.0 Quản lý tài khoản", "Đăng ký, đăng nhập, sửa hồ sơ, đổi mật khẩu, lịch sử đơn", "D7, D8", "D8"),
        ("6.0 Gửi liên hệ", "Kiểm tra form rồi lưu tin nhắn", "-", "D9"),
        ("7.0 Quản trị cửa hàng", "Đơn, sản phẩm, khách, tin nhắn, mã athlete, ngày ra mắt, sao lưu", "D1, D3, D7, D8, D9", "D1, D3, D7, D9"),
    ], widths=[3.8, 6.6, 3.0, 2.6], caption="Các tiến trình của DFD mức 0", size=11)
    R.p("Các kho dữ liệu: D1 sản phẩm (products.json + thay đổi của quản trị viên), D2 đánh giá, D3 mã athlete, D4 phí "
        "ship và thuế (shipping.xml), D5 bảng size, D6 giỏ hàng, D7 đơn hàng, D8 tài khoản, D9 tin nhắn, D10 tỷ giá (lưu "
        "tạm kết quả API trong 1 giờ).")

    R.h3("3.3.6. Sơ đồ quy trình nghiệp vụ (BPMN)")
    R.p("Nhóm mô tả 8 quy trình nghiệp vụ bằng BPMN 2.0, mỗi quy trình một pool chia lane theo người thực hiện. Hai quy "
        "trình quan trọng nhất được trình bày dưới đây; sáu quy trình còn lại ở Phụ lục D. Quy trình đặt hàng (" +
        R.next_fig() + ") đáng chú ý ở chỗ website **kiểm tra lại giỏ hàng ngay lúc bấm đặt** (giỏ có thể vừa đổi ở tab "
        "khác) và **ghi đơn hàng cùng tồn kho trong một lần**, nên không bao giờ có đơn đã lưu mà kho chưa trừ.")
    R.figure(D / "04-bpmn-p5.png", "BPMN quy trình đặt hàng", width=16)
    R.p("Ở quy trình quản trị viên xử lý đơn (" + R.next_fig() + "), khi huỷ một đơn, hệ thống cộng lại số lượng vào "
        "kho; nếu mở lại đơn đã huỷ thì trừ kho lần nữa; nếu lưu lỗi thì ô chọn trạng thái quay về giá trị cũ.")
    R.figure(D / "04-bpmn-p6.png", "BPMN quy trình quản trị viên xử lý đơn hàng", width=16)

    R.h3("3.3.7. Tổ chức mã nguồn")
    R.code("""/
├── index.html              Trang cổng: đếm ngược, lookbook, ô nhập mã
├── pages/                  home, cart, contact, about, account, admin (.html)
├── css/                    reset, base, components (sinh từ LESS), pages, admin
│   └── less/               components.less (nguồn LESS)
├── js/                     27 mô-đun ES: gate, guard, shop, product-popup, cart,
│                           cart-page, shipping, size-finder, auth, admin, ...
├── data/                   products.json, reviews.json, access.json,
│                           size-chart.json, shipping.xml, ANSUR_II_*.csv
├── assets/                 logo, fonts, products (WebP), reviews, videos
├── tools/                  Script Python: crawl, tạo dữ liệu, bảng size, nén ảnh;
│   └── woocommerce/        blueprint + script nhập dữ liệu cho bản cài thử
└── docs/                   sơ đồ (diagrams/), báo cáo (report/)""",
           caption="Cấu trúc thư mục dự án:")
    R.p("Mã nguồn gồm " + str(ctx["html_lines"]) + " dòng HTML, " + str(ctx["css_lines"]) + " dòng CSS và " +
        str(ctx["js_lines"]) + " dòng JavaScript trong " + str(ctx["js_files"]) + " mô-đun. Mỗi mô-đun một nhiệm vụ: "
        "`storage.js` đọc/ghi localStorage an toàn, `cart.js` quản lý giỏ, `shipping.js` tính phí ship và thuế, "
        "`form-validate.js` chứa luật kiểm tra dùng chung, `guard.js` chặn trang theo vai trò. CSS chia theo vai trò: "
        "`reset.css` (đặt lại mặc định), `base.css` (biến màu, font), `components.css` (nút, ô nhập), `pages.css` (từng "
        "trang), `admin.css` (trang quản trị).")

    # ---------- 3.4 Sơ đồ giải thuật ----------
    R.h2("3.4. Sơ đồ giải thuật")
    R.p("Outline yêu cầu sơ đồ giải thuật (GA). Đồ án không dùng thuật toán di truyền, nên nhóm hiểu mục này là **lưu đồ "
        "giải thuật** của các thuật toán thật trong mã nguồn. Năm thuật toán được chọn vì quyết định tính đúng đắn của "
        "website: kiểm tra mã cổng, gợi ý size, tính tổng tiền, đặt hàng và kiểm tra số thẻ. Ký hiệu: hình bầu dục là bắt "
        "đầu/kết thúc, chữ nhật là xử lý, hình thoi là điều kiện, hình bình hành là nhập/xuất, hình trụ là dữ liệu, ô đỏ "
        "là thông báo lỗi.")
    R.h3("3.4.1. Kiểm tra mã ở trang cổng")
    R.p("Trong " + R.next_fig() + ", mã được kiểm tra theo thứ tự: rỗng → mã admin → mã athlete. Mã admin không lưu dạng "
        "chữ trong mã nguồn mà chỉ lưu giá trị băm SHA-256; trình duyệt băm chuỗi vừa nhập rồi so sánh hai giá trị băm. "
        "Mã athlete so khớp không phân biệt hoa thường và chỉ tính các mã đang bật, nên quản trị viên tắt một mã là khách "
        "của athlete đó không vào được nữa.")
    R.figure(D / "05-flowchart-p1.png", "Lưu đồ kiểm tra mã ở trang cổng (js/gate.js)", height=17)
    R.h3("3.4.2. Gợi ý size")
    hm, hf = sc["him"], sc["her"]
    R.p("Thuật toán ở " + R.next_fig() + " gồm ba phần. Thứ nhất, đổi đơn vị (chấp nhận `5'11`, `180 cm`, `1.8 m`, "
        "`165 lbs`, `75 kg`) và loại giá trị vô lý. Thứ hai, ước lượng vòng ngực bằng hồi quy tuyến tính học từ ANSUR II: "
        "với nam `ngực = " + str(hm["intercept"]).replace(".", ",") + " + " + str(hm["perKg"]).replace(".", ",") +
        " × kg − " + str(abs(hm["perCm"])).replace(".", ",") + " × cm`, với nữ `ngực = " + str(hf["intercept"]).replace(".", ",") +
        " + " + str(hf["perKg"]).replace(".", ",") + " × kg − " + str(abs(hf["perCm"])).replace(".", ",") + " × cm`. Hệ số "
        "chiều cao âm vì ở cùng cân nặng, người cao hơn thường gầy hơn. Thứ ba, tra vòng ngực vào các mốc của bảng size "
        "(nam: 84, 90, 96, 104, 112, 120 cm); với đồ bó sát, nếu vòng ngực cách mốc trên dưới 1 cm thì tăng một size cho "
        "thoải mái, và cuối cùng chỉ gợi ý size mà sản phẩm đang bán.")
    R.figure(D / "05-flowchart-p2.png", "Lưu đồ gợi ý size (js/size-finder.js)", height=18)
    R.h3("3.4.3. Tính tổng tiền đơn hàng")
    R.p("Theo " + R.next_fig() + ", khối lượng đơn bằng 0,15 kg bao bì cộng khối lượng ước tính theo loại của từng món. "
        "Khối lượng tính cước được làm tròn lên mỗi 0,5 kg như cách các hãng vận chuyển tính. Phí ship = phí gốc của vùng "
        "+ giá mỗi kg × khối lượng tính cước. Thuế nhập khẩu tính trên tiền hàng sau giảm giá, cộng mức cố định mỗi món "
        "(áp dụng cho EU). VAT/GST tính trên tổng tiền hàng, phí ship và thuế nhập khẩu. Ví dụ: một áo Doom Tech (0,25 kg) "
        "và hai mũ len (0,4 kg mỗi chiếc) gửi đi Mỹ có khối lượng 1,20 kg, làm tròn lên 1,5 kg, phí ship = 24 + 10 × 1,5 "
        "= 39 USD, đúng với số hiển thị trên trang giỏ hàng (mục 4.2.5).")
    R.figure(D / "05-flowchart-p3.png", "Lưu đồ tính tổng tiền (js/shipping.js, js/cart-page.js)", height=17)
    R.h3("3.4.4. Đặt hàng")
    R.p("Lưu đồ đặt hàng (" + R.next_fig() + ") có ba lớp bảo vệ dữ liệu: kiểm tra form, kiểm tra lại giỏ hàng, và ghi "
        "đơn cùng tồn kho bằng hàm `writeAll()`. Hàm này lưu giá trị cũ của các khoá trước khi ghi; nếu một lần ghi bị lỗi "
        "(ví dụ localStorage đầy) thì khôi phục toàn bộ giá trị cũ, mô phỏng tính nguyên tử (atomicity) của transaction "
        "trong CSDL.")
    R.figure(D / "05-flowchart-p4.png", "Lưu đồ đặt hàng (js/cart-page.js)", height=18)
    R.h3("3.4.5. Kiểm tra số thẻ bằng thuật toán Luhn")
    R.p("Thuật toán Luhn (" + R.next_fig() + ") phát hiện lỗi gõ nhầm số thẻ: đi từ chữ số cuối về đầu, nhân đôi các chữ "
        "số ở vị trí lẻ (nếu kết quả lớn hơn 9 thì trừ 9), cộng tất cả lại; số thẻ hợp lệ khi tổng chia hết cho 10. Ví "
        "dụ số thẻ thử `4242 4242 4242 4242` có tổng 80 nên hợp lệ; đổi chữ số cuối thành 1 thì tổng 79, bị báo lỗi (ca "
        "kiểm thử TC23).")
    R.figure(D / "05-flowchart-p5.png", "Lưu đồ thuật toán Luhn (js/form-validate.js)", height=17)

    # ---------- 3.5 Dữ liệu và công cụ ----------
    R.h2("3.5. Dữ liệu và công cụ sử dụng")
    R.table(["Dữ liệu", "Nguồn và cách tạo", "Quy mô"], [
        ("products.json", "Thu thập từ breathedivinity.com (tools/crawl_breathedivinity.py), chuẩn hoá bằng build_products.py; giá USD, tồn kho giả lập",
         str(ctx["n_products"]) + " sản phẩm, " + str(ctx["n_colors"]) + " biến thể màu"),
        ("reviews.json", "Đánh giá thật của khách trên breathedivinity.com, gộp theo người viết (build_reviews.py)", str(ctx["n_reviews"]) + " đánh giá, 192 ảnh"),
        ("size-chart.json", "Tính từ ANSUR II (Gordon và cộng sự, 2014) bằng build_size_chart.py: hệ số hồi quy và bảng size",
         "{:,}".format(hm["sampleSize"]).replace(",", ".") + " nam, " + "{:,}".format(hf["sampleSize"]).replace(",", ".") + " nữ"),
        ("shipping.xml", "Nhóm tự lập: phí theo vùng, thuế VAT/GST, thuế nhập khẩu (số ước tính)", "6 vùng, 15 nước, 8 loại hàng"),
        ("access.json", "Danh sách mã athlete (mã truy cập, kiêm mã giảm giá 10%)", "1 mã mẫu"),
        ("Tỷ giá", "API open.er-api.com, lưu tạm 1 giờ; có tỷ giá dự phòng khi mất mạng (ExchangeRate-API, n.d.)", "Cập nhật mỗi ngày"),
        ("Ảnh, video", "Ảnh sản phẩm, lookbook, video từ breathedivinity.com; nén sang WebP và H.264", "477 ảnh sản phẩm, 4 video"),
    ], widths=[3.0, 9.2, 3.8], caption="Nguồn dữ liệu của website", size=11)
    R.table(["Công cụ", "Mục đích"], [
        ("Visual Studio Code + Live Server", "Soạn mã, chạy thử trên máy (thống nhất trong lớp)"),
        ("Git, GitHub", "Quản lý phiên bản, lưu trữ mã nguồn, mỗi tính năng một commit"),
        ("Vercel", "Hosting web tĩnh, HTTPS, CDN, tự triển khai từ GitHub (Vercel, n.d.)"),
        ("Python 3.12 + Pillow, imageio-ffmpeg", "Thu thập và chuẩn hoá dữ liệu mẫu, tính bảng size, đổi ảnh sang WebP, nén video"),
        ("Node.js + less 4.2.0", "Biên dịch css/less/components.less ra CSS"),
        ("draw.io", "Vẽ Use case, ERD, DFD, BPMN, lưu đồ, kiến trúc"),
        ("Chrome DevTools, Google Lighthouse 13.5", "Gỡ lỗi; đo hiệu năng, khả năng truy cập, SEO"),
        ("W3C Nu Html Checker (trực tuyến và vnu.jar 26.10.12)", "Kiểm tra cú pháp HTML theo đặc tả"),
        ("Playwright", "Tự động thao tác trình duyệt để kiểm thử chức năng và chụp màn hình (Microsoft, n.d.)"),
        ("WordPress Playground, WordPress 7.1, WooCommerce 11.2", "Cài đặt và quản trị thử nền tảng TMĐT mã nguồn mở"),
    ], widths=[6.0, 10.0], caption="Công cụ sử dụng", size=11)

    # ---------- 3.6 Công nghệ ----------
    R.h2("3.6. Mô hình, thuật toán và công nghệ áp dụng")
    R.p("Bảng sau đối chiếu từng nội dung của đề cương học phần với nơi áp dụng trong mã nguồn, giúp giảng viên kiểm tra "
        "phạm vi kiến thức của đồ án.")
    R.table(["Chương đề cương", "Nội dung", "Áp dụng trong SANCTUARY"], [
        ("I. Internet, website TMĐT", "Client/server, HTTP, IP, tên miền, web server", "Vercel phục vụ file qua HTTPS; tên miền sanctuarydivinity.vercel.app"),
        ("II. Thiết kế web", "Yêu cầu, front-end/back-end, admin/customer, đưa web online", "Mục 3.2; trang khách và trang quản trị; GitHub → Vercel"),
        ("III. HTML", "Semantic, ảnh, danh sách, liên kết, bảng, iframe, form", "7 trang; bảng size, bảng admin; iframe bản đồ; 6 loại form"),
        ("IV. CSS", "Selector, box model, CSS3, reset, LESS, responsive, framework", "reset.css; Grid/Flex; ~50 media query; components.less; so sánh framework (Bảng 2.2)"),
        ("V. JavaScript", "Biến, kiểu, toán tử, điều khiển, hàm, đối tượng", "27 mô-đun ES; thuật toán Luhn, gợi ý size, tính phí"),
        ("VI. XML, DOM, AJAX", "Thuộc tính/phương thức DOM, sự kiện, XML, AJAX", "Giao diện vẽ bằng DOM; shipping.xml + XMLHttpRequest; JSON + fetch"),
        ("VII. Mã nguồn mở", "Cài đặt, quản lý sản phẩm, đơn, khách, giao diện", "Bản cài thử WooCommerce (mục 4.6)"),
        ("VIII. Quản trị website", "Mối đe doạ, sao lưu, nâng cấp", "Trang admin có sao lưu/khôi phục; kế hoạch ở mục 5.5"),
    ], widths=[3.6, 5.2, 7.2], caption="Đối chiếu nội dung đề cương với mã nguồn", size=11)
    R.p("Ba đoạn mã tiêu biểu dưới đây minh hoạ phần XML/AJAX, LESS và iframe; các đoạn khác ở Phụ lục E.")
    R.code("""<shipping origin="Ho Chi Minh City, Vietnam">
  <packaging kg="0.15"/>
  <zones>
    <zone id="domestic" base="3" perKg="1.5"/>
    <zone id="northAmerica" base="24" perKg="10"/>
  </zones>
  <countries>
    <country name="Vietnam" zone="domestic">
      <tax label="VAT">8</tax>
      <duty pct="0" perItemUsd="0"/>
    </country>
  </countries>
</shipping>""", caption="Trích data/shipping.xml (rút gọn):")
    R.code("""export function loadShipping() {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "../data/shipping.xml");
    xhr.onload = () => {
      // responseXML là cây DOM của file XML do trình duyệt tự phân tích
      if (xhr.status === 200 && xhr.responseXML) resolve(parseShippingXml(xhr.responseXML));
      else reject(new Error("Cannot load shipping data (status " + xhr.status + ")"));
    };
    xhr.onerror = () => reject(new Error("Network error while loading shipping data"));
    xhr.send();
  });
}
// Duyệt DOM của XML: getElementsByTagName, getAttribute, textContent
for (const z of doc.getElementsByTagName("zone")) {
  data.zones[z.getAttribute("id")] = { base: num(z, "base"), perKg: num(z, "perKg") };
}""", caption="Đọc XML bằng AJAX trong js/shipping.js (rút gọn):")
    R.code("""@btn-border-color: #333;              // biến LESS
.smooth(@props) { transition: @props; }   // mixin có tham số
.btn {
  border: 3px solid @btn-border-color;
  .smooth(background 0.2s, color 0.2s, border-color 0.2s;);
  &:hover { background: var(--color-accent); color: #000; }  // -> .btn:hover
  &--small { padding: 0.5rem 1rem; }                          // -> .btn--small
}""", caption="Biến, mixin và lồng selector trong css/less/components.less (rút gọn):")

    # ---------- 3.7 Đánh giá ----------
    R.h2("3.7. Cách đánh giá và đo lường kết quả")
    R.p("Vì nhóm không có dữ liệu người dùng thật (khảo sát, lượt truy cập), kết quả được đánh giá bằng bốn phương pháp "
        "khách quan, lặp lại được. Nhóm không dùng số liệu khảo sát giả định.")
    R.table(["Phương pháp", "Cách thực hiện", "Tiêu chí"], [
        ("Kiểm thử chức năng tự động", "41 ca kiểm thử viết bằng Playwright, thao tác như người dùng thật trên Chrome rồi kiểm tra DOM, URL, localStorage", "Tỷ lệ ca đạt; mỗi ca có kết quả mong đợi rõ ràng"),
        ("Google Lighthouse 13.5", "Đo 5 trang của bản triển khai trên Vercel ở hai cấu hình mobile và desktop, xoá cache trước mỗi lần đo", "Điểm 4 nhóm; LCP ≤ 2,5 s, CLS ≤ 0,1 (Google, n.d.)"),
        ("W3C Nu Html Checker", "Kiểm tra mã nguồn 7 trang HTML bằng dịch vụ trực tuyến và bản vnu.jar chạy trên máy", "Số lỗi (error) và cảnh báo (warning)"),
        ("Độ chính xác gợi ý size", "So size gợi ý với size suy ra từ vòng ngực đo thật của từng người trong ANSUR II", "% đúng size; % sai không quá 1 size"),
        ("Hiệu quả tối ưu tài nguyên", "So dung lượng ảnh, video trước và sau khi nén", "% dung lượng giảm"),
    ], widths=[3.6, 7.6, 4.8], caption="Phương pháp đánh giá và tiêu chí", size=11)
