#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tính bảng gợi ý size từ bộ dữ liệu đo cơ thể ANSUR II (quân đội Mỹ, ~6.000 người).

Chạy từ thư mục gốc dự án:
    python tools/build_size_chart.py

Đầu vào : data/ANSUR_II_MALE_Public.csv, data/ANSUR_II_FEMALE_Public.csv
Đầu ra  : data/size-chart.json (js/size-finder.js đọc file này bằng fetch)

Ý tưởng (đơn giản, dễ giải thích khi vấn đáp):
  1. Quần áo được chia size theo vòng ngực (cm). Dùng mốc vòng ngực của các bảng size công bố (Nike, ASICS...).
  2. Khách hàng không biết vòng ngực, chỉ biết chiều cao + cân nặng.
     => Dùng dữ liệu ANSUR II để học công thức:  vòng_ngực ≈ a + b * cân_nặng + c * chiều_cao
        (hồi quy tuyến tính bình phương tối thiểu, tính riêng cho nam và nữ).
  3. Web đưa chiều cao + cân nặng của khách vào công thức, ra vòng ngực dự đoán, rồi tra mốc để chọn size.

Đơn vị trong file ANSUR II: chiều dài tính bằng milimét, weightkg tính bằng 1/10 kg.
Script chỉ đọc 3 cột cần thiết (stature, weightkg, chestcircumference).
"""
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = {"him": ROOT / "data" / "ANSUR_II_MALE_Public.csv", "her": ROOT / "data" / "ANSUR_II_FEMALE_Public.csv"}
OUT = ROOT / "data" / "size-chart.json"

SIZES = ["XXS", "XS", "S", "M", "L", "XL"]
# Cận trên vòng ngực (cm) của XXS, XS, S, M, L; từ mốc cuối trở lên là XL.
# Lấy theo các bảng size công bố: nam M ≈ 96-104, L ≈ 104-112; nữ lệch nhỏ hơn khoảng 6 cm.
CHEST_LIMITS = {
    "him": [84, 90, 96, 104, 112],
    "her": [78, 84, 90, 97, 104],
}


def load(path):
    """Trả về danh sách (chiều cao cm, cân nặng kg, vòng ngực cm)."""
    rows = []
    with open(path, newline="", encoding="latin-1") as f:   # file ANSUR II mã hóa Latin-1 (có ký tự é...)
        for r in csv.DictReader(f):
            try:
                height = float(r["stature"]) / 10            # mm -> cm
                weight = float(r["weightkg"]) / 10           # 1/10 kg -> kg
                chest = float(r["chestcircumference"]) / 10  # mm -> cm
            except (KeyError, ValueError):
                continue
            if height > 0 and weight > 0 and chest > 0:
                rows.append((height, weight, chest))
    return rows


def solve3(a, b):
    """Giải hệ 3 phương trình 3 ẩn A·x = b bằng khử Gauss (không cần thư viện ngoài)."""
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    n = 3
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(m[r][col]))
        m[col], m[pivot] = m[pivot], m[col]
        for r in range(col + 1, n):
            factor = m[r][col] / m[col][col]
            for c in range(col, n + 1):
                m[r][c] -= factor * m[col][c]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (m[i][n] - sum(m[i][j] * x[j] for j in range(i + 1, n))) / m[i][i]
    return x


def fit(rows):
    """Hồi quy chest = a + b*weight + c*height. Trả về (a, b, c)."""
    n = len(rows)
    # Ma trận chuẩn: (XᵀX)·beta = Xᵀy với X = [1, weight, height]
    s = [[0.0] * 3 for _ in range(3)]
    t = [0.0] * 3
    for h, w, c in rows:
        x = (1.0, w, h)
        for i in range(3):
            t[i] += x[i] * c
            for j in range(3):
                s[i][j] += x[i] * x[j]
    a, b, c = solve3(s, t)
    return a, b, c


def percentile(values, p):
    values = sorted(values)
    k = (len(values) - 1) * p
    lo, hi = math.floor(k), math.ceil(k)
    return values[lo] + (values[hi] - values[lo]) * (k - lo)


def size_index(chest, limits):
    for i, limit in enumerate(limits):
        if chest < limit:
            return i
    return len(limits)


def main():
    result = {
        "source": "ANSUR II (U.S. Army Anthropometric Survey 2012), public data",
        "note": "Chest circumference is predicted from height and weight with least-squares regression; "
                "size is chosen from published apparel chest ranges.",
        "sizes": SIZES,
    }
    for gender, path in FILES.items():
        rows = load(path)
        a, b, c = fit(rows)

        errors = [(a + b * w + c * h) - chest for h, w, chest in rows]
        rmse = math.sqrt(sum(e * e for e in errors) / len(errors))
        # Độ chính xác: bao nhiêu % người được gợi ý đúng size theo vòng ngực thật
        limits = CHEST_LIMITS[gender]
        exact = sum(1 for h, w, chest in rows if size_index(a + b * w + c * h, limits) == size_index(chest, limits))
        within_one = sum(1 for h, w, chest in rows
                         if abs(size_index(a + b * w + c * h, limits) - size_index(chest, limits)) <= 1)

        result[gender] = {
            "sampleSize": len(rows),
            "intercept": round(a, 4),
            "perKg": round(b, 4),
            "perCm": round(c, 4),
            "rmseCm": round(rmse, 2),
            "chestLimitsCm": limits,
            "exactSizePct": round(100 * exact / len(rows), 1),
            "withinOneSizePct": round(100 * within_one / len(rows), 1),
            # Khoảng chiều cao/cân nặng có trong dữ liệu (P1-P99) để cảnh báo khi khách nhập ngoài khoảng
            "heightRangeCm": [round(percentile([r[0] for r in rows], 0.01)), round(percentile([r[0] for r in rows], 0.99))],
            "weightRangeKg": [round(percentile([r[1] for r in rows], 0.01)), round(percentile([r[1] for r in rows], 0.99))],
        }
        print(gender, {k: v for k, v in result[gender].items() if k != "chestLimitsCm"})

    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("Wrote", OUT)


if __name__ == "__main__":
    main()
