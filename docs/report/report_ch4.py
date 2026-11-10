# -*- coding: utf-8 -*-
"""Chương 4. Kết quả và phân tích."""
from collections import OrderedDict

# Kết quả W3C Nu Html Checker ngày 11/11/2026: (trang, lỗi trước, cảnh báo trước, nội dung lỗi, cách sửa, lỗi sau, cảnh báo sau)
# "Sau" đo bằng Nu Html Checker 26.10.12 chạy trên máy (vnu.jar); cùng bộ kiểm tra ra đúng 5 lỗi, 3 cảnh báo với bản cũ.
W3C = [
    ("index.html", 1, 0, "aria-label trên thẻ div không có vai trò", "Bỏ aria-label, thêm dòng chữ ẩn cho trình đọc màn hình", 0, 0),
    ("pages/home.html", 0, 0, "-", "-", 0, 0),
    ("pages/cart.html", 2, 2, "autocomplete=\"street-address\" cho input một dòng; aria-label trên thẻ p; 2 section thiếu tiêu đề",
     "Đổi thành address-line1; thẻ p thành div role=\"group\"; section thông báo thành div", 0, 0),
    ("pages/contact.html", 0, 0, "-", "-", 0, 0),
    ("pages/about.html", 0, 0, "-", "-", 0, 0),
    ("pages/account.html", 1, 1, "autocomplete=\"street-address\"; 1 section thiếu tiêu đề", "Như trên", 0, 0),
    ("pages/admin.html", 1, 0, "Thẻ img xem trước ảnh chưa có src", "Thêm src giữ chỗ (ảnh GIF trong suốt 1×1)", 0, 0),
]


def vn(x):
    return str(x).replace(".", ",")


