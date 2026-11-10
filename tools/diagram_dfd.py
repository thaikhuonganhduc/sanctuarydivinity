#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sơ đồ luồng dữ liệu (DFD) của SANCTUARY -> docs/diagrams/03-dfd.drawio (2 trang: ngữ cảnh, mức 0)
Ký hiệu Gane-Sarson: tiến trình = chữ nhật bo góc (có số), tác nhân ngoài = chữ nhật, kho dữ liệu = chữ nhật hở 1 đầu.
Chạy: python tools/diagram_dfd.py"""
from drawio import Diagram, save, NOTE

PROCESS = "rounded=1;whiteSpace=wrap;html=1;arcSize=14;fillColor=#fff2cc;strokeColor=#d6b656;fontStyle=1;"
ENTITY = "rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;"
STORE = "shape=partialRectangle;whiteSpace=wrap;html=1;right=0;fillColor=#f5f5f5;align=left;spacingLeft=8;fontSize=11;"
FLOW = "html=1;endArrow=block;endFill=1;fontSize=10;labelBackgroundColor=#ffffff;"
BOTH = FLOW + "startArrow=block;startFill=1;"                  # luồng 2 chiều (đọc + ghi)
ORTHO = "edgeStyle=orthogonalEdgeStyle;rounded=1;"


def side(exit_x, exit_y, entry_x, entry_y):
    """Ép mũi tên đi ra / vào ở 1 điểm cố định trên cạnh hình (0..1), để 2 luồng ngược chiều không chồng nhau."""
    return "exitX=%s;exitY=%s;entryX=%s;entryY=%s;" % (exit_x, exit_y, entry_x, entry_y)


# =============== Trang 1: DFD mức ngữ cảnh ===============
ctx = Diagram("DFD ngữ cảnh")
# Khung cao + điểm ra/vào ở 15% và 85% chiều cao: 2 luồng ngược chiều cách nhau ~160px, nhãn nhiều dòng không đè nhau
system = ctx.node("0\nHệ thống website\nSANCTUARY", 640, 330, 300, 260, PROCESS + "fontSize=15;")
customer = ctx.node("Khách hàng\n(Khách, Thành viên)", 40, 340, 200, 240, ENTITY)
admin = ctx.node("Admin", 1340, 340, 200, 240, ENTITY)
rates = ctx.node("Dịch vụ tỷ giá\n(open.er-api.com)", 690, 60, 200, 70, ENTITY)

ctx.edge(customer, system,
         "mã athlete; đăng ký, đăng nhập;\nlọc, chọn sản phẩm, màu, size;\nchiều cao, cân nặng; giỏ hàng;\n"
         "thông tin giao hàng, thanh toán;\nmã giảm giá; tin nhắn liên hệ",
         FLOW + side(1, 0.15, 0, 0.15))
ctx.edge(system, customer,
         "danh sách, chi tiết sản phẩm;\ngợi ý size; đánh giá;\ntổng tiền (ship, thuế, giảm giá);\n"
         "xác nhận đơn; lịch sử, trạng thái đơn",
         FLOW + side(0, 0.85, 1, 0.85))
ctx.edge(admin, system,
         "mã admin; trạng thái đơn;\nthêm, sửa, ẩn, xoá sản phẩm;\nmã athlete; ngày ra mắt;\nfile backup",
         FLOW + side(0, 0.15, 1, 0.15))
ctx.edge(system, admin,
         "doanh thu, KPI;\ndanh sách đơn, khách hàng,\ntin nhắn; file backup",
         FLOW + side(1, 0.85, 0, 0.85))
ctx.edge(system, rates, "yêu cầu tỷ giá USD", FLOW + side(0.3, 0, 0.3, 1), label_pos=-0.4)
ctx.edge(rates, system, "bảng tỷ giá", FLOW + side(0.7, 1, 0.7, 0), label_pos=0.4)

ctx.node("Hệ thống được coi là 1 tiến trình duy nhất (số 0).\nChỉ thể hiện dữ liệu trao đổi với bên ngoài; "
         "chi tiết bên trong xem trang \"DFD mức 0\".", 40, 680, 520, 60, NOTE)

# =============== Trang 2: DFD mức 0 ===============
d = Diagram("DFD mức 0")
P = {}
P[1] = d.node("1.0\nXác thực truy cập", 880, 20, 240, 70, PROCESS)
for n, (label, y) in {2: ("2.0\nDuyệt, lọc sản phẩm\nvà đánh giá", 250), 3: ("3.0\nQuản lý giỏ hàng", 440),
                      4: ("4.0\nĐặt hàng", 630), 5: ("5.0\nQuản lý tài khoản", 820), 6: ("6.0\nGửi liên hệ", 1000)}.items():
    P[n] = d.node(label, 420, y, 220, 80, PROCESS)
P[7] = d.node("7.0\nQuản trị cửa hàng", 1300, 500, 200, 100, PROCESS)

D = {}
# Thứ tự kho xếp theo tiến trình dùng nó (2.0 -> 6.0 từ trên xuống) để các đường nối ít cắt nhau
for i, (key, label) in enumerate([
    ("D3", "D3 | Mã athlete\n(access.json, sanctuary_athletes)"),
    ("D10", "D10 | Tỷ giá (sanctuary_rates)"),
    ("D2", "D2 | Đánh giá (reviews.json)"),
    ("D5", "D5 | Bảng size (size-chart.json)"),
    ("D1", "D1 | Sản phẩm\n(products.json, overrides, custom)"),
    ("D6", "D6 | Giỏ hàng (sanctuary_cart)"),
    ("D4", "D4 | Phí ship, thuế (shipping.xml)"),
    ("D7", "D7 | Đơn hàng (sanctuary_orders)"),
    ("D8", "D8 | Tài khoản\n(sanctuary_users, session)"),
    ("D9", "D9 | Tin nhắn (sanctuary_messages)"),
]):
    D[key] = d.node(label, 900, 130 + i * 95, 210, 46, STORE)

customer = d.node("Khách hàng", 40, 600, 160, 70, ENTITY)
admin = d.node("Admin", 1520, 515, 120, 70, ENTITY)
api = d.node("Dịch vụ tỷ giá", 230, 270, 160, 50, ENTITY)

# Tác nhân <-> tiến trình (2 chiều: "gửi vào / nhận lại")
d.edge(customer, P[1], "mã athlete / vào trang chủ hoặc báo sai", BOTH + ORTHO + side(0.5, 0, 0, 0.5))
d.edge(admin, P[1], "mã admin / vào trang admin", BOTH + ORTHO + side(0.5, 0, 1, 0.5))
d.edge(customer, P[2], "lọc, chọn sản phẩm /\nsản phẩm, size, đánh giá", BOTH + ORTHO + side(0.75, 0, 0, 0.5))
d.edge(customer, P[3], "thêm, sửa, xoá món /\ngiỏ hàng, tạm tính", BOTH + ORTHO + side(1, 0.2, 0, 0.5))
d.edge(customer, P[4], "giao hàng, thanh toán, mã /\nxác nhận đơn", BOTH + ORTHO + side(1, 0.8, 0, 0.5))
d.edge(customer, P[5], "đăng ký, đăng nhập, hồ sơ /\nlịch sử đơn", BOTH + ORTHO + side(0.75, 1, 0, 0.5))
d.edge(customer, P[6], "tin nhắn / báo đã gửi", BOTH + ORTHO + side(0.4, 1, 0, 0.5))
d.edge(admin, P[7], "thao tác quản trị /\nbáo cáo, danh sách", BOTH)
d.edge(api, P[2], "tỷ giá", FLOW)

# Tiến trình <-> kho dữ liệu. kind: "read" = kho -> tiến trình, "write" = tiến trình -> kho, "both" = 2 chiều.
# Nhãn đặt gần đầu tiến trình (không dồn vào giữa) để các nhãn không đè nhau.
def store_flow(proc, store, label, kind):
    if kind == "read":
        d.edge(D[store], P[proc], label, FLOW, label_pos=0.55)
    else:
        d.edge(P[proc], D[store], label, BOTH if kind == "both" else FLOW, label_pos=-0.55)


store_flow(1, "D3", "mã đang bật", "read")
store_flow(2, "D10", "lưu tạm tỷ giá", "both")
store_flow(2, "D2", "đánh giá", "read")
store_flow(2, "D5", "bảng size", "read")
store_flow(2, "D1", "sản phẩm", "read")
store_flow(3, "D1", "tồn kho, màu", "read")
store_flow(3, "D6", "món trong giỏ", "both")
store_flow(4, "D6", "đọc giỏ, xoá giỏ", "both")
store_flow(4, "D1", "kiểm tra, trừ kho", "both")
store_flow(4, "D3", "mã giảm giá", "read")
store_flow(4, "D4", "phí ship, thuế", "read")
store_flow(4, "D8", "hồ sơ (tự điền)", "read")
store_flow(4, "D7", "đơn mới", "write")
store_flow(5, "D8", "tài khoản", "both")
store_flow(5, "D7", "đơn của tôi", "read")
store_flow(6, "D9", "tin nhắn mới", "write")
for key, label in [("D1", "sản phẩm"), ("D3", "mã athlete"), ("D7", "trạng thái đơn"), ("D9", "đã đọc, xoá")]:
    store_flow(7, key, label, "both")
store_flow(7, "D8", "khách hàng", "read")

d.node("Mũi tên vào kho = ghi; ra khỏi kho = đọc; 2 đầu = đọc và ghi.\n"
       "Kho từ file JSON (D1 gốc, D2, D3 gốc, D4, D5) chỉ đọc được; mọi thay đổi ghi vào localStorage.\n"
       "4.0 ghi đơn (D7) và trừ kho (D1) cùng lúc bằng writeAll(): lỗi thì không ghi gì.",
       1180, 900, 460, 90, NOTE)

save("docs/diagrams/03-dfd.drawio", [ctx, d])
