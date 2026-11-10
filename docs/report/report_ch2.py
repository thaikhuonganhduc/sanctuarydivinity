# -*- coding: utf-8 -*-
"""Chương 2. Cơ sở lý thuyết."""


def build(R, ctx):
    R.h1("CHƯƠNG 2. CƠ SỞ LÝ THUYẾT", chapter=2)
    R.h2("2.1. Tổng quan các khái niệm liên quan")

    # ---- 2.1.1 Internet và hệ thống web ----
    R.h3("2.1.1. Internet, mô hình client/server và hệ thống web")
    R.p("**Internet** là mạng máy tính toàn cầu nối các mạng nhỏ hơn với nhau bằng bộ giao thức TCP/IP. Mỗi thiết bị "
        "có một **địa chỉ IP** để định danh; vì địa chỉ số khó nhớ nên người dùng truy cập qua **tên miền**, và hệ "
        "thống tên miền DNS chịu trách nhiệm đổi tên miền thành địa chỉ IP. **World Wide Web** là dịch vụ chạy trên "
        "Internet, gồm các tài liệu siêu văn bản liên kết với nhau và được truyền bằng giao thức **HTTP**; **HTTPS** là "
        "HTTP được mã hoá bằng TLS để chống nghe lén và giả mạo.")
    R.p("Web hoạt động theo **mô hình client/server**: trình duyệt (client) gửi yêu cầu HTTP, **web server** nhận yêu "
        "cầu, tìm tài nguyên (file HTML, CSS, JavaScript, ảnh, dữ liệu) hoặc chạy chương trình để tạo nội dung, rồi trả "
        "phản hồi kèm mã trạng thái (200 thành công, 404 không tìm thấy...). **Web browser** phân tích HTML thành cây "
        "DOM, áp CSS, chạy JavaScript và vẽ trang lên màn hình. Theo cách tạo nội dung, trang web chia thành **web "
        "tĩnh** (server chỉ trả file có sẵn) và **web động** (server sinh nội dung theo từng yêu cầu, thường có CSDL).")
    R.p("SANCTUARY là web tĩnh về phía máy chủ nhưng *động về phía máy khách*: Vercel chỉ phục vụ file, còn toàn bộ "
        "nghiệp vụ (lọc sản phẩm, tính tiền, lưu đơn hàng) chạy bằng JavaScript trong trình duyệt. Cách làm này phù hợp "
        "phạm vi học phần (lập trình phía máy khách) và triển khai miễn phí, nhưng tạo ra các giới hạn về bảo mật và "
        "đồng bộ dữ liệu được phân tích ở Chương 5.")

    # ---- 2.1.2 Thiết kế website TMĐT ----
    R.h3("2.1.2. Thiết kế website thương mại điện tử")
    R.p("Xây dựng một website TMĐT thường đi qua các bước: (1) xác định yêu cầu (mục tiêu kinh doanh, đối tượng khách, "
        "chức năng); (2) thiết kế cấu trúc trang, giao diện và dữ liệu; (3) lập trình; (4) kiểm thử; (5) đưa lên mạng "
        "bằng cách đăng ký tên miền và thuê hosting; (6) vận hành, bảo trì. Về cấu trúc, website có hai phần: "
        "**front-end** là phần người dùng nhìn thấy và tương tác (HTML, CSS, JavaScript chạy trên trình duyệt), "
        "**back-end** là phần xử lý và lưu trữ phía máy chủ (ngôn ngữ phía server, CSDL). Về người dùng, website TMĐT "
        "có phía **khách hàng** (xem, mua hàng) và phía **quản trị** (quản lý sản phẩm, đơn hàng, khách hàng).")
    R.p("Để đưa website lên mạng, nhóm dùng **Vercel**, dịch vụ hosting cho web tĩnh có sẵn CDN và chứng chỉ HTTPS. Mã "
        "nguồn đặt trên GitHub; mỗi lần đẩy commit mới, Vercel tự động triển khai lại. Website dùng tên miền con miễn phí "
        "`sanctuarydivinity.vercel.app`; khi kinh doanh thật chỉ cần trỏ bản ghi DNS của tên miền riêng về Vercel.")

    # ---- 2.1.3 HTML5 ----
    R.h3("2.1.3. Ngôn ngữ HTML5")
    R.p("HTML (HyperText Markup Language) mô tả cấu trúc và ý nghĩa của nội dung bằng các thẻ. Một tài liệu HTML5 bắt "
        "đầu bằng `<!DOCTYPE html>`, gồm phần `<head>` (khai báo bảng mã, viewport, tiêu đề, liên kết CSS) và `<body>` "
        "(nội dung hiển thị). HTML5 bổ sung các **thẻ phân vùng có ngữ nghĩa** (semantic) như `<header>`, `<nav>`, "
        "`<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`, giúp trình duyệt, công cụ đọc màn hình và máy tìm "
        "kiếm hiểu vai trò của từng vùng (Frain, 2020). Các nhóm thẻ dùng nhiều trong đồ án:")
    R.table(["Nhóm thẻ", "Thẻ tiêu biểu", "Chỗ dùng trong SANCTUARY"], [
        ("Heading", "h1 - h3", "Tiêu đề trang, tên khu sản phẩm, tên sản phẩm trong popup"),
        ("Phân vùng", "header, nav, main, section, article, footer", "Khung chung của cả 7 trang"),
        ("Hình ảnh, đa phương tiện", "img (loading=\"lazy\"), video (poster)", "Ảnh sản phẩm WebP, video hero, lookbook"),
        ("Danh sách", "ul, ol, li, dl/dt/dd", "Danh sách giỏ hàng, thông số sản phẩm, câu hỏi nhanh"),
        ("Liên kết", "a (href, #mục)", "Menu, chuyển tab trang Info bằng #shipping, #privacy"),
        ("Bảng", "table, thead, tbody, th scope", "Bảng size, bảng đơn hàng và sản phẩm trong trang quản trị"),
        ("Khung nhúng", "iframe", "Bản đồ Google Maps địa chỉ UEL ở tab Contact"),
        ("Biểu mẫu", "form, label, input, select, textarea, button", "Cổng mật khẩu, thanh toán, liên hệ, đăng ký, quản trị"),
        ("Hộp thoại", "dialog (showModal)", "Popup sản phẩm, popup đánh giá, popup đăng nhập"),
    ], widths=[3.4, 5.4, 7.2], caption="Các nhóm thẻ HTML5 và nơi áp dụng")
    R.p("Với **form**, HTML5 có các kiểu ô nhập như `email`, `number`, thuộc tính `autocomplete` và kiểm tra có sẵn "
        "(`required`, `pattern`). Nhóm đặt `novalidate` trên form và tự kiểm tra bằng JavaScript để thông báo lỗi thống "
        "nhất, hiện ngay dưới từng ô và giải thích được từng luật khi vấn đáp.")

    # ---- 2.1.4 CSS ----
    R.h3("2.1.4. CSS3, mô hình hộp và thiết kế web đáp ứng")
    R.p("CSS định dạng cách hiển thị của các phần tử HTML. Một luật CSS gồm **selector** (chọn phần tử: theo thẻ, lớp "
        "`.btn`, id `#cart`, thuộc tính `[hidden]`, quan hệ cha con, giả lớp `:hover`, `:focus-visible`) và khối khai "
        "báo **thuộc tính: giá trị**. Khi nhiều luật cùng áp vào một phần tử, trình duyệt chọn theo thứ tự ưu tiên "
        "(cascade) và độ đặc hiệu (specificity) của selector (Grant, 2024). CSS có thể nhúng trực tiếp (inline), viết "
        "trong thẻ `<style>` (internal) hoặc để ở file riêng (external); SANCTUARY dùng file riêng để tái sử dụng cho "
        "nhiều trang.")
    R.p("Theo **mô hình hộp (box model)**, mỗi phần tử là một hộp gồm nội dung, đệm trong (padding), viền (border) và lề "
        "ngoài (margin). File `css/reset.css` đặt `box-sizing: border-box` cho mọi phần tử để chiều rộng khai báo đã bao "
        "gồm padding và border, đồng thời xoá lề mặc định khác nhau giữa các trình duyệt: đây là kỹ thuật **reset CSS**. "
        "**Normalize** là cách tiếp cận nhẹ hơn: giữ lại mặc định hữu ích và chỉ sửa chỗ không thống nhất.")
    R.p("CSS3 bổ sung các mô-đun bố cục **Flexbox** (một chiều) và **Grid** (hai chiều), biến CSS (custom properties), "
        "chuyển động (`transition`, `animation`), bộ lọc (`filter`), tỉ lệ khung (`aspect-ratio`). **Thiết kế web đáp ứng** "
        "(responsive web design) gồm ba thành phần: bố cục linh hoạt, ảnh co giãn và truy vấn phương tiện (media query) "
        "(Frain, 2020). SANCTUARY viết theo hướng **mobile-first**: CSS mặc định cho màn hình hẹp, sau đó dùng "
        "`@media (min-width: 768px)` và `@media (min-width: 1024px)` để mở rộng, ví dụ lưới sản phẩm 2 cột trên điện "
        "thoại, 3 cột trên máy tính bảng và 4 cột trên máy tính.")
    R.p("**LESS** là bộ tiền xử lý CSS: bổ sung biến (`@ten-bien`), lồng selector (`&:hover`), mixin (nhóm thuộc tính "
        "có tham số), hàm; file `.less` phải được biên dịch ra `.css` trước khi trình duyệt dùng (Less.js, n.d.). Biến "
        "LESS chỉ tồn tại lúc biên dịch, khác với biến CSS (`--color-bg`) tồn tại lúc chạy và đổi được bằng JavaScript. "
        "**CSS framework** như Bootstrap hay Tailwind CSS cung cấp sẵn lưới và thành phần giao diện giúp làm nhanh. Nhóm "
        "không dùng framework vì giao diện SANCTUARY mang tính thương hiệu cao (chữ gothic, nền đen tuyền, hiệu ứng "
        "riêng) nên phải ghi đè rất nhiều kiểu mặc định; mặt khác viết CSS thuần giúp thể hiện rõ kiến thức selector, "
        "box model và media query của học phần.")
    R.table(["Tiêu chí", "CSS thuần + LESS (nhóm chọn)", "Bootstrap", "Tailwind CSS"], [
        ("Cách dùng", "Tự viết lớp theo quy ước BEM", "Dùng lớp và thành phần có sẵn", "Ghép nhiều lớp tiện ích nhỏ"),
        ("Dung lượng tải", "Chỉ chứa phần web dùng", "Lớn nếu không lọc bớt", "Nhỏ nếu có bước build lọc lớp"),
        ("Giao diện riêng", "Hoàn toàn chủ động", "Dễ bị giống nhau, phải ghi đè", "Chủ động nhưng HTML dài"),
        ("Giá trị học tập", "Thể hiện rõ selector, box model, media query", "Ít viết CSS", "Ít viết CSS truyền thống"),
    ], widths=[3.0, 4.6, 4.2, 4.2], caption="So sánh lựa chọn CSS thuần với hai CSS framework phổ biến", size=11)

    # ---- 2.1.5 JavaScript ----
    R.h3("2.1.5. Ngôn ngữ JavaScript")
    R.p("JavaScript là ngôn ngữ lập trình chạy trong trình duyệt, giúp trang web phản hồi thao tác của người dùng. Mã "
        "có thể nhúng trong thẻ `<script>` hoặc để ở file riêng; SANCTUARY dùng **ES modules** (`<script type=\"module\">`, "
        "`import`/`export`) để chia mã thành " + str(ctx["js_files"]) + " file, mỗi file một nhiệm vụ (giỏ hàng, tiền "
        "tệ, xác thực...). Các thành phần cơ bản của ngôn ngữ (Haverbeke, 2024) đều xuất hiện trong mã nguồn:")
    R.table(["Khái niệm", "Ví dụ trong SANCTUARY"], [
        ("Biến, kiểu dữ liệu", "`const CART_KEY = \"sanctuary_cart\"` (chuỗi); giá, số lượng (số); mảng giỏ hàng; object sản phẩm"),
        ("Toán tử", "Tính tạm tính `p.price * item.qty`; so sánh `===`; toán tử ba ngôi chọn nhãn thuế"),
        ("Cấu trúc điều khiển", "`if/else` kiểm tra mã cổng; vòng `for` của thuật toán Luhn; `forEach` vẽ danh sách"),
        ("Hàm", "`calcCosts()` tính phí ship và thuế; `recommendSize()` gợi ý size; hàm mũi tên cho sự kiện"),
        ("Đối tượng", "Object luật kiểm tra form `rules`; object đơn hàng; `Set` để lọc trùng mã đơn, loại sản phẩm"),
        ("Bất đồng bộ", "`Promise`, `async/await` khi tải JSON, XML và băm SHA-256"),
    ], widths=[4.0, 12.0], caption="Các khái niệm JavaScript và ví dụ áp dụng", size=11)

    # ---- 2.1.6 DOM ----
    R.h3("2.1.6. Mô hình DOM và xử lý sự kiện")
    R.p("**DOM** (Document Object Model) biểu diễn trang HTML thành một cây đối tượng mà JavaScript đọc và sửa được. "
        "Các phương thức dùng nhiều gồm: tìm phần tử (`getElementById`, `querySelector`, `querySelectorAll`), tạo và gắn "
        "phần tử (`createElement`, `append`, `replaceChildren`), đổi nội dung và thuộc tính (`textContent`, "
        "`setAttribute`, `classList.toggle`, `hidden`, `dataset`). SANCTUARY vẽ phần lớn giao diện động bằng DOM: thẻ sản "
        "phẩm, popup chi tiết, bảng size, giỏ hàng, các bảng của trang quản trị. Nhóm dùng `textContent` thay vì "
        "`innerHTML` cho dữ liệu người dùng nhập để tránh chèn mã độc (XSS).")
    R.p("**Xử lý sự kiện** dùng `addEventListener(tên_sự_kiện, hàm)`. Các sự kiện trong đồ án: `click` (nút, thẻ sản "
        "phẩm), `submit` (form, kèm `preventDefault()` để tự xử lý), `input` và `change` (kiểm tra ô nhập ngay khi gõ, "
        "đổi bộ lọc), `keydown` (Enter, Escape), `scroll` (hiện nút cạnh trang, chữ mờ dần), `storage` và sự kiện tự tạo "
        "`auth-change` (đồng bộ trạng thái giữa các phần của trang).")

    # ---- 2.1.7 XML, JSON, AJAX ----
    R.h3("2.1.7. XML, JSON và AJAX")
    R.p("**XML** (eXtensible Markup Language) là ngôn ngữ đánh dấu do người dùng tự đặt tên thẻ, dùng để lưu và trao "
        "đổi dữ liệu có cấu trúc. Một tài liệu XML gồm khai báo `<?xml version=\"1.0\" encoding=\"UTF-8\"?>`, một phần tử "
        "gốc duy nhất, các phần tử lồng nhau, thuộc tính, nội dung văn bản và chú thích; tài liệu phải *well-formed* (thẻ "
        "đóng mở đúng, phân biệt hoa thường). **JSON** là định dạng dữ liệu dựa trên cú pháp object của JavaScript, gọn "
        "hơn XML và đọc trực tiếp thành object.")
    R.p("**AJAX** là kỹ thuật dùng JavaScript gửi yêu cầu HTTP ở chế độ bất đồng bộ và cập nhật một phần trang mà không "
        "tải lại toàn bộ. Cách cổ điển dùng đối tượng `XMLHttpRequest` (mở yêu cầu bằng `open`, gửi bằng `send`, nhận kết "
        "quả trong sự kiện `onload`; với file XML, thuộc tính `responseXML` trả về sẵn cây DOM của tài liệu). Cách hiện "
        "đại dùng hàm `fetch()` trả về Promise (MDN Web Docs, n.d.-a). SANCTUARY dùng **cả hai** để so sánh: dữ liệu sản "
        "phẩm, đánh giá, bảng size là JSON đọc bằng `fetch`; bảng phí vận chuyển và thuế là XML đọc bằng `XMLHttpRequest`.")
    R.table(["Tiêu chí", "XML + XMLHttpRequest", "JSON + fetch"], [
        ("Cú pháp", "Thẻ mở/đóng, có thuộc tính, chú thích", "Cặp khoá: giá trị, mảng, gọn hơn"),
        ("Đọc dữ liệu", "Duyệt DOM: getElementsByTagName, getAttribute", "response.json() ra object ngay"),
        ("Kiểu dữ liệu", "Mọi giá trị là chuỗi, phải tự đổi sang số", "Có sẵn số, chuỗi, logic, mảng"),
        ("Mô hình lập trình", "Hàm callback (onload, onerror)", "Promise, async/await"),
        ("Dùng trong đồ án", "data/shipping.xml (15 nước, 6 vùng)", "products, reviews, access, size-chart"),
    ], widths=[3.4, 6.3, 6.3], caption="So sánh XML/XMLHttpRequest và JSON/fetch trong đồ án", size=11)

    # ---- 2.1.8 Web Storage, Web Crypto ----
    R.h3("2.1.8. Lưu trữ phía trình duyệt và Web Crypto API")
    R.p("**Web Storage** cho phép lưu cặp khoá - chuỗi trong trình duyệt: `localStorage` giữ lại sau khi tắt trình "
        "duyệt, `sessionStorage` mất khi đóng tab; dung lượng khoảng 5 MB cho mỗi nguồn (origin) và chỉ lưu chuỗi nên "
        "object phải đổi bằng `JSON.stringify`/`JSON.parse` (MDN Web Docs, n.d.-b). SANCTUARY lưu giỏ hàng, đơn hàng, "
        "tài khoản, tin nhắn và thay đổi của quản trị viên trong `localStorage`, còn vai trò sau khi qua cổng lưu trong "
        "`sessionStorage`.")
    R.p("**Web Crypto API** cung cấp các hàm mật mã chạy trong trình duyệt. Hàm `crypto.subtle.digest(\"SHA-256\", ...)` "
        "tạo **giá trị băm** 256 bit: cùng đầu vào luôn ra cùng kết quả nhưng không thể suy ngược đầu vào. Nhóm dùng hàm "
        "băm để không lưu mật khẩu dạng chữ thô; mỗi tài khoản có một **salt** 16 byte ngẫu nhiên (`crypto.getRandomValues`) "
        "ghép vào trước mật khẩu, nên hai người cùng mật khẩu vẫn có hai giá trị băm khác nhau (MDN Web Docs, n.d.-c).")

    # ---- 2.1.9 Mã nguồn mở ----
    R.h3("2.1.9. Hệ thống thương mại điện tử mã nguồn mở")
    R.p("Thay vì tự lập trình, doanh nghiệp có thể dùng nền tảng TMĐT mã nguồn mở: tải về miễn phí, cài lên hosting "
        "riêng, mở rộng bằng plugin/module và đổi giao diện bằng theme. Ba nền tảng trong đề cương là Adobe Commerce "
        "(bản mã nguồn mở là Magento Open Source), PrestaShop và WooCommerce.")
    R.table(["Tiêu chí", "Adobe Commerce / Magento", "PrestaShop", "WooCommerce"], [
        ("Kiến trúc", "Ứng dụng PHP độc lập, mô-đun hoá cao", "Ứng dụng PHP độc lập, có module", "Plugin chạy trên WordPress (PHP)"),
        ("CSDL", "MySQL/MariaDB, có thêm Elasticsearch/OpenSearch", "MySQL/MariaDB", "MySQL/MariaDB (hoặc SQLite qua plugin)"),
        ("Yêu cầu hạ tầng", "Cao: cần máy chủ mạnh, cấu hình phức tạp", "Trung bình", "Thấp: hosting WordPress thông thường"),
        ("Phù hợp", "Doanh nghiệp lớn, nhiều cửa hàng, nhiều kho", "Cửa hàng vừa, bán đa quốc gia", "Cửa hàng nhỏ và vừa, cần nội dung"),
        ("Tùy biến giao diện", "Theme + layout XML", "Theme + module", "Theme WordPress (vd. Storefront), Customizer"),
    ], widths=[3.0, 4.6, 4.0, 4.4], caption="So sánh ba nền tảng TMĐT mã nguồn mở trong đề cương", size=11)
    R.p("Nhóm chọn **WooCommerce** để cài thử vì nhẹ nhất, chạy được trên máy cá nhân, và mô hình sản phẩm có biến thể "
        "(size, màu) của nó tương đồng với dữ liệu của SANCTUARY (WooCommerce, n.d.).")

    # ---- 2.1.10 Quản trị website ----
    R.h3("2.1.10. Quản trị website thương mại điện tử")
    R.p("Quản trị website gồm cập nhật thông tin (sản phẩm, giá, chính sách), theo dõi vận hành và bảo vệ hệ thống. "
        "Các **mối đe doạ** thường gặp được OWASP tổng hợp trong danh sách OWASP Top 10, ví dụ kiểm soát truy cập kém "
        "(broken access control), lỗi mật mã, chèn mã (injection, gồm cả XSS), cấu hình bảo mật sai, dùng thành phần có "
        "lỗ hổng (OWASP Foundation, 2021). Ngoài ra còn mất dữ liệu do lỗi người dùng, hỏng phần cứng hay tấn công từ "
        "chối dịch vụ. Vì vậy website cần **kế hoạch sao lưu** (sao lưu gì, bao lâu một lần, lưu ở đâu, khôi phục thế "
        "nào) và **kế hoạch nâng cấp** (cập nhật thư viện, thêm tính năng, thay đổi hạ tầng mà không làm gián đoạn bán "
        "hàng). Phần áp dụng cho SANCTUARY được trình bày ở mục 5.5.")

    # ---- 2.1.11 Chất lượng web ----
    R.h3("2.1.11. Các tiêu chuẩn đánh giá chất lượng website")
    R.p("**Core Web Vitals** là bộ chỉ số trải nghiệm do Google đề xuất: LCP (thời điểm hiện phần nội dung lớn nhất, "
        "tốt khi ≤ 2,5 s), CLS (mức dịch chuyển bố cục, tốt khi ≤ 0,1) và INP (độ trễ phản hồi thao tác, tốt khi ≤ 200 ms) "
        "(Google, n.d.). Công cụ **Lighthouse** đo trong môi trường mô phỏng và chấm điểm 0 - 100 cho bốn nhóm: "
        "Performance, Accessibility, Best Practices và SEO; khi đo thử nghiệm, TBT (tổng thời gian chặn luồng chính) "
        "được dùng thay cho INP (Chrome for Developers, n.d.). **WCAG 2.2** là chuẩn của W3C về khả năng truy cập, xếp "
        "theo bốn nguyên tắc: nhận biết được, thao tác được, hiểu được và bền vững (W3C, 2023). **W3C Nu Html Checker** "
        "kiểm tra mã HTML có đúng đặc tả hay không (W3C, n.d.).")

    # ---- 2.2 Nghiên cứu liên quan ----
    R.h2("2.2. Các nghiên cứu và dự án liên quan")
    R.p("Nhóm chọn các công trình công bố trong 5 năm gần đây (2021 - 2026), không dùng nguồn của MDPI, Frontiers và "
        "Hindawi theo yêu cầu của giảng viên, tập trung vào bốn vấn đề của đề tài.")
    R.p("**Sản phẩm giới hạn và ý định mua.** Ha (2021) khảo sát 336 người tiêu dùng Việt Nam 18 - 25 tuổi về giày phiên "
        "bản giới hạn. Kết quả cho thấy tính khan hiếm và tính độc đáo của sản phẩm làm tăng giá trị xã hội và giá trị "
        "kinh tế mà khách cảm nhận; hai giá trị này tác động có ý nghĩa đến niềm tin thương hiệu và ý định mua. Đây là cơ "
        "sở để SANCTUARY thiết kế trải nghiệm drop: đồng hồ đếm ngược, cổng truy cập bằng mã, hiển thị số lượng còn lại.")
    R.p("**Trả hàng do sai size trong thời trang trực tuyến.** Stöcker và cộng sự (2021) khảo sát 8.393 khách hàng của "
        "một nhà bán lẻ thời trang trực tuyến tại Đức bằng mô hình Kano phân đoạn, chỉ ra kỳ vọng khác nhau của các nhóm "
        "khách về chính sách và trải nghiệm trả hàng. Nghiên cứu nhấn mạnh việc giảm trả hàng ngay từ trước khi mua, ví "
        "dụ bằng thông tin size và độ vừa vặn rõ ràng. SANCTUARY áp dụng bằng bảng size theo số đo thật và công cụ gợi ý size.")
    R.p("**Hệ thống gợi ý size và độ vừa vặn.** Chatterjee và cộng sự (2022) đề xuất đưa nội dung đánh giá của khách về "
        "size, độ vừa vặn vào mô hình dự đoán size, kết hợp đặc trưng khách hàng và sản phẩm; trên bốn tập dữ liệu của một "
        "sàn TMĐT lớn, F1 (macro) tăng 1,37% - 4,31% so với mô hình gốc. Các hệ thống như vậy cần lịch sử mua hàng lớn. "
        "SANCTUARY là cửa hàng mới chưa có lịch sử, nên nhóm chọn hướng đơn giản hơn: học quan hệ giữa chiều cao, cân "
        "nặng và vòng ngực từ bộ số đo cơ thể công khai ANSUR II (Gordon và cộng sự, 2014), rồi tra vòng ngực vào bảng size.")
    R.p("**Khả năng truy cập của website TMĐT.** Acosta-Vargas và cộng sự (2022) đánh giá 50 website TMĐT xếp hạng cao "
        "theo WCAG 2.1 bằng công cụ WAVE và phương pháp WCAG-EM; lỗi phổ biến nhất là độ tương phản màu, và nguyên tắc "
        "“nhận biết được” bị vi phạm nhiều nhất. Kết quả này đặc biệt đáng lưu ý với giao diện nền đen, chữ xám của "
        "SANCTUARY, nên nhóm đưa điểm Accessibility của Lighthouse vào tiêu chí đánh giá.")
    R.p("**Dự án tham khảo.** Website breathedivinity.com là một thương hiệu quần áo gym cao cấp bán theo đợt drop; nhóm "
        "tham khảo bố cục, cách chia dòng sản phẩm nam/nữ/phụ kiện và dùng danh mục sản phẩm của họ làm dữ liệu mẫu. Ở "
        "phía nền tảng, WooCommerce là dự án mã nguồn mở được nhóm cài thử để so sánh với cách tự lập trình (mục 4.6).")
    R.table(["Công trình", "Đối tượng, phương pháp", "Kết quả chính", "Áp dụng vào SANCTUARY"], [
        ("Ha (2021)", "336 người tiêu dùng trẻ Việt Nam; khảo sát, mô hình cấu trúc", "Khan hiếm, độc đáo → giá trị cảm nhận → ý định mua", "Mô hình drop: đếm ngược, mã athlete, số lượng còn lại"),
        ("Stöcker và cộng sự (2021)", "8.393 khách thời trang trực tuyến; Kano phân đoạn", "Kỳ vọng về trả hàng khác nhau theo nhóm khách", "Bảng size rõ ràng, chính sách đổi trả, gợi ý size"),
        ("Chatterjee và cộng sự (2022)", "4 tập dữ liệu sàn TMĐT; mô hình ngôn ngữ BERT", "Đánh giá của khách giúp dự đoán size tốt hơn", "Gợi ý size; đánh giá có nhãn size đã mua"),
        ("Acosta-Vargas và cộng sự (2022)", "50 website TMĐT; WCAG 2.1, WAVE", "Lỗi tương phản phổ biến nhất", "Đo Accessibility, chú ý tương phản nền tối"),
    ], widths=[3.2, 4.2, 4.3, 4.3], caption="Tóm tắt các nghiên cứu liên quan", size=11)
    R.p("Các nghiên cứu trên cho thấy một khoảng trống mà đồ án có thể lấp ở quy mô nhỏ: chưa có mô tả cụ thể cách hiện "
        "thực những yếu tố này (drop, gợi ý size, khả năng truy cập) trên một website chỉ dùng công nghệ phía máy khách.")

    # ---- 2.3 Lý thuyết, mô hình áp dụng ----
    R.h2("2.3. Lý thuyết và mô hình được áp dụng")
    R.bullets([
        "**Mô hình phát triển lặp, tăng dần:** mỗi vòng thêm một nhóm chức năng hoàn chỉnh, có kiểm tra và commit riêng; "
        "phù hợp nhóm nhỏ và thời gian ngắn, vì luôn có một phiên bản chạy được để góp ý.",
        "**Mô hình hoá hệ thống:** UML Use case (chức năng theo tác nhân), ERD ký pháp chân chim (dữ liệu), DFD ký pháp "
        "Gane-Sarson (luồng dữ liệu) và BPMN 2.0 (quy trình nghiệp vụ), cùng lưu đồ giải thuật cho các thuật toán.",
        "**Mobile-first và nâng cấp dần (progressive enhancement):** viết cho màn hình nhỏ trước, rồi bổ sung bố cục cho "
        "màn hình lớn; nội dung chính vẫn hiện khi tính năng phụ (video, hiệu ứng) không chạy (Frain, 2020).",
        "**Marketing khan hiếm (scarcity):** sản phẩm giới hạn về số lượng hoặc thời gian được cảm nhận giá trị cao hơn "
        "(Ha, 2021); áp dụng qua drop có ngày ra mắt và cổng truy cập riêng.",
        "**Hồi quy tuyến tính bội:** ước lượng vòng ngực từ cân nặng và chiều cao, `ngực = a + b × kg + c × cm`, các hệ "
        "số tìm bằng bình phương tối thiểu trên dữ liệu ANSUR II, tách riêng nam và nữ.",
        "**Quy ước đặt tên BEM (Block - Element - Modifier):** ví dụ `.cart-item__price`, `.btn--small`, giúp CSS chia "
        "mô-đun, dễ đọc và ít xung đột.",
    ])
