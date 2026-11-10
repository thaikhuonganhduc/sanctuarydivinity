# -*- coding: utf-8 -*-
"""Tài liệu tham khảo (APA 7) và Phụ lục."""
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm

# Sắp theo thứ tự chữ cái của tác giả. Mọi tài liệu đều đã được kiểm tra là có thật.
REFERENCES = [
    "Acosta-Vargas, P., Salvador-Acosta, B., Salvador-Ullauri, L., & Jadán-Guerrero, J. (2022). Accessibility challenges of e-commerce websites. *PeerJ Computer Science, 8*, e891. https://doi.org/10.7717/peerj-cs.891",
    "Bootstrap Team. (n.d.). *Bootstrap documentation*. Truy cập ngày 11/11/2026, từ https://getbootstrap.com/docs/",
    "Breathe Divinity. (n.d.). *Breathe Divinity* [Website]. Truy cập ngày 11/11/2026, từ https://breathedivinity.com",
    "Chatterjee, O., Tej, J. R., & Dasaraju, N. V. (2022). Incorporating customer reviews in size and fit recommendation systems for fashion e-commerce. *Proceedings of the SIGIR 2022 Workshop on eCommerce (SIGIR eCom'22)*. https://arxiv.org/abs/2208.06261",
    "Chrome for Developers. (n.d.). *Introduction to Lighthouse*. Google. Truy cập ngày 11/11/2026, từ https://developer.chrome.com/docs/lighthouse/overview",
    "ExchangeRate-API. (n.d.). *Free & open access exchange rate API*. Truy cập ngày 11/11/2026, từ https://www.exchangerate-api.com/docs/free",
    "Frain, B. (2020). *Responsive web design with HTML5 and CSS* (3rd ed.). Packt Publishing.",
    "Google. (n.d.). *Web Vitals*. web.dev. Truy cập ngày 11/11/2026, từ https://web.dev/articles/vitals",
    "Google, Temasek, & Bain & Company. (2024). *e-Conomy SEA 2024: Profits on the rise, harnessing SEA's advantage*. https://www.bain.com/insights/e-conomy-sea-2024/",
    "Gordon, C. C., Blackwell, C. L., Bradtmiller, B., Parham, J. L., Barrientos, P., Paquette, S. P., Corner, B. D., Carson, J. M., Venezia, J. C., Rockwell, B. M., Mucher, M., & Kristensen, S. (2014). *2012 anthropometric survey of U.S. Army personnel: Methods and summary statistics* (Technical Report NATICK/TR-15/007). U.S. Army Natick Soldier Research, Development and Engineering Center. https://apps.dtic.mil/sti/pdfs/ADA611869.pdf",
    "Grant, K. J. (2024). *CSS in depth* (2nd ed.). Manning Publications.",
    "Ha, T. M. (2021). The impact of product characteristics of limited-edition shoes on perceived value, brand trust and purchase intention. *Cogent Business & Management, 8*(1), 1953680. https://doi.org/10.1080/23311975.2021.1953680",
    "Haverbeke, M. (2024). *Eloquent JavaScript* (4th ed.). No Starch Press. https://eloquentjavascript.net/",
    "Less.js. (n.d.). *Getting started*. Truy cập ngày 11/11/2026, từ https://lesscss.org/",
    "MDN Web Docs. (n.d.-a). *XMLHttpRequest*. Mozilla. Truy cập ngày 11/11/2026, từ https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest",
    "MDN Web Docs. (n.d.-b). *Web Storage API*. Mozilla. Truy cập ngày 11/11/2026, từ https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API",
    "MDN Web Docs. (n.d.-c). *SubtleCrypto: digest() method*. Mozilla. Truy cập ngày 11/11/2026, từ https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/digest",
    "Microsoft. (n.d.). *Playwright documentation*. Truy cập ngày 11/11/2026, từ https://playwright.dev/docs/intro",
    "OWASP Foundation. (2021). *OWASP Top 10:2021*. https://owasp.org/Top10/",
    "Stöcker, B., Baier, D., & Brand, B. M. (2021). New insights in online fashion retail returns from a customers' perspective and their dynamics. *Journal of Business Economics, 91*(8), 1149-1187. https://doi.org/10.1007/s11573-021-01032-1",
    "Tailwind Labs. (n.d.). *Tailwind CSS documentation*. Truy cập ngày 11/11/2026, từ https://tailwindcss.com/docs",
    "Vercel. (n.d.). *Vercel documentation*. Truy cập ngày 11/11/2026, từ https://vercel.com/docs",
    "W3C. (2023). *Web Content Accessibility Guidelines (WCAG) 2.2* (W3C Recommendation). https://www.w3.org/TR/WCAG22/",
    "W3C. (n.d.). *Nu Html Checker*. Truy cập ngày 11/11/2026, từ https://validator.w3.org/nu/",
    "WHATWG. (n.d.). *HTML living standard*. Truy cập ngày 11/11/2026, từ https://html.spec.whatwg.org/",
    "WooCommerce. (n.d.). *WooCommerce documentation*. Automattic. Truy cập ngày 11/11/2026, từ https://woocommerce.com/documentation/",
    "WordPress.org. (n.d.). *WordPress Playground documentation*. Truy cập ngày 11/11/2026, từ https://wordpress.github.io/wordpress-playground/",
]


