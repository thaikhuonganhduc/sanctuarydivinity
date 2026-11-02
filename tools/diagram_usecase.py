#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sơ đồ Use Case tổng quan của website SANCTUARY -> docs/diagrams/01-usecase.drawio
Chạy: python tools/diagram_usecase.py"""
from drawio import Diagram, save, ACTOR, USECASE, BOUNDARY, LINE, DASHED_OPEN, GENERALIZE, NOTE

d = Diagram("Use Case tổng quan")
W, H = 230, 56                                   # kích thước 1 use case

d.node("Website SANCTUARY", 240, 20, 880, 1150, BOUNDARY, check=False)

# Cột A: chức năng của Khách (đã vào web bằng mã athlete), rồi chức năng riêng của Thành viên
guest = {}
for i, (key, label) in enumerate([
    ("uc01", "UC01. Vào web bằng mã athlete"),
    ("uc02", "UC02. Xem, lọc và sắp xếp sản phẩm"),
    ("uc03", "UC03. Xem chi tiết sản phẩm"),
    ("uc05", "UC05. Xem và lọc đánh giá"),
    ("uc06", "UC06. Quản lý giỏ hàng"),
    ("uc07", "UC07. Đặt hàng (thanh toán)"),
    ("uc09", "UC09. Đổi tiền tệ hiển thị"),
    ("uc10", "UC10. Gửi tin nhắn liên hệ"),
    ("uc11", "UC11. Đăng ký tài khoản"),
]):
    guest[key] = d.node(label, 280, 70 + i * 80, W, H, USECASE)

member = {}
for i, (key, label) in enumerate([
    ("uc12", "UC12. Đăng nhập / đăng xuất"),
    ("uc13", "UC13. Sửa hồ sơ, địa chỉ"),
    ("uc14", "UC14. Đổi mật khẩu"),
    ("uc15", "UC15. Xem lịch sử đơn hàng"),
]):
    member[key] = d.node(label, 280, 840 + i * 75, W, H, USECASE)

# Cột B: các use case mở rộng (extend) nằm cạnh use case gốc
uc04 = d.node("UC04. Xem bảng size,\ngợi ý size", 560, 220, 200, H, USECASE)
uc08 = d.node("UC08. Áp mã giảm giá\nathlete (10%)", 560, 460, 200, H, USECASE)

# Cột C: chức năng của Admin
admin = {}
for i, (key, label) in enumerate([
    ("uc16", "UC16. Vào trang quản trị\nbằng mã admin"),
    ("uc17", "UC17. Xem tổng quan\n(doanh thu, KPI)"),
    ("uc18", "UC18. Quản lý đơn hàng"),
    ("uc19", "UC19. Quản lý sản phẩm"),
    ("uc20", "UC20. Xem khách hàng"),
    ("uc21", "UC21. Quản lý tin nhắn"),
    ("uc22", "UC22. Quản lý mã athlete"),
    ("uc23", "UC23. Đặt ngày ra mắt"),
    ("uc24", "UC24. Sao lưu / khôi phục\ndữ liệu"),
]):
    admin[key] = d.node(label, 840, 70 + i * 100, W, H + 4, USECASE)

# Tác nhân
khach = d.node("Khách", 110, 350, 30, 60, ACTOR)
thanhvien = d.node("Thành viên", 110, 940, 30, 60, ACTOR)
quantri = d.node("Admin", 1210, 500, 30, 60, ACTOR)

for uc in guest.values():
    d.edge(khach, uc, style=LINE)
for uc in member.values():
    d.edge(thanhvien, uc, style=LINE)
for uc in admin.values():
    d.edge(quantri, uc, style=LINE)

# Thành viên kế thừa mọi chức năng của Khách (tổng quát hoá)
d.edge(thanhvien, khach, style=GENERALIZE)

# Quan hệ mở rộng: mũi tên từ use case mở rộng chỉ về use case gốc
d.edge(uc04, guest["uc03"], "«extend»", DASHED_OPEN)
d.edge(uc08, guest["uc07"], "«extend»", DASHED_OPEN)

d.node("Ghi chú: Khách là người đã nhập mã athlete ở trang cổng.\n"
       "Thành viên = Khách có tài khoản (kế thừa mọi chức năng của Khách).\n"
       "Web không có backend: dữ liệu đọc từ file JSON (fetch) và lưu trong localStorage của trình duyệt.",
       560, 1000, 520, 80, NOTE)

save("docs/diagrams/01-usecase.drawio", [d])
