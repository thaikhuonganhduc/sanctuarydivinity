# -*- coding: utf-8 -*-
"""Các hàm dựng file Word (python-docx) cho báo cáo, trình bày theo báo cáo mẫu giảng viên cung cấp:
- A4, lề 2 cm bốn phía; Times New Roman 13; giãn dòng 1,5; không cách đoạn; thụt đầu dòng 1,27 cm; căn đều.
- PHẦN và CHƯƠNG: in đậm, viết hoa, căn giữa. Mục 1.1: in đậm. Mục 1.1.1: in đậm nghiêng, thụt 1,27 cm.
- Gạch đầu dòng cấp 1 là "-", cấp 2 là "●".
- Bảng: chú thích nghiêng ở TRÊN bảng ("Bảng B.2.1. ..."); hình: chú thích nghiêng ở DƯỚI hình ("Hình B.7.1. ...").
- Số trang ở giữa chân trang; phần đầu đánh số La Mã."""
import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
from docx.shared import Pt, Cm, RGBColor

FONT = "Times New Roman"
BLACK = RGBColor(0, 0, 0)
J = WD_ALIGN_PARAGRAPH.JUSTIFY
C = WD_ALIGN_PARAGRAPH.CENTER
L = WD_ALIGN_PARAGRAPH.LEFT


def set_font(obj, size=None, bold=None, italic=None, name=FONT, color=BLACK):
    f = obj.font
    f.name = name
    if size is not None:
        f.size = Pt(size)
    if bold is not None:
        f.bold = bold
    if italic is not None:
        f.italic = italic
    if color is not None:
        f.color.rgb = color
    rpr = obj.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(a), name)
    # Kiểu Heading mặc định dùng phông theo theme (asciiTheme...), thuộc tính này đè lên tên phông -> xoá đi
    for a in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        if rfonts.get(qn(a)) is not None:
            del rfonts.attrib[qn(a)]


def fmt(p, align=None, first=None, left=None, before=0, after=0, line=1.5, keep_next=None):
    """first: thụt dòng đầu (cm, âm = thụt treo); left: lề trái của đoạn (cm)."""
    pf = p.paragraph_format
    if align is not None:
        pf.alignment = align
    pf.first_line_indent = Cm(first if first is not None else 0)
    pf.left_indent = Cm(left if left is not None else 0)
    pf.space_before, pf.space_after, pf.line_spacing = Pt(before), Pt(after), line
    if keep_next is not None:
        pf.keep_with_next = keep_next


