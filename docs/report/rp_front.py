# -*- coding: utf-8 -*-
"""Bìa (mẫu của giảng viên), lời mở đầu, lời cảm ơn, lời cam kết, mục lục, danh mục hình/bảng, tóm tắt."""
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx_helpers import set_font, fmt, C, J

RIGHT = WD_ALIGN_PARAGRAPH.RIGHT

MEMBERS = [
    ("Thái Khương Anh Đức", "K234161828", "Nhóm trưởng"),
    ("Nguyễn Phan Bảo Hân", "K244161782", "Thành viên"),
    ("Lê Mai Ngọc Ánh", "K244030341", "Thành viên"),
    ("Nguyễn Gia Bảo", "K244030343", "Thành viên"),
    ("Lê Vy", "K244161824", "Thành viên"),
]
TOPIC = "XÂY DỰNG WEBSITE THƯƠNG MẠI ĐIỆN TỬ BÁN QUẦN ÁO GYM “SANCTUARY”"


def cover(R, ctx):
    doc = R.doc
    R.background_image(ctx["img"] / "cover-bg.png")
    first = doc.paragraphs[0]
    fmt(first, line=1.0)

    def line(text, size, before=0, bold=True, italic=False, align=C):
        p = doc.add_paragraph()
        fmt(p, align=align, before=before, line=1.15)
        set_font(p.add_run(text), size, bold, italic)
        return p

    line("KHOA HỆ THỐNG THÔNG TIN", 18, before=44)
    line("ĐỒ ÁN CUỐI KỲ MÔN PHÁT TRIỂN WEB KINH DOANH", 16, before=176)
    line("TÊN ĐỀ TÀI: " + TOPIC, 16, before=8)
    p = line("", 14, before=14, align=RIGHT)
    set_font(p.add_run("GVHD: "), 14, True, True)
    set_font(p.add_run("TS. Trần Duy Thanh"), 14, True, False)
    p = line("", 13, before=2, align=RIGHT)
    set_font(p.add_run("Lớp học phần: 261BIE503002"), 13, False, False)
    line("Thành viên nhóm", 14, before=22, italic=True)
    t = doc.add_table(rows=1, cols=3)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(["Họ và tên", "Mã số sinh viên", "Mức độ hoàn thành"]):
        R._cell(t.rows[0].cells[i], h, 13, bold=True, align=C)
    for name, mssv, _ in MEMBERS:
        cells = t.add_row().cells
        for i, v in enumerate([name, mssv, "100%"]):
            R._cell(cells[i], v, 13, align=C)
    for row in t.rows:
        row.height = Cm(0.85)
    R._set_widths(t, [6.0, 5.0, 4.5])
    line("TP. Hồ Chí Minh, ngày 22 tháng 11 năm 2026", 13, before=26, bold=False, italic=True)


