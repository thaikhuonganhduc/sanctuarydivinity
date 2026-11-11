# -*- coding: utf-8 -*-
"""PHẦN B - CHƯƠNG 8. CÀI ĐẶT VÀ QUẢN TRỊ NỀN TẢNG MÃ NGUỒN MỞ WOOCOMMERCE"""


def build(R, ctx):
    W = ctx["woo"]
    R.chapter(8, "CÀI ĐẶT VÀ QUẢN TRỊ NỀN TẢNG MÃ NGUỒN MỞ WOOCOMMERCE")
    R.p("Để đáp ứng chuẩn đầu ra về hệ thống thương mại điện tử mã nguồn mở, nhóm cài đặt WooCommerce, nhập dữ liệu SANCTUARY "
        "và thực hiện các thao tác quản trị cơ bản: sản phẩm, đơn hàng, khách hàng, vận chuyển, thuế và giao diện. Mọi ảnh trong "
        "chương được chụp từ bản cài thử chạy trên máy của nhóm.")
    R.h3("8.1. Cài đặt")
    R.h4("8.1.1. Lựa chọn môi trường cài đặt")
    R.p("Thay vì cài XAMPP (Apache, PHP, MySQL), nhóm dùng **WordPress Playground**, bản WordPress chạy bằng WebAssembly trên "
        "Node.js, không cần cài PHP, MySQL hay quyền quản trị máy (WordPress.org, n.d.). Các bước cài đặt được mô tả trong một tệp "
        "*blueprint* nên mọi thành viên chạy lại được bằng một lệnh, cho ra cùng một kết quả.")
    R.table(["Thành phần", "Phiên bản / cấu hình"], [
        ("WordPress", "7.1.4 (PHP 8.3, CSDL SQLite do Playground cung cấp)"),
        ("WooCommerce", "11.2.2"),
        ("Theme", "Storefront (theme chính thức của WooCommerce)"),
        ("Cấu hình cửa hàng", "Tên SANCTUARY; địa chỉ 669 Đỗ Mười, TP. Hồ Chí Minh; tiền tệ USD; bật tính thuế; múi giờ Asia/Ho_Chi_Minh"),
        ("Dữ liệu nhập", "12 sản phẩm có biến thể size, 3 khách hàng, 6 đơn hàng, 2 vùng giao hàng, thuế VAT 8% cho Việt Nam"),
    ], widths=[4.4, 12.6], caption="Thông tin bản cài thử WooCommerce", size=12, bold_first=True)
    R.h4("8.1.2. Các bước cài đặt")
    R.bullets([
        "Tạo tệp `tools/woocommerce/blueprint.json`: đăng nhập admin, cài và kích hoạt plugin WooCommerce, cài theme Storefront, đặt thông tin cửa hàng, bỏ màn hình hướng dẫn ban đầu.",
        "Chạy script `tools/woocommerce/build_seed.py` lấy 12 sản phẩm từ `data/products.json`, đổi ảnh sang JPG.",
        "Khởi động máy chủ bằng lệnh bên dưới; khi thấy “Ready! WordPress is running on http://127.0.0.1:9400” là cài xong.",
        "Mở `/sanctuary-seed/run.php` để nhập dữ liệu: script dùng API của WooCommerce (WC_Product_Variable, wc_create_order...) tạo danh mục, thuộc tính, sản phẩm, khách, đơn, vùng giao hàng, thuế và màu theme.",
    ])
    R.code("""npx @wp-playground/cli@3.1.59 server --port=9400 --login \\
    --blueprint=tools/woocommerce/blueprint.json \\
    --mount-dir "<thư mục dự án>\\tools\\woocommerce" /wordpress/sanctuary-seed""", caption="Lệnh khởi động bản cài thử:")
    R.figure(W / "01-plugins.png", "WooCommerce đã được cài và kích hoạt trong trang Plugins", width=15.5)
    R.figure(W / "02-wc-home.png", "Trang chủ quản trị WooCommerce", width=15.5)

    R.h3("8.2. Quản lý sản phẩm")
    R.p("Mỗi sản phẩm SANCTUARY là một *variable product*: thuộc tính toàn cục **Size** (XXS - XXL, One Size) sinh ra các biến "
        "thể, tồn kho quản lý ở cấp sản phẩm. Danh mục hai cấp theo dòng (Sanctuary nam, Sanctuary Selene nữ, Accessories) và "
        "loại hàng (Compression, Oversized Tees, Hoodies...). Bốn sản phẩm đầu được đánh dấu nổi bật.")
    R.figure(W / "03-products.png", "Danh sách sản phẩm SANCTUARY trong WooCommerce", width=15.5)
    R.figure(W / "04-product-edit-top.png", "Màn hình chỉnh sửa sản phẩm", width=15.5)
    R.figure(W / "05-product-variations.png", "Biến thể theo size của một sản phẩm", width=15.5)
    R.figure(W / "06-product-inventory.png", "Thiết lập SKU và tồn kho", width=15.5)
    R.figure(W / "07-categories.png", "Danh mục sản phẩm hai cấp", width=15.5)
    R.figure(W / "08-attributes.png", "Thuộc tính toàn cục Size", width=15.5)

    R.h3("8.3. Quản lý đơn hàng")
    R.p("Sáu đơn mẫu có các trạng thái Completed, Processing, On hold và Cancelled; đơn bị huỷ không trừ kho. Nhóm thao tác thật "
        "trên giao diện quản trị: mở đơn #115, đổi trạng thái từ Processing sang Completed và bấm Update; WooCommerce tự ghi chú "
        "lịch sử thay đổi vào đơn và cập nhật danh sách.")
    R.figure(W / "09-orders.png", "Danh sách đơn hàng", width=15.5)
    R.figure(W / "10-order-detail.png", "Chi tiết một đơn hàng", width=15.5)
    R.figure(W / "11-order-status-updated.png", "Đổi trạng thái đơn hàng sang Completed", width=15.5)
    R.figure(W / "12-orders-after.png", "Danh sách đơn sau khi cập nhật trạng thái", width=15.5)

    R.h3("8.4. Quản lý khách hàng và báo cáo")
    R.p("Trang Customers tự tổng hợp số đơn, tổng chi tiêu và giá trị đơn trung bình của từng khách; trang Analytics hiện doanh "
        "thu, số đơn, sản phẩm bán ra theo khoảng thời gian.")
    R.figure(W / "13-customers.png", "Trang khách hàng của WooCommerce", width=15.5)
    R.figure(W / "18-analytics.png", "Trang báo cáo Analytics", width=15.5)

    R.h3("8.5. Vận chuyển và thuế")
    R.p("Nhóm tạo hai vùng giao hàng tương ứng dữ liệu shipping.xml: Vietnam (phí cố định 3 USD) và International (24 USD cho Mỹ, "
        "Nhật, Hàn, Singapore, Úc, Anh), cùng thuế VAT 8% cho Việt Nam.")
    R.figure(W / "14-shipping-zones.png", "Cấu hình vùng giao hàng", width=15.5)
    R.figure(W / "15-tax.png", "Cấu hình thuế VAT", width=15.5)

    R.h3("8.6. Tùy biến giao diện")
    R.p("Theme Storefront được tùy biến trong Customizer sang nền đen, chữ trắng, nút trắng, nút phụ đỏ và logo SANCTUARY, gần với "
        "phong cách của website tự lập trình. Phía khách hàng có đủ trang cửa hàng, chi tiết sản phẩm chọn size, giỏ hàng và thanh toán.")
    R.figure(W / "16-themes.png", "Theme Storefront được kích hoạt", width=15.5)
    R.figure(W / "17-customizer.png", "Tùy biến màu sắc và logo trong Customizer", width=15.5)
    R.figure(W / "20-shop.png", "Trang cửa hàng WooCommerce sau khi tùy biến", width=15.5)
    R.figure(W / "21-single-product.png", "Trang chi tiết sản phẩm có chọn size", width=15.5)
    R.figure(W / "22-cart.png", "Giỏ hàng WooCommerce", width=15.5)
    R.figure(W / "23-checkout.png", "Trang thanh toán WooCommerce", width=15.5)

    R.h3("8.7. So sánh WooCommerce với website tự lập trình")
    R.table(["Tiêu chí", "SANCTUARY tự lập trình", "WooCommerce"], [
        ("Hạ tầng", "Web tĩnh, không máy chủ ứng dụng, hosting miễn phí", "Cần PHP + MySQL, hosting WordPress"),
        ("Dữ liệu", "JSON/XML + localStorage từng trình duyệt", "CSDL dùng chung cho mọi khách"),
        ("Đơn hàng, thanh toán", "Mô phỏng, chưa có cổng thanh toán", "Đầy đủ, có plugin cổng thanh toán thật"),
        ("Bảo mật", "Mô phỏng phía máy khách", "Xác thực phía máy chủ, phân quyền, cập nhật bảo mật"),
        ("Trải nghiệm thương hiệu", "Tự do hoàn toàn: drop, mã athlete, gợi ý size, đổi tiền tệ", "Theo theme; tính năng riêng phải tìm plugin hoặc tự viết"),
        ("Báo cáo", "Tổng quan tự viết", "Analytics có sẵn, nhiều chỉ số"),
        ("Thời gian xây dựng", "Lâu, viết từng chức năng", "Nhanh, cài và cấu hình"),
        ("Giá trị học tập", "Hiểu sâu HTML, CSS, JavaScript, DOM, AJAX", "Hiểu quy trình vận hành một cửa hàng thật"),
    ], widths=[3.6, 6.7, 6.7], caption="So sánh website tự lập trình với WooCommerce", size=12)
    R.p("Kết luận: WooCommerce giải quyết nhanh những phần website tự lập trình còn thiếu (cơ sở dữ liệu dùng chung, thanh toán "
        "thật, báo cáo), trong khi website tự lập trình chủ động hơn về trải nghiệm thương hiệu. Khi kinh doanh thật, hướng hợp lý "
        "là dùng WooCommerce làm nền tảng quản lý và đưa giao diện SANCTUARY thành theme riêng.")
