#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sơ đồ quy trình nghiệp vụ (BPMN) của SANCTUARY -> docs/diagrams/04-bpmn.drawio (mỗi quy trình 1 trang)
Các bước bám theo code thật (ghi tên file ở chú thích từng quy trình).
Chạy: python tools/diagram_bpmn.py"""
from drawio import Diagram, save

# ---------- Hình BPMN (thư viện BPMN có sẵn của draw.io) ----------
EVENT = ("shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;"
         "perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;fontSize=10;")
START = EVENT + "outline=standard;symbol=general;fillColor=#d5e8d4;strokeColor=#82b366;"
END = EVENT + "outline=end;symbol=general;fillColor=#f8cecc;strokeColor=#b85450;"
END_ERROR = EVENT + "outline=end;symbol=error;fillColor=#f8cecc;strokeColor=#b85450;"
GATEWAY = ("shape=mxgraph.bpmn.gateway2;html=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;"
           "perimeter=rhombusPerimeter;outlineConnect=0;outline=none;symbol=none;gwType=exclusive;fontSize=10;"
           "fillColor=#fff2cc;strokeColor=#d6b656;")
TASK = "rounded=1;whiteSpace=wrap;html=1;arcSize=12;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=11;"
STORE = "shape=datastore;whiteSpace=wrap;html=1;fontSize=9;fillColor=#f5f5f5;strokeColor=#666666;"
POOL = "swimlane;horizontal=0;html=1;startSize=30;fillColor=#e1d5e7;strokeColor=#9673a6;fontStyle=1;fontSize=13;"
LANE = "swimlane;horizontal=0;html=1;startSize=30;fillColor=#f5f5f5;swimlaneFillColor=#ffffff;fontStyle=1;"
FLOW = "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;fontSize=10;labelBackgroundColor=#ffffff;"
ASSOC = "dashed=1;html=1;endArrow=open;endFill=0;strokeColor=#888888;"

SIZES = {"start": (40, 40), "end": (40, 40), "error": (40, 40), "gw": (50, 50), "task": (140, 60), "store": (70, 50)}
STYLES = {"start": START, "end": END, "error": END_ERROR, "gw": GATEWAY, "task": TASK, "store": STORE}
COL_W, LANE_H, ROW_GAP = 175, 220, 62     # hàng -1/0/1 cách nhau 62px, vẫn nằm gọn trong lane cao 220
# Đường quay lại bước trước: đi vòng dưới (bottom) hoặc trên (top) để không cắt qua các bước ở giữa
BACK = {"bottom": "exitX=0.5;exitY=1;entryX=0.5;entryY=1;", "top": "exitX=0.5;exitY=0;entryX=0.5;entryY=0;"}


def bpmn_page(title, pool_label, lanes, elements, flows, note=""):
    """lanes: tên các lane từ trên xuống.
    elements: (khoá, loại, lane, cột, nhãn[, hàng]) - hàng: -1 trên, 0 giữa, 1 dưới trong lane.
    flows: (từ, tới[, nhãn[, "bottom"/"top"/"assoc"]])."""
    d = Diagram(title)
    ncols = max(e[3] for e in elements) + 1
    width = 60 + ncols * COL_W + 40
    pool = d.node(pool_label, 20, 20, width + 30, LANE_H * len(lanes), POOL, check=False)
    lane_ids = {}
    for i, name in enumerate(lanes):
        lane_ids[name] = d.node(name, 30, i * LANE_H, width, LANE_H, LANE, parent=pool, check=False)
    ids = {}
    for key, kind, lane, col, label, *rest in elements:
        row = rest[0] if rest else 0
        w, h = SIZES[kind]
        x = 50 + col * COL_W + (140 - w) / 2
        y = LANE_H / 2 + row * ROW_GAP - h / 2
        ids[key] = d.node(label, x, y, w, h, STYLES[kind], parent=lane_ids[lane])
    for src, dst, *rest in flows:
        label = rest[0] if rest else ""
        mode = rest[1] if len(rest) > 1 else None
        if mode == "assoc":
            d.edge(ids[src], ids[dst], label, ASSOC)
        else:
            d.edge(ids[src], ids[dst], label, FLOW + BACK.get(mode, ""))
    if note:
        d.node(note, 20, 40 + LANE_H * len(lanes), width + 30, 50,
               "text;html=1;whiteSpace=wrap;align=left;verticalAlign=top;fontSize=11;fontColor=#555555;")
    return d


pages = []

# =============== 1. Vào web qua trang cổng (js/gate.js, js/athletes.js) ===============
pages.append(bpmn_page(
    "1. Vào web qua cổng", "Quy trình vào web bằng mật khẩu", ["Người dùng", "Website (gate.js)"],
    [
        ("s", "start", "Người dùng", 0, "Mở trang cổng"),
        ("input", "task", "Người dùng", 1, "Bấm \"Enter using password\",\nnhập mã"),
        ("empty", "gw", "Website (gate.js)", 1, "Mã trống?"),
        ("e_empty", "task", "Website (gate.js)", 2, "Báo \"Please enter\na password\"", 1),
        ("hash", "task", "Website (gate.js)", 3, "Băm mã (SHA-256),\nso với hash mã admin"),
        ("isadmin", "gw", "Website (gate.js)", 4, "Trùng mã admin?"),
        ("roleadmin", "task", "Website (gate.js)", 5, "Lưu vai trò admin\n(sessionStorage)", -1),
        ("goadmin", "end", "Website (gate.js)", 6, "Vào trang Admin", -1),
        ("find", "task", "Website (gate.js)", 5, "Tìm trong các mã\nathlete đang bật", 1),
        ("d3", "store", "Website (gate.js)", 4, "D3 Mã athlete", 1),
        ("match", "gw", "Website (gate.js)", 6, "Có mã khớp?", 1),
        ("rolecust", "task", "Website (gate.js)", 7, "Lưu vai trò customer\n+ athlete giới thiệu", 1),
        ("gohome", "end", "Website (gate.js)", 8, "Vào trang chủ", 1),
        ("wrong", "task", "Người dùng", 7, "Thấy báo\n\"Incorrect password\"", -1),
    ],
    [
        ("s", "input"), ("input", "empty"),
        ("empty", "e_empty", "Có"), ("e_empty", "input", "", "bottom"),
        ("empty", "hash", "Không"), ("hash", "isadmin"),
        ("isadmin", "roleadmin", "Có"), ("roleadmin", "goadmin"),
        ("isadmin", "find", "Không"), ("d3", "find", "đọc", "assoc"), ("find", "match"),
        ("match", "rolecust", "Có"), ("rolecust", "gohome"),
        ("match", "wrong", "Không"), ("wrong", "input", "nhập lại", "top"),
    ],
    "Mã admin không lưu dạng chữ trong code, chỉ lưu hash (js/config.js). Mã athlete so không phân biệt hoa thường; "
    "danh sách lấy từ data/access.json hoặc bản admin đã sửa (localStorage)."))

# =============== 2. Đăng ký tài khoản (js/auth-ui.js, js/auth.js) ===============
pages.append(bpmn_page(
    "2. Đăng ký", "Quy trình đăng ký tài khoản", ["Khách", "Website (auth.js)"],
    [
        ("s", "start", "Khách", 0, "Bấm icon tài khoản\n→ Create account"),
        ("fill", "task", "Khách", 1, "Nhập tên, email,\nmật khẩu, xác nhận"),
        ("valid", "gw", "Website (auth.js)", 1, "Form hợp lệ?"),
        ("err", "task", "Khách", 2, "Sửa theo lỗi\nhiện dưới ô", -1),
        ("exists", "gw", "Website (auth.js)", 2, "Email đã có\ntài khoản?"),
        ("dup", "task", "Khách", 3, "Thấy báo email\nđã được dùng", -1),
        ("hash", "task", "Website (auth.js)", 3, "Tạo salt ngẫu nhiên,\nbăm SHA-256(salt + mật khẩu)"),
        ("save", "task", "Website (auth.js)", 4, "Lưu tài khoản"),
        ("d8", "store", "Website (auth.js)", 4, "D8 Tài khoản", 1),
        ("saved", "gw", "Website (auth.js)", 5, "Lưu được?"),
        ("fail", "error", "Website (auth.js)", 6, "Báo lỗi lưu", 1),
        ("login", "task", "Website (auth.js)", 6, "Đăng nhập luôn\n(lưu session)", -1),
        ("done", "end", "Khách", 7, "Icon tài khoản\nđổi trạng thái"),
    ],
    [
        ("s", "fill"), ("fill", "valid"),
        ("valid", "err", "Không"), ("err", "fill", "", "top"),
        ("valid", "exists", "Có"),
        ("exists", "dup", "Có"), ("dup", "fill", "", "top"),
        ("exists", "hash", "Không"), ("hash", "save"), ("save", "d8", "ghi", "assoc"), ("save", "saved"),
        ("saved", "fail", "Không"), ("saved", "login", "Có"), ("login", "done"),
    ],
    "Luật kiểm tra: tên ≥ 2 ký tự; email đúng dạng; mật khẩu ≥ 8 ký tự, có cả chữ và số; xác nhận phải khớp. "
    "Không lưu mật khẩu dạng chữ, chỉ lưu salt + hash."))

# =============== 3. Đăng nhập (js/auth-ui.js, js/auth.js) ===============
pages.append(bpmn_page(
    "3. Đăng nhập", "Quy trình đăng nhập", ["Thành viên", "Website (auth.js)"],
    [
        ("s", "start", "Thành viên", 0, "Bấm icon tài khoản\n→ Sign in"),
        ("fill", "task", "Thành viên", 1, "Nhập email,\nmật khẩu"),
        ("valid", "gw", "Website (auth.js)", 1, "Form hợp lệ?"),
        ("find", "task", "Website (auth.js)", 2, "Tìm tài khoản\ntheo email"),
        ("d8", "store", "Website (auth.js)", 2, "D8 Tài khoản", 1),
        ("check", "task", "Website (auth.js)", 3, "Băm SHA-256(salt +\nmật khẩu vừa nhập),\nso với hash đã lưu"),
        ("ok", "gw", "Website (auth.js)", 4, "Có tài khoản\nvà khớp hash?"),
        ("wrong", "task", "Thành viên", 5, "Thấy báo \"Incorrect\nemail or password\"", -1),
        ("session", "task", "Website (auth.js)", 5, "Lưu session,\nphát sự kiện auth-change", 1),
        ("done", "end", "Website (auth.js)", 6, "Đã đăng nhập (checkout\ntự điền thông tin)", 1),
    ],
    [
        ("s", "fill"), ("fill", "valid"),
        ("valid", "fill", "Không", "bottom"),
        ("valid", "find", "Có"), ("d8", "find", "đọc", "assoc"), ("find", "check"), ("check", "ok"),
        ("ok", "wrong", "Không"), ("wrong", "fill", "nhập lại", "top"),
        ("ok", "session", "Có"), ("session", "done"),
    ],
    "Sai email hay sai mật khẩu đều báo chung 1 câu, để người khác không dò được email nào đã có tài khoản."))

# =============== 4. Thêm vào giỏ hàng (js/product-popup.js, js/cart.js) ===============
W4 = "Website (product-popup.js, cart.js)"
pages.append(bpmn_page(
    "4. Thêm vào giỏ", "Quy trình thêm sản phẩm vào giỏ", ["Khách", W4],
    [
        ("s", "start", "Khách", 0, "Mở popup sản phẩm"),
        ("pick", "task", "Khách", 1, "Chọn màu, size,\nsố lượng"),
        ("click", "task", "Khách", 2, "Bấm Add to cart"),
        ("hassize", "gw", W4, 2, "Đã chọn size?"),
        ("nosize", "task", "Khách", 3, "Thấy báo\n\"Please select a size\"", -1),
        ("color", "gw", W4, 3, "Màu còn bán?"),
        ("calc", "task", W4, 4, "Số còn thêm được =\ntồn kho − số đã có\ntrong giỏ"),
        ("soldout", "end", W4, 4, "Báo màu đã hết", 1),
        ("room", "gw", W4, 5, "Còn thêm được?"),
        ("add", "task", W4, 6, "Thêm vào giỏ (tối đa\nsố còn lại), lưu", -1),
        ("d6", "store", W4, 6, "D6 Giỏ hàng"),
        ("full", "end", W4, 6, "Báo đã có đủ\nhàng trong giỏ", 1),
        ("saved", "gw", W4, 7, "Lưu được?", -1),
        ("fail", "error", W4, 8, "Báo lỗi lưu giỏ", 1),
        ("ok", "task", W4, 8, "Cập nhật số trên icon\ngiỏ (sự kiện cart-change)", -1),
        ("done", "end", "Khách", 9, "Thấy \"Added ✓\""),
    ],
    [
        ("s", "pick"), ("pick", "click"), ("click", "hassize"),
        ("hassize", "nosize", "Không"), ("nosize", "pick", "", "top"),
        ("hassize", "color", "Có"), ("color", "soldout", "Không"), ("color", "calc", "Có"),
        ("calc", "room"), ("room", "full", "Không"), ("room", "add", "Có"),
        ("add", "d6", "ghi", "assoc"), ("add", "saved"),
        ("saved", "fail", "Không"), ("saved", "ok", "Có"), ("ok", "done"),
    ],
    "Giới hạn tồn kho tính cho cả sản phẩm (cộng mọi màu, size đã có trong giỏ). Thêm được ít hơn số muốn mua "
    "thì báo \"Only n more could be added\". Nút Buy now chạy cùng quy trình rồi chuyển sang trang giỏ hàng."))

# =============== 5. Đặt hàng (js/cart-page.js, js/shipping.js) ===============
W5 = "Website (cart-page.js)"
pages.append(bpmn_page(
    "5. Đặt hàng", "Quy trình đặt hàng (thanh toán)", ["Khách", W5],
    [
        ("s", "start", "Khách", 0, "Mở trang Cart"),
        ("check", "task", W5, 1, "Kiểm tra giỏ: bỏ món\nbị ẩn/xoá, hết màu,\nvượt kho; tính tạm tính"),
        ("code", "task", "Khách", 2, "Nhập mã athlete\n(tuỳ chọn)"),
        ("codegw", "gw", W5, 2, "Mã đang bật?"),
        ("discount", "task", W5, 3, "Giảm 10%", -1),
        ("badcode", "task", "Khách", 3, "Thấy báo mã\nkhông hợp lệ", -1),
        ("fill", "task", "Khách", 4, "Điền giao hàng, chọn\nnước, cách thanh toán"),
        ("ship", "task", W5, 5, "Tính phí ship, thuế,\nthuế nhập khẩu theo nước"),
        ("d4", "store", W5, 5, "D4 Phí ship, thuế", 1),
        ("place", "task", "Khách", 6, "Bấm Place order"),
        ("valid", "gw", W5, 6, "Form hợp lệ? (thẻ:\nLuhn, hạn, CVC)"),
        ("fix", "task", "Khách", 7, "Sửa theo lỗi\nhiện dưới ô", -1),
        ("changed", "gw", W5, 7, "Giỏ vừa thay đổi?\n(kiểm tra lại)"),
        ("review", "task", "Khách", 8, "Xem lại\ntổng tiền mới", -1),
        ("create", "task", W5, 8, "Tạo đơn SD-...,\ntrạng thái Processing"),
        ("save", "task", W5, 9, "Lưu đơn + trừ kho\ncùng lúc (writeAll)"),
        ("d1", "store", W5, 9, "D1 Sản phẩm\n(tồn kho)", -1),
        ("d7", "store", W5, 9, "D7 Đơn hàng", 1),
        ("saved", "gw", W5, 10, "Lưu được?"),
        ("fail", "error", W5, 11, "Báo lỗi,\ngiữ nguyên giỏ", 1),
        ("clear", "task", W5, 11, "Xoá giỏ, cập nhật hồ sơ\n(nếu đã đăng nhập)", -1),
        ("done", "end", "Khách", 12, "Thấy xác nhận\nđơn hàng"),
    ],
    [
        ("s", "check"), ("check", "code"), ("code", "codegw"),
        ("codegw", "discount", "Có"), ("codegw", "badcode", "Không"),
        ("discount", "fill"), ("badcode", "fill"),
        ("fill", "ship"), ("d4", "ship", "đọc", "assoc"), ("ship", "place"), ("place", "valid"),
        ("valid", "fix", "Không"), ("fix", "fill", "", "top"),
        ("valid", "changed", "Có"),
        ("changed", "review", "Có"), ("review", "place", "", "top"),
        ("changed", "create", "Không"), ("create", "save"),
        ("save", "d1", "ghi", "assoc"), ("save", "d7", "ghi", "assoc"), ("save", "saved"),
        ("saved", "fail", "Không"), ("saved", "clear", "Có"), ("clear", "done"),
    ],
    "Bước mã athlete là tuỳ chọn (khách có thể bỏ qua). Đơn và tồn kho được ghi cùng lúc: chỉ cần 1 trong 2 lỗi "
    "là không ghi gì (writeAll trả lại dữ liệu cũ), nên không có đơn mà chưa trừ kho hay ngược lại."))

# =============== 6. Admin xử lý đơn hàng (js/admin.js) ===============
W6 = "Website (admin.js)"
pages.append(bpmn_page(
    "6. Admin xử lý đơn", "Quy trình cập nhật trạng thái đơn hàng", ["Admin", W6, "Khách"],
    [
        ("s", "start", "Admin", 0, "Mở mục Orders"),
        ("find", "task", "Admin", 1, "Tìm, lọc đơn,\nxem chi tiết"),
        ("choose", "task", "Admin", 2, "Chọn trạng thái mới"),
        ("cancel", "gw", W6, 2, "Đơn đã trừ kho và\nđổi sang Cancelled?"),
        ("ret", "task", W6, 3, "Tính cộng lại kho", -1),
        ("reopen", "gw", W6, 3, "Mở lại đơn\nđã huỷ?", 1),
        ("take", "task", W6, 4, "Tính trừ kho\nlần nữa", 1),
        ("save", "task", W6, 5, "Lưu đơn (+ kho)\ncùng lúc"),
        ("d1", "store", W6, 5, "D1 Sản phẩm", -1),
        ("d7", "store", W6, 5, "D7 Đơn hàng", 1),
        ("saved", "gw", W6, 6, "Lưu được?"),
        ("fail", "error", W6, 7, "Trả ô chọn về\ntrạng thái cũ", 1),
        ("toast", "task", "Admin", 7, "Thấy thông báo\n\"marked ...\""),
        ("see", "task", "Khách", 8, "Thấy trạng thái mới\nở trang Account"),
        ("done", "end", "Khách", 9, "Kết thúc"),
    ],
    [
        ("s", "find"), ("find", "choose"), ("choose", "cancel"),
        ("cancel", "ret", "Có"), ("cancel", "reopen", "Không"),
        ("reopen", "take", "Có"), ("reopen", "save", "Không"),
        ("ret", "save"), ("take", "save"),
        ("save", "d1", "ghi", "assoc"), ("save", "d7", "ghi", "assoc"), ("save", "saved"),
        ("saved", "fail", "Không"), ("saved", "toast", "Có"), ("toast", "see"), ("see", "done"),
    ],
    "Chỉ đơn có stockDeducted (đặt từ trang Cart) mới hoàn / trừ kho; đơn mẫu (Sample data) không ảnh hưởng kho. "
    "Trạng thái: Processing → Shipped → Delivered, hoặc Cancelled."))

# =============== 7. Liên hệ và trả lời (js/contact.js, js/admin.js) ===============
W7 = "Website (contact.js, admin.js)"
pages.append(bpmn_page(
    "7. Liên hệ", "Quy trình gửi và xử lý tin nhắn liên hệ", ["Khách", W7, "Admin"],
    [
        ("s", "start", "Khách", 0, "Mở Info → Contact"),
        ("fill", "task", "Khách", 1, "Điền tên, email,\nchủ đề, tin nhắn"),
        ("valid", "gw", W7, 1, "Hợp lệ?"),
        ("fix", "task", "Khách", 2, "Sửa theo lỗi\nhiện dưới ô", -1),
        ("save", "task", W7, 2, "Lưu tin nhắn\n(chưa đọc)"),
        ("saved", "gw", W7, 3, "Lưu được?"),
        ("d9", "store", W7, 3, "D9 Tin nhắn", 1),
        ("err", "task", "Khách", 4, "Thấy báo lỗi, nội dung\nvẫn giữ nguyên", -1),
        ("sent", "task", "Khách", 4, "Thấy \"Message sent\"", 1),
        ("done", "end", "Khách", 5, "Kết thúc", 1),
        ("as", "start", "Admin", 5, "Mở mục Messages\n(số tin chưa đọc)"),
        ("read", "task", "Admin", 6, "Đọc tin,\nđánh dấu đã đọc"),
        ("reply", "gw", "Admin", 7, "Cần trả lời?"),
        ("mail", "task", "Admin", 8, "Bấm Reply\n(mở email, mailto)", -1),
        ("del", "gw", "Admin", 9, "Xoá tin?"),
        ("deltask", "task", "Admin", 10, "Xoá tin nhắn", -1),
        ("aend", "end", "Admin", 11, "Kết thúc"),
    ],
    [
        ("s", "fill"), ("fill", "valid"),
        ("valid", "fix", "Không"), ("fix", "fill", "", "top"),
        ("valid", "save", "Có"), ("save", "d9", "ghi", "assoc"), ("save", "saved"),
        ("saved", "err", "Không"), ("err", "fill", "thử lại", "top"),
        ("saved", "sent", "Có"), ("sent", "done"),
        ("as", "read"), ("d9", "read", "đọc, ghi", "assoc"), ("read", "reply"),
        ("reply", "mail", "Có"), ("reply", "del", "Không"), ("mail", "del"),
        ("del", "deltask", "Có"), ("del", "aend", "Không"), ("deltask", "aend"),
    ],
    "Khách đã đăng nhập được điền sẵn tên và email. Web không gửi email thật: tin nhắn lưu trong localStorage, "
    "admin đọc ở trang Admin và trả lời bằng ứng dụng email của mình (link mailto)."))

# =============== 8. Admin thêm sản phẩm (js/admin.js) ===============
W8 = "Website (admin.js)"
pages.append(bpmn_page(
    "8. Admin thêm sản phẩm", "Quy trình thêm sản phẩm mới", ["Admin", W8],
    [
        ("s", "start", "Admin", 0, "Bấm Add product"),
        ("fill", "task", "Admin", 1, "Điền tên, dòng, danh mục,\ngiá, tồn kho, màu, size"),
        ("photo", "task", "Admin", 2, "Chọn ảnh sản phẩm"),
        ("ptype", "gw", W8, 2, "JPG/PNG/WebP\nvà ≤ 10 MB?"),
        ("perr", "task", "Admin", 3, "Thấy báo lỗi ảnh", -1),
        ("resize", "task", W8, 3, "Đọc ảnh (FileReader),\nthu nhỏ 800px bằng\ncanvas → WebP"),
        ("savebtn", "task", "Admin", 4, "Bấm Save product"),
        ("valid", "gw", W8, 4, "Hợp lệ? (giá > 0, kho ≥ 0,\n≥ 1 size, có ảnh,\ntên không trùng)"),
        ("fix", "task", "Admin", 5, "Sửa theo lỗi\nhiện dưới ô", -1),
        ("save", "task", W8, 5, "Lưu sản phẩm mới\n(id c..., tag New)"),
        ("d1", "store", W8, 5, "D1 Sản phẩm\n(custom)", 1),
        ("saved", "gw", W8, 6, "Lưu được?"),
        ("fail", "error", W8, 7, "Báo bộ nhớ\ntrình duyệt đầy", 1),
        ("show", "task", W8, 7, "Vẽ lại bảng; sản phẩm\nhiện trên shop", -1),
        ("done", "end", "Admin", 8, "Thấy \"Added: ...\""),
    ],
    [
        ("s", "fill"), ("fill", "photo"), ("photo", "ptype"),
        ("ptype", "perr", "Không"), ("perr", "photo", "", "top"),
        ("ptype", "resize", "Có"), ("resize", "savebtn"), ("savebtn", "valid"),
        ("valid", "fix", "Không"), ("fix", "fill", "", "top"),
        ("valid", "save", "Có"), ("save", "d1", "ghi", "assoc"), ("save", "saved"),
        ("saved", "fail", "Không"), ("saved", "show", "Có"), ("show", "done"),
    ],
    "Ảnh được thu nhỏ trước khi lưu vì localStorage chỉ chứa khoảng 5 MB. Sản phẩm mới được xếp vào nhóm trên "
    "shop theo dòng + danh mục; xoá sản phẩm là xoá mềm (deleted), bấm Restore deleted để lấy lại."))

save("docs/diagrams/04-bpmn.drawio", pages)