def build(R, ctx):
    W, WOO, C = ctx["img"] / "web", ctx["img"] / "woo", ctx["comp"]
    sc = ctx["size_chart"]
    R.h1("CHƯƠNG 4. KẾT QUẢ VÀ PHÂN TÍCH", chapter=4)

    # ---------- 4.1 ----------
    R.h2("4.1. Mô tả các kết quả đạt được")
    R.p("Sau 11 tuần, nhóm hoàn thành website SANCTUARY chạy trực tuyến tại https://sanctuarydivinity.vercel.app, một bản "
        "cài thử WooCommerce, bộ sơ đồ phân tích thiết kế và bộ kiểm thử tự động. Bảng dưới tóm tắt các hạng mục; ảnh "
        "minh hoạ ở các mục 4.2 - 4.6, số liệu đo ở mục 4.7.")
    R.table(["Hạng mục", "Kết quả", "Trạng thái"], [
        ("Trang cổng", "Đếm ngược tới ngày ra mắt 01/12/2026, lookbook, nhập mã athlete/admin", "Hoàn thành"),
        ("Cửa hàng", str(ctx["n_products"]) + " sản phẩm, 3 khu, lọc size/màu, sắp xếp giá, đổi 15 loại tiền tệ", "Hoàn thành"),
        ("Chi tiết sản phẩm", "Ảnh theo màu, size XXS - XXL, tồn kho, bảng size cm/in, gợi ý size", "Hoàn thành"),
        ("Đánh giá", str(ctx["n_reviews"]) + " đánh giá có ảnh, lọc theo sao, dòng, loại sản phẩm", "Hoàn thành"),
        ("Giỏ hàng, thanh toán", "Sửa số lượng theo tồn kho, mã giảm giá, phí ship/thuế từ XML, kiểm tra form", "Hoàn thành"),
        ("Tài khoản", "Đăng ký, đăng nhập, hồ sơ, đổi mật khẩu, lịch sử đơn", "Hoàn thành"),
        ("Trang Info, About", "Liên hệ (form + bản đồ iframe), 5 trang chính sách, câu chuyện thương hiệu", "Hoàn thành"),
        ("Trang quản trị", "8 chức năng: tổng quan, đơn, sản phẩm, khách, tin nhắn, mã athlete, ngày ra mắt, sao lưu", "Hoàn thành"),
        ("Mã nguồn mở", "WooCommerce 11.2: 12 sản phẩm, 3 khách, 6 đơn, ship/thuế, giao diện Storefront tối", "Hoàn thành"),
        ("Triển khai", "GitHub + Vercel, HTTPS, tự triển khai khi có commit", "Hoàn thành"),
    ], widths=[3.6, 10.0, 2.4], caption="Tổng hợp kết quả đạt được", size=11, center_cols=(2,))

    # ---------- 4.2 ----------
    R.h2("4.2. Giao diện phía khách hàng")
    R.h3("4.2.1. Trang cổng")
    R.p("Trang cổng (" + R.next_fig() + ") là trang đầu tiên khách nhìn thấy: tên bộ sưu tập, đồng hồ đếm ngược và ảnh "
        "lookbook chạy ngang. Nút “Enter using password” ở góc phải mở hộp nhập mã; nhập sai thì báo lỗi ngay dưới ô.")
    R.figure(W / "01-gate.png", "Trang cổng với đồng hồ đếm ngược tới đợt ra mắt", width=14)
    R.figure(W / "03-gate-wrong.png", "Hộp nhập mã: báo lỗi khi nhập sai mã", width=14)
    R.h3("4.2.2. Trang chủ và cửa hàng")
    R.p("Trang chủ mở đầu bằng video toàn màn hình (" + R.next_fig() + "); cuộn xuống là cửa hàng chia 3 khu Sanctuary "
        "(nam), Sanctuary Selene (nữ) và Accessories, mỗi khu chia nhóm như compression, oversized tee, hoodie. Lưới sản "
        "phẩm 4 cột trên máy tính; mỗi thẻ có ảnh, tên, giá theo tiền tệ đang chọn và các ô màu. Menu **Armory** ở mép "
        "trái trượt ra để lọc theo size, màu và sắp xếp theo giá.")
    R.figure(W / "04-home-hero.png", "Phần đầu trang chủ với video giới thiệu bộ sưu tập", width=14)
    R.figure(W / "06-shop-grid.png", "Lưới sản phẩm của cửa hàng", width=14)
    R.figure(W / "07-armory-menu.png", "Menu Armory: chọn khu, lọc size, màu và sắp xếp giá", width=14)
    R.h3("4.2.3. Chi tiết sản phẩm, bảng size và gợi ý size")
    R.p("Bấm vào thẻ sản phẩm mở popup chi tiết (" + R.next_fig() + "): ảnh trượt theo màu đang chọn, nút size, số lượng "
        "giới hạn theo tồn kho, nút Add to cart và Buy now. Mục **Size chart** hiện bảng số đo theo cm/kg hoặc in/lb, dòng "
        "của size đang chọn được tô sáng; mục **Find your size** nhận chiều cao, cân nặng và trả về size gợi ý kèm lưu ý "
        "theo kiểu dáng (ví dụ cao 178 cm, nặng 75 kg được gợi ý size M).")
    R.figure(W / "09-product-popup.png", "Popup chi tiết sản phẩm", width=14)
    R.figure(W / "11-size-chart.png", "Bảng size đo theo cm/kg, tô sáng size đang chọn", width=12.5)
    R.figure(W / "12-size-finder.png", "Kết quả gợi ý size từ chiều cao và cân nặng", width=12.5)
    R.h3("4.2.4. Đánh giá của khách hàng")
    R.p("Nút **Reviews** mở popup đánh giá (" + R.next_fig() + ") gồm điểm trung bình, bộ lọc theo số sao, dòng nam/nữ, "
        "loại sản phẩm, kèm số lượng của từng lựa chọn; mỗi đánh giá có ảnh thật của khách, bấm vào để xem lớn và trượt ảnh.")
    R.figure(W / "14-reviews.png", "Popup đánh giá với bộ lọc và ảnh của khách", width=14)
    R.h3("4.2.5. Giỏ hàng và thanh toán")
    R.p("Trang giỏ hàng (" + R.next_fig() + ") có danh sách món (đổi số lượng, xoá, hiện tồn kho), khối tóm tắt đơn và "
        "form thanh toán. Phí ship, thuế nhập khẩu và VAT/GST thay đổi ngay khi khách đổi nước nhận hàng; ví dụ trong ảnh "
        "là đơn 1,20 kg gửi đi Mỹ, phí ship 39 USD và thuế nhập khẩu ước tính 15%, đúng như phép tính ở mục 3.4.3. Khi bấm "
        "Place order mà dữ liệu sai, lỗi hiện ngay dưới từng ô; đặt thành công thì hiện mã đơn.")
    R.figure(W / "19-checkout-errors.png", "Giỏ hàng, tóm tắt đơn và lỗi kiểm tra form thanh toán", width=14)
    R.figure(W / "21-order-done.png", "Thông báo đặt hàng thành công kèm mã đơn", width=12)
    R.h3("4.2.6. Trang Info và About")
    R.p("Trang Info (" + R.next_fig() + ") gom liên hệ và 5 trang chính sách vào các tab; tab Contact có thông tin liên "
        "hệ, câu hỏi nhanh dẫn tới chính sách liên quan, bản đồ Google Maps nhúng bằng iframe (địa chỉ Trường Đại học Kinh "
        "tế - Luật) và form liên hệ có kiểm tra. Trang About kể câu chuyện thương hiệu.")
    R.figure(W / "22-contact.png", "Trang Info: thông tin liên hệ, bản đồ iframe và form liên hệ", width=14)
    R.figure(W / "27-about.png", "Trang About: câu chuyện thương hiệu SANCTUARY", width=14)
    R.h3("4.2.7. Tài khoản khách hàng")
    R.p("Biểu tượng người ở góc phải mở popup **Sign in / Create account** (" + R.next_fig() + "). Đăng nhập xong, trang "
        "Account cho sửa thông tin, đổi mật khẩu và xem lịch sử đơn cùng trạng thái do quản trị viên cập nhật.")
    R.figure(W / "28-signin-popup.png", "Popup đăng nhập và tạo tài khoản", width=13)
    R.figure(W / "29-account.png", "Trang Account: hồ sơ và lịch sử đơn hàng", width=14)

    # ---------- 4.3 ----------
    R.h2("4.3. Trang quản trị")
    R.p("Trang quản trị chỉ mở được với vai trò admin. Trang **Overview** (" + R.next_fig() + ") hiện doanh thu (không "
        "tính đơn huỷ), số đơn, giá trị đơn trung bình, số khách, tin nhắn chưa đọc, sản phẩm sắp hết hàng và bán chạy. "
        "Trang **Orders** tìm, lọc, đổi trạng thái đơn; huỷ đơn thì hoàn kho. Trang **Products** thêm sản phẩm mới có ảnh "
        "(ảnh được thu nhỏ bằng canvas trước khi lưu), sửa giá, tồn kho, nổi bật, ẩn/hiện, xoá mềm và khôi phục. Trang "
        "**Athlete codes** thêm, bật/tắt, xoá mã; trang **Backup** tải về file sao lưu JSON, khôi phục từ file, xoá dữ liệu "
        "và tạo dữ liệu mẫu để thuyết trình.")
    R.figure(W / "30-admin-overview.png", "Trang quản trị: tổng quan doanh thu và chỉ số", width=14)
    R.figure(W / "31-admin-orders.png", "Quản lý đơn hàng và đổi trạng thái", width=14)
    R.figure(W / "33-admin-product-form.png", "Form thêm sản phẩm mới", width=14)
    R.figure(W / "36-admin-codes.png", "Quản lý mã athlete", width=14)
    R.figure(W / "38-admin-backup.png", "Sao lưu, khôi phục và dữ liệu mẫu", width=14)

    # ---------- 4.4 ----------
    R.h2("4.4. Giao diện đáp ứng trên nhiều thiết bị")
    R.p("Trên điện thoại 390 px (" + R.next_fig() + "), menu chuyển xuống dưới logo, lưới sản phẩm còn 2 cột, popup sản "
        "phẩm xếp ảnh trên thông tin dưới, giỏ hàng và form xếp thành một cột. Trên máy tính bảng 820 px, lưới có 3 cột. "
        "Ở cả ba độ rộng, trang không bị cuộn ngang (ca kiểm thử TC39 - TC41).")
    R.figure(C / "mobile-1.png", "Giao diện điện thoại: trang cổng, trang chủ, cửa hàng", width=15)
    R.figure(C / "mobile-2.png", "Giao diện điện thoại: chi tiết sản phẩm, giỏ hàng, trang Info", width=15)

    # ---------- 4.5 ----------
    R.h2("4.5. Đưa website chạy trực tuyến")
    R.p("Website triển khai theo đúng các bước của Chương II đề cương: mã nguồn đặt trong kho GitHub công khai; dự án "
        "Vercel liên kết với kho này, mỗi lần đẩy commit lên nhánh `main` thì Vercel tự tải mã, triển khai lên CDN và cấp "
        "chứng chỉ HTTPS. Tệp `vercel.json` cấu hình chuyển hướng: truy cập `/` hoặc `/index.html` được chuyển tới "
        "`/password` (trang cổng). Vì là web tĩnh nên không cần máy chủ ứng dụng hay CSDL, chi phí hosting bằng 0 với gói "
        "miễn phí. Khi kinh doanh thật, nhóm chỉ cần mua tên miền riêng rồi khai báo bản ghi DNS trỏ về Vercel.")

    # ---------- 4.6 WooCommerce ----------
    R.h2("4.6. Cài đặt và quản trị thử WooCommerce")
    R.h3("4.6.1. Cài đặt")
    R.p("Thay vì cài XAMPP, nhóm dùng **WordPress Playground**, bản WordPress chạy bằng WebAssembly trên Node.js, không "
        "cần cài PHP, MySQL hay quyền quản trị máy (WordPress.org, n.d.). Một tệp *blueprint* mô tả các bước cài đặt nên "
        "ai trong nhóm cũng chạy lại được bằng một lệnh. Phiên bản: WordPress 7.1.4, PHP 8.3, WooCommerce 11.2.2, theme "
        "Storefront. Dữ liệu SANCTUARY (12 sản phẩm có biến thể size, 3 khách, 6 đơn) được nhập bằng script PHP dùng API "
        "của WooCommerce; sau đó nhóm thao tác trực tiếp trên trang quản trị.")
    R.code("""npx @wp-playground/cli@3.1.59 server --port=9400 --login \\
    --blueprint=tools/woocommerce/blueprint.json \\
    --mount-dir "<thư mục dự án>\\tools\\woocommerce" /wordpress/sanctuary-seed
# Sau khi server chạy: mở http://127.0.0.1:9400/sanctuary-seed/run.php để nhập dữ liệu mẫu""",
           caption="Lệnh khởi động bản cài thử (các bước cài đặt nằm trong blueprint.json):")
    R.figure(WOO / "01-plugins.png", "WooCommerce đã được cài và kích hoạt trong trang Plugins", width=14)
    R.h3("4.6.2. Quản lý sản phẩm")
    R.p("Mỗi sản phẩm là một *variable product*: thuộc tính toàn cục **Size** (XXS - XXL, One Size) sinh ra các biến thể, "
        "tồn kho quản lý ở cấp sản phẩm, danh mục hai cấp theo dòng (nam/nữ/phụ kiện) và loại hàng (" + R.next_fig() + ").")
    R.figure(WOO / "03-products.png", "Danh sách sản phẩm SANCTUARY trong WooCommerce", width=14)
    R.figure(WOO / "05-product-variations.png", "Biến thể theo size của một sản phẩm", width=14)
    R.h3("4.6.3. Quản lý đơn hàng và khách hàng")
    R.p("Sáu đơn mẫu có các trạng thái Completed, Processing, On hold và Cancelled. Nhóm mở đơn #115 trên trang quản trị, "
        "đổi trạng thái từ Processing sang Completed và bấm Update (" + R.next_fig() + "); WooCommerce tự ghi ghi chú lịch sử "
        "vào đơn. Trang Customers tự tổng hợp số đơn, tổng chi tiêu và giá trị đơn trung bình của từng khách.")
    R.figure(WOO / "11-order-status-updated.png", "Đổi trạng thái đơn hàng trên trang quản trị WooCommerce", width=14)
    R.figure(WOO / "13-customers.png", "Trang khách hàng: số đơn, tổng chi tiêu, giá trị đơn trung bình", width=14)
    R.h3("4.6.4. Vận chuyển, thuế và tùy biến giao diện")
    R.p("Nhóm tạo hai vùng giao hàng (Vietnam: phí cố định 3 USD; International: 24 USD cho 6 nước) và thuế VAT 8% cho "
        "Việt Nam, tương ứng dữ liệu trong shipping.xml (" + R.next_fig() + "). Giao diện Storefront được tùy biến trong "
        "Customizer sang nền đen, chữ trắng, nút đỏ và logo SANCTUARY, gần với phong cách của website tự lập trình.")
    R.figure(WOO / "14-shipping-zones.png", "Cấu hình vùng giao hàng", width=14)
    R.figure(WOO / "17-customizer.png", "Tùy biến màu sắc và logo của theme Storefront trong Customizer", width=14)
    R.figure(WOO / "21-single-product.png", "Trang chi tiết sản phẩm trên cửa hàng WooCommerce sau khi tùy biến", width=14)
    R.h3("4.6.5. So sánh WooCommerce với website tự lập trình")
    R.table(["Tiêu chí", "SANCTUARY tự lập trình", "WooCommerce"], [
        ("Hạ tầng", "Web tĩnh, không máy chủ ứng dụng, hosting miễn phí", "Cần PHP + MySQL, hosting WordPress"),
        ("Dữ liệu", "JSON/XML + localStorage từng trình duyệt", "CSDL dùng chung cho mọi khách"),
        ("Đơn hàng, thanh toán", "Mô phỏng, không có cổng thanh toán", "Đầy đủ, có plugin cổng thanh toán thật"),
        ("Bảo mật", "Mô phỏng phía máy khách", "Xác thực phía máy chủ, phân quyền, cập nhật bảo mật"),
        ("Giao diện, trải nghiệm", "Tự do hoàn toàn: drop, gợi ý size, đổi tiền tệ", "Theo theme; tính năng riêng phải tìm plugin hoặc tự viết"),
        ("Thời gian làm", "Lâu (viết từng chức năng)", "Nhanh (cài và cấu hình)"),
        ("Giá trị học tập", "Hiểu sâu HTML, CSS, JS, DOM, AJAX", "Hiểu quy trình vận hành một cửa hàng thật"),
    ], widths=[3.4, 6.3, 6.3], caption="So sánh website tự lập trình với WooCommerce", size=11)

    # ---------- 4.7 Số liệu đo ----------
    R.h2("4.7. Bảng biểu và số liệu đánh giá")
    R.h3("4.7.1. Kiểm thử chức năng")
    tests = ctx["tests"]
    groups = OrderedDict()
    for t in tests:
        g = groups.setdefault(t["group"], [0, 0, []])
        g[0] += 1
        g[1] += 1 if t["ok"] else 0
        g[2].append(t["id"])
    R.p("Bộ kiểm thử gồm " + str(len(tests)) + " ca, chạy tự động bằng Playwright trên Google Chrome; mỗi ca thao tác như "
        "người dùng (bấm, nhập, chọn) rồi kiểm tra kết quả thật trong DOM, địa chỉ trang và localStorage. Bảng dưới tổng hợp "
        "theo nhóm chức năng; chi tiết từng ca ở Phụ lục B.")
    R.table(["Nhóm chức năng", "Mã ca", "Số ca", "Đạt", "Tỷ lệ"],
            [(g, v[2][0] + " - " + v[2][-1], str(v[0]), str(v[1]), "%d%%" % round(100 * v[1] / v[0])) for g, v in groups.items()] +
            [("**Tổng**", "", "**" + str(len(tests)) + "**", "**" + str(sum(t["ok"] for t in tests)) + "**",
              "**%d%%**" % round(100 * sum(t["ok"] for t in tests) / len(tests)))],
            widths=[5.0, 3.6, 2.2, 2.2, 3.0], caption="Kết quả kiểm thử chức năng theo nhóm", center_cols=(1, 2, 3, 4))
    R.p("Trong lần chạy đầu, 3 ca không đạt; khi kiểm tra lại, cả 3 đều do kịch bản kiểm thử viết sai chứ không phải lỗi "
        "của website: (1) ca lọc màu đếm cả một sản phẩm có màu Void Black nhưng đã ngừng bán, trong khi website ẩn màu ngừng "
        "bán là đúng thiết kế; (2) ca lịch sử đơn chèn đơn thử thiếu trường `userEmail` nên trang Account bỏ qua, đúng với "
        "cơ chế kiểm tra cấu trúc dữ liệu khi đọc; (3) ca đổi trạng thái gọi sai hàm của Playwright. Sau khi sửa kịch bản, "
        "toàn bộ " + str(len(tests)) + " ca đạt. Nhóm ghi lại điều này vì nó cho thấy cơ chế kiểm tra dữ liệu của website hoạt "
        "động đúng như thiết kế.")
    online = ctx["tests_online"]
    R.p("Bộ kiểm thử cũng được chạy trên bản triển khai thật tại sanctuarydivinity.vercel.app và đạt " +
        str(sum(t["ok"] for t in online)) + "/" + str(len(online)) + " ca. Khác biệt duy nhất giữa hai môi trường là trang cổng "
        "trên Vercel có địa chỉ `/password` (cấu hình trong vercel.json) thay vì `/index.html`, nên ca TC01 được viết để chấp "
        "nhận cả hai địa chỉ.")

    R.h3("4.7.2. Hiệu năng và chất lượng theo Lighthouse")
    lh = ctx["lighthouse"]
    names = {"Gate": "Cổng", "Home": "Trang chủ", "Cart": "Giỏ hàng", "Info": "Info", "About": "About"}
    rows = []
    for r in lh:
        def mark(v, good):
            return (str(v), "E2EFDA") if v >= good else ((str(v), "FFF2CC") if v >= 50 else (str(v), "F8CBAD"))
        rows.append((("Mobile" if r["mode"] == "mobile" else "Desktop"), names[r["name"]], mark(r["performance"], 90),
                     mark(r["accessibility"], 90), mark(r["bestPractices"], 90), mark(r["seo"], 90),
                     vn(r["LCP"]), vn(r["CLS"]), vn(r["TBT"]), r["weight"].replace("Total size was ", "").replace(",", ".")))
    R.p("Nhóm đo 5 trang của bản triển khai trên Vercel bằng Lighthouse 13.5 ở cả cấu hình mobile (giả lập điện thoại "
        "tầm trung, mạng 4G chậm) và desktop, xoá bộ nhớ đệm trước mỗi lần đo; thời điểm đo là ngày 11/11/2026. Ô xanh là "
        "điểm ≥ 90, vàng là 50 - 89, đỏ là dưới 50.")
    R.table(["Cấu hình", "Trang", "Perf.", "Access.", "Best Pr.", "SEO", "LCP", "CLS", "TBT", "Dung lượng"], rows,
            widths=[1.8, 2.0, 1.2, 1.4, 1.4, 1.1, 1.4, 1.3, 1.4, 2.0], caption="Kết quả đo Google Lighthouse (điểm 0 - 100)",
            size=10, center_cols=(2, 3, 4, 5, 6, 7, 8, 9))
    desk = [r for r in lh if r["mode"] == "desktop"]
    pick =lambda data, mode, name: [r for r in data if r["mode"] == mode and r["name"] == name][0]
    before = ctx["lighthouse_before"]
    home_m, about_m, info_m = pick(lh, "mobile", "Home"), pick(lh, "mobile", "About"), pick(lh, "mobile", "Info")
    R.p("Kết quả nổi bật: **Accessibility đạt 100 và SEO đạt 100 ở cả 10 lần đo**, không còn mục kiểm tra nào của hai nhóm "
        "này bị trượt; Best Practices 96 - 100. Trên desktop, cả 5 trang đạt hiệu năng " + str(min(r["performance"] for r in desk)) +
        " - 100 với LCP ≤ " + vn(max(float(r["LCP"].split()[0]) for r in desk)) + " s và CLS gần như bằng 0. Trên mobile, giỏ "
        "hàng và Info đạt từ " + str(min(pick(lh, "mobile", "Cart")["performance"], info_m["performance"])) + " trở lên; điểm yếu còn lại là **trang chủ (LCP " +
        vn(home_m["LCP"]) + ")** vì phải tải video hero, tổng dung lượng khoảng " + home_m["weight"].replace("Total size was ", "").replace(",", ".") +
        ", và **trang About (LCP " + vn(about_m["LCP"]) + ")** vì ảnh lớn đầu trang. Trang Info nặng thêm khoảng 600 KB so với lần "
        "đo đầu (" + pick(before, "mobile", "Info")["weight"].replace("Total size was ", "").replace(",", ".") + " → " +
        info_m["weight"].replace("Total size was ", "").replace(",", ".") + ") do bản đồ Google Maps nhúng bằng iframe; đây là "
        "đánh đổi chấp nhận được vì iframe chỉ tải khi cuộn tới (`loading=\"lazy\"`).")
    R.p("**So sánh trước và sau khi tối ưu.** Lần đo đầu (cùng ngày, trên bản triển khai trước đó) phát hiện ba vấn đề: trang "
        "cổng có CLS rất cao, cả 5 trang thiếu thẻ `meta description`, và thẻ sản phẩm có `aria-label` không khớp chữ hiển thị. "
        "Khi điều tra CLS, nhóm thấy nguyên nhân **không chỉ** là ảnh thiếu kích thước như dự đoán ban đầu: khối lookbook nằm "
        "trong flex container căn giữa (`align-items: center`) nên co theo nội dung; khi ảnh chưa tải, ảnh chỉ rộng khoảng 100 "
        "px rồi nở ra 900 px. Nhóm sửa bằng `width: 100%` cho khối lookbook kết hợp khai báo `width`/`height` thật của ảnh, thêm "
        "`meta description` cho 7 trang, và để thẻ sản phẩm lấy tên từ nội dung hiển thị.")
    cmp_rows = []
    for mode in ("desktop", "mobile"):
        b, a = pick(before, mode, "Gate"), pick(lh, mode, "Gate")
        cmp_rows.append(("Cổng (" + mode + ")", "%d → **%d**" % (b["performance"], a["performance"]),
                         "%s → **%s**" % (vn(b["CLS"]), vn(a["CLS"])), "%s → **%s**" % (vn(b["LCP"]), vn(a["LCP"])),
                         "%d → **%d**" % (b["seo"], a["seo"])))
    for name in ("Home", "Cart", "Info", "About"):
        b, a = pick(before, "desktop", name), pick(lh, "desktop", name)
        cmp_rows.append((names[name] + " (desktop)", "%d → **%d**" % (b["performance"], a["performance"]),
                         "%s → **%s**" % (vn(b["CLS"]), vn(a["CLS"])), "%s → **%s**" % (vn(b["LCP"]), vn(a["LCP"])),
                         "%d → **%d**" % (b["seo"], a["seo"])))
    R.table(["Trang", "Performance", "CLS", "LCP", "SEO"], cmp_rows, widths=[4.0, 3.0, 3.0, 3.2, 2.8],
            caption="Lighthouse trước và sau khi tối ưu (đo trên Vercel ngày 11/11/2026)", size=11, center_cols=(1, 2, 3, 4))
    R.p("Kết quả Lighthouse có dao động nhỏ giữa các lần đo do mạng và tải của máy chủ, nên nhóm chỉ kết luận ở các thay đổi "
        "lớn: CLS trang cổng về 0 và điểm hiệu năng tăng " + str(pick(lh, "desktop", "Gate")["performance"] - pick(before, "desktop", "Gate")["performance"]) +
        " điểm trên desktop.", italic=True)

    R.h3("4.7.3. Kiểm tra mã HTML theo W3C")
    R.p("Lần kiểm tra đầu bằng dịch vụ W3C Nu Html Checker trực tuyến phát hiện 5 lỗi và 3 cảnh báo ở 4/7 trang. Sau khi "
        "sửa, nhóm kiểm tra lại bằng chính Nu Html Checker bản chạy trên máy (vnu.jar 26.10.12, vì dịch vụ trực tuyến chặn yêu "
        "cầu tự động); để chắc hai bản cho kết quả như nhau, nhóm chạy bản trên máy với mã nguồn cũ và nhận đúng 5 lỗi, 3 cảnh báo.")
    R.table(["Trang", "Trước (lỗi / cảnh báo)", "Nội dung", "Cách sửa", "Sau"],
            [(a, "%d / %d" % (b, c), d, e, "%d / %d" % (f, g)) for a, b, c, d, e, f, g in W3C] +
            [("**Tổng**", "**%d / %d**" % (sum(x[1] for x in W3C), sum(x[2] for x in W3C)), "", "",
              "**%d / %d**" % (sum(x[5] for x in W3C), sum(x[6] for x in W3C)))],
            widths=[3.4, 2.1, 4.4, 4.7, 1.4], caption="Kết quả kiểm tra W3C Nu Html Checker trước và sau khi sửa (7 trang)",
            size=10.5, center_cols=(1, 4))
    R.p("Sau khi sửa, **cả 7 trang không còn lỗi và cảnh báo nào**. Các lỗi đều thuộc loại thuộc tính dùng sai ngữ cảnh, "
        "không ảnh hưởng hiển thị; khi sửa, nhóm tránh cách “chữa cháy” làm phát sinh lỗi khác. Ví dụ, với đồng hồ đếm ngược, "
        "cách nhanh nhất để hết lỗi W3C là thêm `role=\"timer\"`, nhưng khi đó nhãn “Time until the drop” lại không chứa chữ "
        "đang hiển thị (“19 Days 18 Hours...”), trái tiêu chí WCAG 2.5.3 *Label in Name*; vì vậy nhóm bỏ `aria-label` và thêm "
        "một dòng chữ ẩn dành cho trình đọc màn hình. Sau các thay đổi, bộ " + str(len(tests)) + " ca kiểm "
        "thử được chạy lại và vẫn đạt 100%, cả ở máy lẫn trên bản triển khai Vercel.")

    R.h3("4.7.4. Độ chính xác của mô hình gợi ý size")
    hm, hf = sc["him"], sc["her"]
    R.table(["Chỉ số", "Nam", "Nữ"], [
        ("Số người trong dữ liệu ANSUR II", "{:,}".format(hm["sampleSize"]).replace(",", "."), "{:,}".format(hf["sampleSize"]).replace(",", ".")),
        ("Sai số RMSE khi ước lượng vòng ngực", vn(hm["rmseCm"]) + " cm", vn(hf["rmseCm"]) + " cm"),
        ("Gợi ý đúng size", vn(hm["exactSizePct"]) + "%", vn(hf["exactSizePct"]) + "%"),
        ("Sai không quá 1 size", vn(hm["withinOneSizePct"]) + "%", vn(hf["withinOneSizePct"]) + "%"),
        ("Khoảng tin cậy của dữ liệu (P1 - P99)", "%d - %d cm; %d - %d kg" % tuple(hm["heightRangeCm"] + hm["weightRangeKg"]),
         "%d - %d cm; %d - %d kg" % tuple(hf["heightRangeCm"] + hf["weightRangeKg"])),
    ], widths=[7.0, 4.5, 4.5], caption="Độ chính xác của mô hình gợi ý size trên dữ liệu ANSUR II", center_cols=(1, 2))
    R.p("Chỉ dùng hai số đo khách dễ biết là chiều cao và cân nặng, mô hình đoán đúng size cho " + vn(hm["exactSizePct"]) +
        "% nam và " + vn(hf["exactSizePct"]) + "% nữ, và gần như luôn nằm trong phạm vi một size. Độ chính xác của nữ thấp hơn "
        "vì vòng ngực nữ phụ thuộc nhiều vào yếu tố ngoài chiều cao, cân nặng. Khi số đo nằm ngoài khoảng P1 - P99, website "
        "hiện thêm lưu ý kết quả chỉ là ước lượng.")

    R.h3("4.7.5. Hiệu quả tối ưu ảnh và video")
    R.table(["Tài nguyên", "Trước khi nén", "Sau khi nén", "Giảm"], [
        ("477 ảnh sản phẩm (JPG → WebP)", "94,2 MB", "30,9 MB", "67%"),
        ("192 ảnh đánh giá (JPG → WebP)", "4,2 MB", "3,0 MB", "29%"),
        ("10 ảnh lookbook trang cổng (JPG/PNG → WebP)", "14 MB", "3,4 MB", "76%"),
        ("4 đoạn video (H.264, CRF 20)", "79 MB", "19,7 MB", "75%"),
        ("**Tổng**", "**191,4 MB**", "**57,0 MB**", "**70%**"),
    ], widths=[7.4, 3.0, 3.0, 2.6], caption="Dung lượng ảnh, video trước và sau khi tối ưu", center_cols=(1, 2, 3))
    R.p("Nhờ tối ưu, các trang không có video (giỏ hàng, Info) chỉ tải khoảng 450 - 490 KB. Ảnh lookbook và video được so "
        "sánh với bản gốc bằng chỉ số PSNR (45 - 48 dB) và SSIM (≥ 0,995), mắt thường gần như không thấy khác biệt.")

    # ---------- 4.8 ----------
    R.h2("4.8. Phân tích và đánh giá kết quả")
    R.p("Về **chức năng**, website thực hiện đủ luồng của một cửa hàng TMĐT từ lúc vào cổng tới khi quản trị viên xử lý "
        "đơn, và 100% ca kiểm thử đạt. Các luật kiểm tra dữ liệu (form, tồn kho, cấu trúc localStorage) không chỉ chặn "
        "lỗi nhập liệu mà còn ngăn dữ liệu không hợp lệ làm hỏng trang, như đã thấy trong lần kiểm thử đầu.")
    R.p("Về **chất lượng kỹ thuật**, điểm Accessibility tuyệt đối cho thấy việc dùng HTML semantic, nhãn cho ô nhập và "
        "điều khiển bằng bàn phím có hiệu quả; điều này đáng chú ý vì lỗi tương phản là lỗi phổ biến nhất của các website "
        "TMĐT (Acosta-Vargas và cộng sự, 2022) mà giao diện nền tối rất dễ mắc. Mã HTML hợp lệ hoàn toàn theo W3C, SEO đạt "
        "100. Vòng đo - sửa - đo lại cho thấy giá trị của việc đo bằng công cụ: lỗi xô lệch bố cục ở trang cổng không thấy rõ "
        "bằng mắt nhưng làm mất 40 điểm hiệu năng, và chỉ cần một dòng CSS để sửa khi đã tìm đúng nguyên nhân. Hiệu năng trên "
        "desktop rất tốt; điểm yếu còn lại là trang chủ và About khi xem trên điện thoại, do video và ảnh lớn.")
    R.p("Về **giá trị cho người mua**, công cụ gợi ý size cho kết quả đúng hoặc lệch tối đa một size với gần như mọi "
        "người trong dữ liệu, giải quyết trực tiếp vấn đề chọn sai size, nguyên nhân trả hàng phổ biến của thời trang trực "
        "tuyến (Stöcker và cộng sự, 2021). Về **mã nguồn mở**, bản cài thử cho thấy WooCommerce giải quyết nhanh những phần "
        "website tự lập trình còn thiếu (CSDL dùng chung, thanh toán thật), trong khi website tự lập trình chủ động hơn về "
        "trải nghiệm thương hiệu.")
