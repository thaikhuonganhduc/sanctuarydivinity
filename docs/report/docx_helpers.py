# -*- coding: utf-8 -*-
"""Các hàm dựng file Word (python-docx) dùng cho build_report.py.
Định dạng: Times New Roman 13, thụt đầu dòng 1,27 cm, giãn dòng 1,5, lề trái 3 cm, phải 2 cm, trên/dưới 2 cm."""
import re
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
from docx.shared import Pt, Cm, RGBColor, Emu

FONT = "Times New Roman"
BLACK = RGBColor(0, 0, 0)


def set_font(run_or_style, size=None, bold=None, italic=None, name=FONT, color=BLACK):
    f = run_or_style.font
    f.name = name
    if size is not None:
        f.size = Pt(size)
    if bold is not None:
        f.bold = bold
    if italic is not None:
        f.italic = italic
    if color is not None:
        f.color.rgb = color
    el = run_or_style.element
    rpr = el.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(a), name)


def para_format(p_or_style, align=None, indent=None, before=0, after=6, line=1.5, keep_next=None, left=None, hanging=None):
    pf = p_or_style.paragraph_format
    if align is not None:
        pf.alignment = align
    # indent=None nghĩa là KHÔNG thụt (đặt 0); để None thì kiểu sẽ kế thừa 1,27 cm của Normal
    pf.first_line_indent = Cm(indent) if indent is not None else Cm(0)
    if hanging is not None:
        pf.first_line_indent = Cm(-hanging)
    if left is not None:
        pf.left_indent = Cm(left)
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line
    if keep_next is not None:
        pf.keep_with_next = keep_next