def build(R, ctx):
    cover(R, ctx)
    R.new_section("lowerRoman", 1)

    # ---------- Lời mở đầu ----------
    R.front_heading("LỜI MỞ ĐẦU", page_break=False)
    R.ps(
        "Thương mại điện tử đã trở thành kênh bán hàng chính của nhiều thương hiệu thời trang, đặc biệt là các thương "
        "hiệu nhỏ hướng tới giới trẻ. Với dòng quần áo tập gym cao cấp, cách bán hàng còn đặc biệt hơn: sản phẩm ra mắt "
        "theo từng đợt giới hạn (drop), khách hàng chủ yếu đến từ cộng đồng của các vận động viên, người có ảnh hưởng, và "
        "trải nghiệm thương hiệu quan trọng không kém chính sản phẩm. Website vì thế không chỉ là nơi trưng bày hàng hoá "
        "mà còn là “không gian” để thương hiệu kể câu chuyện của mình.",
        "Từ nhận định đó, nhóm phát triển **“SANCTUARY”**, website thương mại điện tử cho một thương hiệu quần áo gym mang "
        "phong cách tối, gai góc và cao cấp. SANCTUARY không chỉ có các chức năng bán hàng thông thường như xem sản phẩm, "
        "giỏ hàng, thanh toán, mà còn mô phỏng trọn vẹn mô hình drop: trang cổng có đồng hồ đếm ngược, khách vào cửa hàng "
        "bằng mã của từng athlete, công cụ gợi ý size dựa trên dữ liệu số đo cơ thể thật, cùng trang quản trị giúp chủ cửa "
        "hàng theo dõi doanh thu, đơn hàng, sản phẩm và mã athlete.",
        "Đồ án được xây dựng bằng HTML5, CSS3 (kèm bộ tiền xử lý LESS) và JavaScript thuần, dữ liệu lưu ở JSON và XML, đọc "
        "bằng AJAX, giao diện điều khiển qua mô hình DOM, triển khai trực tuyến trên Vercel. Bên cạnh đó, nhóm cài đặt và "
        "quản trị thử nền tảng mã nguồn mở WooCommerce để so sánh với cách tự lập trình. Toàn bộ quá trình được thực hiện "
        "theo tư duy phân tích - thiết kế bài bản: từ hình thành ý tưởng kinh doanh, phân tích nghiệp vụ, mô hình hoá hệ "
        "thống, thiết kế dữ liệu và giao diện, cho đến kiểm thử và đo lường chất lượng.",
        "Thông qua SANCTUARY, nhóm mong muốn thể hiện khả năng vận dụng kiến thức của học phần Phát triển Web kinh doanh "
        "vào một sản phẩm hoàn chỉnh, chạy được trên môi trường thật và có giá trị tham khảo cho các thương hiệu thời trang "
        "nhỏ muốn bán hàng trực tuyến.")

    # ---------- Lời cảm ơn + Lời cam kết ----------
    R.front_heading("LỜI CẢM ƠN")
    R.ps(
        "Lời đầu tiên, nhóm xin chân thành cảm ơn Trường Đại học Kinh tế - Luật, ĐHQG-HCM cùng quý thầy cô Khoa Hệ thống "
        "thông tin đã đưa học phần Phát triển Web kinh doanh vào chương trình đào tạo. Những kiến thức của môn học không chỉ "
        "giúp nhóm hoàn thành đồ án mà còn là hành trang quý báu cho công việc sau này.",
        "Nhóm đặc biệt gửi lời cảm ơn sâu sắc đến **TS. Trần Duy Thanh**, giảng viên hướng dẫn, đã tận tình truyền đạt kiến "
        "thức về HTML, CSS, JavaScript, XML, mô hình DOM, các hệ thống thương mại điện tử mã nguồn mở, cũng như giải đáp "
        "những thắc mắc của nhóm trong suốt quá trình thực hiện. Dù đã cố gắng hoàn thiện đồ án ở mức tốt nhất, nhóm không "
        "tránh khỏi thiếu sót; nhóm rất mong nhận được góp ý của thầy để hoàn thiện hơn.",
        "Cuối cùng, nhóm xin kính chúc thầy thật nhiều sức khoẻ và thành công trong sự nghiệp trồng người.")
    R.p("Nhóm sinh viên thực hiện", align=RIGHT, indent=False, italic=True)
    h = R.front_heading("LỜI CAM KẾT", page_break=False)
    h.paragraph_format.space_before = Pt(18)
    R.ps(
        "Nhóm xin cam kết toàn bộ nội dung đồ án “Xây dựng website thương mại điện tử bán quần áo gym SANCTUARY” là kết quả "
        "nghiên cứu và làm việc nghiêm túc của các thành viên trong nhóm, tuân thủ yêu cầu và quy định của học phần. Các tài "
        "liệu, số liệu tham khảo đều được trích dẫn đầy đủ theo chuẩn APA.",
        "Danh mục sản phẩm, mô tả, hình ảnh và đánh giá mẫu được tham khảo từ website breathedivinity.com để làm dữ liệu học "
        "tập theo cho phép của giảng viên; tên thương hiệu, logo và toàn bộ mã nguồn SANCTUARY là của nhóm. Website là đồ án "
        "học tập, không kinh doanh thật. Nếu có sai sót, nhóm xin hoàn toàn chịu trách nhiệm.")
    R.p("Nhóm sinh viên thực hiện", align=RIGHT, indent=False, italic=True)

    # ---------- Mục lục và danh mục ----------
    R.front_heading("MỤC LỤC")
    p = R.doc.add_paragraph(); p.paragraph_format.first_line_indent = Cm(0)
    R.field(p, 'TOC \\o "1-3" \\h \\z \\u', "Mở bằng Word và cập nhật trường để hiện mục lục.")
    R.front_heading("DANH MỤC HÌNH ẢNH")
    p = R.doc.add_paragraph(); p.paragraph_format.first_line_indent = Cm(0)
    R.field(p, 'TOC \\h \\z \\t "HinhCaption,1"', "Cập nhật trường để hiện danh mục hình.")
    R.front_heading("DANH MỤC BẢNG BIỂU")
    p = R.doc.add_paragraph(); p.paragraph_format.first_line_indent = Cm(0)
    R.field(p, 'TOC \\h \\z \\t "BangCaption,1"', "Cập nhật trường để hiện danh mục bảng.")

    # ---------- Tóm tắt ----------
    R.front_heading("TÓM TẮT")
    sc = ctx["size_chart"]
    lh = [r for r in ctx["lighthouse"] if r["mode"] == "desktop"]
    tests = ctx["tests"]
    R.ps(
        "Đồ án xây dựng website **“SANCTUARY”**, nền tảng thương mại điện tử cho một thương hiệu quần áo tập gym cao cấp "
        "bán theo từng đợt ra mắt giới hạn (drop). Website được phát triển bằng HTML5, CSS3/LESS và JavaScript thuần theo "
        "kiến trúc web tĩnh, dữ liệu sản phẩm lưu ở JSON và phí vận chuyển lưu ở XML, đọc bằng AJAX (`fetch` và "
        "`XMLHttpRequest`), trạng thái người dùng lưu bằng Web Storage, triển khai trên Vercel tại "
        "sanctuarydivinity.vercel.app.",
        "SANCTUARY cho phép khách vào cửa hàng bằng mã của từng athlete, xem " + str(ctx["n_products"]) + " sản phẩm theo ba "
        "dòng nam, nữ và phụ kiện, lọc theo size, màu, sắp xếp theo giá, đổi 15 loại tiền tệ, xem " + str(ctx["n_reviews"]) +
        " đánh giá có ảnh, nhận gợi ý size từ chiều cao và cân nặng dựa trên bộ số đo cơ thể ANSUR II, đặt hàng với phí vận "
        "chuyển và thuế tính theo nước nhận, quản lý tài khoản và lịch sử đơn. Trang quản trị gồm tám chức năng: tổng quan "
        "doanh thu, đơn hàng, sản phẩm, khách hàng, tin nhắn, mã athlete, ngày ra mắt và sao lưu dữ liệu. Song song, nhóm cài "
        "đặt và quản trị thử WooCommerce trên WordPress.",
        "Kết quả kiểm chứng: " + str(sum(t["ok"] for t in tests)) + "/" + str(len(tests)) + " ca kiểm thử chức năng tự động "
        "đạt trên cả máy cá nhân và bản triển khai; Google Lighthouse cho điểm Accessibility và SEO 100, hiệu năng trên máy "
        "tính " + str(min(r["performance"] for r in lh)) + " - 100; mã HTML không còn lỗi theo W3C. Công cụ gợi ý size đúng "
        "size với " + str(sc["him"]["exactSizePct"]).replace(".", ",") + "% nam, " + str(sc["her"]["exactSizePct"]).replace(".", ",") +
        "% nữ và lệch không quá một size với hơn 97% trường hợp. Đồ án thể hiện sự kết hợp giữa ý tưởng kinh doanh, phân "
        "tích nghiệp vụ, thiết kế giao diện và kỹ thuật lập trình web phía máy khách.")
