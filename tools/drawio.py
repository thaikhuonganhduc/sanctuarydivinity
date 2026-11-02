#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thư viện nhỏ để tạo file sơ đồ .drawio (mở bằng draw.io / app.diagrams.net) từ code Python.
Dùng cho các script tools/diagram_*.py (Use Case, ERD, DFD, BPMN của báo cáo).

File .drawio thực chất là XML: mỗi hình / mũi tên là 1 thẻ <mxCell>, vị trí nằm trong <mxGeometry>.
Script chỉ tạo bản đầu; nhóm có thể mở bằng draw.io để kéo chỉnh, rồi xuất PNG dán vào báo cáo.
"""
from pathlib import Path
from xml.sax.saxutils import quoteattr

# ---------- Kiểu hình hay dùng ----------
ACTOR = "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;"
USECASE = "ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;"
BOUNDARY = "rounded=0;whiteSpace=wrap;html=1;fillColor=none;verticalAlign=top;fontStyle=1;fontSize=14;"
LINE = "endArrow=none;html=1;"
DASHED_OPEN = "dashed=1;endArrow=open;endFill=0;html=1;"
GENERALIZE = "endArrow=block;endFill=0;endSize=12;html=1;"
NOTE = "shape=note;whiteSpace=wrap;html=1;size=14;align=left;spacingLeft=6;fillColor=#fff2cc;strokeColor=#d6b656;"
TEXT = "text;html=1;whiteSpace=wrap;align=left;verticalAlign=top;"


class Diagram:
    """1 trang sơ đồ. node()/edge() trả về id để nối mũi tên."""

    def __init__(self, name):
        self.name = name
        self.cells = []        # chuỗi XML của từng mxCell
        self.boxes = {}        # id -> (parent, x, y, w, h, kiểm tra đè?) để kiểm tra hình đè nhau
        self.next_id = 2       # id 0 và 1 là gốc bắt buộc của draw.io

    def _id(self):
        self.next_id += 1
        return "c" + str(self.next_id)

    def node(self, label, x, y, w, h, style, parent="1", check=True):
        """Thêm 1 hình. label có thể xuống dòng bằng \\n. check=False cho khung chứa (pool, boundary)."""
        cid = self._id()
        value = label.replace("\n", "<br>")
        self.cells.append(
            '<mxCell id="%s" value=%s style=%s vertex="1" parent="%s">'
            '<mxGeometry x="%s" y="%s" width="%s" height="%s" as="geometry"/></mxCell>'
            % (cid, quoteattr(value), quoteattr(style), parent, x, y, w, h))
        self.boxes[cid] = (parent, x, y, w, h, check)
        return cid

    def edge(self, source, target, label="", style=LINE, parent="1", points=None, label_pos=0):
        """Thêm 1 mũi tên từ source tới target. points: các điểm gấp khúc [(x, y), ...].
        label_pos: vị trí nhãn dọc theo mũi tên, -1 = sát đầu source, 0 = giữa, 1 = sát đầu target."""
        cid = self._id()
        pts = ""
        if points:
            pts = '<Array as="points">%s</Array>' % "".join('<mxPoint x="%s" y="%s"/>' % p for p in points)
        pos = ' x="%s"' % label_pos if label_pos else ""
        self.cells.append(
            '<mxCell id="%s" value=%s style=%s edge="1" parent="%s" source="%s" target="%s">'
            '<mxGeometry%s relative="1" as="geometry">%s</mxGeometry></mxCell>'
            % (cid, quoteattr(label.replace("\n", "<br>")), quoteattr(style), parent, source, target, pos, pts))
        return cid

    def overlaps(self):
        """Các cặp hình (cùng khung chứa) đè lên nhau; dùng để tự kiểm tra bố cục."""
        found = []
        items = [(k, v) for k, v in self.boxes.items() if v[5]]
        for i, (a, (pa, ax, ay, aw, ah, _)) in enumerate(items):
            for b, (pb, bx, by, bw, bh, _) in items[i + 1:]:
                if pa == pb and ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah:
                    found.append((a, b))
        return found

    def xml(self):
        body = '<mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(self.cells)
        return ('<diagram name=%s><mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" '
                'page="1" pageScale="1" pageWidth="1654" pageHeight="1169" math="0" shadow="0">'
                '<root>%s</root></mxGraphModel></diagram>' % (quoteattr(self.name), body))


def save(path, diagrams):
    """Ghi 1 file .drawio (mỗi Diagram là 1 trang/tab). Báo lỗi nếu có hình đè nhau."""
    for d in diagrams:
        bad = d.overlaps()
        if bad:
            raise SystemExit("Trang '%s' có hình đè nhau: %s" % (d.name, bad))
    path = Path(__file__).resolve().parent.parent / path     # tính từ thư mục gốc dự án, chạy ở đâu cũng đúng chỗ
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('<mxfile host="app.diagrams.net">%s</mxfile>' % "".join(d.xml() for d in diagrams), encoding="utf-8")
    print("Đã lưu", path, "(%d trang)" % len(diagrams))
