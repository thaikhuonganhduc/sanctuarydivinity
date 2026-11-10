#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lưu đồ giải thuật (flowchart) của 4 thuật toán chính -> docs/diagrams/05-flowchart.drawio (mỗi thuật toán 1 trang).
Các bước bám theo code thật: js/gate.js, js/size-finder.js + js/product-popup.js, js/shipping.js + js/cart-page.js,
js/cart-page.js (submit) + js/form-validate.js.
Ký hiệu chuẩn: hình bầu dục = bắt đầu/kết thúc, chữ nhật = xử lý, thoi = điều kiện, bình hành = nhập/xuất, trụ = dữ liệu.
Chạy: python tools/diagram_flowchart.py"""
from drawio import Diagram, save

TERM = "rounded=1;arcSize=50;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1;fontSize=12;"
PROC = "rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;"
DEC = "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=11;"
IO = "shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;size=0.12;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=12;"
DATA = "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;size=8;fillColor=#f5f5f5;strokeColor=#666666;fontSize=10;"
ERR = "rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=12;"
ARROW = "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;fontSize=11;labelBackgroundColor=#ffffff;"
DASH = "dashed=1;html=1;endArrow=open;endFill=0;strokeColor=#888888;"

SIZE = {"term": (170, 50), "proc": (230, 60), "dec": (230, 90), "io": (230, 60), "data": (130, 60), "err": (230, 60)}
STYLE = {"term": TERM, "proc": PROC, "dec": DEC, "io": IO, "data": DATA, "err": ERR}
COL_X = {-1: 40, 0: 330, 1: 640, 2: 900}     # tâm cột: trái (dữ liệu), chính, nhánh phải, nhánh xa
ROW_H = 115


def flowchart(title, nodes, edges):
    """nodes: (khoá, loại, cột, hàng, nhãn). edges: (từ, tới[, nhãn[, kiểu]]). Kiểu:
       "data" = nét đứt nối dữ liệu;
       "back" = quay về bước trước / nhảy tới Kết thúc: đi vòng qua lề phải, vào hình đích từ cạnh phải;
       "loop" = vòng lặp: đi xuống, sang khe giữa cột chính và cột phải, lên trên rồi vào đỉnh hình đích."""
    d = Diagram(title)
    ids, geo = {}, {}
    for key, kind, col, row, label in nodes:
        w, h = SIZE[kind]
        cx = COL_X[col] + 115
        cy = 40 + row * ROW_H + 45
        ids[key] = d.node(label, cx - w // 2, cy - h // 2, w, h, STYLE[kind])
        geo[key] = (cx, cy, w, h)
    gutter = max(cx + w // 2 for cx, cy, w, h in geo.values()) + 30     # lề phải cho mũi tên quay lại
    slot = COL_X[0] + 115 + 115 + (COL_X[1] - COL_X[0] - 230) // 2     # khe giữa cột chính và cột phải
    for e in edges:
        src, dst = e[0], e[1]
        label = e[2] if len(e) > 2 else ""
        kind = e[3] if len(e) > 3 else ""
        (sx, sy, sw, sh), (tx, ty, tw, th) = geo[src], geo[dst]
        if kind == "data":
            d.edge(ids[src], ids[dst], label, DASH)
        elif kind == "back":
            d.edge(ids[src], ids[dst], label, ARROW + "exitX=1;exitY=0.5;entryX=1;entryY=0.5;",
                   points=[(gutter, sy), (gutter, ty)], label_pos=-0.6)
            gutter += 25                                                   # mũi tên sau đi ngoài mũi tên trước
        elif kind == "loop":
            below, above = sy + sh // 2 + 18, ty - th // 2 - 18
            d.edge(ids[src], ids[dst], label, ARROW + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;",
                   points=[(sx, below), (slot, below), (slot, above), (tx, above)])
        elif kind.startswith("exit"):                                      # tự chỉ định điểm ra/vào
            d.edge(ids[src], ids[dst], label, ARROW + kind)
        else:
            d.edge(ids[src], ids[dst], label, ARROW)
    return d


# ---------- 1. Kiểm tra mã ở trang cổng (js/gate.js) ----------
gate = flowchart("1. Kiểm tra mã cổng", [
    ("s", "term", 0, 0, "Bắt đầu"),
    ("in", "io", 0, 1, "Nhập mã vào ô Password\nrồi bấm Enter"),
    ("empty", "dec", 0, 2, "Mã rỗng?"),
    ("e1", "err", 1, 2, "Báo \"Please enter\na password.\""),
    ("hash", "proc", 0, 3, "h = SHA-256(mã)\n(Web Crypto API)"),
    ("isAdmin", "dec", 0, 4, "h = ADMIN_CODE_HASH?"),
    ("admin", "proc", 1, 4, "sessionStorage.role = \"admin\""),
    ("goAdmin", "io", 1, 5, "Chuyển sang admin.html"),
    ("load", "proc", 0, 5, "Tải danh sách mã athlete\nđang bật"),
    ("dsrc", "data", -1, 5, "access.json hoặc\nlocalStorage\nsanctuary_athletes"),
    ("match", "dec", 0, 6, "Có mã trùng\n(không phân biệt\nhoa thường)?"),
    ("cust", "proc", 0, 7, "role = \"customer\"\nlưu tên athlete (nguồn khách)"),
    ("goHome", "io", 0, 8, "Chuyển sang home.html"),
    ("e2", "err", 1, 6, "Báo \"Incorrect password.\""),
    ("end", "term", 0, 9, "Kết thúc"),
], [
    ("s", "in"), ("in", "empty"), ("empty", "e1", "Có"), ("empty", "hash", "Không"),
    ("hash", "isAdmin"), ("isAdmin", "admin", "Có"), ("admin", "goAdmin"), ("isAdmin", "load", "Không"),
    ("dsrc", "load", "", "data"), ("load", "match"), ("match", "cust", "Có"), ("match", "e2", "Không"),
    ("cust", "goHome"), ("goHome", "end"), ("goAdmin", "end", "", "back"), ("e1", "in", "nhập lại", "back"),
    ("e2", "in", "nhập lại", "back"),
])

# ---------- 2. Gợi ý size (js/size-finder.js, hàm calculate trong js/product-popup.js) ----------
size = flowchart("2. Gợi ý size", [
    ("s", "term", 0, 0, "Bắt đầu"),
    ("in", "io", 0, 1, "Nhập chiều cao, cân nặng\nbấm Calculate"),
    ("parse", "proc", 0, 2, "Đổi đơn vị: ft/in/m -> cm;\nlbs -> kg"),
    ("valid", "dec", 0, 3, "120 ≤ cao ≤ 230 cm và\n30 ≤ nặng ≤ 200 kg?"),
    ("err", "err", 1, 3, "Báo nhập sai định dạng"),
    ("chart", "proc", 0, 4, "Tải hệ số theo giới tính\n(tải 1 lần, dùng lại)"),
    ("dchart", "data", -1, 4, "size-chart.json\n(tính từ ANSUR II)"),
    ("chest", "proc", 0, 5, "ngực = a + b·kg + c·cm\n(hồi quy tuyến tính)"),
    ("idx", "proc", 0, 6, "i = vị trí mốc ngực đầu tiên\nlớn hơn \"ngực\" (không có -> XXL)"),
    ("snug", "dec", 0, 7, "Đồ ôm và cách mốc\ntrên < 1 cm?"),
    ("up", "proc", 1, 7, "i = i + 1\n(lên 1 size cho thoải mái)"),
    ("pick", "proc", 0, 8, "Chọn size CÓ BÁN\ngần i nhất"),
    ("range", "dec", 0, 9, "Ngoài khoảng P1-P99\ncủa dữ liệu?"),
    ("warn", "proc", 1, 9, "Thêm câu lưu ý\n\"kết quả ước lượng\""),
    ("out", "io", 0, 10, "Hiện size + ghi chú kiểu dáng\n+ nút \"Use size\""),
    ("end", "term", 0, 11, "Kết thúc"),
], [
    ("s", "in"), ("in", "parse"), ("parse", "valid"), ("valid", "err", "Không"), ("valid", "chart", "Có"),
    ("dchart", "chart", "", "data"), ("chart", "chest"), ("chest", "idx"), ("idx", "snug"),
    ("snug", "up", "Có"), ("snug", "pick", "Không"), ("up", "pick", "", "exitX=0.5;exitY=1;entryX=1;entryY=0.5;"), ("pick", "range"),
    ("range", "warn", "Có"), ("range", "out", "Không"), ("warn", "out", "", "exitX=0.5;exitY=1;entryX=1;entryY=0.5;"), ("out", "end"), ("err", "in", "nhập lại", "back"),
])

# ---------- 3. Tính tổng tiền đơn hàng (js/shipping.js calcCosts + js/cart-page.js render) ----------
total = flowchart("3. Tính tổng tiền", [
    ("s", "term", 0, 0, "Bắt đầu"),
    ("read", "proc", 0, 1, "Đọc giỏ hàng, sản phẩm,\nbảng phí ship (XML)"),
    ("dcart", "data", -1, 1, "localStorage\nsanctuary_cart"),
    ("dxml", "data", -1, 2, "shipping.xml\n(XMLHttpRequest)"),
    ("init", "proc", 0, 2, "tạm_tính = 0\nkg = 0,15 (bao bì)"),
    ("more", "dec", 0, 3, "Còn món chưa tính?"),
    ("add", "proc", 1, 3, "tạm_tính += giá × SL\nkg += kg_theo_loại × SL"),
    ("code", "dec", 0, 4, "Có mã athlete\nhợp lệ?"),
    ("disc", "proc", 1, 4, "giảm = 10% × tạm_tính"),
    ("ship", "proc", 0, 5, "kg_tính_cước = làm tròn lên 0,5 kg\nship = phí_gốc_vùng + giá/kg × kg"),
    ("duty", "proc", 0, 6, "thuế_NK = (tạm_tính − giảm) × %NK\n+ phí_cố_định × số_món"),
    ("tax", "proc", 0, 7, "VAT = (tạm_tính − giảm + ship\n+ thuế_NK) × %thuế của nước"),
    ("sum", "proc", 0, 8, "tổng = tạm_tính − giảm + ship\n+ thuế_NK + VAT"),
    ("out", "io", 0, 9, "Hiện bảng tổng tiền theo\ntiền tệ khách chọn (tỷ giá)"),
    ("end", "term", 0, 10, "Kết thúc"),
], [
    ("s", "read"), ("dcart", "read", "", "data"), ("dxml", "read", "", "data"), ("read", "init"), ("init", "more"),
    ("more", "add", "Có"), ("add", "more", "", "loop"), ("more", "code", "Không"), ("code", "disc", "Có"), ("code", "ship", "Không"),
    ("disc", "ship", "", "exitX=0.5;exitY=1;entryX=1;entryY=0.5;"), ("ship", "duty"), ("duty", "tax"), ("tax", "sum"), ("sum", "out"), ("out", "end"),
])

# ---------- 4. Đặt hàng (submit trong js/cart-page.js, luật kiểm tra trong js/form-validate.js) ----------
order = flowchart("4. Đặt hàng", [
    ("s", "term", 0, 0, "Bắt đầu"),
    ("in", "io", 0, 1, "Khách điền form và\nbấm Place order"),
    ("val", "proc", 0, 2, "Kiểm tra từng ô: bắt buộc, email,\nSĐT 8-15 số, thẻ (Luhn), hạn, CVC"),
    ("ok", "dec", 0, 3, "Mọi ô hợp lệ?"),
    ("e1", "err", 1, 3, "Hiện lỗi dưới từng ô sai"),
    ("check", "proc", 0, 4, "Vẽ lại giỏ: bỏ món đã ẩn/xoá,\ngiảm SL vượt tồn kho"),
    ("chg", "dec", 0, 5, "Giỏ vừa thay đổi?"),
    ("e2", "err", 1, 5, "Báo khách xem lại tổng mới"),
    ("make", "proc", 0, 6, "Tạo đơn: mã \"SD-\" + thời gian (cơ số 36),\ntrạng thái Processing"),
    ("save", "proc", 0, 7, "Ghi CÙNG LÚC: đơn hàng\n+ tồn kho đã trừ (writeAll)"),
    ("dstore", "data", -1, 7, "localStorage\norders, overrides"),
    ("saved", "dec", 0, 8, "Ghi thành công?"),
    ("e3", "err", 1, 8, "Báo lỗi, giữ nguyên giỏ\n(không có đơn \"nửa vời\")"),
    ("done", "proc", 0, 9, "Xoá giỏ; nếu đang đăng nhập thì\nlưu địa chỉ vào hồ sơ"),
    ("out", "io", 0, 10, "Hiện \"Order placed\" + mã đơn"),
    ("end", "term", 0, 11, "Kết thúc"),
], [
    ("s", "in"), ("in", "val"), ("val", "ok"), ("ok", "e1", "Không"), ("ok", "check", "Có"), ("check", "chg"),
    ("chg", "e2", "Có"), ("chg", "make", "Không"), ("make", "save"), ("save", "dstore", "", "data"), ("save", "saved"),
    ("saved", "e3", "Không"), ("saved", "done", "Có"), ("done", "out"), ("out", "end"),
    ("e1", "in", "sửa lại", "back"), ("e2", "end", "", "back"), ("e3", "end", "", "back"),
])

# ---------- 5. Thuật toán Luhn kiểm tra số thẻ (rules.card trong js/form-validate.js) ----------
luhn = flowchart("5. Kiểm tra số thẻ (Luhn)", [
    ("s", "term", 0, 0, "Bắt đầu"),
    ("in", "io", 0, 1, "Chuỗi số thẻ (bỏ khoảng trắng)"),
    ("len", "dec", 0, 2, "Chỉ gồm 13-19\nchữ số?"),
    ("bad", "err", 1, 2, "Không hợp lệ"),
    ("init", "proc", 0, 3, "sum = 0; i = 0\n(i đếm từ chữ số CUỐI)"),
    ("loop", "dec", 0, 4, "i < số chữ số?"),
    ("d", "proc", 1, 4, "d = chữ số thứ i tính từ cuối"),
    ("odd", "dec", 1, 5, "i lẻ?"),
    ("dbl", "proc", 2, 5, "d = d × 2;\nnếu d > 9 thì d = d − 9"),
    ("acc", "proc", 1, 6, "sum = sum + d; i = i + 1"),
    ("mod", "dec", 0, 7, "sum chia hết cho 10?"),
    ("bad2", "err", 1, 7, "Không hợp lệ"),
    ("good", "proc", 0, 8, "Hợp lệ"),
    ("end", "term", 0, 9, "Kết thúc"),
], [
    ("s", "in"), ("in", "len"), ("len", "bad", "Không"), ("len", "init", "Có"), ("init", "loop"),
    ("loop", "d", "Có"), ("d", "odd"), ("odd", "dbl", "Có"), ("odd", "acc", "Không"), ("dbl", "acc", "", "exitX=0.5;exitY=1;entryX=1;entryY=0.5;"), ("acc", "loop", "", "loop"),
    ("loop", "mod", "Không"), ("mod", "good", "Có"), ("mod", "bad2", "Không"), ("good", "end"),
    ("bad", "end", "", "back"), ("bad2", "end", "", "back"),
])

save("docs/diagrams/05-flowchart.drawio", [gate, size, total, order, luhn])
