# -*- coding: utf-8 -*-
"""Dựng báo cáo đồ án cuối kỳ (Word) theo cấu trúc báo cáo mẫu: Phần A (ý tưởng kinh doanh),
Phần B (xây dựng và phát triển website), Phần C (tổng kết).
Chạy:  python docs/report/build_report.py
Sau đó chạy docs/report/finalize_report.ps1 để Word cập nhật mục lục, danh mục hình và bảng."""
import json
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))

from docx_helpers import Report  # noqa: E402
import rp_front, rp_a, rp_b1, rp_b2, rp_b3_4, rp_b5, rp_b6, rp_b7, rp_b8, rp_c  # noqa: E402

IMG = HERE / "img"


def side_by_side(files, out, height=1600, gap=40):
    """Ghép nhiều ảnh (cùng chiều cao) thành 1 ảnh ngang, nền trắng."""
    ims = [Image.open(f).convert("RGB") for f in files]
    ims = [im.resize((int(im.width * height / im.height), height)) for im in ims]
    canvas = Image.new("RGB", (sum(im.width for im in ims) + gap * (len(ims) - 1), height), "white")
    x = 0
    for im in ims:
        canvas.paste(im, (x, 0))
        x += im.width + gap
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out)
    return out


def make_composites():
    w, c = IMG / "web", IMG / "composite"
    side_by_side([w / "40-m-gate.png", w / "41-m-home.png", w / "42-m-shop.png"], c / "mobile-1.png")
    side_by_side([w / "43-m-product.png", w / "44-m-cart.png", w / "45-m-contact.png"], c / "mobile-2.png")
    # Bảng màu thương hiệu (vẽ từ biến màu trong css/base.css)
    from PIL import ImageDraw, ImageFont
    colors = [("#000000", "Đen tuyền\n#000000\nnền chính"), ("#141414", "Than\n#141414\nnền khối"),
              ("#2A2A2A", "Xám viền\n#2A2A2A\nđường viền"), ("#8A8A8A", "Xám chữ phụ\n#8A8A8A\nchú thích"),
              ("#F2F2F2", "Trắng ngà\n#F2F2F2\nchữ chính"), ("#CC0000", "Đỏ thương hiệu\n#CC0000\nđiểm nhấn")]
    im = Image.new("RGB", (1800, 520), "white")
    d = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/times.ttf", 34)
    except OSError:
        font = ImageFont.load_default()
    for i, (hexc, label) in enumerate(colors):
        x = 30 + i * 295
        d.rectangle([x, 30, x + 260, 290], fill=hexc, outline="#999999", width=2)
        d.multiline_text((x + 130, 310), label, fill="black", font=font, anchor="ma", align="center", spacing=8)
    im.save(c / "palette.png")


def context():
    """Số liệu thật đọc từ mã nguồn và kết quả đo, để báo cáo không ghi số tay."""
    load = lambda p: json.loads((ROOT / p).read_text(encoding="utf-8"))
    products = load("data/products.json")["products"]
    reviews = load("data/reviews.json")["reviews"]

    def lines(pattern):
        return sum(len(p.read_text(encoding="utf-8").splitlines()) for p in ROOT.glob(pattern))
    data = HERE / "data"
    return {
        "root": ROOT, "img": IMG, "web": IMG / "web", "woo": IMG / "woo", "comp": IMG / "composite",
        "diag": ROOT / "docs" / "diagrams" / "png",
        "products": products, "n_products": len(products), "n_colors": sum(len(p["colors"]) for p in products),
        "n_reviews": len(reviews), "reviews": reviews, "size_chart": load("data/size-chart.json"),
        "js_files": len(list((ROOT / "js").glob("*.js"))),
        "js_lines": lines("js/*.js"), "css_lines": lines("css/*.css"), "html_lines": lines("pages/*.html") + lines("index.html"),
        "lighthouse": json.loads((data / "lighthouse-results.json").read_text(encoding="utf-8")),
        "lighthouse_before": json.loads((data / "lighthouse-before.json").read_text(encoding="utf-8")),
        "tests": json.loads((data / "functional-tests.json").read_text(encoding="utf-8")),
        "tests_online": json.loads((data / "functional-tests-online.json").read_text(encoding="utf-8")),
    }


def main():
    make_composites()
    ctx = context()
    R = Report()
    for mod in (rp_front, rp_a, rp_b1, rp_b2, rp_b3_4, rp_b5, rp_b6, rp_b7, rp_b8, rp_c):
        mod.build(R, ctx)
    # Tên file có thể truyền vào (ví dụ khi file cũ đang mở trong Word): python build_report.py TenKhac.docx
    out = HERE / (sys.argv[1] if len(sys.argv) > 1 else "BaoCao_DoAn_SANCTUARY_v3.docx")
    R.save(out)
    print("Đã lưu", out)


if __name__ == "__main__":
    main()
