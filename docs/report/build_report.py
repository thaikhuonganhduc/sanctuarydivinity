# -*- coding: utf-8 -*-
"""Dựng báo cáo đồ án cuối kỳ (file Word) theo outline của giảng viên.
Chạy:  python docs/report/build_report.py
Kết quả: docs/report/BaoCao_DoAn_SANCTUARY.docx
Mở bằng Word rồi bấm Yes khi Word hỏi cập nhật trường (mục lục, danh mục hình/bảng), hoặc chạy finalize_report.ps1."""
import json
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))

from docx_helpers import Report  # noqa: E402
import report_front, report_ch1, report_ch2, report_ch3, report_ch4, report_ch5_6, report_back  # noqa: E402

IMG = HERE / "img"
DIAG = ROOT / "docs" / "diagrams" / "png"
COMP = IMG / "composite"


def side_by_side(files, out, height=1600, gap=40):
    """Ghép nhiều ảnh (cùng chiều cao) thành 1 ảnh ngang, nền trắng."""
    ims = [Image.open(f).convert("RGB") for f in files]
    ims = [im.resize((int(im.width * height / im.height), height)) for im in ims]
    w = sum(im.width for im in ims) + gap * (len(ims) - 1)
    canvas = Image.new("RGB", (w, height), "white")
    x = 0
    for im in ims:
        canvas.paste(im, (x, 0))
        x += im.width + gap
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out)
    return out


def make_composites():
    w = IMG / "web"
    side_by_side([w / "40-m-gate.png", w / "41-m-home.png", w / "42-m-shop.png"], COMP / "mobile-1.png")
    side_by_side([w / "43-m-product.png", w / "44-m-cart.png", w / "45-m-contact.png"], COMP / "mobile-2.png")


def context():
    """Số liệu thật đọc từ mã nguồn và kết quả đo, để báo cáo không ghi số tay."""
    products = json.loads((ROOT / "data" / "products.json").read_text(encoding="utf-8"))["products"]
    reviews = json.loads((ROOT / "data" / "reviews.json").read_text(encoding="utf-8"))
    reviews = reviews["reviews"] if isinstance(reviews, dict) else reviews
    size_chart = json.loads((ROOT / "data" / "size-chart.json").read_text(encoding="utf-8"))

    def lines(pattern):
        return sum(len(p.read_text(encoding="utf-8").splitlines()) for p in ROOT.glob(pattern))
    return {
        "root": ROOT, "img": IMG, "diag": DIAG, "comp": COMP,
        "products": products, "n_products": len(products),
        "n_colors": sum(len(p["colors"]) for p in products),
        "n_reviews": len(reviews), "size_chart": size_chart,
        "js_files": len(list((ROOT / "js").glob("*.js"))),
        "js_lines": lines("js/*.js"), "css_lines": lines("css/*.css"),
        "html_lines": lines("pages/*.html") + lines("index.html"),
        "lighthouse": json.loads((HERE / "data" / "lighthouse-results.json").read_text(encoding="utf-8")),
        # Lần đo đầu (trước khi sửa CLS, W3C, meta description) để so sánh trước/sau
        "lighthouse_before": json.loads((HERE / "data" / "lighthouse-before.json").read_text(encoding="utf-8")),
        "tests_online": json.loads((HERE / "data" / "functional-tests-online.json").read_text(encoding="utf-8")),
        "tests": json.loads((HERE / "data" / "functional-tests.json").read_text(encoding="utf-8")),
    }


def main():
    make_composites()
    ctx = context()
    R = Report()
    report_front.build(R, ctx)
    report_ch1.build(R, ctx)
    report_ch2.build(R, ctx)
    report_ch3.build(R, ctx)
    report_ch4.build(R, ctx)
    report_ch5_6.build(R, ctx)
    report_back.build(R, ctx)
    out = HERE / "BaoCao_DoAn_SANCTUARY.docx"
    R.save(out)
    print("Đã lưu", out)


if __name__ == "__main__":
    main()
