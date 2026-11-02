#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sơ đồ quan hệ thực thể (ERD) của SANCTUARY -> docs/diagrams/02-erd.drawio
Web không có CSDL thật: đây là mô hình dữ liệu LOGIC (chuẩn hoá thành bảng) của dữ liệu đang nằm trong
file JSON (data/) và localStorage. Màu xanh dương = file JSON, xanh lá = localStorage.
Chạy: python tools/diagram_erd.py"""
from drawio import Diagram, save, NOTE

JSON_STYLE = "rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=6;fillColor=#dae8fc;strokeColor=#6c8ebf;"
LOCAL_STYLE = "rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=6;fillColor=#d5e8d4;strokeColor=#82b366;"
REL = "edgeStyle=orthogonalEdgeStyle;html=1;endFill=0;startFill=0;rounded=0;"
SOFT = "edgeStyle=orthogonalEdgeStyle;html=1;dashed=1;endArrow=open;endFill=0;rounded=0;fontColor=#666666;"
W = 270

d = Diagram("ERD")


def entity(name, store, fields, x, y, local=False):
    """1 thực thể: tên + nơi lưu ở đầu, gạch ngang, rồi các thuộc tính (PK = khoá chính, FK = khoá ngoại)."""
    label = ('<div style="text-align:center"><b>%s</b><br><i style="font-size:10px">%s</i></div><hr>%s'
             % (name, store, "<br>".join(fields)))
    lines = sum(f.count("\n") + 1 for f in fields)          # thuộc tính có \n chiếm 2 dòng
    return d.node(label, x, y, W, 56 + 16 * lines, LOCAL_STYLE if local else JSON_STYLE)


def rel(a, b, start, end, label=""):
    """Quan hệ a -> b với ký hiệu chân chim (crow's foot) ở 2 đầu."""
    d.edge(a, b, label, REL + "startArrow=%s;endArrow=%s;" % (start, end))


# ---------- Khách hàng, đơn hàng ----------
user = entity("USER", "localStorage: sanctuary_users", [
    "<u>PK</u> email", "name", "phone", "address", "city", "country",
    "salt", "password_hash (SHA-256)", "created_at"], 40, 40, local=True)
athlete = entity("ATHLETE_CODE", "access.json / localStorage: sanctuary_athletes", [
    "<u>PK</u> code", "name", "active (true/false)"], 40, 400)
order = entity("ORDER", "localStorage: sanctuary_orders", [
    "<u>PK</u> order_number (SD-...)", "FK user_email (trống = khách vãng lai)", "FK discount_code",
    "FK ship_country", "order_date", "status (Processing, Shipped,\nDelivered, Cancelled)", "payment (card, paypal, cod)",
    "currency (tiền đang xem)", "total_usd", "stock_deducted", "ship_name, ship_email, ship_phone", "ship_address, ship_city"],
    380, 40, local=True)
item = entity("ORDER_ITEM", "nằm trong ORDER.items", [
    "<u>PK</u> order_number + line_no", "FK order_number", "FK product_id", "color_name", "size", "qty"], 720, 40, local=True)
cart = entity("CART_ITEM", "localStorage: sanctuary_cart", [
    "<u>PK</u> product_id + color + size", "FK product_id", "qty"], 720, 330, local=True)

# ---------- Sản phẩm ----------
product = entity("PRODUCT", "products.json + sanctuary_custom_products", [
    "<u>PK</u> product_id (p01..., c... = admin thêm)", "FK category", "name", "gender (him, her, unisex)",
    "price_usd", "stock", "featured", "tag", "material, weight, fit, care", "description", "source (link tham khảo)",
    "is_custom", "hidden (ghi đè)", "deleted (ghi đè)"], 1060, 40)
color = entity("PRODUCT_COLOR", "nằm trong PRODUCT.colors", [
    "<u>PK</u> color_id", "FK product_id", "name", "hex", "available"], 1400, 40)
image = entity("COLOR_IMAGE", "nằm trong COLOR.images", [
    "<u>PK</u> image_id", "FK color_id", "path (.webp hoặc data URL)", "sort_order"], 1740, 40)
size = entity("PRODUCT_SIZE", "nằm trong PRODUCT.sizes", [
    "<u>PK</u> product_id + size", "FK product_id", "size (XXS...XXL, One size)"], 1400, 250)
feature = entity("PRODUCT_FEATURE", "nằm trong PRODUCT.features", [
    "<u>PK</u> feature_id", "FK product_id", "text"], 1400, 420)
chart = entity("SIZE_CHART_ROW", "size-chart.json (tính từ ANSUR II)", [
    "<u>PK</u> gender + size", "chest_min_cm, chest_max_cm", "waist_cm (P25-P75)", "height_cm (P25-P75)",
    "weight_kg (P25-P75)", "people (số người trong mẫu)"], 1740, 250)

# ---------- Phí ship, thuế ----------
zone = entity("SHIPPING_ZONE", "shipping.json: zones", [
    "<u>PK</u> zone_id", "base_usd", "per_kg_usd"], 40, 720)
country = entity("COUNTRY", "shipping.json: countries", [
    "<u>PK</u> country_name", "FK zone_id", "tax_label (VAT, GST...)", "tax_pct", "duty_pct", "duty_per_item_usd"], 380, 720)
category = entity("CATEGORY_WEIGHT", "shipping.json: categoryKg", [
    "<u>PK</u> category", "weight_kg"], 1060, 720)

# ---------- Đánh giá, liên hệ ----------
message = entity("MESSAGE", "localStorage: sanctuary_messages", [
    "<u>PK</u> message_date", "name", "email", "topic", "message", "read"], 720, 720, local=True)
review = entity("REVIEW", "reviews.json", [
    "<u>PK</u> review_id", "reviewer_name", "rating (trung bình)", "verified", "lang"], 1400, 720)
entry = entity("REVIEW_ENTRY", "nằm trong REVIEW.entries", [
    "<u>PK</u> entry_id", "FK review_id", "rating", "text", "lang", "product_name (chữ, không phải FK)"], 1740, 560)
rimage = entity("REVIEW_IMAGE", "nằm trong REVIEW.images", [
    "<u>PK</u> image_id", "FK review_id", "path"], 1740, 860)

# ---------- Quan hệ (ký hiệu chân chim) ----------
rel(user, order, "ERzeroToOne", "ERzeroToMany", "đặt")                 # đơn khách vãng lai không có user
rel(athlete, order, "ERzeroToOne", "ERzeroToMany", "giảm giá cho")
rel(order, item, "ERmandOne", "ERoneToMany", "gồm")
rel(product, item, "ERmandOne", "ERzeroToMany", "được mua trong")
rel(product, cart, "ERmandOne", "ERzeroToMany", "nằm trong giỏ")
rel(product, color, "ERmandOne", "ERoneToMany", "có")
rel(color, image, "ERmandOne", "ERoneToMany", "có")
rel(product, size, "ERmandOne", "ERoneToMany", "bán size")
rel(product, feature, "ERmandOne", "ERzeroToMany", "mô tả bằng")
rel(zone, country, "ERmandOne", "ERoneToMany", "thuộc vùng")
rel(country, order, "ERmandOne", "ERzeroToMany", "giao tới")
rel(category, product, "ERmandOne", "ERzeroToMany", "nặng theo loại")
rel(review, entry, "ERmandOne", "ERoneToMany", "gồm")
rel(review, rimage, "ERmandOne", "ERzeroToMany", "kèm ảnh")

# Liên kết mềm (không phải khoá ngoại): code tra cứu bằng giá trị, nét đứt
d.edge(size, chart, "tra theo size + giới tính", SOFT)
# REVIEW_ENTRY.product_name -> PRODUCT cũng là tra cứu mềm (so tên gần đúng, xem matchReviews),
# không vẽ đường để sơ đồ đỡ rối; đã ghi chú ngay trong thuộc tính product_name

d.node("<b>Chú thích</b><br>"
       "Xanh dương: dữ liệu gốc trong file JSON (data/), đọc bằng fetch<br>"
       "Xanh lá: dữ liệu sinh ra khi dùng web, lưu trong localStorage<br>"
       "PK: khoá chính · FK: khoá ngoại · Nét đứt: tra cứu bằng giá trị, không phải khoá ngoại<br>"
       "|| một và chỉ một · o| không hoặc một · |&lt; một hoặc nhiều · o&lt; không hoặc nhiều<br>"
       "MESSAGE.email không ràng buộc với USER (ai cũng gửi liên hệ được)",
       40, 1000, 640, 110, NOTE)

save("docs/diagrams/02-erd.drawio", [d])
