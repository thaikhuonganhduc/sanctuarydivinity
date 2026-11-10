#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sơ đồ kiến trúc (client/server) và sơ đồ trang (sitemap) của SANCTUARY -> docs/diagrams/06-architecture.drawio
Chạy: python tools/diagram_architecture.py"""
from drawio import Diagram, save

BOX = "rounded=1;arcSize=6;whiteSpace=wrap;html=1;verticalAlign=top;fontStyle=1;fontSize=14;spacingTop=6;"
CLIENT = BOX + "fillColor=#dae8fc;strokeColor=#6c8ebf;"
SERVER = BOX + "fillColor=#d5e8d4;strokeColor=#82b366;"
EXT = BOX + "fillColor=#fff2cc;strokeColor=#d6b656;"
DEV = BOX + "fillColor=#f5f5f5;strokeColor=#666666;"
ITEM = "rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#999999;fontSize=11;"
STORE = "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;size=8;fillColor=#ffffff;strokeColor=#666666;fontSize=11;"
ARROW = "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;fontSize=11;labelBackgroundColor=#ffffff;"
BOTH = ARROW + "startArrow=block;startFill=1;"
DASH = ARROW + "dashed=1;"
PAGE = "rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;fontStyle=1;"
SUB = "rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#6c8ebf;fontSize=11;dashed=1;"
ADMINP = "rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=12;fontStyle=1;"
GATEP = "rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=12;fontStyle=1;"
LINE = "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;fontSize=10;labelBackgroundColor=#ffffff;"

# ================= Trang 1: kiến trúc =================
a = Diagram("Kiến trúc hệ thống")
# Máy khách (trình duyệt)
browser = a.node("MÁY KHÁCH: trình duyệt (Chrome, Edge, Safari...)", 40, 40, 520, 470, CLIENT, check=False)
for i, (lbl) in enumerate([
        "HTML5 semantic (7 trang)\nindex, home, cart, contact, about, account, admin",
        "CSS3: reset, base, components (biên dịch từ LESS),\npages, admin; media query mobile-first",
        "JavaScript thuần (ES modules, 27 file)\nDOM + xử lý sự kiện, fetch / XMLHttpRequest",
        "Web Crypto API: SHA-256 (mã admin, mật khẩu + salt)"]):
    a.node(lbl, 60, 80 + i * 75, 480, 60, ITEM, parent="1")
ls = a.node("localStorage: giỏ hàng, đơn hàng,\ntài khoản, tin nhắn, thay đổi của admin", 60, 390, 230, 100, STORE)
ss = a.node("sessionStorage:\nvai trò (customer/admin),\nnguồn athlete", 310, 390, 230, 100, STORE)

# Máy chủ (Vercel)
srv = a.node("MÁY CHỦ WEB: Vercel (hosting tĩnh, CDN, HTTPS)", 700, 40, 470, 330, SERVER, check=False)
a.node("Tên miền: sanctuarydivinity.vercel.app\nvercel.json: \"/\" -> \"/password\" (trang cổng)", 720, 80, 430, 55, ITEM)
a.node("File tĩnh: *.html, *.css, *.js", 720, 150, 205, 50, ITEM)
a.node("Ảnh WebP, video MP4,\nfont, logo", 945, 150, 205, 50, ITEM)
a.node("Dữ liệu JSON: products, reviews,\naccess, size-chart", 720, 215, 205, 60, STORE)
a.node("Dữ liệu XML:\nshipping.xml", 945, 215, 205, 60, STORE)
a.node("Không có CSDL và mã phía máy chủ:\nmọi xử lý nghiệp vụ chạy trong trình duyệt", 720, 295, 430, 55, ITEM)

# Dịch vụ ngoài
ext = a.node("DỊCH VỤ BÊN NGOÀI", 700, 420, 470, 160, EXT, check=False)
a.node("open.er-api.com\n(API tỷ giá, JSON)", 720, 460, 205, 60, ITEM)
a.node("Google Maps\n(nhúng bằng iframe)", 945, 460, 205, 60, ITEM)
a.node("Dự phòng: mất mạng thì dùng tỷ giá cố định trong currency.js", 720, 530, 430, 35, ITEM)

# Phát triển
dev = a.node("MÁY NHÓM PHÁT TRIỂN", 40, 580, 520, 200, DEV, check=False)
a.node("VS Code + Live Server, Git", 60, 620, 230, 45, ITEM)
a.node("Python: crawl dữ liệu mẫu, tạo JSON,\nbảng size (ANSUR II), nén ảnh/video", 310, 620, 230, 70, ITEM)
a.node("Node.js: biên dịch LESS -> CSS", 60, 680, 230, 45, ITEM)
a.node("draw.io: sơ đồ phân tích thiết kế", 310, 705, 230, 45, ITEM)
gh = a.node("GitHub\nthaikhuonganhduc/sanctuarydivinity", 700, 650, 470, 60, EXT)

a.edge(browser, srv, "HTTP GET (HTTPS): tải trang,\nfetch JSON, XMLHttpRequest XML", BOTH + "exitX=1;exitY=0.35;entryX=0;entryY=0.5;")
a.edge(browser, ext, "fetch tỷ giá /\niframe bản đồ", BOTH + "exitX=1;exitY=0.85;entryX=0;entryY=0.5;")
a.edge(dev, gh, "git push", ARROW)
# Đi vòng mép phải để không cắt qua khung "Dịch vụ bên ngoài"
a.edge(gh, srv, "tự động deploy\nkhi có commit mới", DASH + "exitX=1;exitY=0.5;entryX=1;entryY=0.5;",
       points=[(1220, 680), (1220, 205)])

# ================= Trang 2: sơ đồ trang =================
m = Diagram("Sơ đồ trang (sitemap)")
gate = m.node("index.html (cổng)\nĐếm ngược, lookbook,\nô nhập mã", 520, 30, 220, 75, GATEP)
home = m.node("home.html\nTrang chủ + cửa hàng", 200, 190, 220, 60, PAGE)
admin = m.node("admin.html\nTrang quản trị", 860, 190, 220, 60, ADMINP)
m.edge(gate, home, "mã athlete", LINE)
m.edge(gate, admin, "mã admin", LINE)
subs = ["Video hero, video xen kẽ", "Cửa hàng: 3 khu, nhóm sản phẩm", "Menu Armory: lọc size/màu,\nsắp xếp giá",
        "Popup sản phẩm: màu, size,\nbảng size, gợi ý size", "Popup Reviews: lọc sao,\nslideshow ảnh"]
for i, lbl in enumerate(subs):            # các phần nằm trong trang chủ (khung nét đứt)
    n = m.node(lbl, 30, 290 + i * 70, 220, 55, SUB)
    m.edge(home, n, "", LINE)
pages = [("cart.html\nGiỏ hàng + thanh toán", 300), ("contact.html (Info)\nContact, Shipping/Returns,\nđiều khoản, chính sách, bản đồ", 380),
         ("about.html\nCâu chuyện thương hiệu", 480), ("account.html\nThông tin, đổi mật khẩu,\nlịch sử đơn", 560)]
for lbl, y in pages:
    account = m.node(lbl, 330, y, 230, 70, PAGE)      # sau vòng lặp, biến account là trang cuối (account.html)
    m.edge(home, account, "", LINE)
popup = m.node("Popup Sign in /\nCreate account\n(trên mọi trang khách)", 600, 560, 200, 70, SUB)
m.edge(popup, account, "đăng nhập xong", LINE)
admin_subs = ["Overview (doanh thu, KPI)", "Orders (đổi trạng thái)", "Products (thêm, sửa, ẩn, xoá)", "Customers",
              "Messages", "Athlete codes", "Launch date", "Backup (sao lưu, khôi phục,\ndữ liệu mẫu)"]
for i, lbl in enumerate(admin_subs):
    n = m.node(lbl, 880, 290 + i * 62, 200, 48, SUB)
    m.edge(admin, n, "", LINE)

save("docs/diagrams/06-architecture.drawio", [a, m])
