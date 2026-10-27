#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo data/reviews.json từ dữ liệu crawl (data/bd-reviews.json).

Chạy từ thư mục gốc dự án:
    python tools/build_reviews.py

Những gì script làm:
  - Bỏ review nhắc tên thương hiệu gốc (Breathe Divinity / BD) trong lời khách (claude.md: không dùng thương hiệu của họ).
  - Gộp các review của CÙNG MỘT NGƯỜI (cùng tên hiển thị) thành 1 đánh giá:
      * ảnh trùng nhau (cùng nội dung file) chỉ giữ 1 ảnh, các ảnh còn lại hiện dạng slideshow
      * mọi lời đánh giá và sản phẩm của người đó được giữ trong "entries"
      * điểm sao = trung bình các lần đánh giá
    Lưu ý: tên hiển thị chỉ là "Họ + chữ cái đầu" (ví dụ "Chris C."), nên 2 người khác nhau trùng tên vẫn có thể bị gộp nhầm.
  - Gắn nhãn ngôn ngữ (en, ko...) theo chữ viết để trình duyệt chọn đúng font.

Cần chạy tools/optimize_images.py sau đó để tạo ảnh WebP cho các ảnh được dùng.
"""
import hashlib
import json
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "bd-reviews.json"
OUT = ROOT / "data" / "reviews.json"

BRAND = re.compile(r"breathe|divinity|\bbd\b", re.I)


def detect_lang(text):
    if re.search(r"[가-힯]", text):
        return "ko"
    if re.search(r"[぀-ヿ]", text):
        return "ja"
    if re.search(r"[一-鿿]", text):
        return "zh"
    if re.search(r"[Ѐ-ӿ]", text):
        return "ru"
    if re.search(r"[฀-๿]", text):
        return "th"
    if re.search(r"[؀-ۿ]", text):
        return "ar"
    return "en"


def image_hash(base):
    """Băm nội dung ảnh để nhận ra 2 review dùng cùng 1 ảnh. Ưu tiên file gốc, không có thì dùng WebP."""
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        path = ROOT / (base + ext)
        if path.exists():
            return hashlib.md5(path.read_bytes()).hexdigest()
    return base   # không thấy file: coi như ảnh riêng


def main():
    raw = json.loads(SRC.read_text(encoding="utf-8"))["reviews"]
    groups = OrderedDict()   # tên (chữ thường) -> danh sách review của người đó
    skipped = 0
    for r in raw:
        if BRAND.search(r["comment"]) or BRAND.search(r["name"]) or BRAND.search(r["product"]):
            skipped += 1
            continue
        groups.setdefault(" ".join(r["name"].lower().split()), []).append(r)

    out = []
    for items in groups.values():
        entries, images, seen = [], [], set()
        for r in items:
            text = " ".join(r["comment"].split())
            entries.append({
                "rating": float(r["stars"]),
                "text": text,
                "lang": detect_lang(text),
                "product": r["product"].strip(),
            })
            base = r["image"][:-4]                    # bỏ đuôi .jpg, web tự thử .webp rồi .jpg
            digest = image_hash(base)
            if digest not in seen:
                seen.add(digest)
                images.append(base)

        primary = max(entries, key=lambda e: len(e["text"]))   # lời đánh giá dài nhất hiện trên thẻ
        out.append(OrderedDict([
            ("id", "r%03d" % (len(out) + 1)),
            ("name", items[0]["name"].strip()),
            ("lang", primary["lang"]),
            ("rating", round(sum(e["rating"] for e in entries) / len(entries), 1)),
            ("verified", any(r["verified"] for r in items)),
            ("images", images),
            ("entries", entries),
        ]))

    OUT.write_text(json.dumps({"reviews": out}, ensure_ascii=False, indent=2), encoding="utf-8")
    merged = [o for o in out if len(o["entries"]) > 1]
    print("Wrote %s: %d reviews (bỏ %d review nhắc thương hiệu gốc)" % (OUT, len(out), skipped))
    print("  gộp: %d người có nhiều đánh giá, %d người có nhiều ảnh (slideshow)" % (
        len(merged), sum(1 for o in out if len(o["images"]) > 1)))


if __name__ == "__main__":
    main()
