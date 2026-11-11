# -*- coding: utf-8 -*-
"""PHẦN C. TỔNG KẾT BÁO CÁO; TỔNG HỢP CÁC LINK; LỜI KẾT LUẬN; TÀI LIỆU THAM KHẢO"""
from collections import OrderedDict

from docx.shared import Cm, Pt
from docx_helpers import C, L

W3C = [  # (trang, lỗi trước, cảnh báo trước, nội dung, cách sửa, lỗi sau, cảnh báo sau) - đo 11/11/2026
    ("index.html", 1, 0, "aria-label trên thẻ div không có vai trò", "Bỏ aria-label, thêm dòng chữ ẩn cho trình đọc màn hình", 0, 0),
    ("pages/home.html", 0, 0, "-", "-", 0, 0),
    ("pages/cart.html", 2, 2, "autocomplete=\"street-address\" cho input một dòng; aria-label trên thẻ p; 2 section thiếu tiêu đề",
     "Đổi thành address-line1; thẻ p thành div role=\"group\"; section thông báo thành div", 0, 0),
    ("pages/contact.html", 0, 0, "-", "-", 0, 0),
    ("pages/about.html", 0, 0, "-", "-", 0, 0),
    ("pages/account.html", 1, 1, "autocomplete=\"street-address\"; 1 section thiếu tiêu đề", "Như trên", 0, 0),
    ("pages/admin.html", 1, 0, "Thẻ img xem trước ảnh chưa có src", "Thêm src giữ chỗ (ảnh GIF trong suốt 1×1)", 0, 0),
]

