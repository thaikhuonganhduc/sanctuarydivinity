# Tạo dữ liệu mẫu cho bản cài thử WooCommerce (Chương VII - mã nguồn mở).
# Lấy 12 sản phẩm từ data/products.json (giống web SANCTUARY), đổi ảnh đầu tiên sang JPG
# và ghi ra tools/woocommerce/seed/ để blueprint.json mount vào WordPress Playground.
# Chạy: python tools/woocommerce/build_seed.py
import json, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "tools", "woocommerce", "seed")
PICK = ["p04", "p05", "p11", "p14", "p16", "p20", "p23", "p12", "p25", "p26", "p28", "p31"]
CATEGORY_NAMES = {"compression": "Compression", "oversize": "Oversized Tees", "tops": "Stringers & Tops",
                  "hoodies": "Hoodies & Crewnecks", "bottoms": "Bottoms", "accessories": "Accessories",
                  "bodysuits": "Bodysuits"}

os.makedirs(os.path.join(OUT, "img"), exist_ok=True)
products = json.load(open(os.path.join(ROOT, "data", "products.json"), encoding="utf-8"))["products"]
by_id = {p["id"]: p for p in products}
items = []
for pid in PICK:
    p = by_id[pid]
    src = os.path.join(ROOT, p["colors"][0]["images"][0])
    img_name = pid + ".jpg"
    im = Image.open(src).convert("RGB")
    im.thumbnail((900, 900))
    im.save(os.path.join(OUT, "img", img_name), "JPEG", quality=86)
    items.append({
        "sku": "SAN-" + pid.upper(),
        "name": p["name"],
        "price": p["price"],
        "category": CATEGORY_NAMES.get(p["category"], p["category"]),
        "line": "Sanctuary Selene (Women)" if p["gender"] == "her" else ("Accessories" if p["gender"] == "unisex" else "Sanctuary (Men)"),
        "colors": [c["name"] for c in p["colors"]],
        # Mô tả: dùng danh sách "features" của web, ghép thành gạch đầu dòng HTML
        "description": p.get("description") or "<ul>" + "".join("<li>" + x + "</li>" for x in p.get("features", [])) + "</ul>",
        "short": p["specs"].get("fit", ""),
        "sizes": p.get("sizes", []),
        "stock": int(p.get("stock") or 0),
        "image": img_name,
    })
json.dump({"products": items}, open(os.path.join(OUT, "seed.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(items), "san pham")

# Logo trắng cho header nền đen của Storefront (thu nhỏ còn rộng 360px)
logo = Image.open(os.path.join(ROOT, "assets", "logo", "logo-white.png"))
logo.thumbnail((360, 360))
logo.save(os.path.join(OUT, "img", "logo.png"))
