#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Đổi ảnh sản phẩm và ảnh review đang được web dùng sang WebP (nhẹ hơn JPG khoảng một nửa).

Chạy từ thư mục gốc dự án (cần: pip install pillow):
    python tools/optimize_images.py

Script chỉ chuyển những ảnh được nhắc tới trong data/products.json và data/reviews.json.
File gốc (JPG/PNG) giữ nguyên trên máy (đã được .gitignore, không đưa lên GitHub).
Chạy lại nhiều lần vẫn an toàn: ảnh WebP đã có sẽ được bỏ qua.
"""
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
QUALITY = 80         # chất lượng WebP (0-100)
MAX_WIDTH = 800      # ảnh crawl đã là 800px; đặt trần để đảm bảo không to hơn


def convert(src, dst):
    """JPG -> WebP. Trả về (kích thước gốc, kích thước mới) theo byte; None nếu không có file gốc."""
    if dst.exists():
        return None
    if not src.exists():
        return None
    with Image.open(src) as im:
        im = im.convert("RGB")
        if im.width > MAX_WIDTH:
            im = im.resize((MAX_WIDTH, round(im.height * MAX_WIDTH / im.width)), Image.LANCZOS)
        im.save(dst, "WEBP", quality=QUALITY, method=6)
    return src.stat().st_size, dst.stat().st_size


def main():
    targets = []   # danh sách đường dẫn .webp cần có (tính từ thư mục gốc)

    products = json.loads((ROOT / "data" / "products.json").read_text(encoding="utf-8"))["products"]
    for p in products:
        for color in p["colors"]:
            targets.extend(color["images"])

    reviews = json.loads((ROOT / "data" / "reviews.json").read_text(encoding="utf-8"))["reviews"]
    targets.extend(r["image"] + ".webp" for r in reviews)

    before = after = done = missing = 0
    for rel in dict.fromkeys(targets):            # bỏ trùng, giữ thứ tự
        dst = ROOT / rel
        # ảnh gốc có thể là .jpg, .jpeg hoặc .png
        src = next((dst.with_suffix(ext) for ext in (".jpg", ".jpeg", ".png") if dst.with_suffix(ext).exists()), dst.with_suffix(".jpg"))
        result = convert(src, dst)
        if result:
            before += result[0]
            after += result[1]
            done += 1
        elif not dst.exists():
            missing += 1
            print("Thiếu ảnh gốc:", rel)

    print("Đã chuyển %d ảnh: %.1f MB -> %.1f MB" % (done, before / 1e6, after / 1e6))
    total = sum((ROOT / rel).stat().st_size for rel in dict.fromkeys(targets) if (ROOT / rel).exists())
    print("Tổng dung lượng ảnh web dùng: %.1f MB (%d ảnh), thiếu %d" % (total / 1e6, len(set(targets)), missing))


if __name__ == "__main__":
    main()
