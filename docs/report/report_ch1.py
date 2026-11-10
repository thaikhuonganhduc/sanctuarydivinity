# -*- coding: utf-8 -*-
"""Chương 1. Giới thiệu (kèm kế hoạch thực hiện và bảng phân công)."""
from docx.shared import Cm
from report_front import MEMBERS

WEEKS = ["14/09", "21/09", "28/09", "05/10", "12/10", "19/10", "26/10", "02/11", "09/11", "16/11", "23/11"]
# (công việc, phụ trách, tuần bắt đầu, tuần kết thúc, sản phẩm)  - tuần đánh số từ 1
PLAN = [
    ("Lập nhóm, chọn đề tài, lập kế hoạch", "Anh Đức", 1, 1, "Kế hoạch, kênh làm việc nhóm"),
    ("Khảo sát web tham khảo, xác định yêu cầu", "Ngọc Ánh, Lê Vy", 1, 2, "Danh sách yêu cầu chức năng"),
    ("Nhận diện thương hiệu, phác thảo giao diện", "Bảo Hân", 2, 3, "Logo, bảng màu, phác thảo"),
    ("Phân tích thiết kế: Use case, ERD, DFD, BPMN", "Lê Vy", 3, 5, "Bộ sơ đồ draw.io"),
    ("Thu thập, xử lý dữ liệu mẫu và bảng size", "Anh Đức, Gia Bảo", 4, 6, "products.json, reviews.json, size-chart.json"),
    ("Lập trình giao diện HTML/CSS đáp ứng", "Bảo Hân", 7, 8, "7 trang HTML, 5 file CSS"),
    ("Lập trình chức năng JavaScript", "Anh Đức", 7, 8, "Giỏ hàng, thanh toán, tài khoản, quản trị"),
    ("Nội dung Info, About, form liên hệ", "Ngọc Ánh", 7, 8, "Trang chính sách, liên hệ"),
    ("Đánh giá, lọc và sắp xếp sản phẩm", "Gia Bảo", 7, 8, "Popup Reviews, menu Armory"),
    ("Triển khai lên GitHub và Vercel", "Anh Đức", 8, 8, "Website chạy online"),
    ("Bổ sung XML/AJAX, LESS, iframe", "Anh Đức, Bảo Hân, Ngọc Ánh", 9, 9, "shipping.xml, components.less, bản đồ"),
    ("Cài đặt, quản trị thử WooCommerce", "Anh Đức", 9, 9, "Bản cài thử, ảnh minh chứng"),
    ("Kiểm thử, đo Lighthouse và W3C", "Gia Bảo", 9, 10, "41 ca kiểm thử, bảng số đo"),
    ("Viết báo cáo", "Cả nhóm", 9, 10, "Báo cáo Word"),
    ("Slides, kịch bản thuyết trình", "Lê Vy", 10, 10, "Slides, kịch bản"),
    ("Nộp bài (dự kiến 22/11/2026)", "Anh Đức", 10, 10, "Mã nguồn, báo cáo, slides"),
    ("Thuyết trình và vấn đáp", "Cả nhóm", 11, 11, "Phần trình bày của mỗi thành viên"),
]


