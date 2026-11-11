# -*- coding: utf-8 -*-
"""PHẦN B - CHƯƠNG 1. LÝ THUYẾT VÀ ỨNG DỤNG"""


def build(R, ctx):
    R.part_heading("B", "XÂY DỰNG VÀ PHÁT TRIỂN WEBSITE")
    R.chapter(1, "LÝ THUYẾT VÀ ỨNG DỤNG")
    R.p("Chương này trình bày các khái niệm, công nghệ của học phần và cách nhóm áp dụng chúng vào website SANCTUARY. Mỗi "
        "mục gồm phần lý thuyết và phần ứng dụng trong đồ án, kèm tên file mã nguồn để tiện đối chiếu.")

    R.h3("1.1. Internet, mô hình client/server và hệ thống web")
    R.h4("1.1.1. Khái niệm")
    R.ps(
        "**Internet** là mạng máy tính toàn cầu kết nối các mạng nhỏ hơn bằng bộ giao thức TCP/IP. Mỗi thiết bị có một **địa "
        "chỉ IP**; vì địa chỉ số khó nhớ nên người dùng truy cập qua **tên miền**, hệ thống DNS đổi tên miền thành địa chỉ IP. "
        "**World Wide Web** là dịch vụ trên Internet gồm các tài liệu siêu văn bản liên kết với nhau, truyền bằng giao thức "
        "**HTTP**; **HTTPS** là HTTP được mã hoá bằng TLS để chống nghe lén và giả mạo.",
        "Web hoạt động theo **mô hình client/server**: trình duyệt (client) gửi yêu cầu HTTP, **web server** tìm tài nguyên "
        "(HTML, CSS, JavaScript, ảnh, dữ liệu) hoặc chạy chương trình để tạo nội dung rồi trả phản hồi kèm mã trạng thái (200 "
        "thành công, 404 không tìm thấy...). **Trình duyệt** phân tích HTML thành cây DOM, áp CSS, chạy JavaScript và vẽ trang. "
        "Theo cách tạo nội dung, có **web tĩnh** (máy chủ trả file có sẵn) và **web động** (máy chủ sinh nội dung theo yêu cầu, "
        "thường kèm cơ sở dữ liệu). Website TMĐT gồm phần **front-end** (giao diện, chạy trên trình duyệt) và **back-end** (xử "
        "lý, lưu trữ trên máy chủ), phục vụ hai nhóm người dùng là **khách hàng** và **quản trị viên**.")
    R.table(["Tiêu chí", "Web tĩnh (SANCTUARY)", "Web động (ví dụ WooCommerce)"], [
        ("Nội dung", "File có sẵn; JavaScript tạo giao diện động trên trình duyệt", "Máy chủ sinh HTML theo từng yêu cầu"),
        ("Dữ liệu", "File JSON/XML + Web Storage của trình duyệt", "Cơ sở dữ liệu trên máy chủ (MySQL...)"),
        ("Hosting", "CDN tĩnh, miễn phí (Vercel)", "Cần máy chủ chạy PHP/Node, có chi phí"),
        ("Tốc độ", "Nhanh, file được phân phối qua CDN", "Phụ thuộc máy chủ và truy vấn CSDL"),
        ("Bảo mật nghiệp vụ", "Mô phỏng phía máy khách", "Xử lý, xác thực ở máy chủ"),
        ("Dữ liệu dùng chung", "Không (mỗi trình duyệt một bản)", "Có (mọi người dùng chung CSDL)"),
    ], widths=[3.4, 6.8, 6.8], caption="So sánh web tĩnh và web động", size=12, bold_first=True)
    R.h4("1.1.2. Ứng dụng trong đồ án")
    R.p("SANCTUARY là web tĩnh về phía máy chủ nhưng *động về phía máy khách*: Vercel chỉ phục vụ file qua HTTPS, còn toàn bộ "
        "nghiệp vụ (lọc sản phẩm, tính tiền, lưu đơn hàng) chạy bằng JavaScript trong trình duyệt. Website có cả phía khách hàng "
        "(6 trang) và phía quản trị (`pages/admin.html`). Cách làm này phù hợp phạm vi học phần, triển khai miễn phí, nhưng tạo "
        "ra giới hạn về bảo mật và đồng bộ dữ liệu được phân tích ở Phần C.")

    R.h3("1.2. Ngôn ngữ HTML5")
    R.h4("1.2.1. Khái niệm")
    R.p("HTML (HyperText Markup Language) mô tả cấu trúc và ý nghĩa nội dung bằng các thẻ. Tài liệu HTML5 bắt đầu bằng "
        "`<!DOCTYPE html>`, gồm `<head>` (bảng mã, viewport, tiêu đề, mô tả, liên kết CSS) và `<body>` (nội dung). HTML5 bổ sung "
        "các **thẻ phân vùng có ngữ nghĩa** như `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`, giúp trình "
        "duyệt, trình đọc màn hình và máy tìm kiếm hiểu vai trò từng vùng (Frain, 2020; WHATWG, n.d.).")
    R.h4("1.2.2. Ứng dụng trong đồ án")
    R.table(["Nhóm thẻ", "Thẻ tiêu biểu", "Chỗ dùng trong SANCTUARY"], [
        ("Tiêu đề", "h1 - h3", "Tiêu đề trang, tên khu sản phẩm, tên sản phẩm trong popup"),
        ("Phân vùng", "header, nav, main, section, article, footer", "Khung chung của cả 7 trang"),
        ("Hình ảnh, đa phương tiện", "img (width, height, loading=\"lazy\"), video (poster)", "Ảnh sản phẩm WebP, lookbook, video hero"),
        ("Danh sách", "ul, ol, li, dl/dt/dd", "Giỏ hàng, thông số sản phẩm, câu hỏi nhanh"),
        ("Liên kết", "a (href, #mục)", "Menu, chuyển tab trang Info bằng #shipping, #privacy"),
        ("Bảng", "table, thead, tbody, th scope", "Bảng size, các bảng của trang quản trị"),
        ("Khung nhúng", "iframe", "Bản đồ Google Maps (địa chỉ UEL) ở tab Contact"),
        ("Biểu mẫu", "form, label, input, select, textarea, button", "Cổng, thanh toán, liên hệ, đăng ký, tài khoản, quản trị"),
        ("Hộp thoại", "dialog (showModal)", "Popup sản phẩm, popup đánh giá, popup đăng nhập"),
        ("Thẻ meta", "meta charset, viewport, description", "Mọi trang; description phục vụ SEO"),
    ], widths=[3.3, 6.0, 7.7], caption="Các nhóm thẻ HTML5 và nơi áp dụng", size=12)

    R.h3("1.3. CSS3, mô hình hộp và thiết kế web đáp ứng")
    R.h4("1.3.1. Khái niệm")
    R.ps(
        "CSS định dạng cách hiển thị của phần tử HTML. Một luật CSS gồm **selector** (theo thẻ, lớp `.btn`, id `#cart`, thuộc "
        "tính `[hidden]`, quan hệ cha con, giả lớp `:hover`) và các cặp **thuộc tính: giá trị**. Khi nhiều luật cùng áp vào một "
        "phần tử, trình duyệt chọn theo thứ tự ưu tiên (cascade) và độ đặc hiệu (specificity) (Grant, 2024).",
        "Theo **mô hình hộp (box model)**, mỗi phần tử gồm nội dung, padding, border và margin. **Reset CSS** xoá các kiểu mặc "
        "định khác nhau giữa trình duyệt; **normalize** chỉ sửa chỗ không thống nhất. CSS3 có Flexbox (bố cục một chiều), Grid "
        "(hai chiều), biến CSS, `transition`, `filter`, `aspect-ratio`. **Thiết kế web đáp ứng** gồm bố cục linh hoạt, ảnh co "
        "giãn và truy vấn phương tiện (media query) (Frain, 2020).")
    R.h4("1.3.2. Ứng dụng trong đồ án")
    R.bullets([
        "CSS chia 5 file theo vai trò: `reset.css` (đặt `box-sizing: border-box`, xoá lề mặc định), `base.css` (biến màu, phông), `components.css` (nút, ô nhập), `pages.css` (từng trang), `admin.css`.",
        "Viết theo hướng **mobile-first**: lưới sản phẩm mặc định 2 cột, `@media (min-width: 768px)` thành 3 cột, `@media (min-width: 1024px)` thành 4 cột; toàn bộ dự án có khoảng 50 media query.",
        "Đặt tên lớp theo quy ước **BEM** (Block - Element - Modifier), ví dụ `.cart-item__price`, `.btn--small`.",
        "Dùng `filter` để tô tối bản đồ nhúng, `aspect-ratio` giữ tỉ lệ khung bản đồ, `prefers-reduced-motion` tắt hiệu ứng cho người dùng nhạy cảm chuyển động.",
    ])

    R.h3("1.4. Bộ tiền xử lý LESS và CSS framework")
    R.h4("1.4.1. Khái niệm")
    R.p("**LESS** là bộ tiền xử lý CSS, bổ sung biến (`@ten-bien`), lồng selector (`&:hover`), mixin (nhóm thuộc tính có tham "
        "số) và hàm; file `.less` phải được biên dịch ra `.css` trước khi trình duyệt dùng (Less.js, n.d.). Biến LESS chỉ tồn tại "
        "lúc biên dịch, khác biến CSS tồn tại lúc chạy. **CSS framework** như Bootstrap hay Tailwind CSS cung cấp sẵn lưới và "
        "thành phần giao diện giúp làm nhanh (Bootstrap Team, n.d.; Tailwind Labs, n.d.).")
    R.h4("1.4.2. Ứng dụng trong đồ án")
    R.p("File `css/less/components.less` dùng biến, lồng selector và mixin có tham số; lệnh `npm run build:css` biên dịch nó "
        "thành `css/components.css`. Nhóm không dùng CSS framework vì giao diện SANCTUARY mang tính thương hiệu cao, sẽ phải ghi "
        "đè rất nhiều kiểu mặc định, đồng thời viết CSS thuần thể hiện rõ hơn kiến thức của học phần.")
    R.code("""@btn-border-color: #333;                   // biến LESS
.smooth(@props) { transition: @props; }    // mixin có tham số
.btn {
  border: 3px solid @btn-border-color;
  .smooth(background 0.2s, color 0.2s, border-color 0.2s;);
  &:hover { background: var(--color-accent); color: #000; }   // -> .btn:hover
  &--small { padding: 0.5rem 1rem; }                           // -> .btn--small
}""", caption="Trích css/less/components.less:")
    R.table(["Tiêu chí", "CSS thuần + LESS (nhóm chọn)", "Bootstrap", "Tailwind CSS"], [
        ("Cách dùng", "Tự viết lớp theo BEM", "Dùng lớp, thành phần có sẵn", "Ghép nhiều lớp tiện ích nhỏ"),
        ("Dung lượng tải", "Chỉ chứa phần web dùng", "Lớn nếu không lọc bớt", "Nhỏ nếu có bước build lọc lớp"),
        ("Giao diện riêng", "Hoàn toàn chủ động", "Dễ giống nhau, phải ghi đè", "Chủ động nhưng HTML dài"),
        ("Giá trị học tập", "Thể hiện rõ selector, box model, media query", "Ít viết CSS", "Ít viết CSS truyền thống"),
    ], widths=[3.2, 4.8, 4.5, 4.5], caption="So sánh CSS thuần với hai CSS framework phổ biến", size=12)

    R.h3("1.5. Ngôn ngữ JavaScript")
    R.h4("1.5.1. Khái niệm")
    R.p("JavaScript là ngôn ngữ lập trình chạy trong trình duyệt, giúp trang phản hồi thao tác của người dùng. Mã có thể nhúng "
        "trong thẻ `<script>` hoặc để ở file riêng; **ES modules** (`<script type=\"module\">`, `import`/`export`) cho phép chia "
        "mã thành nhiều file nhỏ. Ngôn ngữ gồm biến, kiểu dữ liệu, toán tử, cấu trúc điều khiển, hàm, đối tượng và cơ chế bất "
        "đồng bộ Promise/async-await (Haverbeke, 2024).")
    R.h4("1.5.2. Ứng dụng trong đồ án")
    R.table(["Khái niệm", "Ví dụ trong SANCTUARY"], [
        ("Biến, kiểu dữ liệu", "`const CART_KEY = \"sanctuary_cart\"` (chuỗi); giá, số lượng (số); mảng giỏ hàng; object sản phẩm"),
        ("Toán tử", "Tạm tính `p.price * item.qty`; so sánh `===`; toán tử ba ngôi chọn nhãn thuế"),
        ("Cấu trúc điều khiển", "`if/else` kiểm tra mã cổng; vòng `for` của thuật toán Luhn; `forEach` vẽ danh sách"),
        ("Hàm", "`calcCosts()` tính phí ship, thuế; `recommendSize()` gợi ý size; hàm mũi tên xử lý sự kiện"),
        ("Đối tượng", "Object luật kiểm tra form `rules`; object đơn hàng; `Set` lọc trùng mã đơn, loại sản phẩm"),
        ("Bất đồng bộ", "`Promise`, `async/await` khi tải JSON, XML và băm SHA-256"),
        ("Mô-đun", str(ctx["js_files"]) + " file ES module, mỗi file một nhiệm vụ (giỏ hàng, tiền tệ, xác thực, quản trị...)"),
    ], widths=[4.0, 13.0], caption="Các khái niệm JavaScript và ví dụ áp dụng", size=12)

    R.h3("1.6. Mô hình DOM và xử lý sự kiện")
    R.h4("1.6.1. Khái niệm")
    R.p("**DOM** (Document Object Model) biểu diễn trang HTML thành cây đối tượng mà JavaScript đọc và sửa được: tìm phần tử "
        "(`getElementById`, `querySelector`), tạo và gắn phần tử (`createElement`, `append`), đổi nội dung, thuộc tính "
        "(`textContent`, `setAttribute`, `classList`, `dataset`). **Xử lý sự kiện** dùng `addEventListener(sự_kiện, hàm)` để chạy "
        "mã khi người dùng bấm, gõ, gửi form, cuộn trang.")
    R.h4("1.6.2. Ứng dụng trong đồ án")
    R.p("Phần lớn giao diện động được vẽ bằng DOM: thẻ sản phẩm, popup chi tiết, bảng size, giỏ hàng, các bảng quản trị. Dữ "
        "liệu người dùng nhập luôn được ghi bằng `textContent` thay vì `innerHTML` để tránh chèn mã độc (XSS). Các sự kiện được "
        "dùng: `click`, `submit` (kèm `preventDefault()`), `input` và `change` (kiểm tra ô nhập khi gõ, đổi bộ lọc), `keydown` "
        "(Enter, Escape), `scroll` (hiện nút cạnh trang), `storage` và sự kiện tự tạo `auth-change` (đồng bộ trạng thái đăng nhập).")
    R.code("""// Tạo 1 thẻ sản phẩm bằng DOM (js/products.js, rút gọn)
const card = document.createElement("article");
card.className = "product-card";
card.tabIndex = 0;                          // bấm được bằng bàn phím
card.setAttribute("role", "button");
card.addEventListener("click", () => onOpen(product));
card.addEventListener("keydown", (e) => {
  if (e.key === "Enter" || e.key === " ") { e.preventDefault(); onOpen(product); }
});""", caption="Tạo phần tử và gắn sự kiện bằng DOM:")

    R.h3("1.7. XML, JSON và AJAX")
    R.h4("1.7.1. Khái niệm")
    R.ps(
        "**XML** (eXtensible Markup Language) là ngôn ngữ đánh dấu do người dùng tự đặt tên thẻ, dùng để lưu và trao đổi dữ liệu "
        "có cấu trúc; tài liệu phải *well-formed* (một phần tử gốc, thẻ đóng mở đúng). **JSON** là định dạng dữ liệu dựa trên cú "
        "pháp object của JavaScript, gọn hơn XML và đọc trực tiếp thành object.",
        "**AJAX** là kỹ thuật dùng JavaScript gửi yêu cầu HTTP bất đồng bộ và cập nhật một phần trang mà không tải lại. Cách cổ "
        "điển dùng `XMLHttpRequest` (`open`, `send`, sự kiện `onload`; với XML, `responseXML` trả về sẵn cây DOM); cách hiện đại "
        "dùng hàm `fetch()` trả về Promise (MDN Web Docs, n.d.-a).")
    R.h4("1.7.2. Ứng dụng trong đồ án")
    R.p("SANCTUARY dùng **cả hai cách** để so sánh: sản phẩm, đánh giá, mã athlete, bảng size là JSON đọc bằng `fetch`; bảng phí "
        "vận chuyển và thuế `data/shipping.xml` đọc bằng `XMLHttpRequest`, sau đó duyệt cây DOM của XML bằng `getElementsByTagName`, "
        "`getAttribute`. Tỷ giá lấy từ API JSON open.er-api.com (ExchangeRate-API, n.d.).")
    R.code("""export function loadShipping() {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "../data/shipping.xml");
    xhr.onload = () => {
      if (xhr.status === 200 && xhr.responseXML) resolve(parseShippingXml(xhr.responseXML));
      else reject(new Error("Cannot load shipping data (status " + xhr.status + ")"));
    };
    xhr.onerror = () => reject(new Error("Network error while loading shipping data"));
    xhr.send();
  });
}""", caption="Đọc XML bằng AJAX trong js/shipping.js:")
    R.table(["Tiêu chí", "XML + XMLHttpRequest", "JSON + fetch"], [
        ("Cú pháp", "Thẻ mở/đóng, thuộc tính, chú thích", "Cặp khoá: giá trị, mảng, gọn hơn"),
        ("Đọc dữ liệu", "Duyệt DOM: getElementsByTagName, getAttribute", "response.json() ra object ngay"),
        ("Kiểu dữ liệu", "Mọi giá trị là chuỗi, phải tự đổi sang số", "Có sẵn số, chuỗi, logic, mảng"),
        ("Mô hình lập trình", "Hàm callback (onload, onerror)", "Promise, async/await"),
        ("Dùng trong đồ án", "data/shipping.xml (6 vùng, 15 nước)", "products, reviews, access, size-chart"),
    ], widths=[3.4, 6.8, 6.8], caption="So sánh XML/XMLHttpRequest và JSON/fetch", size=12)

    R.h3("1.8. Lưu trữ phía trình duyệt (Web Storage)")
    R.h4("1.8.1. Khái niệm")
    R.p("**Web Storage** cho phép lưu cặp khoá - chuỗi trong trình duyệt: `localStorage` giữ lại sau khi tắt trình duyệt, "
        "`sessionStorage` mất khi đóng tab; dung lượng khoảng 5 MB mỗi nguồn và chỉ lưu chuỗi, nên object phải đổi bằng "
        "`JSON.stringify`/`JSON.parse` (MDN Web Docs, n.d.-b).")
    R.h4("1.8.2. Ứng dụng trong đồ án")
    R.p("Vì không có máy chủ, SANCTUARY dùng `localStorage` làm “cơ sở dữ liệu” phía trình duyệt cho giỏ hàng, đơn hàng, tài "
        "khoản, tin nhắn và thay đổi của quản trị viên; vai trò sau khi qua cổng lưu trong `sessionStorage`. File `js/storage.js` "
        "đọc dữ liệu có kiểm tra cấu trúc (bỏ qua bản ghi hỏng) và có hàm `writeAll()` ghi nhiều khoá cùng lúc, lỗi giữa chừng "
        "thì hoàn tác, mô phỏng transaction của cơ sở dữ liệu.")

    R.h3("1.9. Web Crypto API")
    R.h4("1.9.1. Khái niệm")
    R.p("**Web Crypto API** cung cấp hàm mật mã chạy trong trình duyệt. `crypto.subtle.digest(\"SHA-256\", ...)` tạo **giá trị "
        "băm** 256 bit: cùng đầu vào luôn ra cùng kết quả nhưng không suy ngược được đầu vào. **Salt** là chuỗi ngẫu nhiên ghép "
        "vào mật khẩu trước khi băm để hai người cùng mật khẩu có hai giá trị băm khác nhau (MDN Web Docs, n.d.-c).")
    R.h4("1.9.2. Ứng dụng trong đồ án")
    R.p("Mã quản trị không lưu dạng chữ trong mã nguồn mà chỉ lưu giá trị băm SHA-256 (`js/config.js`); khi nhập, trình duyệt "
        "băm chuỗi vừa nhập rồi so sánh. Mật khẩu tài khoản được băm cùng salt 16 byte ngẫu nhiên (`crypto.getRandomValues`) "
        "riêng cho từng tài khoản (`js/auth.js`); đăng nhập sai email hay sai mật khẩu đều báo chung một câu để không lộ email "
        "nào đã đăng ký.")

    R.h3("1.10. Python và dữ liệu số đo cơ thể ANSUR II")
    R.h4("1.10.1. Khái niệm")
    R.p("**ANSUR II** là bộ số đo cơ thể công khai của quân đội Mỹ (2012), gồm hơn 6.000 người với hàng trăm số đo (Gordon và "
        "cộng sự, 2014). **Hồi quy tuyến tính bội** ước lượng một đại lượng từ nhiều biến bằng phương pháp bình phương tối "
        "thiểu, dạng `y = a + b·x1 + c·x2`.")
    R.h4("1.10.2. Ứng dụng trong đồ án")
    sc = ctx["size_chart"]
    R.p("Script `tools/build_size_chart.py` (Python) học công thức vòng ngực theo cân nặng và chiều cao, tách riêng nam ("
        + "{:,}".format(sc["him"]["sampleSize"]).replace(",", ".") + " người) và nữ (" + "{:,}".format(sc["her"]["sampleSize"]).replace(",", ".") +
        " người), rồi tính bảng size (vòng ngực, eo, chiều cao, cân nặng của từng size) và ghi ra `data/size-chart.json`. Các script "
        "Python khác dùng để thu thập và chuẩn hoá dữ liệu mẫu, đổi ảnh sang WebP và nén video.")

    R.h3("1.11. Vercel, GitHub và quy trình triển khai")
    R.h4("1.11.1. Khái niệm")
    R.p("**Git** quản lý phiên bản mã nguồn; **GitHub** lưu trữ kho mã trực tuyến. **Vercel** là nền tảng hosting cho web tĩnh "
        "và ứng dụng front-end, có CDN toàn cầu, HTTPS mặc định và tự động triển khai khi kho mã có commit mới (CI/CD) (Vercel, n.d.).")
    R.h4("1.11.2. Ứng dụng trong đồ án")
    R.p("Kho mã `thaikhuonganhduc/sanctuarydivinity` trên GitHub được liên kết với Vercel; mỗi lần đẩy commit lên nhánh `main`, "
        "website tại sanctuarydivinity.vercel.app được cập nhật sau khoảng 20 giây. Tệp `vercel.json` chuyển hướng `/` sang "
        "`/password` (trang cổng). Mỗi tính năng là một commit có thông điệp rõ ràng, làm bằng chứng tiến độ.")

    R.h3("1.12. Nền tảng thương mại điện tử mã nguồn mở")
    R.h4("1.12.1. Khái niệm")
    R.p("Nền tảng TMĐT mã nguồn mở cho phép tải về miễn phí, cài lên hosting riêng, mở rộng bằng plugin/module và đổi giao "
        "diện bằng theme. Ba nền tảng trong đề cương là Adobe Commerce (bản mã nguồn mở là Magento Open Source), PrestaShop và "
        "WooCommerce (WooCommerce, n.d.).")
    R.table(["Tiêu chí", "Adobe Commerce / Magento", "PrestaShop", "WooCommerce"], [
        ("Kiến trúc", "Ứng dụng PHP độc lập, mô-đun hoá cao", "Ứng dụng PHP độc lập, có module", "Plugin chạy trên WordPress"),
        ("Yêu cầu hạ tầng", "Cao, cấu hình phức tạp", "Trung bình", "Thấp, hosting WordPress thông thường"),
        ("Phù hợp", "Doanh nghiệp lớn, nhiều cửa hàng", "Cửa hàng vừa, đa quốc gia", "Cửa hàng nhỏ và vừa"),
        ("Tùy biến giao diện", "Theme + layout XML", "Theme + module", "Theme (Storefront), Customizer"),
    ], widths=[3.2, 4.8, 4.2, 4.8], caption="So sánh ba nền tảng thương mại điện tử mã nguồn mở", size=12)
    R.h4("1.12.2. Ứng dụng trong đồ án")
    R.p("Nhóm chọn WooCommerce để cài thử vì nhẹ nhất, chạy được trên máy cá nhân bằng WordPress Playground, và mô hình sản "
        "phẩm có biến thể (size, màu) tương đồng dữ liệu của SANCTUARY. Quá trình cài đặt và quản trị trình bày ở Chương 8.")

    R.h3("1.13. Tối ưu hiệu năng web và Core Web Vitals")
    R.h4("1.13.1. Khái niệm")
    R.p("**Core Web Vitals** là bộ chỉ số trải nghiệm do Google đề xuất: **LCP** (thời điểm hiện phần nội dung lớn nhất, tốt khi "
        "≤ 2,5 s), **CLS** (mức dịch chuyển bố cục, tốt khi ≤ 0,1) và **INP** (độ trễ phản hồi thao tác, tốt khi ≤ 200 ms) (Google, "
        "n.d.). **Lighthouse** đo trong môi trường mô phỏng và chấm điểm 0 - 100 cho bốn nhóm Performance, Accessibility, Best "
        "Practices, SEO; khi đo thử nghiệm, TBT (tổng thời gian chặn luồng chính) dùng thay cho INP (Chrome for Developers, n.d.). "
        "Các kỹ thuật tối ưu phổ biến gồm nén ảnh theo định dạng mới (WebP), tải lười ảnh ngoài màn hình, khai báo kích thước ảnh "
        "để trình duyệt giữ chỗ, nén video và giảm mã JavaScript chặn hiển thị.")
    R.h4("1.13.2. Ứng dụng trong đồ án")
    R.bullets([
        "Ảnh sản phẩm, đánh giá, lookbook đổi sang WebP bằng script Python; video nén H.264 (CRF 20); tổng dung lượng giảm khoảng 70%.",
        "Ảnh dùng `loading=\"lazy\"`; ảnh lookbook khai báo `width`/`height` thật để trình duyệt giữ chỗ, tránh xô lệch bố cục.",
        "JavaScript dạng module tải sau khi phân tích HTML; dữ liệu dùng chung (bảng size, tỷ giá) chỉ tải một lần.",
        "Đo Lighthouse trên bản triển khai trước và sau khi sửa để chứng minh hiệu quả (Phần C, mục 1.5.2).",
    ])
    R.h3("1.14. Khả năng truy cập web (WCAG)")
    R.h4("1.14.1. Khái niệm")
    R.p("**WCAG 2.2** là chuẩn của W3C về khả năng truy cập nội dung web, xếp theo bốn nguyên tắc: nhận biết được, thao tác được, "
        "hiểu được và bền vững; mỗi tiêu chí có mức A, AA, AAA (W3C, 2023). Nghiên cứu trên 50 website thương mại điện tử xếp hạng "
        "cao cho thấy lỗi tương phản màu là lỗi phổ biến nhất, và nguyên tắc “nhận biết được” bị vi phạm nhiều nhất "
        "(Acosta-Vargas và cộng sự, 2022).")
    R.h4("1.14.2. Ứng dụng trong đồ án")
    R.bullets([
        "HTML có ngữ nghĩa, mỗi ô nhập có `label`; lỗi form ghi bằng chữ ngay dưới ô, thông báo lỗi chung có `role=\"alert\"` để trình đọc màn hình đọc ngay.",
        "Thẻ sản phẩm, nút màu, size, menu, popup điều khiển được bằng bàn phím; Esc đóng popup; tên đọc của thẻ sản phẩm lấy từ chữ hiển thị (tiêu chí 2.5.3 Label in Name).",
        "Chữ sáng trên nền đen bảo đảm độ tương phản; chữ phụ dùng màu xám đủ tương phản.",
        "Tôn trọng tuỳ chọn `prefers-reduced-motion`: dừng video nền, tắt hiệu ứng chuyển động.",
        "Trang Accessibility công bố cam kết, cách làm và hạn chế còn lại của website.",
    ])

    R.h3("1.15. Công cụ hỗ trợ")
    R.table(["Công cụ", "Mục đích"], [
        ("Visual Studio Code + Live Server", "Soạn mã, chạy thử trên máy (thống nhất trong lớp)"),
        ("draw.io", "Vẽ sơ đồ Use case, ERD, DFD, BPMN, lưu đồ, kiến trúc"),
        ("Node.js + less 4.2.0", "Biên dịch LESS ra CSS"),
        ("Python 3.12 (Pillow, imageio-ffmpeg)", "Thu thập dữ liệu mẫu, tính bảng size, đổi ảnh WebP, nén video"),
        ("Chrome DevTools, Google Lighthouse", "Gỡ lỗi; đo hiệu năng, khả năng truy cập, SEO (Chrome for Developers, n.d.)"),
        ("W3C Nu Html Checker", "Kiểm tra cú pháp HTML theo đặc tả (W3C, n.d.)"),
        ("Playwright", "Tự động thao tác trình duyệt để kiểm thử và chụp màn hình (Microsoft, n.d.)"),
        ("WordPress Playground", "Chạy WordPress + WooCommerce trên máy mà không cần XAMPP (WordPress.org, n.d.)"),
    ], widths=[6.0, 11.0], caption="Các công cụ hỗ trợ phát triển", size=12)
