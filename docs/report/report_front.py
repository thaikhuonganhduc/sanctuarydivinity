# -*- coding: utf-8 -*-
"""Trang bìa, lời cảm ơn, nhận xét, mục lục, danh mục, thông tin tác giả + metadata, tóm tắt."""
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Pt, Cm
from docx_helpers import set_font

MEMBERS = [
    ("Thái Khương Anh Đức", "K234161828", "Nhóm trưởng"),
    ("Nguyễn Phan Bảo Hân", "K244161782", "Thành viên"),
    ("Lê Mai Ngọc Ánh", "K244030341", "Thành viên"),
    ("Nguyễn Gia Bảo", "K244030343", "Thành viên"),
    ("Lê Vy", "K244161824", "Thành viên"),
]
TOPIC = "XÂY DỰNG WEBSITE THƯƠNG MẠI ĐIỆN TỬ BÁN QUẦN ÁO GYM SANCTUARY"


def cover(R, ctx):
    doc = R.doc
    R.background_image(ctx["img"] / "cover-bg.png")
    first = doc.paragraphs[0]
    first.paragraph_format.first_line_indent = Cm(0)
    first.paragraph_format.space_after = Pt(0)
    first.paragraph_format.line_spacing = 1.0

    def line(text, size, before=0, bold=True, italic=False, align=WD_ALIGN_PARAGRAPH.CENTER, after=0):
        p = doc.add_paragraph()
        p.alignment = align
        pf = p.paragraph_format
        pf.first_line_indent = Cm(0)
        pf.space_before, pf.space_after, pf.line_spacing = Pt(before), Pt(after), 1.15
        r = p.add_run(text)
        set_font(r, size, bold, italic)
        return p

    line("KHOA HỆ THỐNG THÔNG TIN", 18, before=44)
    line("ĐỒ ÁN CUỐI KỲ MÔN PHÁT TRIỂN WEB KINH DOANH", 16, before=176)
    line("TÊN ĐỀ TÀI: " + TOPIC, 16, before=8)
    p = line("", 14, before=14, align=WD_ALIGN_PARAGRAPH.RIGHT)
    r = p.add_run("GVHD: "); set_font(r, 14, True, True)
    r = p.add_run("TS. Trần Duy Thanh"); set_font(r, 14, True, False)
    p = line("", 13, before=2, align=WD_ALIGN_PARAGRAPH.RIGHT)
    r = p.add_run("Lớp học phần: 261BIE503002"); set_font(r, 13, False, False)
    line("Thành viên nhóm", 14, before=22, italic=True, after=6)

    t = doc.add_table(rows=1, cols=3)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(["Họ và tên", "Mã số sinh viên", "Mức độ hoàn thành"]):
        R._cell(t.rows[0].cells[i], h, 13, bold=True, center=True)
    for name, mssv, _ in MEMBERS:
        cells = t.add_row().cells
        for i, v in enumerate([name, mssv, "100%"]):
            R._cell(cells[i], v, 13, center=True)
    for row in t.rows:
        row.height = Cm(0.85)
    R._set_widths(t, [6.0, 5.0, 4.5])
    line("TP. Hồ Chí Minh, tháng 11 năm 2026", 13, before=26, bold=False, italic=True)