class Report:
    def __init__(self):
        self.doc = Document()
        self.part = ""          # "A", "B", "C"
        self.chap = 0
        self.fig_no = 0
        self.tab_no = 0
        self._styles()
        sec = self.doc.sections[0]
        sec.page_height, sec.page_width = Cm(29.7), Cm(21)
        self._margins(sec)

    # ================= Kiểu chữ =================
    def _styles(self):
        st = self.doc.styles
        n = st["Normal"]
        set_font(n, 13)
        fmt(n, align=J, first=1.27)
        heads = [  # tên, căn, đậm, nghiêng, viết hoa, thụt trái, thụt dòng đầu
            ("Heading 1", C, True, False, True, 0, 0),       # PHẦN, LỜI MỞ ĐẦU, TÀI LIỆU THAM KHẢO...
            ("Heading 2", C, True, False, True, 0, 0),       # CHƯƠNG
            ("Heading 3", L, True, False, False, 0.63, 0),   # 1.1.
            ("Heading 4", J, True, True, False, 0, 1.27),    # 1.1.1.
            ("Heading 5", J, True, True, False, 0, 1.27),    # 1.1.1.1.
        ]
        for name, al, b, i, caps, left, first in heads:
            s = st[name]
            set_font(s, 13, b, i)
            fmt(s, align=al, first=first, left=left, keep_next=True)
            s.font.all_caps = caps
            s.paragraph_format.widow_control = True
        for name in ("HinhCaption", "BangCaption"):
            s = st.add_style(name, 1)
            s.base_style = n
            set_font(s, 12, False, True)
            fmt(s, align=C, line=1.3, before=3 if name == "HinhCaption" else 6, after=6 if name == "HinhCaption" else 3)
        st["BangCaption"].paragraph_format.keep_with_next = True
        s = st.add_style("CellText", 1)
        s.base_style = n
        set_font(s, 13)
        fmt(s, align=J, line=1.3, before=1, after=1)
        s = st.add_style("CodeText", 1)
        s.base_style = n
        set_font(s, 9.5, name="Consolas")
        fmt(s, align=L, line=1.0)
        s = st.add_style("Bullet1", 1)
        s.base_style = n
        fmt(s, align=J, first=-0.64, left=1.27)
        s = st.add_style("Bullet2", 1)
        s.base_style = n
        fmt(s, align=J, first=-0.64, left=1.91)
        for i in (1, 2, 3):
            try:
                s = st["TOC %d" % i]
            except KeyError:
                s = st.add_style("TOC %d" % i, 1)
            set_font(s, 13, bold=(i < 3))
            fmt(s, align=L, line=1.3, after=2, left=[0, 0.4, 0.9][i - 1])

    def _margins(self, sec):
        sec.top_margin = sec.bottom_margin = sec.left_margin = sec.right_margin = Cm(2)
        sec.header_distance, sec.footer_distance = Cm(1), Cm(1)

    # ================= Phần (section) và số trang =================
    def new_section(self, page_fmt, start=1):
        sec = self.doc.add_section(WD_SECTION.NEW_PAGE)
        self._margins(sec)
        for old in sec._sectPr.findall(qn("w:pgNumType")):
            sec._sectPr.remove(old)
        pg = OxmlElement("w:pgNumType")
        pg.set(qn("w:fmt"), page_fmt)
        pg.set(qn("w:start"), str(start))
        # Chuẩn OOXML: pgNumType đứng trước cols/docGrid
        nxt = next((c for c in sec._sectPr if c.tag in (qn("w:cols"), qn("w:docGrid"), qn("w:titlePg"))), None)
        if nxt is not None:
            nxt.addprevious(pg)
        else:
            sec._sectPr.append(pg)
        sec.footer.is_linked_to_previous = False
        p = sec.footer.paragraphs[0]
        p.alignment = C
        p.paragraph_format.first_line_indent = Cm(0)
        self.field(p, "PAGE", "1", size=13)
        return sec

    def field(self, paragraph, instr, placeholder="", size=None):
        def run_with(el):
            r = paragraph.add_run()
            if size:
                set_font(r, size)
            r._r.append(el)
        b = OxmlElement("w:fldChar"); b.set(qn("w:fldCharType"), "begin"); run_with(b)
        it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = " %s " % instr; run_with(it)
        s = OxmlElement("w:fldChar"); s.set(qn("w:fldCharType"), "separate"); run_with(s)
        r = paragraph.add_run(placeholder)
        if size:
            set_font(r, size)
        e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), "end"); run_with(e)

    # ================= Chữ =================
    def _runs(self, p, text, size=None, bold=None, italic=None):
        """Định dạng nhanh trong chuỗi: **đậm**, *nghiêng*, ***đậm nghiêng***, `mã`."""
        for part in re.split(r"(\*\*\*.+?\*\*\*|\*\*.+?\*\*|\*[^*\s][^*]*?\*|`[^`]+`)", text):
            if not part:
                continue
            if part.startswith("***"):
                r = p.add_run(part[3:-3]); r.bold = True; r.italic = True
            elif part.startswith("**"):
                r = p.add_run(part[2:-2]); r.bold = True
            elif part.startswith("`"):
                r = p.add_run(part[1:-1]); set_font(r, (size or 13) - 1, name="Consolas")
                continue
            elif part.startswith("*"):
                r = p.add_run(part[1:-1]); r.italic = True
            else:
                r = p.add_run(part)
            if size:
                r.font.size = Pt(size)
            if bold:
                r.bold = True
            if italic:
                r.italic = True

    def p(self, text, align=None, indent=True, size=None, bold=None, italic=None, keep_next=None, style=None):
        para = self.doc.add_paragraph(style=style)
        if not indent:
            para.paragraph_format.first_line_indent = Cm(0)
        if align is not None:
            para.alignment = align
        if keep_next:
            para.paragraph_format.keep_with_next = True
        self._runs(para, text, size, bold, italic)
        return para

    def ps(self, *texts):
        for t in texts:
            self.p(t)

    def bullets(self, items, level=1):
        """items: chuỗi, hoặc (chuỗi, [mục con...]) để có gạch đầu dòng cấp 2."""
        for it in items:
            sub = None
            if isinstance(it, tuple):
                it, sub = it
            para = self.doc.add_paragraph(style="Bullet1" if level == 1 else "Bullet2")
            para.paragraph_format.tab_stops.add_tab_stop(Cm(1.27 if level == 1 else 1.91), WD_TAB_ALIGNMENT.LEFT)
            para.add_run(("-" if level == 1 else "●") + "\t")
            self._runs(para, it)
            if sub:
                self.bullets(sub, level=2)

    # ================= Tiêu đề =================
    def front_heading(self, text, page_break=True):
        """Tiêu đề phần đầu/cuối (LỜI MỞ ĐẦU, TÀI LIỆU THAM KHẢO...): Heading 1 để vào mục lục."""
        h = self.doc.add_heading(text, level=1)
        h.paragraph_format.page_break_before = page_break
        self.part = ""
        return h

    def part_heading(self, letter, title):
        # Phần A mở đầu nội dung chính: section mới, số trang Ả Rập bắt đầu từ 1 (section mới đã sang trang)
        first = not getattr(self, "_body_started", False)
        if first:
            self.new_section("decimal", 1)
            self._body_started = True
        self.part = letter
        h = self.doc.add_heading("PHẦN %s. %s" % (letter, title), level=1)
        h.paragraph_format.page_break_before = not first
        self._first_chapter = True
        return h

    def chapter(self, num, title):
        self.chap, self.fig_no, self.tab_no = num, 0, 0
        h = self.doc.add_heading("CHƯƠNG %d. %s" % (num, title), level=2)
        h.paragraph_format.page_break_before = not getattr(self, "_first_chapter", False)
        self._first_chapter = False
        return h

    def h3(self, text):
        return self.doc.add_heading(text, level=3)

    def h4(self, text):
        return self.doc.add_heading(text, level=4)

    def h5(self, text):
        return self.doc.add_heading(text, level=5)

    def page_break(self):
        self.doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    # ================= Hình =================
    def _label(self, kind, n):
        return "%s %s.%d.%d" % (kind, self.part, self.chap, n) if self.part else "%s %d" % (kind, n)

    def next_fig(self, k=1):
        return self._label("Hình", self.fig_no + k)

    def next_tab(self, k=1):
        return self._label("Bảng", self.tab_no + k)

    @staticmethod
    def _fit_image(path, max_px=2400):
        """Ảnh lớn hơn max_px thì lưu bản thu nhỏ vào img/_fit/ để file Word nhẹ (2400 px trên 17 cm ~ 360 dpi)."""
        from PIL import Image
        path = Path(path)
        im = Image.open(path)
        # Word (python-docx) không nhận WebP: đổi sang PNG; ảnh nhỏ, đúng định dạng thì dùng luôn
        if max(im.size) <= max_px and path.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".bmp"):
            return path
        out = Path(__file__).resolve().parent / "img" / "_fit" / (path.parent.name + "-" + path.stem + ".png")
        out.parent.mkdir(parents=True, exist_ok=True)
        if not out.exists() or out.stat().st_mtime < path.stat().st_mtime:
            im = im.convert("RGB")
            im.thumbnail((max_px, max_px), Image.LANCZOS)
            im.save(out, optimize=True)
        return out

    def figure(self, path, caption, width=15.5, height=None):
        path = self._fit_image(path)
        self.fig_no += 1
        para = self.doc.add_paragraph()
        fmt(para, align=C, line=1.0, before=6, keep_next=True)
        if height:
            para.add_run().add_picture(str(path), height=Cm(height))
        else:
            para.add_run().add_picture(str(path), width=Cm(width))
        cap = self.doc.add_paragraph(style="HinhCaption")
        self._runs(cap, self._label("Hình", self.fig_no) + ". " + caption)
        return self._label("Hình", self.fig_no)

    # ================= Bảng =================
    def table(self, headers, rows, widths=None, caption=None, size=12, header_fill="D9D9D9", center_cols=(),
              bold_first=False, tight=False, align_cells=L, col_fills=None):
        """rows: danh sách hàng; ô có thể là (chữ, màu nền). col_fills: màu nền theo cột cho tiêu đề."""
        # Theo báo cáo mẫu: chữ trong bảng cỡ 13, giãn dòng 1,5. Bảng nhiều cột (cỡ < 11) giữ chữ nhỏ để không tràn.
        size = 13 if size >= 12 else (12 if size >= 11 else size)
        self._cell_line = 1.5 if size >= 12 else 1.15
        if caption:
            self.tab_no += 1
            cap = self.doc.add_paragraph(style="BangCaption")
            self._runs(cap, self._label("Bảng", self.tab_no) + ". " + caption)
        t = self.doc.add_table(rows=1 if headers else 0, cols=len(widths) if widths else len(headers))
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        if headers:
            for i, h in enumerate(headers):
                c = t.rows[0].cells[i]
                self._cell(c, h, size, bold=True, align=C)
                self._shade(c, (col_fills[i] if col_fills else header_fill))
            tr_pr = t.rows[0]._tr.get_or_add_trPr()
            hdr = OxmlElement("w:tblHeader"); hdr.set(qn("w:val"), "true"); tr_pr.append(hdr)
        for row in rows:
            cells = t.add_row().cells
            for i, v in enumerate(row):
                fill = None
                if isinstance(v, tuple):
                    v, fill = v
                self._cell(cells[i], str(v), size, bold=(bold_first and i == 0), align=(C if i in center_cols else align_cells))
                if fill:
                    self._shade(cells[i], fill)
        if widths:
            self._set_widths(t, widths)
        if tight:
            mar = parse_xml('<w:tblCellMar %s><w:left w:w="28" w:type="dxa"/><w:right w:w="28" w:type="dxa"/></w:tblCellMar>'
                            % nsdecls("w"))
            look = t._tbl.tblPr.find(qn("w:tblLook"))
            if look is not None:
                look.addprevious(mar)
            else:
                t._tbl.tblPr.append(mar)
        gap = self.doc.add_paragraph()
        fmt(gap, line=1.0, after=4)
        return t

    def kv_table(self, rows, caption=None, widths=(4.2, 12.8), size=12.5):
        """Bảng 2 cột không có hàng tiêu đề (mô tả use case): cột trái in đậm, căn giữa."""
        return self.table(None, rows, widths=list(widths), caption=caption, size=size, bold_first=True, center_cols=(0,),
                          align_cells=J)

    @staticmethod
    def _set_widths(t, widths):
        for i, w in enumerate(widths):
            t.columns[i].width = Cm(w)
            for cell in t.columns[i].cells:
                cell.width = Cm(w)
        tbl_pr = t._tbl.tblPr
        tbl_w = tbl_pr.find(qn("w:tblW"))
        if tbl_w is None:
            tbl_w = OxmlElement("w:tblW")
            tbl_pr.append(tbl_w)
        tbl_w.set(qn("w:type"), "dxa")
        tbl_w.set(qn("w:w"), str(int(sum(widths) * 567)))
        for old in tbl_pr.findall(qn("w:tblLayout")):
            tbl_pr.remove(old)
        layout = OxmlElement("w:tblLayout"); layout.set(qn("w:type"), "fixed")
        nxt = next((c for c in tbl_pr if c.tag in (qn("w:tblCellMar"), qn("w:tblLook"))), None)
        if nxt is not None:
            nxt.addprevious(layout)
        else:
            tbl_pr.append(layout)

    def _cell(self, cell, text, size, bold=False, align=J):
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        para = cell.paragraphs[0]
        for k, line in enumerate(text.split("\n")):
            if k:
                para = cell.add_paragraph()
            para.style = self.doc.styles["CellText"]
            para.alignment = align
            para.paragraph_format.line_spacing = getattr(self, "_cell_line", 1.3)
            self._runs(para, line, size=size, bold=bold or None)

    @staticmethod
    def _shade(cell, fill):
        tc_pr = cell._tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), fill)
        nxt = next((c for c in tc_pr if c.tag in (qn("w:noWrap"), qn("w:tcMar"), qn("w:textDirection"),
                                                   qn("w:tcFitText"), qn("w:vAlign"), qn("w:hideMark"))), None)
        if nxt is not None:
            nxt.addprevious(shd)
        else:
            tc_pr.append(shd)

    def code(self, text, caption=None):
        if caption:
            self.p(caption, indent=False, italic=True, size=12, keep_next=True)
        t = self.doc.add_table(rows=1, cols=1)
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = t.rows[0].cells[0]
        self._set_widths(t, [16.5])
        self._shade(c, "F2F2F2")
        para = c.paragraphs[0]
        for k, line in enumerate(text.strip("\n").split("\n")):
            if k:
                para = c.add_paragraph()
            para.style = self.doc.styles["CodeText"]
            set_font(para.add_run(line if line else " "), 9.5, name="Consolas")
        gap = self.doc.add_paragraph()
        fmt(gap, line=1.0, after=4)

    # ================= Ảnh nền trang bìa =================
    def background_image(self, path):
        para = self.doc.paragraphs[0] if self.doc.paragraphs else self.doc.add_paragraph()
        inline = para.add_run().add_picture(str(path), width=Cm(21), height=Cm(29.7))._inline
        graphic = inline.find(qn("a:graphic"))
        anchor = parse_xml(
            '<wp:anchor %s distT="0" distB="0" distL="0" distR="0" simplePos="0" relativeHeight="0" '
            'behindDoc="1" locked="1" layoutInCell="1" allowOverlap="1">'
            '<wp:simplePos x="0" y="0"/>'
            '<wp:positionH relativeFrom="page"><wp:posOffset>0</wp:posOffset></wp:positionH>'
            '<wp:positionV relativeFrom="page"><wp:posOffset>0</wp:posOffset></wp:positionV>'
            '<wp:extent cx="%d" cy="%d"/><wp:effectExtent l="0" t="0" r="0" b="0"/><wp:wrapNone/>'
            '<wp:docPr id="900" name="Cover background"/><wp:cNvGraphicFramePr/></wp:anchor>'
            % (nsdecls("wp", "a", "pic", "r"), Cm(21), Cm(29.7)))
        anchor.append(graphic)
        inline.getparent().replace(inline, anchor)
        return para

    def save(self, path):
        cp = self.doc.core_properties
        cp.title = "Báo cáo đồ án Phát triển Web kinh doanh - Website SANCTUARY"
        cp.author = "Nhóm SANCTUARY - UEL"
        cp.language = "vi-VN"
        self.doc.save(str(path))