def build(R, ctx):
    D = ctx["diag"]
    # ---------- Tài liệu tham khảo ----------
    R.h1("TÀI LIỆU THAM KHẢO", chapter="TL")
    R.p("Tài liệu trình bày theo chuẩn APA (ấn bản 7), sắp xếp theo thứ tự chữ cái của tác giả.", indent=False, italic=True)
    for ref in REFERENCES:
        p = R.p(ref, indent=False, after=6, align=WD_ALIGN_PARAGRAPH.LEFT)   # căn trái: URL dài không làm giãn chữ
        p.paragraph_format.left_indent = Cm(1.27)
        p.paragraph_format.first_line_indent = Cm(-1.27)      # thụt treo theo APA
        p.paragraph_format.line_spacing = 1.3

    # ---------- Phụ lục ----------
    R.h1("PHỤ LỤC", chapter="PL")
    R.h2("Phụ lục A. Liên kết và hướng dẫn truy cập")
    R.table(["Nội dung", "Liên kết / cách dùng"], [
        ("Website (bản triển khai)", "https://sanctuarydivinity.vercel.app"),
        ("Mã nguồn (GitHub, công khai)", "https://github.com/thaikhuonganhduc/sanctuarydivinity"),
        ("Mã vào cửa hàng (khách)", "SANCTUARY-DEMO: bấm “Enter using password” ở góc phải trang cổng rồi nhập mã"),
        ("Mã quản trị", "Nhóm gửi riêng cho giảng viên khi chấm, không ghi trong báo cáo vì lý do bảo mật"),
        ("Dữ liệu demo cho trang quản trị", "Admin → Backup → Add sample data (3 khách, 8 đơn, 3 tin nhắn); khách mẫu đăng nhập bằng mật khẩu Sanctuary1"),
        ("Chạy trên máy", "Mở thư mục dự án bằng VS Code, chuột phải index.html → Open with Live Server"),
        ("Biên dịch LESS", "npm install, rồi npm run build:css"),
        ("Bản cài thử WooCommerce", "Xem lệnh ở mục 4.6.1; tài khoản quản trị của bản cài thử: admin / password"),
        ("Sơ đồ (draw.io) và ảnh PNG", "docs/diagrams/*.drawio và docs/diagrams/png/"),
    ], widths=[4.6, 11.4], caption="Liên kết và thông tin truy cập", size=11, bold_first=True)

    R.h2("Phụ lục B. Chi tiết các ca kiểm thử chức năng")
    rows = []
    for t in ctx["tests"]:
        actual = t["actual"]
        if len(actual) > 150:
            actual = actual[:147] + "..."
        rows.append((t["id"], t["name"], t["expected"], actual, ("Đạt", "E2EFDA") if t["ok"] else ("Không đạt", "F8CBAD")))
    R.table(["Mã", "Ca kiểm thử", "Kết quả mong đợi", "Kết quả thực tế", "KQ"], rows,
            widths=[1.3, 3.8, 3.8, 5.6, 1.5], caption="Danh sách 41 ca kiểm thử chức năng (chạy ngày 11/11/2026)", size=9.5,
            center_cols=(0, 4))

    R.h2("Phụ lục C. Kết quả Lighthouse chi tiết")
    names = {"Gate": "Cổng", "Home": "Trang chủ", "Cart": "Giỏ hàng", "Info": "Info", "About": "About"}
    R.table(["Cấu hình", "Trang", "FCP", "LCP", "TBT", "CLS", "Speed Index", "Lỗi Accessibility / SEO còn lại"],
            [("Mobile" if r["mode"] == "mobile" else "Desktop", names[r["name"]], r["FCP"].replace(".", ","), r["LCP"].replace(".", ","),
              r["TBT"], r["CLS"].replace(".", ","), r["SI"].replace(".", ","),
              "; ".join(r["failedA11y"] + r["failedSeo"]) or "-") for r in ctx["lighthouse"]],
            widths=[1.7, 1.9, 1.3, 1.3, 1.3, 1.2, 1.6, 5.7], caption="Chỉ số thời gian của Lighthouse 13.5", size=9.5,
            center_cols=(2, 3, 4, 5, 6))

    R.h2("Phụ lục D. Các sơ đồ BPMN còn lại")
    for page, title in [(1, "Vào web qua cổng"), (2, "Đăng ký tài khoản"), (3, "Đăng nhập"), (4, "Thêm sản phẩm vào giỏ"),
                        (7, "Liên hệ"), (8, "Quản trị viên thêm sản phẩm")]:
        R.figure(D / ("04-bpmn-p%d.png" % page), "BPMN quy trình " + title.lower(), width=16)

    R.h2("Phụ lục E. Một số đoạn mã nguồn tiêu biểu")
    R.code("""<section class="contact-info" aria-label="Contact details">
  <h2 class="glass__title">Find us</h2>
  <div class="contact-map">
    <iframe src="https://www.google.com/maps?q=...&output=embed"
            title="Map: University of Economics and Law, Ho Chi Minh City"
            loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
  </div>
</section>""", caption="E.1. HTML semantic và iframe bản đồ (pages/contact.html, rút gọn):")
    R.code("""/* Mobile-first: mặc định 2 cột, màn hình lớn hơn thì thêm cột */
.product-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: var(--space-2); }
@media (min-width: 768px)  { .product-grid { grid-template-columns: repeat(3, 1fr); gap: var(--space-3); } }
@media (min-width: 1024px) { .product-grid { grid-template-columns: repeat(4, 1fr); } }""",
           caption="E.2. Lưới sản phẩm đáp ứng bằng CSS Grid và media query (css/pages.css):")
    R.code("""// Ghi nhiều khoá cùng lúc; lỗi giữa chừng thì trả lại giá trị cũ (mô phỏng transaction)
export function writeAll(entries) {
  let before;
  try { before = entries.map(([key]) => [key, localStorage.getItem(key)]); } catch (e) { return false; }
  try {
    entries.forEach(([key, value]) => {
      if (value === null) localStorage.removeItem(key);
      else localStorage.setItem(key, JSON.stringify(value));
    });
    return true;
  } catch (e) {
    before.forEach(([key, raw]) => {
      try { if (raw === null) localStorage.removeItem(key); else localStorage.setItem(key, raw); } catch (err) {}
    });
    return false;
  }
}""", caption="E.3. Ghi đơn hàng và tồn kho cùng lúc (js/storage.js):")
    R.code("""async function sha256(text) {
  const bytes = new TextEncoder().encode(text);
  const hash = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(hash)].map((b) => b.toString(16).padStart(2, "0")).join("");
}
export async function login(email, password) {
  const user = readUsers().find((u) => u.email === normalizeEmail(email));
  // Báo chung 1 câu cho cả 2 trường hợp, không để lộ email nào đã có tài khoản
  if (!user || (await sha256(user.salt + password)) !== user.passwordHash)
    throw new Error("Incorrect email or password.");
  localStorage.setItem(SESSION_KEY, user.email);
  return publicUser(user);
}""", caption="E.4. Băm mật khẩu kèm salt bằng Web Crypto API (js/auth.js):")
    R.code("""// Xử lý sự kiện: bấm nút hoặc nhấn Enter trong ô nhập thì tính size
calcBtn.addEventListener("click", calculate);
[heightInput, weightInput].forEach((i) =>
  i.addEventListener("keydown", (e) => { if (e.key === "Enter") calculate(); }));

// Ước lượng vòng ngực rồi tra mốc của bảng size
const chest = g.intercept + g.perKg * weightKg + g.perCm * heightCm;
let index = g.chestLimitsCm.findIndex((limit) => chest < limit);
if (index === -1) index = SIZES.length - 1;     // vượt mốc cuối -> XXL""",
           caption="E.5. Sự kiện DOM và thuật toán gợi ý size (js/product-popup.js, js/size-finder.js):")