def build(R, ctx):
    cover(R, ctx)
    R.new_section("lowerRoman", 1)

    # ---------- Lời cảm ơn ----------
    R.front_title("LỜI CẢM ƠN", page_break=False)
    R.p("Nhóm xin gửi lời cảm ơn chân thành đến **TS. Trần Duy Thanh**, giảng viên học phần Phát triển Web kinh doanh, "
        "Khoa Hệ thống thông tin, Trường Đại học Kinh tế - Luật (ĐHQG-HCM). Những buổi giảng về HTML, CSS, JavaScript, "
        "XML, mô hình DOM và các hệ thống thương mại điện tử mã nguồn mở là nền tảng để nhóm hoàn thành đồ án này.")
    R.p("Nhóm cũng cảm ơn các bạn trong lớp đã góp ý giao diện trong quá trình làm, và các tác giả của những tài liệu, "
        "bộ dữ liệu mở được nhóm trích dẫn ở cuối báo cáo. Do thời gian và kinh nghiệm còn hạn chế, báo cáo khó tránh "
        "khỏi thiếu sót; nhóm rất mong nhận được nhận xét của thầy để hoàn thiện hơn.")
    R.p("Nhóm thực hiện", align=WD_ALIGN_PARAGRAPH.RIGHT, indent=False, italic=True)

    # ---------- Nhận xét của giảng viên ----------
    R.front_title("NHẬN XÉT CỦA GIẢNG VIÊN")
    for _ in range(14):
        R.p("." * 118, indent=False, after=4, size=12)
    R.p("TP. Hồ Chí Minh, ngày ...... tháng ...... năm 2026", align=WD_ALIGN_PARAGRAPH.RIGHT, indent=False, italic=True)
    R.p("Giảng viên", align=WD_ALIGN_PARAGRAPH.RIGHT, indent=False, bold=True)

    # ---------- Mục lục và danh mục ----------
    R.front_title("MỤC LỤC")
    p = R.doc.add_paragraph(); p.paragraph_format.first_line_indent = Cm(0)
    R.field(p, 'TOC \\o "1-3" \\h \\z \\u', "Mở bằng Word và chọn cập nhật trường để hiện mục lục.")
    R.front_title("DANH MỤC HÌNH")
    p = R.doc.add_paragraph(); p.paragraph_format.first_line_indent = Cm(0)
    R.field(p, 'TOC \\h \\z \\t "HinhCaption,1"', "Cập nhật trường để hiện danh mục hình.")
    R.front_title("DANH MỤC BẢNG")
    p = R.doc.add_paragraph(); p.paragraph_format.first_line_indent = Cm(0)
    R.field(p, 'TOC \\h \\z \\t "BangCaption,1"', "Cập nhật trường để hiện danh mục bảng.")

    R.front_title("DANH MỤC TỪ VIẾT TẮT")
    abbr = [
        ("AJAX", "Asynchronous JavaScript and XML: gửi/nhận dữ liệu với máy chủ mà không tải lại trang"),
        ("API", "Application Programming Interface: giao diện lập trình ứng dụng"),
        ("BPMN", "Business Process Model and Notation: ký pháp mô hình quy trình nghiệp vụ"),
        ("CDN", "Content Delivery Network: mạng phân phối nội dung"),
        ("CLS", "Cumulative Layout Shift: chỉ số dịch chuyển bố cục"),
        ("CSDL", "Cơ sở dữ liệu"),
        ("CSS", "Cascading Style Sheets: ngôn ngữ định dạng trang web"),
        ("DFD", "Data Flow Diagram: sơ đồ luồng dữ liệu"),
        ("DNS", "Domain Name System: hệ thống tên miền"),
        ("DOM", "Document Object Model: mô hình đối tượng tài liệu"),
        ("ERD", "Entity Relationship Diagram: sơ đồ quan hệ thực thể"),
        ("FCP", "First Contentful Paint: thời điểm hiện nội dung đầu tiên"),
        ("GVHD", "Giảng viên hướng dẫn"),
        ("HTML", "HyperText Markup Language: ngôn ngữ đánh dấu siêu văn bản"),
        ("HTTP(S)", "HyperText Transfer Protocol (Secure): giao thức truyền siêu văn bản (bảo mật)"),
        ("JSON", "JavaScript Object Notation: định dạng dữ liệu dạng văn bản"),
        ("LCP", "Largest Contentful Paint: thời điểm hiện phần nội dung lớn nhất"),
        ("LESS", "Leaner Style Sheets: bộ tiền xử lý CSS"),
        ("SEO", "Search Engine Optimization: tối ưu cho máy tìm kiếm"),
        ("SHA-256", "Secure Hash Algorithm 256 bit: hàm băm mật mã"),
        ("TBT", "Total Blocking Time: tổng thời gian luồng chính bị chặn"),
        ("TMĐT", "Thương mại điện tử"),
        ("UI/UX", "User Interface / User Experience: giao diện / trải nghiệm người dùng"),
        ("UML", "Unified Modeling Language: ngôn ngữ mô hình hoá thống nhất"),
        ("WCAG", "Web Content Accessibility Guidelines: hướng dẫn về khả năng truy cập nội dung web"),
        ("XML", "eXtensible Markup Language: ngôn ngữ đánh dấu mở rộng"),
    ]
    R.table(["Từ viết tắt", "Ý nghĩa"], abbr, widths=[3.2, 12.8], bold_first=True)

    # ---------- Thông tin tác giả và metadata ----------
    R.h1("THÔNG TIN TÁC GIẢ VÀ METADATA")
    # Hai bảng ở phần đầu không đánh số (không đưa vào Danh mục bảng), chỉ có tiêu đề
    R.p("Thành viên nhóm thực hiện", indent=False, bold=True, keep_next=True, after=4)
    R.table(["STT", "Họ và tên", "MSSV", "Vai trò"],
            [(str(i + 1), n, m, v) for i, (n, m, v) in enumerate(MEMBERS)],
            widths=[1.3, 6.2, 4.0, 4.5], center_cols=(0, 2))
    meta = [
        ("Tên đề tài", "Xây dựng website thương mại điện tử bán quần áo gym SANCTUARY"),
        ("Học phần", "Phát triển Web kinh doanh (Business Web Development), mã học phần BIE5030, 3 tín chỉ"),
        ("Lớp học phần", "261BIE503002"),
        ("Giảng viên hướng dẫn", "TS. Trần Duy Thanh"),
        ("Đơn vị", "Bộ môn Thương mại điện tử, Khoa Hệ thống thông tin, Trường Đại học Kinh tế - Luật, ĐHQG-HCM"),
        ("Loại sản phẩm", "Website TMĐT front-end (HTML5, CSS3/LESS, JavaScript thuần, JSON, XML) kèm trang quản trị; "
                          "bản cài thử WooCommerce cho phần mã nguồn mở"),
        ("Website (bản triển khai)", "https://sanctuarydivinity.vercel.app (mã truy cập cho khách: SANCTUARY-DEMO)"),
        ("Mã nguồn", "https://github.com/thaikhuonganhduc/sanctuarydivinity"),
        ("Thời gian thực hiện", "14/09/2026 - 29/11/2026 (11 tuần)"),
        ("Từ khoá", "thương mại điện tử; thiết kế web đáp ứng; JavaScript; DOM; AJAX; XML; gợi ý size; WooCommerce"),
        ("Ghi chú", "Đồ án học tập, không phải cửa hàng thật (student project, not a real store). Phong cách và dữ liệu "
                    "sản phẩm mẫu tham khảo breathedivinity.com; tên và logo SANCTUARY là của nhóm."),
    ]
    R.p("Thông tin chung (metadata) của đồ án", indent=False, bold=True, keep_next=True, after=4)
    R.table(["Thuộc tính", "Nội dung"], meta, widths=[4.2, 11.8], bold_first=True)

    # ---------- Tóm tắt ----------
    R.h1("TÓM TẮT")
    sc = ctx["size_chart"]
    R.p("Báo cáo trình bày quá trình phân tích, thiết kế, xây dựng và đánh giá **SANCTUARY**, một website thương mại "
        "điện tử bán quần áo tập gym theo phong cách tối, cao cấp và bán theo từng đợt ra mắt giới hạn (drop). Đề tài "
        "nhằm vận dụng kiến thức của học phần Phát triển Web kinh doanh: HTML5, CSS3, JavaScript, XML, mô hình DOM và "
        "hệ thống TMĐT mã nguồn mở, để giải quyết ba vấn đề thường gặp của cửa hàng thời trang trực tuyến: trải nghiệm "
        "duyệt và mua hàng trên nhiều thiết bị, khó chọn đúng size khi không thử đồ, và nhu cầu bán độc quyền cho cộng "
        "đồng khách hàng của từng vận động viên (athlete).")
    R.p("Nhóm theo cách tiếp cận phát triển lặp, tăng dần: khảo sát website tham khảo, phân tích yêu cầu bằng sơ đồ "
        "Use case, ERD, DFD và BPMN, rồi xây dựng web tĩnh không cần máy chủ ứng dụng. Toàn bộ nghiệp vụ chạy trong trình "
        "duyệt: dữ liệu sản phẩm đọc từ JSON bằng `fetch`, bảng phí vận chuyển đọc từ XML bằng `XMLHttpRequest`, giao "
        "diện vẽ bằng DOM, trạng thái lưu bằng Web Storage, mật khẩu băm SHA-256 kèm salt. Website có " +
        str(ctx["n_products"]) + " sản phẩm, " + str(ctx["n_reviews"]) + " đánh giá, cổng truy cập bằng mã athlete, "
        "giỏ hàng, thanh toán có kiểm tra dữ liệu (kể cả thuật toán Luhn cho số thẻ), tài khoản khách hàng, trang quản "
        "trị tám chức năng và công cụ gợi ý size dựa trên hồi quy tuyến tính từ bộ số đo cơ thể ANSUR II (" +
        "{:,}".format(sc["him"]["sampleSize"] + sc["her"]["sampleSize"]).replace(",", ".") + " người). Song song, nhóm "
        "cài đặt thử WooCommerce trên WordPress để so sánh với cách tự lập trình.")
    lh = [r for r in ctx["lighthouse"] if r["mode"] == "desktop"]
    gate_after = [r for r in lh if r["name"] == "Gate"][0]
    gate_before = [r for r in ctx["lighthouse_before"] if r["mode"] == "desktop" and r["name"] == "Gate"][0]
    tests = ctx["tests"]
    R.p("Kết quả đánh giá cho thấy " + str(sum(t["ok"] for t in tests)) + "/" + str(len(tests)) + " ca kiểm thử chức "
        "năng tự động đạt, cả trên máy lẫn trên bản triển khai; Google Lighthouse cho điểm Accessibility và SEO 100 ở cả 5 "
        "trang chính, hiệu năng trên máy tính " + str(min(r["performance"] for r in lh)) + " - 100; mã HTML không còn lỗi "
        "theo W3C Nu Html Checker. Vòng đo - sửa - đo lại giúp đưa chỉ số xô lệch bố cục (CLS) của trang cổng từ " +
        gate_before["CLS"].replace(".", ",") + " về " + gate_after["CLS"].replace(".", ",") + " và điểm hiệu năng của trang "
        "này từ " + str(gate_before["performance"]) + " lên " + str(gate_after["performance"]) + " (máy tính). Mô "
        "hình gợi ý size đoán đúng size của " + str(sc["him"]["exactSizePct"]).replace(".", ",") + "% nam và " +
        str(sc["her"]["exactSizePct"]).replace(".", ",") + "% nữ trong dữ liệu, sai không quá một size với " +
        str(sc["him"]["withinOneSizePct"]).replace(".", ",") + "% nam và " + str(sc["her"]["withinOneSizePct"]).replace(".", ",") +
        "% nữ. Các hạn chế chính là bảo mật chỉ ở mức mô phỏng phía máy khách, dữ liệu nằm riêng trong từng trình duyệt, "
        "và trang chủ tải chậm trên điện thoại do video dung lượng lớn. Báo cáo đề "
        "xuất hướng phát triển: bổ sung máy chủ và cơ sở dữ liệu, cổng thanh toán thật, và đưa cửa hàng lên nền tảng "
        "WooCommerce khi kinh doanh thật.")
    R.p("**Từ khoá:** thương mại điện tử, thiết kế web đáp ứng, JavaScript, DOM, AJAX, XML, gợi ý size, WooCommerce.",
        indent=False)