class Report:
    def __init__(self):
        self.doc = Document()
        self.chapter = "0"
        self.fig_no = 0
        self.tab_no = 0
        self._setup_styles()
        sec = self.doc.sections[0]
        sec.page_height, sec.page_width = Cm(29.7), Cm(21)
        self._margins(sec)

    # ---------- Kiểu chữ ----------
    def _setup_styles(self):
        st = self.doc.styles
        normal = st["Normal"]
        set_font(normal, 13)
        para_format(normal, align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=1.27, after=6, line=1.5)
        for name, size, bold, italic, align, before, after, upper in [
            ("Heading 1", 14, True, False, WD_ALIGN_PARAGRAPH.CENTER, 0, 18, True),
            ("Heading 2", 13, True, False, WD_ALIGN_PARAGRAPH.LEFT, 12, 6, False),
            ("Heading 3", 13, True, True, WD_ALIGN_PARAGRAPH.LEFT, 8, 4, False)]:
            s = st[name]
            set_font(s, size, bold, italic)
            para_format(s, align=align, indent=None, before=before, after=after, line=1.5, keep_next=True)
            s.font.all_caps = upper
        st["Heading 1"].paragraph_format.page_break_before = True
        for name, size in [("Title", 14)]:
            set_font(st[name], size, True)
        # Chú thích hình / bảng (dùng để tạo Danh mục hình, Danh mục bảng)
        for name in ("HinhCaption", "BangCaption"):
            s = st.add_style(name, 1)
            s.base_style = normal
            set_font(s, 12, False, True)
            para_format(s, align=WD_ALIGN_PARAGRAPH.CENTER, indent=None, before=4, after=10, line=1.15)
        st["BangCaption"].paragraph_format.keep_with_next = True
        st["BangCaption"].paragraph_format.space_before = Pt(8)
        st["BangCaption"].paragraph_format.space_after = Pt(4)
        s = st.add_style("FrontTitle", 1)
        s.base_style = normal
        set_font(s, 14, True)
        para_format(s, align=WD_ALIGN_PARAGRAPH.CENTER, indent=None, after=18, line=1.5)
        s.font.all_caps = True
        s = st.add_style("CellText", 1)
        s.base_style = normal
        set_font(s, 12)
        para_format(s, align=WD_ALIGN_PARAGRAPH.LEFT, indent=None, before=1, after=1, line=1.1)
        s = st.add_style("CodeText", 1)
        s.base_style = normal
        set_font(s, 9.5, name="Consolas")
        para_format(s, align=WD_ALIGN_PARAGRAPH.LEFT, indent=None, before=0, after=0, line=1.0)
        for lst in ("List Bullet", "List Number"):
            s = st[lst]
            set_font(s, 13)
            para_format(s, align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=None, after=3, line=1.5, left=1.27, hanging=0.5)
        # Mục lục: chữ Times New Roman
        for i in (1, 2, 3):
            try:
                s = st["TOC %d" % i]
            except KeyError:
                s = st.add_style("TOC %d" % i, 1)
            set_font(s, 13, bold=(i == 1))
            para_format(s, align=WD_ALIGN_PARAGRAPH.LEFT, indent=None, after=2, line=1.3, left=0.6 * (i - 1))

    def _margins(self, sec):
        sec.top_margin, sec.bottom_margin = Cm(2), Cm(2)
        sec.left_margin, sec.right_margin = Cm(3), Cm(2)
        sec.header_distance, sec.footer_distance = Cm(1), Cm(1)

    # ---------- Phần (section) và số trang ----------
    def new_section(self, page_fmt=None, start=None, footer=True):
        sec = self.doc.add_section(WD_SECTION.NEW_PAGE)
        self._margins(sec)
        for old in sec._sectPr.findall(qn("w:pgNumType")):      # section mới chép cả thẻ của section trước -> xoá
            sec._sectPr.remove(old)
        if page_fmt:
            pg = OxmlElement("w:pgNumType")
            pg.set(qn("w:fmt"), page_fmt)
            if start is not None:
                pg.set(qn("w:start"), str(start))
            # Chuẩn OOXML bắt buộc pgNumType đứng TRƯỚC cols/docGrid trong sectPr, sai thứ tự Word báo file lỗi
            nxt = next((c for c in sec._sectPr if c.tag in (qn("w:cols"), qn("w:formProt"), qn("w:vAlign"),
                                                             qn("w:noEndnote"), qn("w:titlePg"), qn("w:textDirection"),
                                                             qn("w:bidi"), qn("w:rtlGutter"), qn("w:docGrid"))), None)
            if nxt is not None:
                nxt.addprevious(pg)
            else:
                sec._sectPr.append(pg)
        if footer:
            sec.footer.is_linked_to_previous = False
            p = sec.footer.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = None
            self.field(p, "PAGE", "1", size=12)
        return sec

    def field(self, paragraph, instr, placeholder="", size=None):
        def run_with(el):
            r = paragraph.add_run()
            if size:
                set_font(r, size)
            r._r.append(el)
            return r
        b = OxmlElement("w:fldChar"); b.set(qn("w:fldCharType"), "begin"); run_with(b)
        it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = " %s " % instr; run_with(it)
        s = OxmlElement("w:fldChar"); s.set(qn("w:fldCharType"), "separate"); run_with(s)
        r = paragraph.add_run(placeholder)
        if size:
            set_font(r, size)
        e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), "end"); run_with(e)

    # ---------- Nội dung ----------
    def _runs(self, p, text, size=None, bold=None, italic=None):
        """Chữ có định dạng nhanh: **đậm**, *nghiêng*, `mã`."""
        for part in re.split(r"(\*\*.+?\*\*|\*[^*\s][^*]*?\*|`[^`]+`)", text):
            if not part:
                continue
            if part.startswith("**"):
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

    def p(self, text, align=None, indent=True, size=None, bold=None, italic=None, after=None, keep_next=None, style=None):
        para = self.doc.add_paragraph(style=style)
        if not indent:
            para.paragraph_format.first_line_indent = Cm(0)
        if align is not None:
            para.alignment = align
        if after is not None:
            para.paragraph_format.space_after = Pt(after)
        if keep_next:
            para.paragraph_format.keep_with_next = True
        self._runs(para, text, size, bold, italic)
        return para

    def bullets(self, items, numbered=False):
        for it in items:
            para = self.doc.add_paragraph(style="List Number" if numbered else "List Bullet")
            self._runs(para, it)

    def h1(self, text, chapter=None):
        if chapter is not None:
            self.chapter, self.fig_no, self.tab_no = str(chapter), 0, 0
        return self.doc.add_heading(text, level=1)

    def h2(self, text):
        return self.doc.add_heading(text, level=2)

    def h3(self, text):
        return self.doc.add_heading(text, level=3)

    def front_title(self, text, page_break=True):
        para = self.doc.add_paragraph(style="FrontTitle")
        if page_break:
            para.paragraph_format.page_break_before = True
        para.add_run(text)
        return para

    def page_break(self):
        self.doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    # ---------- Hình ----------
    @staticmethod
    def _fit_image(path, max_px=2400):
        """Ảnh rộng/cao hơn max_px thì lưu bản thu nhỏ (JPEG chất lượng cao) vào img/_fit/ để file Word nhẹ.
        2400 px trên khổ 16 cm tương đương ~380 dpi, vẫn nét khi in."""
        from pathlib import Path
        from PIL import Image
        path = Path(path)
        im = Image.open(path)
        if max(im.size) <= max_px:
            return path
        # Lưu vào docs/report/img/_fit/<thư mục gốc>-<tên ảnh>.png (thêm tên thư mục để không trùng tên)
        out = Path(__file__).resolve().parent / "img" / "_fit" / (path.parent.name + "-" + path.stem + ".png")
        out.parent.mkdir(parents=True, exist_ok=True)
        if not out.exists() or out.stat().st_mtime < path.stat().st_mtime:
            im = im.convert("RGB")
            im.thumbnail((max_px, max_px), Image.LANCZOS)
            im.save(out, optimize=True)
        return out

    def figure(self, path, caption, width=15.0, height=None):
        path = self._fit_image(path)
        self.fig_no += 1
        para = self.doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.first_line_indent = Cm(0)
        para.paragraph_format.keep_with_next = True
        para.paragraph_format.space_before = Pt(6)
        para.paragraph_format.space_after = Pt(0)
        para.paragraph_format.line_spacing = 1.0
        if height:
            para.add_run().add_picture(str(path), height=Cm(height))
        else:
            para.add_run().add_picture(str(path), width=Cm(width))
        cap = self.doc.add_paragraph(style="HinhCaption")
        label = "Hình %s.%d. " % (self.chapter, self.fig_no)
        r = cap.add_run(label); r.bold = True; r.italic = False
        self._runs(cap, caption)
        return label.strip()

    def next_fig(self):
        return "Hình %s.%d" % (self.chapter, self.fig_no + 1)

    def next_tab(self):
        return "Bảng %s.%d" % (self.chapter, self.tab_no + 1)

    # ---------- Bảng ----------
    def table(self, headers, rows, widths=None, caption=None, size=12, header_fill="D9D9D9", center_cols=(), bold_first=False,
              tight=False):
        if caption:
            self.tab_no += 1
            cap = self.doc.add_paragraph(style="BangCaption")
            r = cap.add_run("Bảng %s.%d. " % (self.chapter, self.tab_no)); r.bold = True; r.italic = False
            self._runs(cap, caption)
        ncol = len(headers)
        t = self.doc.add_table(rows=1, cols=ncol)
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        for i, h in enumerate(headers):
            c = t.rows[0].cells[i]
            self._cell(c, h, size, bold=True, center=True)
            self._shade(c, header_fill)
        tr_pr = t.rows[0]._tr.get_or_add_trPr()
        hdr = OxmlElement("w:tblHeader"); hdr.set(qn("w:val"), "true"); tr_pr.append(hdr)
        for row in rows:
            cells = t.add_row().cells
            for i, v in enumerate(row):
                fill = None
                if isinstance(v, tuple):          # (chữ, màu nền)
                    v, fill = v
                self._cell(cells[i], str(v), size, bold=(bold_first and i == 0), center=(i in center_cols))
                if fill:
                    self._shade(cells[i], fill)
        if widths:
            self._set_widths(t, widths)
        if tight:      # lề trong ô 0,05 cm (mặc định 0,19 cm) cho bảng nhiều cột hẹp như Gantt
            mar = parse_xml('<w:tblCellMar %s><w:left w:w="28" w:type="dxa"/><w:right w:w="28" w:type="dxa"/></w:tblCellMar>'
                            % nsdecls("w"))
            look = t._tbl.tblPr.find(qn("w:tblLook"))
            if look is not None:
                look.addprevious(mar)          # tblCellMar phải đứng trước tblLook
            else:
                t._tbl.tblPr.append(mar)
        after = self.doc.add_paragraph()
        after.paragraph_format.space_after = Pt(2)
        after.paragraph_format.line_spacing = 1.0
        return t

    @staticmethod
    def _set_widths(t, widths):
        """Word dùng độ rộng lưới cột (tblGrid/gridCol) và tổng độ rộng bảng, nên phải đặt cả ba: lưới, ô, bảng."""
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
        tbl_w.set(qn("w:w"), str(int(sum(widths) * 567)))          # 1 cm = 567 twip
        # Thứ tự chuẩn trong tblPr: ... tblW, jc, tblCellSpacing, tblInd, tblBorders, shd, tblLayout, tblCellMar, tblLook
        for old in tbl_pr.findall(qn("w:tblLayout")):      # t.autofit = False đã tạo sẵn 1 thẻ -> tránh trùng
            tbl_pr.remove(old)
        layout = OxmlElement("w:tblLayout"); layout.set(qn("w:type"), "fixed")
        nxt = next((c for c in tbl_pr if c.tag in (qn("w:tblCellMar"), qn("w:tblLook"), qn("w:tblCaption"),
                                                    qn("w:tblDescription"))), None)
        if nxt is not None:
            nxt.addprevious(layout)
        else:
            tbl_pr.append(layout)

    def _cell(self, cell, text, size, bold=False, center=False):
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        lines = text.split("\n")
        para = cell.paragraphs[0]
        for k, line in enumerate(lines):
            if k:
                para = cell.add_paragraph()
            para.style = self.doc.styles["CellText"]
            if center:
                para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            self._runs(para, line, size=size, bold=bold or None)

    @staticmethod
    def _shade(cell, fill):
        tc_pr = cell._tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), fill)
        # Thứ tự trong tcPr: tcW, gridSpan, vMerge, tcBorders, shd, noWrap, tcMar, textDirection, tcFitText, vAlign...
        nxt = next((c for c in tc_pr if c.tag in (qn("w:noWrap"), qn("w:tcMar"), qn("w:textDirection"),
                                                   qn("w:tcFitText"), qn("w:vAlign"), qn("w:hideMark"))), None)
        if nxt is not None:
            nxt.addprevious(shd)
        else:
            tc_pr.append(shd)

    def code(self, text, caption=None):
        """Đoạn mã nguồn: khung 1 ô nền xám, chữ Consolas."""
        if caption:
            self.p(caption, indent=False, italic=True, size=12, after=2, keep_next=True)
        t = self.doc.add_table(rows=1, cols=1)
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = t.rows[0].cells[0]
        self._set_widths(t, [16])
        self._shade(c, "F2F2F2")
        lines = text.strip("\n").split("\n")
        para = c.paragraphs[0]
        for k, line in enumerate(lines):
            if k:
                para = c.add_paragraph()
            para.style = self.doc.styles["CodeText"]
            r = para.add_run(line if line else " ")
            set_font(r, 9.5, name="Consolas")
        sp = self.doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(2)

    # ---------- Ảnh nền trang bìa (nằm sau chữ, phủ cả trang) ----------
    def background_image(self, path):
        para = self.doc.paragraphs[0] if self.doc.paragraphs else self.doc.add_paragraph()
        run = para.add_run()
        inline = run.add_picture(str(path), width=Cm(21), height=Cm(29.7))._inline
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
        # Không bật cờ updateFields: cờ này làm Word hỏi "cập nhật trường?" mỗi lần mở file (và treo khi chạy ẩn).
        # Mục lục và danh mục được cập nhật bằng finalize_report.ps1 (Word).
        self.doc.core_properties.title = "Báo cáo đồ án cuối kỳ - Website SANCTUARY"
        self.doc.core_properties.author = "Nhóm SANCTUARY - UEL"
        self.doc.core_properties.language = "vi-VN"
        self.doc.save(str(path))
