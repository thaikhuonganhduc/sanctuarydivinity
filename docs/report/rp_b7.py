# -*- coding: utf-8 -*-
"""PHẦN B - CHƯƠNG 7. THIẾT KẾ GIAO DIỆN VÀ LUỒNG GIAO DIỆN"""


def impl(R, caption, rows):
    """Bảng triển khai: thành phần giao diện → kỹ thuật/sự kiện → file mã nguồn."""
    R.table(["Thành phần", "Kỹ thuật / xử lý", "File"], rows, widths=[4.0, 9.0, 4.0], caption=caption, size=11)


def build(R, ctx):
    W, D = ctx["web"], ctx["diag"]
    R.chapter(7, "THIẾT KẾ GIAO DIỆN VÀ LUỒNG GIAO DIỆN")

    R.h3("7.1. Nguyên tắc thiết kế giao diện")
    R.bullets([
        "**Tối giản, tối màu, đặt sản phẩm làm trung tâm:** nền đen tuyền, chữ trắng ngà, chỉ một màu nhấn đỏ; ảnh sản phẩm lớn, ít chữ.",
        "**Nhất quán nhận diện:** logo gothic ở giữa đầu trang, tiêu đề phông Angel Wish, chữ in hoa giãn rộng; màu khai báo bằng biến CSS dùng chung.",
        "**Ưu tiên điện thoại (mobile-first):** viết CSS cho màn hình hẹp trước, mở rộng bằng media query; vùng bấm đủ lớn cho ngón tay.",
        "**Ít chuyển trang:** chi tiết sản phẩm, đánh giá, đăng nhập mở dạng cửa sổ nổi (dialog) để khách không mất vị trí khi duyệt.",
        "**Phản hồi tức thì:** lỗi nhập liệu hiện ngay dưới ô, nút đổi trạng thái (“Added ✓”), số lượng giỏ cập nhật trên biểu tượng.",
        "**Khả năng truy cập:** HTML có ngữ nghĩa, nhãn cho ô nhập, điều khiển bằng bàn phím, Esc đóng popup, tôn trọng tuỳ chọn giảm chuyển động.",
    ])
    R.h3("7.2. Cấu trúc điều hướng hệ thống")
    R.p(R.next_fig() + " là sơ đồ trang của website. Từ trang cổng, mã athlete dẫn vào trang chủ, mã quản trị dẫn vào trang quản "
        "trị. Trang chủ gom cả cửa hàng và các popup (sản phẩm, đánh giá) để khách duyệt liền mạch; trang Info dùng tab chuyển "
        "bằng địa chỉ `#mục` nên chia sẻ được đường dẫn tới từng chính sách; popup đăng nhập có trên mọi trang phía khách.")
    R.figure(D / "06-architecture-p2.png", "Sitemap của website SANCTUARY (phía khách hàng và phía quản trị)", width=16.5)

    R.h3("7.3. Cấu trúc cơ bản của website")
    R.h4("7.3.1. Header")
    R.p("Header gồm nút Exit (thoát về trang cổng) ở góc trái, liên kết Info và About hai bên logo, biểu tượng tài khoản và giỏ "
        "hàng (có huy hiệu số món) ở góc phải. Ở trang chủ, header ghim cố định và thu nhỏ logo khi cuộn (" + R.next_fig() + ").")
    R.figure(W / "50-header.png", "Header của website", width=16.5)
    R.h4("7.3.2. Footer")
    R.p("Footer gồm bộ chọn vùng/tiền tệ và dòng bản quyền kèm ghi chú “Student project, not a real store” theo yêu cầu đồ án (" + R.next_fig() + ").")
    R.figure(W / "51-footer.png", "Footer của website", width=16.5)
    impl(R, "Triển khai các thành phần dùng chung", [
        ("Biểu tượng giỏ hàng", "Đọc giỏ trong localStorage, hiện số món; lắng nghe sự kiện cart-change và storage để cập nhật", "header.js, cart.js"),
        ("Biểu tượng tài khoản", "Tạo liên kết bằng DOM; chưa đăng nhập thì mở popup, đã đăng nhập thì sang trang Account", "auth-ui.js"),
        ("Header ghim", "Sự kiện scroll thêm lớp is-scrolled để thu nhỏ logo", "header.js"),
        ("Bộ chọn tiền tệ", "select + sự kiện change; lưu lựa chọn, vẽ lại giá", "currency.js, shop.js"),
        ("Chặn truy cập", "Mỗi trang gọi requireAccess() ngay trong head", "guard.js"),
    ])

    R.h3("7.4. Cấu trúc chi tiết “Trang cổng”")
    R.p("Trang cổng (" + R.next_fig() + ") là trang đầu tiên khách nhìn thấy: đồng hồ đếm ngược (ngày, giờ, phút, giây) tới ngày "
        "ra mắt, tên dòng sản phẩm DOOMTECH™, tên bộ sưu tập Spider-Corpse, ngày ra mắt và dải ảnh lookbook xếp dọc. Nút “Enter "
        "using password” ở góc phải trên mở hộp nhập mã (" + R.next_fig(2) + "); nhập sai thì báo lỗi ngay dưới ô (" + R.next_fig(3) + ").")
    R.p("Bố cục trang cổng từ trên xuống:", keep_next=True)
    R.bullets([
        "**Góc phải trên:** nút “Enter using password”, bấm mở hộp nhập mã nằm ngay dưới, không chuyển trang.",
        "**Giữa trang:** đồng hồ đếm ngược bốn ô (Days, Hours, Mins, Secs) cỡ chữ lớn; ô giây có gạch ngang như một chi tiết trang trí.",
        "**Khối giới thiệu drop:** dòng DOOMTECH™ giãn chữ rộng, tên bộ sưu tập SPIDER-CORPSE, dòng COLLECTION X kèm ngày ra mắt.",
        "**Lookbook:** 10 ảnh chiến dịch xếp dọc, rộng tối đa 900 px, co theo màn hình.",
    ])
    R.figure(W / "01-gate.png", "Giao diện “Trang cổng”", width=15.5)
    R.figure(W / "02-gate-dialog.png", "Hộp nhập mã truy cập mở ra ở góc phải trên", width=15.5)
    R.figure(W / "03-gate-wrong.png", "Thông báo khi nhập sai mã", width=15.5)
    impl(R, "Triển khai ở trang cổng", [
        ("Đồng hồ đếm ngược", "setInterval mỗi giây tính thời gian còn lại tới mốc ra mắt (mặc định hoặc do quản trị viên đặt)", "countdown.js"),
        ("Hộp nhập mã", "Sự kiện click mở/đóng (aria-expanded); sự kiện submit kiểm tra mã", "gate.js"),
        ("Kiểm tra mã", "SHA-256 bằng Web Crypto; tìm mã athlete đang bật (fetch access.json)", "gate.js, athletes.js"),
        ("Lookbook", "img có width/height và loading=\"lazy\" để không xô lệch bố cục", "index.html, pages.css"),
    ])

    R.h3("7.5. Cấu trúc chi tiết “Trang chủ” và cửa hàng")
    R.h4("7.5.1. Phần mở đầu và video")
    R.p("Trang chủ mở đầu bằng video toàn màn hình với dòng chữ “Collection X Is Out Now” dẫn xuống cửa hàng (" + R.next_fig() +
        "). Giữa các khu sản phẩm có các đoạn video ngắn tạo nhịp (" + R.next_fig(2) + "); video tự dừng nếu người dùng bật giảm chuyển động.")
    R.figure(W / "04-home-hero.png", "Phần mở đầu trang chủ với video giới thiệu bộ sưu tập", width=15.5)
    R.figure(W / "54-break-video.png", "Đoạn video chuyển tiếp giữa các khu sản phẩm", width=15.5)
    R.h4("7.5.2. Các khu sản phẩm")
    R.p("Cửa hàng chia ba khu: Sanctuary (nam), Sanctuary Selene (nữ) và Accessories. Mỗi khu chia nhóm theo loại (compression, "
        "oversized tee, stringer, hoodie, quần...). Thẻ sản phẩm có ảnh (rê chuột hiện ảnh thứ hai), tên, giá theo tiền tệ đang "
        "chọn và các ô màu (" + R.next_fig() + " đến " + R.next_fig(4) + ").")
    R.p("Bố cục mỗi thẻ sản phẩm:", keep_next=True)
    R.bullets([
        "**Ảnh:** tỉ lệ cố định, ảnh của màu đầu tiên; rê chuột hiện ảnh thứ hai.",
        "**Tên và giá:** tên sản phẩm in hoa, giá theo tiền tệ đang chọn bên dưới.",
        "**Ô màu và nhãn:** các chấm màu theo mã hex của từng màu sản phẩm; sản phẩm có nhãn (ví dụ New với sản phẩm quản trị viên vừa thêm) hiện dòng chữ đỏ dưới cùng.",
        "**Tương tác:** cả thẻ là một nút (role=\"button\", tabindex=0), bấm chuột hoặc Enter/Space đều mở popup.",
    ])
    R.figure(W / "05-shop.png", "Phần đầu cửa hàng: thẻ dòng nam, nữ và khu Sanctuary", width=15.5)
    R.figure(W / "06-shop-grid.png", "Lưới sản phẩm theo nhóm", width=15.5)
    R.figure(W / "52-selene.png", "Khu Sanctuary Selene (dòng nữ)", width=15.5)
    R.figure(W / "53-accessories.png", "Khu Accessories (phụ kiện)", width=15.5)
    R.h4("7.5.3. Menu Armory: lọc và sắp xếp")
    R.p("Tab Armory ở mép trái trượt menu ra từ cạnh màn hình (" + R.next_fig() + "): chọn khu để cuộn tới, lọc theo size, màu, "
        "sắp xếp giá tăng/giảm và xoá bộ lọc. Khi đang lọc, một dòng ghi chú cho biết bộ lọc đang áp dụng và số sản phẩm (" + R.next_fig(2) + ").")
    R.figure(W / "07-armory-menu.png", "Menu Armory", width=15.5)
    R.figure(W / "08-filter-applied.png", "Kết quả lọc theo size, màu và sắp xếp theo giá", width=15.5)
    impl(R, "Triển khai ở trang chủ", [
        ("Tải sản phẩm", "fetch products.json, áp ghi đè và sản phẩm do quản trị viên thêm, bỏ sản phẩm ẩn/xoá", "products.js"),
        ("Thẻ sản phẩm", "createElement, gắn click/keydown (Enter, Space) mở popup", "products.js"),
        ("Chia khu, nhóm", "Gom sản phẩm theo gender và category, vẽ tiêu đề nhóm", "shop.js"),
        ("Lọc, sắp xếp", "Sự kiện change trên các select; ẩn thẻ không khớp, sắp xếp lại trong mỗi nhóm", "shop.js"),
        ("Menu Armory", "Sự kiện click mở/đóng, click ra ngoài và Esc để đóng", "shop.js"),
        ("Video, hiệu ứng cuộn", "Sự kiện scroll làm mờ chữ; prefers-reduced-motion dừng video", "home-ui.js"),
    ])

    R.h3("7.6. Cấu trúc chi tiết “Chi tiết sản phẩm”")
    R.p("Popup chi tiết (" + R.next_fig() + ") gồm slideshow ảnh theo màu, tên, giá, nút màu, nút size XXS - XXL, số lượng (giới "
        "hạn theo tồn kho), dòng tồn kho, nút Add to cart và Buy now, thông số chất liệu, đặc điểm và đánh giá liên quan. Chọn màu "
        "khác thì ảnh đổi theo (" + R.next_fig(2) + ").")
    R.figure(W / "09-product-popup.png", "Giao diện popup “Chi tiết sản phẩm”", width=15.5)
    R.figure(W / "10-product-color.png", "Ảnh đổi theo màu được chọn", width=15.5)
    R.p("Mục Size chart hiện bảng số đo của từng size (vòng ngực, eo, chiều cao, cân nặng), đổi được giữa cm/kg và in/lb, dòng "
        "của size đang chọn được tô sáng (" + R.next_fig() + ", " + R.next_fig(2) + "). Mục Find your size nhận chiều cao, cân "
        "nặng và trả về size gợi ý kèm lưu ý theo kiểu dáng, có nút “Use size” để chọn nhanh (" + R.next_fig(3) + ").")
    R.figure(W / "11-size-chart.png", "Bảng size đơn vị cm/kg", width=12)
    R.figure(W / "55-size-chart-inch.png", "Bảng size đơn vị in/lb", width=12)
    R.figure(W / "12-size-finder.png", "Kết quả gợi ý size", width=12)
    R.figure(W / "13-added.png", "Nút đổi thành “Added ✓” sau khi thêm vào giỏ", width=12)
    impl(R, "Triển khai ở chi tiết sản phẩm", [
        ("Popup", "Thẻ dialog, showModal(); Esc và nút đóng", "product-popup.js"),
        ("Slideshow ảnh", "Dùng chung cho sản phẩm và đánh giá; nút trước/sau, chấm chỉ vị trí", "slideshow.js"),
        ("Chọn màu, size", "Nút có aria-pressed; màu ngừng bán bị khoá; size tô sáng dòng tương ứng trong bảng size", "product-popup.js"),
        ("Bảng size", "Tạo table/thead/tbody bằng DOM từ size-chart.json; đổi đơn vị vẽ lại bảng", "product-popup.js"),
        ("Gợi ý size", "Đổi đơn vị, hồi quy tuyến tính, tra mốc size", "size-finder.js"),
        ("Thêm vào giỏ", "Kiểm tra size, màu, tồn kho; lưu localStorage; phát sự kiện cart-change", "product-popup.js, cart.js"),
        ("Đánh giá liên quan", "So khớp tên sản phẩm; không có thì lấy đánh giá cùng loại", "product-reviews.js"),
    ])

    R.h3("7.7. Cấu trúc chi tiết “Đánh giá”")
    R.p("Nút Reviews ở mép trái mở popup đánh giá (" + R.next_fig() + "): điểm trung bình, tổng số đánh giá, ba hàng bộ lọc (số "
        "sao, dòng, loại sản phẩm) có số lượng trên từng nút, và lưới thẻ đánh giá có ảnh thật; chọn bộ lọc thì lưới cập nhật "
        "ngay (" + R.next_fig(2) + "). Bấm một thẻ để xem ảnh lớn và đọc toàn bộ nội dung (" + R.next_fig(3) + ").")
    R.figure(W / "14-reviews.png", "Giao diện popup “Đánh giá”", width=15.5)
    R.figure(W / "15-reviews-filter.png", "Kết quả lọc đánh giá theo số sao", width=15.5)
    R.figure(W / "15b-review-detail.png", "Chi tiết một đánh giá với slideshow ảnh", width=15.5)
    impl(R, "Triển khai ở đánh giá", [
        ("Bộ lọc", "Object FILTERS gồm nhãn, lựa chọn và hàm kiểm tra; đếm số lượng cho từng nút", "reviews.js"),
        ("Hiện thêm", "Nút Show more vẽ thêm thẻ", "reviews.js"),
        ("Ảnh đánh giá", "Thử .webp trước, lỗi thì dùng .jpg (sự kiện error)", "product-reviews.js"),
        ("Mở/đóng popup", "Nút Reviews hiện sau khi cuộn qua phần video đầu trang", "reviews-panel.js"),
    ])

    R.h3("7.8. Cấu trúc chi tiết nhóm trang “Giỏ hàng và Thanh toán”")
    R.h4("7.8.1. Giỏ hàng")
    R.p("Trang Cart (" + R.next_fig() + ") hiện danh sách món (ảnh, tên, màu, size, nút +/−, Remove, số còn trong kho), khối tóm "
        "tắt đơn (tạm tính, giảm giá, phí ship theo khối lượng, thuế nhập khẩu, VAT/GST, tổng) và mục gợi ý “You may also like”. "
        "Giỏ trống thì hiện thông báo và nút tiếp tục mua (" + R.next_fig(2) + ").")
    R.p("Bố cục trang giỏ hàng trên máy tính chia hai cột:", keep_next=True)
    R.bullets([
        "**Cột trái:** danh sách món; mỗi dòng có ảnh, tên, màu, size, bộ chọn số lượng, Remove, số còn trong kho, giá dòng (kèm giá mỗi món nếu số lượng > 1).",
        "**Cột phải (ghim khi cuộn):** Order summary gồm ô mã athlete, tạm tính, giảm giá, phí ship kèm khối lượng, thuế nhập khẩu (nếu có), VAT/GST, tổng; bên dưới là form Checkout.",
        "**Cuối trang:** dải “You may also like” lướt ngang bằng hai nút, gợi ý sản phẩm chưa có trong giỏ.",
        "**Trên điện thoại:** hai cột xếp thành một cột, tóm tắt đơn nằm sau danh sách món.",
    ])
    R.figure(W / "16-cart.png", "Giao diện “Giỏ hàng”", width=15.5)
    R.figure(W / "56-cart-empty.png", "Giỏ hàng trống", width=15.5)
    R.figure(W / "18-discount.png", "Áp mã giảm giá athlete", width=15.5)
    R.h4("7.8.2. Thanh toán")
    R.p("Form thanh toán gồm thông tin giao hàng, nước nhận, phương thức thanh toán (thẻ, PayPal, Apple Pay, Google Pay) và thông "
        "tin thẻ. Lỗi hiện ngay dưới từng ô khi bấm Place order hoặc khi rời ô (" + R.next_fig() + ", " + R.next_fig(2) + "). Đặt "
        "thành công, website hiện mã đơn và email nhận xác nhận (" + R.next_fig(3) + "), đồng thời bật popup “Order placed” "
        "ở góc trên bên phải, tự ẩn sau 2,5 giây (" + R.next_fig(4) + ").")
    R.figure(W / "19-checkout-errors.png", "Lỗi kiểm tra thông tin giao hàng", width=15.5)
    R.figure(W / "20-checkout-card-errors.png", "Lỗi kiểm tra thông tin thẻ", width=15.5)
    R.figure(W / "21-order-done.png", "Thông báo đặt hàng thành công", width=13)
    R.figure(W / "73-toast-order.png", "Popup “Order placed” sau khi đặt hàng", width=15.5)
    impl(R, "Triển khai ở giỏ hàng và thanh toán", [
        ("Danh sách món", "Vẽ bằng DOM; +/− khoá theo tồn kho; Remove xoá dòng", "cart-page.js"),
        ("Phí ship, thuế", "XMLHttpRequest đọc shipping.xml; calcCosts() tính theo nước", "shipping.js"),
        ("Mã giảm giá", "So với mã athlete đang bật, giảm 10%", "cart-page.js, athletes.js"),
        ("Kiểm tra form", "Object luật rules (bắt buộc, email, SĐT, Luhn, hạn thẻ, CVC); kiểm tra khi gõ và khi gửi", "form-validate.js"),
        ("Nhận diện hãng thẻ", "Sự kiện input đọc các số đầu, làm sáng nhãn Visa/Mastercard/Amex/JCB", "cart-page.js"),
        ("Đặt hàng", "Kiểm tra lại giỏ; writeAll() ghi đơn + tồn kho cùng lúc", "cart-page.js, storage.js"),
        ("Popup thành công", "showToast() tạo khối thông báo bằng DOM, setTimeout tự ẩn sau 2,5 giây; aria-live để trình đọc màn hình đọc nội dung", "toast.js"),
    ])

    R.h3("7.9. Cấu trúc chi tiết nhóm trang “Tài khoản người dùng”")
    R.p("Popup Sign in / Create account (" + R.next_fig() + ") có hai thẻ chuyển qua lại; form đăng ký kiểm tra dữ liệu và báo lỗi "
        "dưới từng ô (" + R.next_fig(2) + "). Trang Account (" + R.next_fig(3) + ") gồm lời chào, hồ sơ và địa chỉ, đổi mật khẩu, "
        "đăng xuất và lịch sử đơn hàng kèm trạng thái.")
    R.figure(W / "28-signin-popup.png", "Giao diện popup “Đăng nhập”", width=15.5)
    R.figure(W / "28b-register-errors.png", "Giao diện “Đăng ký” và thông báo lỗi", width=15.5)
    R.figure(W / "62-account-2.png", "Giao diện trang “Tài khoản” với hồ sơ và lịch sử đơn hàng", width=15.5)
    R.p("Trang Account chia hai cột: cột trái là lời chào kèm email và ngày tham gia, form Details and address (họ tên, SĐT, "
        "địa chỉ, thành phố, nước), mục Change password thu gọn và nút Sign out; cột phải là danh sách đơn, mỗi đơn có mã, ngày, "
        "ảnh và tên từng món, trạng thái tô màu theo loại (Processing, Shipped, Delivered, Cancelled) và tổng tiền. Khách chưa "
        "đăng nhập mở trang này thì thấy lời mời đăng nhập hoặc tạo tài khoản.")
    R.p("Tạo tài khoản hoặc đăng nhập thành công thì popup đóng lại và một thông báo nhỏ hiện ở góc trên bên phải, ghi tên "
        "khách, rồi tự ẩn sau 2,5 giây (" + R.next_fig() + ", " + R.next_fig(2) + ").")
    R.figure(W / "70-toast-register.png", "Popup “Account created” sau khi tạo tài khoản", width=15.5)
    R.figure(W / "71-toast-signin.png", "Popup “Signed in” sau khi đăng nhập", width=15.5)
    impl(R, "Triển khai ở tài khoản người dùng", [
        ("Đăng ký", "Kiểm tra form; tạo salt (getRandomValues), băm SHA-256; lưu sanctuary_users", "auth.js, auth-ui.js"),
        ("Đăng nhập", "Băm lại với salt đã lưu, so sánh; lưu sanctuary_session; phát auth-change", "auth.js"),
        ("Hồ sơ, mật khẩu", "Form có kiểm tra; đổi mật khẩu cần mật khẩu hiện tại", "account-page.js"),
        ("Lịch sử đơn", "Đọc sanctuary_orders, lọc theo email, đơn mới nhất trước", "account-page.js"),
    ])

    R.h3("7.10. Cấu trúc chi tiết nhóm trang “Thông tin” (Info)")
    R.h4("7.10.1. Liên hệ")
    R.p("Tab Contact (" + R.next_fig() + ") gồm thông tin liên hệ mẫu, câu hỏi nhanh dẫn tới chính sách liên quan, bản đồ Google "
        "Maps nhúng bằng iframe (địa chỉ Trường Đại học Kinh tế - Luật) và form liên hệ có bộ đếm ký tự (" + R.next_fig(2) + "). "
        "Gửi thành công thì hiện dòng xác nhận dưới form (" + R.next_fig(4) + ") và popup “Message sent” tự ẩn sau 2,5 giây (" +
        R.next_fig(5) + ").")
    R.figure(W / "22-contact.png", "Giao diện “Liên hệ”", width=15.5)
    R.figure(W / "23-contact-full.png", "Toàn trang “Liên hệ” với bản đồ iframe và form", width=11)
    R.figure(W / "24-contact-errors.png", "Form liên hệ báo lỗi khi để trống", width=11)
    R.figure(W / "25-contact-sent.png", "Thông báo gửi tin nhắn thành công", width=11)
    R.figure(W / "72-toast-contact.png", "Popup “Message sent” sau khi gửi tin nhắn", width=15.5)
    R.h4("7.10.2. Các trang chính sách")
    R.p("Năm tab chính sách là Shipping/Returns, Terms and Conditions, Terms of Service, Privacy Policy và Accessibility (" +
        R.next_fig() + " đến " + R.next_fig(5) + "). Nội dung tham khảo cấu trúc trang chính sách của thương hiệu tham chiếu, được "
        "nhóm viết lại cho SANCTUARY và ghi rõ đây là website học tập.")
    R.figure(W / "26-policy-shipping.png", "Giao diện “Shipping/Returns”", width=15.5)
    R.figure(W / "57-policy-terms.png", "Giao diện “Terms and Conditions”", width=15.5)
    R.figure(W / "58-policy-tos.png", "Giao diện “Terms of Service”", width=15.5)
    R.figure(W / "59-policy-privacy.png", "Giao diện “Privacy Policy”", width=15.5)
    R.figure(W / "60-policy-accessibility.png", "Giao diện “Accessibility”", width=15.5)
    impl(R, "Triển khai ở trang Info", [
        ("Chuyển tab", "Đọc location.hash, ẩn/hiện section; sự kiện click trên tab và popstate (nút quay lại)", "info.js"),
        ("Form liên hệ", "Kiểm tra dữ liệu; bộ đếm ký tự (sự kiện input); lưu sanctuary_messages", "contact.js"),
        ("Bản đồ", "iframe Google Maps, loading=\"lazy\", lọc màu tối bằng CSS filter", "contact.html, pages.css"),
    ])

    R.h3("7.11. Cấu trúc chi tiết trang “Về chúng tôi” (About)")
    R.p("Trang About (" + R.next_fig() + ", " + R.next_fig(2) + ") kể câu chuyện thương hiệu qua các mục Our story, The name, The "
        "craft, The drops và câu hỏi thường gặp, xen kẽ ảnh lookbook lớn.")
    R.figure(W / "27-about.png", "Giao diện “Về chúng tôi” (phần đầu)", width=15.5)
    R.figure(W / "61-about-2.png", "Giao diện “Về chúng tôi” (mục The craft, The drops)", width=15.5)

    R.h3("7.12. Cấu trúc chi tiết nhóm trang “Quản trị viên”")
    admin = [
        ("Tổng quan (Overview)", "30-admin-overview.png", "Các thẻ chỉ số (doanh thu không tính đơn huỷ, số đơn và đơn chờ xử lý, giá trị đơn trung bình, khách, tin chưa đọc, hàng sắp hết), bảng đơn gần đây, sản phẩm sắp hết hàng và sản phẩm bán chạy."),
        ("Quản lý “Orders”", "31-admin-orders.png", "Ô tìm kiếm, bộ lọc trạng thái, bảng đơn có ô chọn trạng thái và nút xem chi tiết từng đơn."),
        ("Đổi trạng thái đơn", "39-admin-order-status.png", "Chọn trạng thái mới ngay trong bảng; trạng thái được tô màu theo loại và có thông báo nhỏ sau khi lưu."),
        ("Chi tiết đơn hàng", "64-admin-order-detail.png", "Mở rộng một đơn để xem từng món hàng, thông tin người nhận, phương thức thanh toán, mã giảm giá đã dùng."),
        ("Quản lý “Products”", "32-admin-products.png", "Bảng sản phẩm với ô sửa giá, tồn kho, công tắc nổi bật, ẩn/hiện, nút xoá; tìm kiếm, lọc danh mục, khôi phục sản phẩm đã xoá, đặt lại theo dữ liệu gốc."),
        ("Thêm sản phẩm", "33-admin-product-form.png", "Form thêm sản phẩm: tên, dòng, danh mục, giá, tồn kho, màu (tên + mã màu), size, ảnh có xem trước, đặc điểm, nổi bật."),
        ("Quản lý “Customers”", "34-admin-customers.png", "Danh sách tài khoản khách với SĐT, nơi ở, ngày tham gia, số đơn, tổng chi tiêu; tìm theo tên, email."),
        ("Quản lý “Messages”", "35-admin-messages.png", "Danh sách tin nhắn, tin chưa đọc được đánh dấu; nút đánh dấu đã đọc, trả lời qua email, xoá."),
        ("Quản lý “Athlete codes”", "36-admin-codes.png", "Form thêm mã có nút gợi ý mã; bảng mã với công tắc bật/tắt, sao chép, xoá; đặt lại theo access.json."),
        ("Đặt “Launch date”", "37-admin-launch.png", "Chọn ngày giờ ra mắt theo giờ Việt Nam, xem thời gian còn lại, khôi phục mặc định."),
        ("Sao lưu “Backup”", "38-admin-backup.png", "Tải file sao lưu, khôi phục từ file, thêm dữ liệu mẫu, xoá dữ liệu cửa hàng."),
    ]
    for i, (t, f, d) in enumerate(admin, 1):
        R.h4("7.12.%d. %s" % (i, t))
        R.p(d)
        R.figure(W / f, "Giao diện " + t[0].lower() + t[1:], width=15.5)
    impl(R, "Triển khai ở trang quản trị", [
        ("Chặn quyền", "requireAccess(\"admin\") trong head", "guard.js"),
        ("Chuyển mục", "Liên kết #mục, đọc hash hiện panel tương ứng", "admin.js"),
        ("Bảng dữ liệu", "Hàm table() tạo table/thead/tbody bằng DOM, dữ liệu ghi bằng textContent", "admin.js"),
        ("Đổi trạng thái đơn", "Sự kiện change; hoàn kho khi huỷ; writeAll()", "admin.js, storage.js"),
        ("Ảnh sản phẩm", "FileReader + canvas thu nhỏ 800 px, xuất WebP", "admin.js"),
        ("Sao lưu", "Blob + liên kết tải xuống; khôi phục đọc file, kiểm tra cấu trúc", "admin.js"),
    ])

    R.h3("7.13. Giao diện trên thiết bị di động và máy tính bảng")
    R.p("Trên điện thoại 390 px, logo ở giữa, menu gọn lại, lưới sản phẩm 2 cột, popup sản phẩm xếp ảnh trên thông tin dưới, giỏ "
        "hàng và form xếp một cột (" + R.next_fig() + ", " + R.next_fig(2) + "). Trang About, trang Account và popup thông báo "
        "thành công cũng co theo màn hình; popup rộng gần hết chiều ngang, chừa lề 16 px hai bên (" + R.next_fig(3) + "). Trên "
        "máy tính bảng 820 px, lưới có 3 cột (" + R.next_fig(4) + "). Ở mọi độ rộng, trang không bị cuộn ngang.")
    R.figure(ctx["comp"] / "mobile-1.png", "Giao diện điện thoại: trang cổng, trang chủ, cửa hàng", width=16)
    R.figure(ctx["comp"] / "mobile-2.png", "Giao diện điện thoại: chi tiết sản phẩm, giỏ hàng, trang Info", width=16)
    R.figure(ctx["comp"] / "mobile-3.png", "Giao diện điện thoại: trang About, trang Account, popup “Message sent”", width=16)
    R.figure(W / "46-t-shop.png", "Giao diện máy tính bảng: lưới sản phẩm 3 cột", height=14)