REFERENCES = [
    "Acosta-Vargas, P., Salvador-Acosta, B., Salvador-Ullauri, L., & Jadán-Guerrero, J. (2022). Accessibility challenges of e-commerce websites. *PeerJ Computer Science, 8*, e891. https://doi.org/10.7717/peerj-cs.891",
    "Bootstrap Team. (n.d.). *Bootstrap documentation*. Truy cập ngày 11/11/2026, từ https://getbootstrap.com/docs/",
    "Breathe Divinity. (n.d.). *Breathe Divinity* [Website]. Truy cập ngày 11/11/2026, từ https://breathedivinity.com",
    "Chatterjee, O., Tej, J. R., & Dasaraju, N. V. (2022). Incorporating customer reviews in size and fit recommendation systems for fashion e-commerce. *Proceedings of the SIGIR 2022 Workshop on eCommerce (SIGIR eCom'22)*. https://arxiv.org/abs/2208.06261",
    "Chrome for Developers. (n.d.). *Introduction to Lighthouse*. Google. Truy cập ngày 11/11/2026, từ https://developer.chrome.com/docs/lighthouse/overview",
    "Cốc Cốc. (2024). *Khám phá thị trường fitness qua xu hướng tập luyện và khả năng chi tiêu của người Việt*. Brands Vietnam. https://www.brandsvietnam.com/congdong/topic/339625-coc-coc-kham-pha-thi-truong-fitness-qua-xu-huong-tap-luyen-va-kha-nang-chi-tieu-cua-nguoi-viet",
    "ExchangeRate-API. (n.d.). *Free & open access exchange rate API*. Truy cập ngày 11/11/2026, từ https://www.exchangerate-api.com/docs/free",
    "FashionUnited. (2025, April 29). *Gymshark hits record revenue in FY24, yet profit continues to fall*. https://fashionunited.uk/news/business/gymshark-hits-record-revenue-in-fy24-yet-profit-continues-to-fall/2025042981343",
    "Frain, B. (2020). *Responsive web design with HTML5 and CSS* (3rd ed.). Packt Publishing.",
    "Google. (n.d.). *Web Vitals*. web.dev. Truy cập ngày 11/11/2026, từ https://web.dev/articles/vitals",
    "Google, Temasek, & Bain & Company. (2024). *e-Conomy SEA 2024: Profits on the rise, harnessing SEA's advantage*. https://www.bain.com/insights/e-conomy-sea-2024/",
    "Gordon, C. C., Blackwell, C. L., Bradtmiller, B., Parham, J. L., Barrientos, P., Paquette, S. P., Corner, B. D., Carson, J. M., Venezia, J. C., Rockwell, B. M., Mucher, M., & Kristensen, S. (2014). *2012 anthropometric survey of U.S. Army personnel: Methods and summary statistics* (Technical Report NATICK/TR-15/007). U.S. Army Natick Soldier Research, Development and Engineering Center. https://apps.dtic.mil/sti/pdfs/ADA611869.pdf",
    "Grant, K. J. (2024). *CSS in depth* (2nd ed.). Manning Publications.",
    "Ha, T. M. (2021). The impact of product characteristics of limited-edition shoes on perceived value, brand trust and purchase intention. *Cogent Business & Management, 8*(1), 1953680. https://doi.org/10.1080/23311975.2021.1953680",
    "Haverbeke, M. (2024). *Eloquent JavaScript* (4th ed.). No Starch Press. https://eloquentjavascript.net/",
    "IMARC Group. (n.d.). *Vietnam athleisure market report*. Truy cập ngày 11/11/2026, từ https://www.imarcgroup.com/vietnam-athleisure-market",
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


def vn(x):
    return str(x).replace(".", ",")


def kib(r):
    return r["weight"].replace("Total size was ", "").replace(",", ".")


def build(R, ctx):
    sc, lh, before, tests, online = ctx["size_chart"], ctx["lighthouse"], ctx["lighthouse_before"], ctx["tests"], ctx["tests_online"]
    pick = lambda data, mode, name: [r for r in data if r["mode"] == mode and r["name"] == name][0]
    names = {"Gate": "Cổng", "Home": "Trang chủ", "Cart": "Giỏ hàng", "Info": "Info", "About": "About"}
    passed = sum(t["ok"] for t in tests)
    hm, hf = sc["him"], sc["her"]
    desk = [r for r in lh if r["mode"] == "desktop"]

    R.part_heading("C", "TỔNG KẾT BÁO CÁO")
    # ======================= CHƯƠNG 1 =======================
    R.chapter(1, "TỔNG KẾT VÀ ĐÁNH GIÁ")
    R.h3("1.1. Kết quả đạt được")
    R.p("Sau 11 tuần, nhóm hoàn thành website SANCTUARY chạy trực tuyến tại https://sanctuarydivinity.vercel.app, bản cài thử "
        "WooCommerce, bộ tài liệu phân tích thiết kế và bộ kiểm thử tự động. " + R.next_tab() + " đối chiếu kết quả với các mục "
        "tiêu cụ thể đã đặt ở Phần A.")
    R.table(["Mục tiêu", "Kết quả", "Đánh giá"], [
        ("Mô phỏng mô hình drop: đếm ngược, mã athlete, mã giảm giá", "Trang cổng, kiểm tra mã bằng SHA-256, giảm 10%, quản lý mã trong admin", ("Đạt", "E2EFDA")),
        ("Duyệt, lọc, sắp xếp, đổi tiền tệ", str(ctx["n_products"]) + " sản phẩm, 3 khu, lọc size/màu, sắp xếp giá, 15 loại tiền tệ", ("Đạt", "E2EFDA")),
        ("Chi tiết sản phẩm, bảng size, gợi ý size", "Ảnh theo màu, bảng size cm/in, gợi ý size đúng " + vn(hm["exactSizePct"]) + "% (nam)", ("Đạt", "E2EFDA")),
        ("Giỏ hàng, thanh toán, phí ship và thuế", "Không vượt tồn kho, kiểm tra Luhn, phí và thuế theo 15 nước từ XML", ("Đạt", "E2EFDA")),
        ("Tài khoản thành viên", "Đăng ký, đăng nhập, hồ sơ, đổi mật khẩu, lịch sử đơn; mật khẩu băm kèm salt", ("Đạt", "E2EFDA")),
        ("Trang quản trị 8 chức năng", "Tổng quan, đơn, sản phẩm, khách, tin nhắn, mã athlete, ngày ra mắt, sao lưu", ("Đạt", "E2EFDA")),
        ("Đáp ứng mọi màn hình", "Không cuộn ngang ở 390, 820, 1440 px; lưới 2/3/4 cột", ("Đạt", "E2EFDA")),
        ("Kỹ thuật theo đề cương", "HTML5, CSS3, LESS, JavaScript, DOM, sự kiện, XML, AJAX, iframe", ("Đạt", "E2EFDA")),
        ("Chất lượng kỹ thuật", "Accessibility 100, SEO 100, W3C 0 lỗi, " + str(passed) + "/" + str(len(tests)) + " ca kiểm thử đạt", ("Đạt", "E2EFDA")),
        ("Cài đặt, quản trị mã nguồn mở", "WooCommerce 11.2: sản phẩm biến thể, đơn, khách, ship/thuế, giao diện", ("Đạt", "E2EFDA")),
    ], widths=[5.2, 9.4, 2.4], caption="Đối chiếu kết quả với mục tiêu", size=12, center_cols=(2,))

    R.h3("1.2. Ưu điểm")
    good = [
        ("Bao phủ đủ kiến thức học phần trên một sản phẩm thống nhất",
         "Website dùng HTML5 có ngữ nghĩa, biểu mẫu, bảng, khung nhúng; CSS3, box model, reset, LESS, thiết kế đáp ứng; JavaScript, "
         "DOM và xử lý sự kiện; XML và AJAX bằng cả `XMLHttpRequest` lẫn `fetch`; cài đặt nền tảng mã nguồn mở và có kế hoạch quản trị."),
        ("Mô phỏng trọn vẹn mô hình kinh doanh drop",
         "Đồng hồ đếm ngược, cổng truy cập bằng mã athlete, mã kiêm giảm giá để đo hiệu quả từng người giới thiệu, ngày ra mắt do "
         "quản trị viên điều chỉnh; giao diện và câu chuyện thương hiệu nhất quán từ trang cổng đến trang About."),
        ("Gợi ý size dựa trên dữ liệu thật",
         "Thay vì một bảng size tĩnh, website học công thức từ số đo của hơn 6.000 người (ANSUR II), lệch không quá một size với "
         + vn(hm["withinOneSizePct"]) + "% nam và " + vn(hf["withinOneSizePct"]) + "% nữ, giải quyết trực tiếp nguyên nhân trả hàng "
         "phổ biến của thời trang trực tuyến (Stöcker và cộng sự, 2021)."),
        ("Minh bạch chi phí cho khách quốc tế",
         "Phí vận chuyển theo khối lượng, thuế nhập khẩu và VAT/GST của 15 nước hiển thị trước khi đặt hàng; giá quy đổi 15 loại "
         "tiền tệ theo tỷ giá thật, có tỷ giá dự phòng khi mất mạng."),
        ("Chú trọng tính đúng của dữ liệu",
         "Không cho mua vượt tồn kho, kiểm tra lại giỏ lúc đặt hàng, ghi đơn và tồn kho cùng lúc có hoàn tác, đọc dữ liệu có kiểm "
         "tra cấu trúc nên dữ liệu hỏng không làm sập trang."),
        ("Khả năng truy cập và mã nguồn chuẩn",
         "Lighthouse Accessibility 100 trên mọi trang dù giao diện nền tối, trong khi lỗi tương phản là lỗi phổ biến nhất của "
         "website thương mại điện tử (Acosta-Vargas và cộng sự, 2022); mã HTML không còn lỗi theo W3C."),
        ("Trang quản trị đủ để vận hành",
         "Tám chức năng quản trị giúp một nhóm nhỏ tự vận hành cửa hàng, kể cả sao lưu, khôi phục và dữ liệu mẫu để thuyết trình."),
        ("Chi phí vận hành gần như bằng 0",
         "Web tĩnh trên gói miễn phí của Vercel, tự triển khai khi có commit mới, HTTPS và CDN mặc định."),
        ("Đánh giá bằng số liệu khách quan, lặp lại được",
         "Mọi kết quả trong báo cáo (kiểm thử, Lighthouse, W3C, độ chính xác gợi ý size) đều đo bằng công cụ và script nằm trong "
         "kho mã nguồn, ai cũng chạy lại được."),
    ]
    for i, (t, d) in enumerate(good, 1):
        R.h4("1.2.%d. %s" % (i, t))
        R.p(d)
    R.h3("1.3. Nhược điểm")
    bad = [
        ("Chưa có máy chủ và cơ sở dữ liệu thật",
         "Đơn hàng, tài khoản, thay đổi của quản trị viên chỉ nằm trong trình duyệt đang dùng; khách đặt hàng trên máy này thì quản "
         "trị viên trên máy khác không thấy. Việc chuyển dữ liệu phải qua file sao lưu."),
        ("Bảo mật chỉ ở mức mô phỏng",
         "Mọi mã JavaScript, kể cả giá trị băm của mã quản trị, đều xem được bằng công cụ của trình duyệt; `guard.js` chỉ chặn ở giao "
         "diện, người sửa sessionStorage vẫn vào được trang quản trị. Giá trị băm SHA-256 của mã ngắn có thể bị dò bằng từ điển."),
        ("Thanh toán mới mô phỏng luồng",
         "Website chỉ kiểm tra định dạng thẻ (Luhn, hạn, CVC), chưa kết nối cổng thanh toán và chưa gửi email xác nhận."),
        ("Hiệu năng trên điện thoại chưa tối ưu",
         "Trang chủ (video hero, khoảng " + kib(pick(lh, "mobile", "Home")) + ") có LCP " + vn(pick(lh, "mobile", "Home")["LCP"]) +
         " và trang About có LCP " + vn(pick(lh, "mobile", "About")["LCP"]) + " trên cấu hình điện thoại, chưa đạt ngưỡng 2,5 s; bản đồ nhúng làm trang Info nặng thêm khoảng 600 KB."),
        ("Chi tiết giao diện trên điện thoại",
         "Hai tab Armory và Reviews ở mép trái che một phần tên sản phẩm ở cột trái trên màn hình hẹp."),
        ("Dữ liệu mẫu lấy từ thương hiệu khác",
         "Phù hợp mục đích học tập nhưng không dùng được cho kinh doanh thật; các con số phí vận chuyển, thuế là ước tính."),
    ]
    for i, (t, d) in enumerate(bad, 1):
        R.h4("1.3.%d. %s" % (i, t))
        R.p(d)
    R.h3("1.4. Hướng phát triển")
    R.table(["STT", "Hạng mục", "Hướng phát triển"], [
        ("1", "Máy chủ và cơ sở dữ liệu", "- Thêm máy chủ (Node.js hoặc PHP) và cơ sở dữ liệu theo ERD đã thiết kế.\n- Tính giá, tồn kho, xác thực ở phía máy chủ."),
        ("2", "Thanh toán", "- Tích hợp cổng thanh toán trong nước (VNPay, MoMo) và quốc tế.\n- Gửi email xác nhận đơn, thông báo đổi trạng thái."),
        ("3", "Bảo mật", "- Băm mật khẩu chậm (bcrypt/Argon2), giới hạn số lần đăng nhập sai.\n- Thêm Content-Security-Policy; theo dõi danh sách OWASP Top 10."),
        ("4", "Gợi ý size", "- Kết hợp phản hồi “vừa/chật/rộng” trong đánh giá khi có lịch sử bán hàng (Chatterjee và cộng sự, 2022).\n- Gợi ý theo kiểu dáng từng sản phẩm."),
        ("5", "Hiệu năng", "- Ảnh poster nhẹ, tải video sau; bản video riêng cho điện thoại.\n- Chỉ tải bản đồ khi khách bấm “Show map”."),
        ("6", "Trải nghiệm", "- Dời tab Armory/Reviews trên điện thoại.\n- Danh sách yêu thích, thông báo khi có drop mới."),
        ("7", "Đo lường người dùng", "- Khảo sát, kiểm thử khả dụng với khách hàng mục tiêu.\n- Phân tích hành vi bằng công cụ thống kê truy cập."),
        ("8", "Nền tảng", "- Khi kinh doanh thật, cân nhắc chuyển sang WooCommerce, giữ giao diện SANCTUARY làm theme riêng."),
    ], widths=[1.2, 4.2, 11.6], caption="Bảng tổng hợp hướng phát triển", size=12, center_cols=(0,))

    # ---------- 1.5 Kiểm chứng hiệu suất ----------
    R.h3("1.5. Thành tựu triển khai và kiểm chứng hiệu suất trên môi trường Production")
    R.p("Một kết quả quan trọng của đồ án là website không chỉ chạy trên máy cục bộ mà đã được triển khai công khai trên Vercel tại "
        "https://sanctuarydivinity.vercel.app. Để kiểm chứng khách quan, nhóm đánh giá bằng bốn phương pháp lặp lại được và không "
        "dùng số liệu khảo sát giả định.")
    R.h4("1.5.1. Kiểm thử chức năng tự động")
    groups = OrderedDict()
    for t in tests:
        g = groups.setdefault(t["group"], [0, 0, []])
        g[0] += 1; g[1] += 1 if t["ok"] else 0; g[2].append(t["id"])
    R.p("Bộ kiểm thử gồm " + str(len(tests)) + " ca, viết bằng Playwright, chạy trên Google Chrome; mỗi ca thao tác như người dùng "
        "(bấm, nhập, chọn) rồi kiểm tra kết quả thật trong DOM, địa chỉ trang và localStorage. Bộ kiểm thử được chạy cả trên máy "
        "cục bộ và trên bản triển khai Vercel, đều đạt " + str(sum(t["ok"] for t in online)) + "/" + str(len(online)) + " ca.")
    R.table(["Nhóm chức năng", "Mã ca", "Số ca", "Đạt", "Tỷ lệ"],
            [(g, v[2][0] + " - " + v[2][-1], str(v[0]), str(v[1]), "%d%%" % round(100 * v[1] / v[0])) for g, v in groups.items()] +
            [("**Tổng**", "", "**%d**" % len(tests), "**%d**" % passed, "**%d%%**" % round(100 * passed / len(tests)))],
            widths=[5.0, 3.6, 2.4, 2.4, 3.6], caption="Kết quả kiểm thử chức năng theo nhóm", size=12, center_cols=(1, 2, 3, 4))
    R.p("Ở lần chạy đầu, 3 ca không đạt; khi kiểm tra lại, cả 3 đều do kịch bản kiểm thử viết sai chứ không phải lỗi website: ca "
        "lọc màu đếm cả một sản phẩm có màu đã ngừng bán (website ẩn màu này là đúng thiết kế), ca lịch sử đơn chèn đơn thử thiếu "
        "trường `userEmail` nên trang Account bỏ qua (đúng cơ chế kiểm tra dữ liệu), ca đổi trạng thái gọi sai hàm của công cụ. Sau "
        "khi sửa kịch bản, toàn bộ ca đạt. Chi tiết từng ca ở " + R.next_tab() + ".")
    rows = []
    for t in tests:
        a = t["actual"] if len(t["actual"]) <= 140 else t["actual"][:137] + "..."
        rows.append((t["id"], t["name"], t["expected"], a, ("Đạt", "E2EFDA") if t["ok"] else ("Không đạt", "F8CBAD")))
    R.table(["Mã", "Ca kiểm thử", "Kết quả mong đợi", "Kết quả thực tế", "KQ"], rows, widths=[1.3, 4.0, 4.0, 6.2, 1.5],
            caption="Chi tiết " + str(len(tests)) + " ca kiểm thử chức năng (chạy ngày 11/11/2026)", size=10, center_cols=(0, 4), align_cells=L)

    R.h4("1.5.2. Hiệu năng và chất lượng theo Google Lighthouse")
    R.p("Nhóm đo 5 trang của bản triển khai bằng Lighthouse 13.5 ở cấu hình mobile (giả lập điện thoại tầm trung, mạng 4G chậm) và "
        "desktop, xoá bộ nhớ đệm trước mỗi lần đo, ngày 11/11/2026. Ô xanh là điểm ≥ 90, vàng là 50 - 89. Ngưỡng tốt của Core Web "
        "Vitals là LCP ≤ 2,5 s và CLS ≤ 0,1 (Google, n.d.).")

    def mark(v):
        return (str(v), "E2EFDA") if v >= 90 else ((str(v), "FFF2CC") if v >= 50 else (str(v), "F8CBAD"))
    R.table(["Cấu hình", "Trang", "Perf.", "Access.", "Best Pr.", "SEO", "LCP", "CLS", "TBT", "Dung lượng"],
            [("Mobile" if r["mode"] == "mobile" else "Desktop", names[r["name"]], mark(r["performance"]), mark(r["accessibility"]),
              mark(r["bestPractices"]), mark(r["seo"]), vn(r["LCP"]), vn(r["CLS"]), r["TBT"], kib(r)) for r in lh],
            widths=[1.8, 2.0, 1.2, 1.4, 1.4, 1.1, 1.4, 1.3, 1.4, 2.0], caption="Kết quả đo Google Lighthouse (điểm 0 - 100)",
            size=10, center_cols=tuple(range(2, 10)))
    R.p("Ba hình dưới là ảnh chụp báo cáo Lighthouse của ba lần đo minh hoạ thực hiện lúc 13:10 ngày 11/11/2026 trên bản triển "
        "khai; điểm hiệu năng có thể lệch 1 - 3 điểm so với bảng trên do dao động giữa các lần đo.")
    R.figure(ctx["web"] / "lh-desktop-gate.png", "Báo cáo Lighthouse trang cổng trên cấu hình desktop", width=16)
    R.figure(ctx["web"] / "lh-desktop-home.png", "Báo cáo Lighthouse trang chủ trên cấu hình desktop", width=16)
    R.figure(ctx["web"] / "lh-mobile-cart.png", "Báo cáo Lighthouse trang giỏ hàng trên cấu hình mobile", width=16)
    R.p("**Accessibility và SEO đạt 100 ở cả 10 lần đo**, Best Practices 96 - 100. Trên desktop, cả 5 trang đạt hiệu năng " +
        str(min(r["performance"] for r in desk)) + " - 100 với LCP ≤ " + vn(max(float(r["LCP"].split()[0]) for r in desk)) +
        " s. Điểm yếu còn lại là trang chủ và About trên cấu hình điện thoại do video và ảnh lớn.")
    R.p("**Vòng đo - sửa - đo lại.** Lần đo đầu phát hiện trang cổng có CLS rất cao, cả 5 trang thiếu `meta description` và thẻ sản "
        "phẩm có nhãn không khớp chữ hiển thị. Khi điều tra CLS, nhóm thấy nguyên nhân không chỉ là ảnh thiếu kích thước như dự "
        "đoán: khối lookbook nằm trong flex container căn giữa nên co theo nội dung, ảnh chưa tải chỉ rộng khoảng 100 px rồi nở ra "
        "900 px. Nhóm sửa bằng `width: 100%` cho khối lookbook kết hợp khai báo kích thước ảnh, thêm `meta description` cho 7 trang "
        "và để thẻ sản phẩm lấy tên từ nội dung hiển thị.")
    cmp_rows = []
    for mode in ("desktop", "mobile"):
        b, a = pick(before, mode, "Gate"), pick(lh, mode, "Gate")
        cmp_rows.append(("Cổng (" + mode + ")", "%d → **%d**" % (b["performance"], a["performance"]),
                         "%s → **%s**" % (vn(b["CLS"]), vn(a["CLS"])), "%s → **%s**" % (vn(b["LCP"]), vn(a["LCP"])), "%d → **%d**" % (b["seo"], a["seo"])))
    for name in ("Home", "Cart", "Info", "About"):
        b, a = pick(before, "desktop", name), pick(lh, "desktop", name)
        cmp_rows.append((names[name] + " (desktop)", "%d → **%d**" % (b["performance"], a["performance"]),
                         "%s → **%s**" % (vn(b["CLS"]), vn(a["CLS"])), "%s → **%s**" % (vn(b["LCP"]), vn(a["LCP"])), "%d → **%d**" % (b["seo"], a["seo"])))
    R.table(["Trang", "Performance", "CLS", "LCP", "SEO"], cmp_rows, widths=[4.2, 3.2, 3.2, 3.6, 2.8],
            caption="Lighthouse trước và sau khi tối ưu", size=12, center_cols=(1, 2, 3, 4))
    R.p("Kết quả Lighthouse dao động nhẹ giữa các lần đo do mạng và tải máy chủ, nên nhóm chỉ kết luận ở thay đổi lớn: CLS trang "
        "cổng về 0 và điểm hiệu năng tăng " + str(pick(lh, "desktop", "Gate")["performance"] - pick(before, "desktop", "Gate")["performance"]) +
        " điểm trên desktop.", italic=True)
    R.h4("1.5.3. Kiểm tra mã HTML theo W3C")
    R.p("Lần kiểm tra đầu bằng W3C Nu Html Checker trực tuyến phát hiện 5 lỗi và 3 cảnh báo ở 4/7 trang. Sau khi sửa, nhóm kiểm tra "
        "lại bằng bản chạy trên máy (vnu.jar 26.10.12, vì dịch vụ trực tuyến chặn yêu cầu tự động); để chắc hai bản cho kết quả "
        "như nhau, nhóm chạy bản trên máy với mã nguồn cũ và nhận đúng 5 lỗi, 3 cảnh báo.")
    R.table(["Trang", "Trước (lỗi / cảnh báo)", "Nội dung", "Cách sửa", "Sau"],
            [(a, "%d / %d" % (b, c), d, e, "%d / %d" % (f, g)) for a, b, c, d, e, f, g in W3C] +
            [("**Tổng**", "**%d / %d**" % (sum(x[1] for x in W3C), sum(x[2] for x in W3C)), "", "", "**0 / 0**")],
            widths=[3.4, 2.1, 4.4, 4.7, 1.4], caption="Kết quả kiểm tra W3C trước và sau khi sửa", size=11, center_cols=(1, 4))
    R.h4("1.5.4. Độ chính xác của công cụ gợi ý size")
    R.table(["Chỉ số", "Nam", "Nữ"], [
        ("Số người trong dữ liệu ANSUR II", "{:,}".format(hm["sampleSize"]).replace(",", "."), "{:,}".format(hf["sampleSize"]).replace(",", ".")),
        ("Sai số RMSE khi ước lượng vòng ngực", vn(hm["rmseCm"]) + " cm", vn(hf["rmseCm"]) + " cm"),
        ("Gợi ý đúng size", vn(hm["exactSizePct"]) + "%", vn(hf["exactSizePct"]) + "%"),
        ("Sai không quá 1 size", vn(hm["withinOneSizePct"]) + "%", vn(hf["withinOneSizePct"]) + "%"),
    ], widths=[8.0, 4.5, 4.5], caption="Độ chính xác của công cụ gợi ý size", size=12, center_cols=(1, 2))
    R.p("Chỉ với chiều cao và cân nặng, mô hình đoán đúng size cho " + vn(hm["exactSizePct"]) + "% nam và " + vn(hf["exactSizePct"]) +
        "% nữ, gần như luôn nằm trong phạm vi một size. Độ chính xác của nữ thấp hơn vì vòng ngực nữ phụ thuộc nhiều vào yếu tố "
        "ngoài chiều cao, cân nặng.")
    R.h4("1.5.5. Hiệu quả tối ưu ảnh và video")
    R.table(["Tài nguyên", "Trước", "Sau", "Giảm"], [
        ("477 ảnh sản phẩm (JPG → WebP)", "94,2 MB", "30,9 MB", "67%"),
        ("192 ảnh đánh giá (JPG → WebP)", "4,2 MB", "3,0 MB", "29%"),
        ("10 ảnh lookbook (JPG/PNG → WebP)", "14 MB", "3,4 MB", "76%"),
        ("4 đoạn video (H.264, CRF 20)", "79 MB", "19,7 MB", "75%"),
        ("**Tổng**", "**191,4 MB**", "**57,0 MB**", "**70%**"),
    ], widths=[7.6, 3.0, 3.0, 3.4], caption="Dung lượng ảnh, video trước và sau khi tối ưu", size=12, center_cols=(1, 2, 3))
    R.h4("1.5.6. Giá trị của việc triển khai thực tế")
    R.ps(
        "**Môi trường demo trực quan.** Giảng viên truy cập và thao tác trực tiếp toàn bộ luồng từ trang cổng, mua hàng đến quản "
        "trị trên môi trường thật thay vì chỉ xem mã nguồn hay video.",
        "**Tự động hoá triển khai (CI/CD).** Mỗi commit lên nhánh `main` được Vercel tự triển khai sau khoảng 20 giây, giúp cả "
        "nhóm làm việc trên một phiên bản chung và phát hiện lỗi sớm; nhờ đó vòng đo - sửa - đo lại ở mục 1.5.2 hoàn thành trong "
        "một buổi.",
        "**Phát hiện lỗi chỉ có trên môi trường thật.** Ví dụ trang cổng trên Vercel có địa chỉ `/password` thay vì `/index.html`; "
        "bộ kiểm thử phát hiện điểm khác biệt này và được viết lại để chạy đúng ở cả hai môi trường.")

    # ---------- 1.6 Quản trị website ----------
    R.h3("1.6. Kế hoạch quản trị website")
    R.h4("1.6.1. Các mối đe doạ bảo mật và biện pháp")
    R.p("Nhóm đối chiếu website với các nhóm rủi ro trong danh sách OWASP Top 10 (OWASP Foundation, 2021):")
    R.table(["Mối đe doạ", "Rủi ro với SANCTUARY", "Biện pháp hiện có", "Biện pháp khi kinh doanh thật"], [
        ("Kiểm soát truy cập kém", "Sửa sessionStorage để vào trang admin", "guard.js chặn giao diện; mã admin chỉ lưu dạng băm", "Xác thực phía máy chủ, phiên đăng nhập, phân quyền"),
        ("Lộ, dò mật khẩu", "Dò giá trị băm bằng từ điển", "SHA-256 + salt 16 byte riêng từng tài khoản", "Băm chậm (bcrypt/Argon2), giới hạn số lần thử"),
        ("Chèn mã (XSS)", "Tin nhắn, tên khách chứa mã độc", "Ghi bằng textContent", "Content-Security-Policy, lọc dữ liệu ở máy chủ"),
        ("Sửa dữ liệu phía máy khách", "Sửa giá, tồn kho trong localStorage", "Kiểm tra cấu trúc khi đọc", "Tính giá, tồn kho ở máy chủ"),
        ("Mất dữ liệu", "Xoá dữ liệu trình duyệt, đổi máy", "Sao lưu/khôi phục JSON trong trang admin", "Sao lưu CSDL tự động hằng ngày"),
        ("Gián đoạn dịch vụ", "Hosting hoặc API tỷ giá lỗi", "CDN của Vercel; tỷ giá dự phòng", "Giám sát uptime, phương án dự phòng"),
        ("Lộ thông tin cấu hình", "Mã demo, mã admin trong mã nguồn", "Chỉ lưu băm; tắt gợi ý mã demo khi nộp", "Biến môi trường, không đưa bí mật lên kho mã"),
    ], widths=[3.0, 4.0, 4.5, 4.5], caption="Mối đe doạ và biện pháp bảo mật", size=11)
    R.h4("1.6.2. Kế hoạch sao lưu")
    R.p("Nhóm áp dụng nguyên tắc 3-2-1: ít nhất 3 bản dữ liệu, trên 2 loại nơi lưu khác nhau, 1 bản ở ngoài máy làm việc.")
    R.table(["Đối tượng", "Cách sao lưu", "Tần suất", "Nơi lưu", "Khôi phục"], [
        ("Mã nguồn, dữ liệu gốc", "Commit Git, đẩy lên GitHub", "Mỗi tính năng", "Máy cá nhân + GitHub", "git checkout / revert"),
        ("Bản triển khai", "Vercel giữ lịch sử từng lần triển khai", "Tự động", "Vercel", "Promote bản cũ (rollback)"),
        ("Dữ liệu vận hành", "Admin → Backup → Download backup", "Cuối mỗi ngày bán", "Ổ đám mây của nhóm", "Admin → Backup → Restore"),
        ("Ảnh, video gốc", "Lưu riêng ngoài kho Git", "Khi có tài nguyên mới", "Ổ đám mây", "Nén lại bằng compress_media.py"),
    ], widths=[3.4, 4.4, 2.4, 3.0, 3.8], caption="Kế hoạch sao lưu", size=11)
    R.h4("1.6.3. Kế hoạch nâng cấp")
    R.ps(
        "Nâng cấp được thực hiện theo giai đoạn ở mục 1.4: ngắn hạn tối ưu hiệu năng trên điện thoại và chi tiết giao diện; "
        "trung hạn thêm máy chủ, cơ sở dữ liệu và cổng thanh toán; dài hạn cân nhắc chuyển nền tảng sang WooCommerce.",
        "Mỗi lần nâng cấp làm trên nhánh Git riêng, chạy lại bộ kiểm thử tự động, Lighthouse và W3C, đạt yêu cầu mới gộp vào nhánh "
        "`main` để Vercel triển khai; có sự cố thì quay lại bản triển khai trước trên Vercel trong vài giây.")

    # ======================= Link, kết luận, tài liệu tham khảo =======================
    R.front_heading("TỔNG HỢP CÁC LINK")
    for label, url in [("Link website", "https://sanctuarydivinity.vercel.app (mã truy cập: SANCTUARY-DEMO)"),
                       ("Link GitHub", "https://github.com/thaikhuonganhduc/sanctuarydivinity"),
                       ("Link sơ đồ draw.io", "thư mục docs/diagrams trong kho GitHub"),
                       ("Link Figma prototype", "https://www.figma.com/design/Ymn9HLXeZGQY9WTITtkXhr"),
                       ("Link Slide", "...................................................................."),
                       ("Link video Demo", "...................................................................."),
                       ("Link phân công công việc và Gantt Chart", "...................................................................."),
                       ("Link Google Drive tài liệu nhóm", "....................................................................")]:
        R.p("- " + label + ": " + url, indent=False)
    R.front_heading("LỜI KẾT LUẬN")
    R.ps(
        "Đồ án SANCTUARY giúp nhóm đi trọn quy trình xây dựng một website thương mại điện tử: từ hình thành ý tưởng kinh doanh, "
        "phân tích thị trường, đặc tả nghiệp vụ, mô hình hoá hệ thống, thiết kế dữ liệu và giao diện, đến lập trình, triển khai và "
        "kiểm chứng bằng số liệu. Website không chỉ đáp ứng các chức năng bán hàng mà còn thể hiện được cá tính của một thương "
        "hiệu luxury gymwear với mô hình drop, mã athlete và công cụ gợi ý size dựa trên dữ liệu.",
        "Quá trình thực hiện giúp nhóm hiểu sâu HTML, CSS, JavaScript, DOM, XML và AJAX, đồng thời rèn kỹ năng làm việc nhóm, quản "
        "lý mã nguồn và tư duy đo lường: không dừng ở “chạy được” mà kiểm tra, sửa và chứng minh chất lượng. SANCTUARY vẫn còn "
        "nhiều hướng phát triển như máy chủ và cơ sở dữ liệu thật, cổng thanh toán, bảo mật phía máy chủ, hy vọng sẽ là nền tảng "
        "để nhóm phát triển thành một cửa hàng thực thụ trong tương lai.")
    R.front_heading("TÀI LIỆU THAM KHẢO")
    for ref in REFERENCES:
        p = R.p(ref, indent=False, align=L)
        p.paragraph_format.left_indent = Cm(1.27)
        p.paragraph_format.first_line_indent = Cm(-1.27)
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_after = Pt(6)