def build(R, ctx):
    R.new_section("decimal", 1)
    R.h1("CHƯƠNG 1. GIỚI THIỆU", chapter=1)

    R.h2("1.1. Bối cảnh và lý do thực hiện dự án")
    R.p("Thương mại điện tử Việt Nam tăng trưởng nhanh trong những năm gần đây. Theo báo cáo e-Conomy SEA 2024 của "
        "Google, Temasek và Bain & Company, tổng giá trị hàng hoá giao dịch (GMV) của TMĐT Việt Nam năm 2024 ước đạt "
        "khoảng 22 tỷ USD, tăng 18% so với năm trước và chiếm hơn 60% nền kinh tế số của cả nước (Google và cộng sự, "
        "2024). Thời trang là một trong những ngành hàng bán trực tuyến nhiều nhất, nhưng cũng là ngành có tỷ lệ trả "
        "hàng cao, chủ yếu vì khách không được thử đồ trước khi mua (Stöcker và cộng sự, 2021).")
    R.p("Trong thời trang, dòng quần áo tập gym cao cấp (luxury gymwear) có cách kinh doanh riêng: thương hiệu nhỏ, "
        "thiết kế cầu kỳ, may cắt theo lô (cut-and-sew) và mở bán theo từng đợt giới hạn gọi là *drop*. Khách hàng chủ "
        "yếu đến từ cộng đồng của các vận động viên, người có ảnh hưởng (gọi chung là *athlete*). Với mô hình này, "
        "website không chỉ là nơi trưng bày mà còn phải tạo cảm giác khan hiếm và độc quyền: đếm ngược tới ngày mở bán, "
        "cổng truy cập riêng, mã giảm giá theo từng athlete. Nghiên cứu trên người tiêu dùng trẻ Việt Nam cũng cho thấy "
        "tính khan hiếm và độc đáo của sản phẩm phiên bản giới hạn làm tăng giá trị cảm nhận và ý định mua (Ha, 2021).")
    R.p("Đồ án cuối kỳ của học phần Phát triển Web kinh doanh (BIE5030) yêu cầu nhóm xây dựng một website TMĐT bằng "
        "HTML, CSS, JavaScript, XML và DOM, đồng thời tìm hiểu một hệ thống TMĐT mã nguồn mở. Nhóm chọn đề tài quần áo "
        "gym vì nó đòi hỏi nhiều kỹ thuật của môn học cùng lúc: giao diện giàu hình ảnh và đáp ứng nhiều màn hình, lọc "
        "và sắp xếp sản phẩm, xử lý biểu mẫu, tính toán giỏ hàng, và một bài toán dữ liệu có ý nghĩa thực tế là gợi ý "
        "size. Thương hiệu được đặt tên **SANCTUARY** với phong cách tối, mạnh, underground; phong cách trình bày và dữ "
        "liệu sản phẩm mẫu tham khảo website breathedivinity.com (Breathe Divinity, n.d.).")

    R.h2("1.2. Vấn đề cần giải quyết")
    R.p("Từ bối cảnh trên, nhóm xác định năm vấn đề mà website cần giải quyết:")
    R.bullets([
        "**Trải nghiệm trên nhiều thiết bị.** Phần lớn khách xem hàng trên điện thoại, trong khi ảnh sản phẩm thời "
        "trang lớn và nặng. Website phải hiển thị tốt từ 390 px đến 1440 px mà vẫn tải nhanh.",
        "**Khó chọn đúng size khi mua trực tuyến.** Chọn sai size là lý do trả hàng phổ biến nhất của thời trang trực "
        "tuyến (Stöcker và cộng sự, 2021). Khách cần một bảng size rõ ràng và một công cụ gợi ý size đơn giản từ chiều "
        "cao, cân nặng.",
        "**Bán độc quyền theo đợt drop.** Cửa hàng cần cổng truy cập bằng mã của từng athlete, đồng hồ đếm ngược tới "
        "ngày ra mắt, và dùng chính mã đó làm mã giảm giá để đo hiệu quả của từng người giới thiệu.",
        "**Vận hành cửa hàng.** Chủ cửa hàng cần xem doanh thu, xử lý đơn, cập nhật giá và tồn kho, quản lý mã athlete, "
        "đọc tin nhắn và sao lưu dữ liệu, dù trong phạm vi đồ án website không có máy chủ ứng dụng.",
        "**Yêu cầu học thuật.** Website phải thể hiện đủ phạm vi kiến thức của đề cương (HTML5 semantic, form, bảng, "
        "iframe; CSS box model, responsive, LESS; JavaScript, DOM, sự kiện, XML, AJAX; mã nguồn mở; quản trị website) và "
        "mã nguồn phải đủ rõ để mỗi thành viên giải thích được khi vấn đáp.",
    ])

    R.h2("1.3. Mục tiêu của dự án")
    R.p("**Mục tiêu tổng quát:** xây dựng một website TMĐT hoàn chỉnh ở phía người dùng (front-end) cho thương hiệu "
        "quần áo gym SANCTUARY, chạy được trực tuyến, có trang quản trị, và đánh giá được bằng số liệu đo đạc khách quan.")
    R.p("**Mục tiêu cụ thể** (mỗi mục tiêu có tiêu chí để kiểm tra ở Chương 5):", keep_next=True)
    R.table(["Mã", "Mục tiêu", "Tiêu chí đạt"], [
        ("MT1", "Xây dựng đủ luồng mua hàng: cổng, trang chủ, cửa hàng, chi tiết, giỏ, thanh toán, tài khoản",
         "Mọi ca kiểm thử chức năng của luồng mua hàng đều đạt"),
        ("MT2", "Thiết kế đáp ứng, ưu tiên điện thoại (mobile-first)", "Không cuộn ngang ở 390, 820 và 1440 px"),
        ("MT3", "Áp dụng đủ kỹ thuật trong đề cương (HTML5, CSS3, LESS, JavaScript, DOM, XML, AJAX, iframe)",
         "Mỗi kỹ thuật có ít nhất một chỗ dùng thật trong mã nguồn"),
        ("MT4", "Xây dựng công cụ gợi ý size dựa trên dữ liệu số đo cơ thể thật", "Đúng size ≥ 50%, sai không quá 1 size ≥ 95%"),
        ("MT5", "Xây dựng trang quản trị cho đơn hàng, sản phẩm, khách hàng, mã athlete, sao lưu", "8 chức năng quản trị chạy được"),
        ("MT6", "Đảm bảo chất lượng kỹ thuật", "Lighthouse Accessibility ≥ 90; LCP desktop ≤ 2,5 s; HTML hợp lệ theo W3C"),
        ("MT7", "Cài đặt và quản trị thử một nền tảng TMĐT mã nguồn mở", "Cài được WooCommerce, quản lý được sản phẩm, đơn, khách, giao diện"),
    ], widths=[1.4, 8.4, 6.2], caption="Mục tiêu cụ thể và tiêu chí đánh giá", center_cols=(0,))

    R.h2("1.4. Phạm vi và giới hạn của dự án")
    R.p("**Phạm vi.** Website gồm 7 trang HTML: trang cổng (`index.html`), trang chủ kiêm cửa hàng, giỏ hàng kèm thanh "
        "toán, trang Info (liên hệ và chính sách), giới thiệu thương hiệu, tài khoản và trang quản trị. Người dùng có ba "
        "vai trò: khách (đã nhập mã athlete), thành viên (khách có tài khoản) và quản trị viên. Dữ liệu mẫu gồm " +
        str(ctx["n_products"]) + " sản phẩm với " + str(ctx["n_colors"]) + " biến thể màu, " + str(ctx["n_reviews"]) +
        " đánh giá có ảnh, 15 nước giao hàng. Ngoài website, nhóm cài thử WooCommerce để thực hiện phần mã nguồn mở.")
    R.p("**Giới hạn.** Đây là đồ án học tập, không kinh doanh thật, nên nhóm chấp nhận các giới hạn sau và trình bày "
        "rõ ở mục 5.3:")
    R.bullets([
        "Không có máy chủ ứng dụng và cơ sở dữ liệu: đơn hàng, tài khoản, thay đổi của quản trị viên lưu trong "
        "`localStorage` của từng trình duyệt, không đồng bộ giữa các máy.",
        "Bảo mật chỉ ở mức mô phỏng phía máy khách (băm mật khẩu, chặn trang theo vai trò); người dùng hiểu kỹ thuật "
        "có thể sửa dữ liệu bằng công cụ của trình duyệt.",
        "Thanh toán là giả lập: chỉ kiểm tra định dạng số thẻ, không kết nối cổng thanh toán.",
        "Phí vận chuyển và thuế là số ước tính để minh hoạ cách tính, không phải báo giá thật.",
        "Sản phẩm, mô tả, ảnh và đánh giá mẫu lấy từ breathedivinity.com để làm dữ liệu học tập; nhóm không dùng tên và "
        "logo của thương hiệu này.",
    ])

    R.h2("1.5. Phương pháp nghiên cứu và cách tiếp cận")
    R.p("Nhóm kết hợp các phương pháp sau:")
    R.bullets([
        "**Nghiên cứu tài liệu:** đề cương và giáo trình của học phần (Frain, 2020; Haverbeke, 2024; Grant, 2024), tài "
        "liệu chuẩn của W3C, WHATWG, MDN, và các nghiên cứu về TMĐT thời trang trong 5 năm gần đây.",
        "**Khảo sát trường hợp (case study):** phân tích bố cục, danh mục sản phẩm và luồng mua hàng của breathedivinity.com "
        "để rút ra yêu cầu cho SANCTUARY.",
        "**Phân tích và thiết kế hướng mô hình:** mô tả hệ thống bằng sơ đồ Use case, ERD, DFD, BPMN và lưu đồ giải thuật "
        "trước khi lập trình.",
        "**Phát triển lặp, tăng dần (iterative and incremental):** chia thành các vòng ngắn, mỗi vòng hoàn thành một "
        "nhóm chức năng chạy được (cổng → cửa hàng → giỏ hàng → tài khoản → quản trị), kiểm tra rồi mới làm tiếp. Mỗi "
        "tính năng là một commit Git để theo dõi tiến độ.",
        "**Thực nghiệm và đo lường:** kiểm thử chức năng tự động, đo Google Lighthouse, kiểm tra W3C Validator, đánh giá "
        "độ chính xác của mô hình gợi ý size trên dữ liệu ANSUR II.",
    ])

    R.h2("1.6. Kế hoạch thực hiện")
    R.p("Đồ án thực hiện trong 11 tuần, từ 14/09/2026 đến 29/11/2026. " + R.next_tab() + " trình bày kế hoạch dạng "
        "biểu đồ Gantt: ô tô đậm là tuần thực hiện công việc. Mốc nộp bài và thuyết trình là dự kiến, sẽ điều chỉnh theo "
        "lịch chính thức của lớp.")
    headers = ["STT", "Công việc", "Phụ trách"] + [str(i + 1) for i in range(len(WEEKS))]   # cột 1..11 = tuần
    rows = []
    for i, (task, who, a, b, _) in enumerate(PLAN):
        cells = [str(i + 1), task, who]
        for w in range(1, len(WEEKS) + 1):
            cells.append(("", "1F4E79") if a <= w <= b else "")
        rows.append(cells)
    R.table(headers, rows, widths=[1.0, 5.3, 3.1] + [0.6] * len(WEEKS), caption="Kế hoạch thực hiện đồ án (biểu đồ Gantt)",
            size=9.5, center_cols=tuple([0] + list(range(3, 3 + len(WEEKS)))), tight=True)
    R.p("Cột 1 - 11 là tuần T1 - T11. Tuần T1 bắt đầu ngày 14/09/2026; các tuần tiếp theo bắt đầu lần lượt vào " +
        ", ".join(WEEKS[1:]) + ".",
        indent=False, italic=True, size=11)
    R.table(["STT", "Công việc", "Thời gian", "Sản phẩm bàn giao"],
            [(str(i + 1), t, "T%d" % a if a == b else "T%d - T%d" % (a, b), out) for i, (t, _, a, b, out) in enumerate(PLAN)],
            widths=[1.0, 6.4, 2.4, 6.2], caption="Sản phẩm bàn giao theo từng công việc", size=11, center_cols=(0, 2))

    R.h2("1.7. Bảng phân công công việc")
    assign = [
        ("Thái Khương Anh Đức\n(nhóm trưởng)", "Lập kế hoạch, điều phối, quản lý GitHub; kiến trúc và cấu trúc thư mục; "
         "JavaScript lõi: giỏ hàng, thanh toán, tính phí ship (XML/AJAX), tài khoản (SHA-256), trang quản trị; xử lý dữ "
         "liệu bằng Python và bảng size ANSUR II; triển khai Vercel; cài đặt WooCommerce; tổng hợp báo cáo", "100%"),
        ("Nguyễn Phan Bảo Hân", "Nhận diện thương hiệu (logo, màu, font); HTML/CSS trang cổng, trang chủ, cửa hàng, "
         "popup sản phẩm; thiết kế đáp ứng; viết LESS cho các thành phần dùng chung", "100%"),
        ("Lê Mai Ngọc Ánh", "Khảo sát yêu cầu; nội dung trang Info (chính sách, điều khoản) và About; form liên hệ và "
         "kiểm tra dữ liệu; nhúng bản đồ iframe; viết Chương 1, 2 và tài liệu tham khảo", "100%"),
        ("Nguyễn Gia Bảo", "Thu thập dữ liệu mẫu; popup đánh giá, slideshow; lọc và sắp xếp sản phẩm; kiểm thử chức "
         "năng, đo Lighthouse, W3C; viết Chương 4", "100%"),
        ("Lê Vy", "Khảo sát yêu cầu; sơ đồ Use case, ERD, DFD, BPMN và lưu đồ giải thuật; viết Chương 3, 5, 6; slides và "
         "kịch bản thuyết trình", "100%"),
    ]
    R.table(["Thành viên", "Công việc phụ trách", "Mức độ hoàn thành"], assign, widths=[4.0, 9.6, 2.4],
            caption="Bảng phân công công việc", center_cols=(2,))
    R.p("Mỗi thành viên đều tham gia viết báo cáo và trình bày phần mình phụ trách khi thuyết trình, vấn đáp.")

    R.h2("1.8. Cấu trúc của báo cáo")
    R.p("Ngoài phần mở đầu, báo cáo gồm sáu chương theo outline của giảng viên. Chương 2 trình bày cơ sở lý thuyết và "
        "các nghiên cứu liên quan. Chương 3 trình bày phương pháp thực hiện: quy trình, đặc tả hệ thống, sơ đồ giải "
        "thuật, dữ liệu, công cụ và cách đánh giá. Chương 4 trình bày kết quả và phân tích. Chương 5 thảo luận điểm "
        "mạnh, hạn chế và kế hoạch quản trị website. Chương 6 kết luận và đề xuất hướng phát triển. Cuối báo cáo là tài "
        "liệu tham khảo (chuẩn APA) và phụ lục.")
