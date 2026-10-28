#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chuyển dữ liệu crawl (data/bd-products.json) thành data/products.json đúng cấu trúc của web.

Chạy từ thư mục gốc dự án:
    python tools/build_products.py

Những gì script làm:
  - Gộp các sản phẩm cùng tên khác màu ("... [NIGHTMARE]", "... [VOID BLACK]") thành 1 sản phẩm nhiều màu.
  - Bỏ hàng đấu giá (Auction), giá 0.
  - Suy ra category + gender (him/her/unisex) từ type và tag của shop gốc.
  - Đổi size gốc (2XS..5XL) về thang XXS..XL của đồ án.
  - Tách thông số (GSM, Care, chất liệu, form) từ mô tả; bỏ dòng "Size Guide" và dòng giao hàng.
  - Thay tên thương hiệu gốc (Breathe Divinity / BD) bằng SANCTUARY (claude.md: không dùng thương hiệu của họ).
  - Số lượng tồn kho `stock` shop gốc không công khai -> TẠO GIẢ LẬP (có hàng: 4..120, hết hàng: 0).
    Sau này admin sẽ sửa số này.
"""
import json
import re
import zlib
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "bd-products.json"
REVIEWS = ROOT / "data" / "reviews.json"
OUT = ROOT / "data" / "products.json"

SIZES = ["XXS", "XS", "S", "M", "L", "XL", "XXL"]   # nhóm chọn bán đủ XXS -> XXL cho mọi sản phẩm quần áo
SIZE_MAP = {"2XS": "XXS", "XXS": "XXS", "XS": "XS", "S": "S", "M": "M", "L": "L", "XL": "XL", "2XL": "XXL", "XXL": "XXL"}
MAX_IMAGES = 4   # số ảnh giữ lại cho mỗi màu

# type của shop gốc -> category của web
CATEGORY = {
    "Compression": "compression", "": "compression",
    "Oversized Tee": "oversize",
    "Hoodie": "hoodies", "Crewneck": "hoodies",
    "Bodysuit": "bodysuits",
    "Sweatpants": "bottoms", "Cargos": "bottoms", "Shorts": "bottoms", "Leggings": "bottoms", "Jeans": "bottoms",
    "Stringer": "tops", "Cut-off Tee": "tops", "Beater": "tops", "Baby Tee": "tops", "Sports Bra": "tops",
    "Cap": "accessories", "Beanie": "accessories",
}

# Màu hiển thị (chấm màu) cho từng tên màu của shop gốc
HEX = {
    "VOID BLACK": "#0a0a0a", "NIGHTMARE": "#8b0a1a", "DIVINE WHITE": "#f2f2f2", "GLOW IN THE DARK": "#39d353",
    "DARKNESS": "#1b1b1b", "BLOSSOM PINK": "#e8a0b8", "VINTAGE": "#6b6b6b", "DUSK": "#4a4458", "BONESAW": "#c9c0ac",
    "GHOST": "#cfd2d6", "HEAVENLY PINK": "#f0b6c8", "HEAVENLY RED": "#a81d23", "VINTAGE WASH": "#58595b",
    "ANGEL WASHED": "#b9bcc2", "ALLOY WASHED": "#7d8187", "2-PACK": "#2b2b2b", "NOCTURNE": "#1d2a4a",
    "AMETHYST": "#6a3fa0", "PUMPKIN": "#d2691e", "CLARK/CARNAGE": "#8b0000", "WIDOW": "#111111",
    "MIDNIGHT": "#101830", "PORCELAIN": "#ece7de", "SHADOW": "#2e2e2e", "PLATINUM": "#c7c9cc", "SCORCH": "#c2410c",
    "ARC LIGHT": "#e0e7ff", "DECAY": "#4d5b3d", "ABYSSAL": "#0b2a3a", "HAZELNUT": "#8b6b4a",
    "BLUEBERRY MUFFIN": "#4b5d8a", "IVORY": "#f5f0e1", "VINTAGE WASHED": "#5f6063", "REVENANT": "#3b3b3b",
}

BRAND = re.compile(r"breathe\s*divinity|breathedivinity|\bBD\b", re.I)


def base_title(title):
    return re.sub(r"\s*\[[^\]]*\]\s*$", "", title).strip()


def color_name(title):
    m = re.search(r"\[([^\]]*)\]\s*$", title)
    return m.group(1).strip() if m else "Default"


def gender_of(p, category):
    if category == "accessories":
        return "unisex"
    tags = " ".join(p["tags"]).upper()
    if "WOMENS" in tags:
        return "her"
    return "him"


def map_size(label):
    # "S (30)" -> "S", "2XL (38)" -> "2XL"
    key = re.sub(r"\s*\(.*\)", "", label).strip().upper()
    return SIZE_MAP.get(key)


def clean_text(text):
    return BRAND.sub("SANCTUARY", text)


def parse_description(desc, title):
    """Trả về (description, features, specs)."""
    lines = [l.strip() for l in desc.splitlines() if l.strip()]
    care = ""
    features = []
    for line in lines:
        low = line.lower()
        if line.lower() == title.lower() or line.lower() == base_title(title).lower():
            continue
        if low.startswith("care:"):
            care = line.split(":", 1)[1].strip()
            continue
        if low.startswith("size guide") or low.startswith("ships in") or low.startswith("shipping"):
            continue
        features.append(clean_text(line))

    joined = " ".join(features)
    gsm = re.search(r"(\d{3})\s*GSM", joined, re.I)
    material = ""
    for f in features:
        m = re.search(r"\d+%[^.;]*", f)
        if m:
            material = re.sub(r"\s*\(grams per square meter\)", "", m.group(0)).strip()
            break
    fit = ""
    for f in features:
        if re.search(r"\b(fit|fitted|oversized|boxy|relaxed|compression|second-skin)\b", f, re.I) and len(f) < 90:
            fit = f
            break
    specs = {"material": material, "weight": (gsm.group(1) + " GSM") if gsm else "", "fit": fit, "care": clean_text(care)}
    # Mỗi dòng mô tả là 1 ý (hiện thành danh sách trong popup), không có đoạn mô tả riêng
    return "", features, specs


def review_counts(names):
    """Đếm số review nhắc tới từng sản phẩm (để chọn sản phẩm nổi bật)."""
    counts = {n: 0 for n in names}
    if not REVIEWS.exists():
        return counts
    for r in json.loads(REVIEWS.read_text(encoding="utf-8"))["reviews"]:
        product = r.get("product", "")
        for n in names:
            if base_title(product) == n:
                counts[n] += 1
    return counts


def fake_stock(key):
    """Số tồn kho giả lập ổn định theo tên sản phẩm (4..120)."""
    h = zlib.crc32(key.encode("utf-8")) % 1000
    return 4 + (h * 116) // 999


def main():
    products = json.loads(SRC.read_text(encoding="utf-8"))["products"]
    groups = OrderedDict()
    for p in products:
        if p["type"] == "Auction" or p["price"] <= 0:
            continue
        groups.setdefault(base_title(p["title"]), []).append(p)

    counts = review_counts(list(groups))
    top = sorted(groups, key=lambda n: -counts[n])[:8]

    out = []
    for i, (name, items) in enumerate(groups.items(), start=1):
        first = items[0]
        category = CATEGORY.get(first["type"], "tops")
        description, features, specs = parse_description(first["description"], first["title"])

        colors = []
        sizes = set()
        any_available = False
        for p in items:
            avail = any(v["available"] for v in p["variants"])
            any_available = any_available or avail
            for v in p["variants"]:
                for opt in (v["option1"], v["option2"], v["option3"]):
                    s = map_size(opt) if opt else None
                    if s:
                        sizes.add(s)
            cname = color_name(p["title"])
            colors.append({
                "name": cname.title() if cname != "Default" else "Black",
                "hex": HEX.get(cname.upper(), "#2b2b2b"),
                "images": [re.sub(r"\.(jpe?g|png)$", ".webp", i) for i in p["images"][:MAX_IMAGES]],   # ảnh WebP do tools/optimize_images.py tạo
                "available": avail,
            })

        stock = fake_stock(name) if any_available else 0
        # Phụ kiện (mũ, nón): giữ size của shop gốc hoặc "One size"; quần áo: bán đủ dải XXS -> XXL
        if category == "accessories":
            sizes_list = [s for s in SIZES if s in sizes] or ["One size"]
        else:
            sizes_list = SIZES
        out.append(OrderedDict([
            ("id", "p%02d" % i),
            ("name", name),
            ("category", category),
            ("gender", gender_of(first, category)),
            ("price", float(first["price"])),
            ("currency", "USD"),
            ("colors", colors),
            ("sizes", sizes_list),
            ("featured", name in top),
            ("inStock", stock > 0),
            ("stock", stock),
            ("tag", "" if stock > 0 else "Sold out"),
            ("specs", specs),
            ("description", description),
            ("features", features),
            ("source", first["url"]),
        ]))

    OUT.write_text(json.dumps({"products": out}, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Wrote", OUT, "-", len(out), "products,", sum(len(p["colors"]) for p in out), "colors")


if __name__ == "__main__":
    main()
