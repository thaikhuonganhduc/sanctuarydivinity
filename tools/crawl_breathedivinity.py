#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crawl breathedivinity.com cho đồ án web.
Chạy trên máy bạn, chỉ cần Python 3.8+ (không cần cài thư viện nào).

Chạy từ thư mục gốc dự án:
    python tools/crawl_breathedivinity.py                 # toàn bộ sản phẩm + 200 review
    python tools/crawl_breathedivinity.py --reviews 100   # đổi số review
    python tools/crawl_breathedivinity.py --width 1200    # đổi độ rộng ảnh sản phẩm (px)

Chạy lại nhiều lần vẫn an toàn: ảnh đã tải sẽ được bỏ qua.

Kết quả:
    data/bd-products.json               sản phẩm (đường dẫn ảnh local)
    data/bd-reviews.json                review: ảnh, tên, ngày, số sao, comment, sản phẩm
    assets/products/<handle>/NN.jpg     ảnh sản phẩm
    assets/reviews/crawled/lx_<id>.jpg  ảnh review
Script KHÔNG ghi đè data/products.json, data/reviews.json hay ảnh sẵn có.
"""
import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

SHOP = "https://breathedivinity.com"
LOOX = "https://loox.io/widget/EJbQDfDdRK/reviews"
LOOX_QS = "h=&total=20146&language=en&page={page}"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")

ROOT = Path(__file__).resolve().parent.parent
PRODUCT_IMG_DIR = ROOT / "assets" / "products"
REVIEW_IMG_DIR = ROOT / "assets" / "reviews" / "crawled"
DATA_DIR = ROOT / "data"


def log(*args):
    print(*args, flush=True)


def http_get(url, tries=6, timeout=30):
    last = None
    for i in range(tries):
        wait = 1.5 * (i + 1)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (429, 503):  # bị giới hạn tốc độ -> chờ lâu hơn
                try:
                    wait = max(wait, float(e.headers.get("Retry-After") or 0))
                except ValueError:
                    pass
                wait = max(wait, 15 * (i + 1))
                if i < tries - 1:
                    log(f"  server báo quá tải ({e.code}), chờ {wait:.0f}s rồi thử lại...")
        except Exception as e:  # noqa: BLE001
            last = e
        if i < tries - 1:
            time.sleep(wait)
    raise RuntimeError(f"GET failed: {url} ({last})")


def norm(s):
    return re.sub(r"\s+", " ", html.unescape(s or "")).strip().lower()


def strip_tags(s):
    s = re.sub(r"<br\s*/?>", "\n", s or "", flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s).strip()


def slug(s, n=80):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", s or "").strip("-")[:n] or "item"


def ext_of(url, default=".jpg"):
    m = re.search(r"\.(jpe?g|png|webp|gif)$", url.split("?")[0], re.I)
    return "." + m.group(1).lower() if m else default


def sized(url, width):
    return url + ("&" if "?" in url else "?") + f"width={width}"


# ---------------------------------------------------------------- sản phẩm
def fetch_products():
    items, page = [], 1
    while page <= 50:
        raw = http_get(f"{SHOP}/products.json?limit=250&page={page}")
        try:
            batch = json.loads(raw).get("products", [])
        except ValueError:
            sys.exit("products.json không trả về JSON (shop có thể đang bật trang mật khẩu).")
        if not batch:
            break
        items.extend(batch)
        if len(batch) < 250:  # trang cuối, không cần gọi thêm trang trống
            break
        page += 1
        time.sleep(0.5)
    return items


def build_products(raw, width):
    out, jobs = [], []
    for p in raw:
        folder = PRODUCT_IMG_DIR / slug(p["handle"])
        local_by_src, paths = {}, []
        for i, img in enumerate(p.get("images", []), 1):
            dest = folder / f"{i:02d}{ext_of(img['src'])}"
            rel = dest.relative_to(ROOT).as_posix()
            jobs.append((sized(img["src"], width), dest))
            local_by_src[img["src"]] = rel
            paths.append(rel)
        variants = []
        for v in p.get("variants", []):
            fi = (v.get("featured_image") or {}).get("src")
            cmp_price = v.get("compare_at_price")
            variants.append({
                "id": v["id"],
                "title": v.get("title"),
                "sku": v.get("sku"),
                "option1": v.get("option1"),
                "option2": v.get("option2"),
                "option3": v.get("option3"),
                "price": float(v["price"]),
                "comparePrice": float(cmp_price) if cmp_price else None,
                "available": bool(v.get("available")),
                "image": local_by_src.get(fi),
            })
        prices = [v["price"] for v in variants]
        out.append({
            "id": p["id"],
            "handle": p["handle"],
            "title": p["title"],
            "type": p.get("product_type") or "",
            "vendor": p.get("vendor"),
            "tags": p.get("tags", []),
            "url": f"{SHOP}/products/{p['handle']}",
            "price": min(prices) if prices else None,
            "available": any(v["available"] for v in variants),
            "options": [{"name": o.get("name"), "values": o.get("values", [])}
                        for o in p.get("options", [])],
            "variants": variants,
            "images": paths,
            "description": strip_tags(p.get("body_html")),
            "descriptionHtml": p.get("body_html") or "",
            "createdAt": p.get("created_at"),
            "publishedAt": p.get("published_at"),
        })
    return out, jobs


# ------------------------------------------------------------------ review
CARD_RE = re.compile(r'<div\b[^>]*\bclass="grid-item-wrap[^"]*"[^>]*>', re.S)


def parse_reviews(page_html):
    starts = list(CARD_RE.finditer(page_html))
    out = []
    for i, m in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(page_html)
        chunk = page_html[m.start():end]
        rid = re.search(r'data-id="([^"]+)"', m.group(0))
        photo = re.search(r'<img\b[^>]*\bsrc="((?:https?:)?//images\.loox\.io/[^"]+)"', chunk)
        if not rid or not photo:
            continue  # review không có ảnh -> bỏ qua
        src = photo.group(1)
        if src.startswith("//"):
            src = "https:" + src
        name = re.search(r'class="block title"[^>]*>([^<]*)', chunk)
        ts = re.search(r'data-time="(\d+)"', chunk)
        stars = re.search(r"Rating icons:\s*(\d+)\s*/\s*5", chunk)
        text = re.search(r'class="pre-wrap main-text"[^>]*>(.*?)</div>', chunk, re.S)
        prod = re.search(r'class="name[^"]*"[^>]*>(.*?)</div>', chunk, re.S)
        when = (datetime.fromtimestamp(int(ts.group(1)) / 1000, timezone.utc)
                if ts else None)
        out.append({
            "id": rid.group(1),
            "name": html.unescape(name.group(1)).strip() if name else "",
            "date": when.strftime("%Y-%m-%d") if when else None,
            "createdAt": when.isoformat() if when else None,
            "stars": int(stars.group(1)) if stars else None,
            "comment": strip_tags(text.group(1)) if text else "",
            "product": re.sub(r"\s+", " ", strip_tags(prod.group(1))) if prod else "",
            "verified": "loox-verified-badge" in chunk,
            "imageRemote": src,
        })
    return out


def fetch_reviews(limit):
    out, seen, page = [], set(), 1
    while len(out) < limit and page <= 80:
        url = f"{LOOX}?{LOOX_QS.format(page=page)}"
        batch = parse_reviews(http_get(url).decode("utf-8", "replace"))
        if not batch:
            break
        for r in batch:
            if r["id"] not in seen and len(out) < limit:
                seen.add(r["id"])
                out.append(r)
        log(f"  review trang {page}: {len(out)}/{limit}")
        page += 1
        time.sleep(0.8)
    return out


def build_reviews(reviews, products):
    by_title = {norm(p["title"]): p["handle"] for p in products}
    jobs, used = [], set()
    for r in reviews:
        base = "lx_" + re.sub(r"[^A-Za-z0-9_-]", "", r["id"])
        if base.lower() in used:  # Windows không phân biệt hoa/thường
            base += "_2"
        used.add(base.lower())
        dest = REVIEW_IMG_DIR / (base + ext_of(r["imageRemote"]))
        r["image"] = dest.relative_to(ROOT).as_posix()
        r["productHandle"] = by_title.get(norm(r["product"]))
        jobs.append((r["imageRemote"], dest))
    return jobs


# ------------------------------------------------------------------ tải ảnh
def download(job):
    url, dest = job
    if dest.exists() and dest.stat().st_size > 0:
        return True, url
    try:
        data = http_get(url)
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmp = dest.with_name(dest.name + ".part")
        tmp.write_bytes(data)
        tmp.replace(dest)
        return True, url
    except Exception as e:  # noqa: BLE001
        return False, f"{url} -> {e}"


def download_all(jobs, workers=3):
    ok, failed = 0, []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for i, (good, info) in enumerate(ex.map(download, jobs), 1):
            if good:
                ok += 1
            else:
                failed.append(info)
            if i % 50 == 0 or i == len(jobs):
                log(f"  ảnh {i}/{len(jobs)} (lỗi: {len(failed)})")
    return ok, failed


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--reviews", type=int, default=200, help="số review có ảnh cần lấy (mặc định 200)")
    ap.add_argument("--width", type=int, default=800, help="độ rộng ảnh sản phẩm, px (mặc định 800)")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    log("1/4 Lấy danh sách sản phẩm...")
    raw = fetch_products()
    products, jobs_p = build_products(raw, args.width)
    log(f"  {len(products)} sản phẩm, {len(jobs_p)} ảnh")

    log(f"2/4 Lấy {args.reviews} review từ Loox...")
    reviews = fetch_reviews(args.reviews)
    jobs_r = build_reviews(reviews, products)
    matched = sum(1 for r in reviews if r["productHandle"])
    log(f"  {len(reviews)} review, khớp được sản phẩm: {matched}/{len(reviews)}")

    log("3/4 Ghi file JSON...")
    write_json(DATA_DIR / "bd-products.json", {
        "meta": {"source": SHOP, "fetchedAt": now, "count": len(products),
                 "imageWidth": args.width,
                 "priceNote": "Giá lấy đúng như shop trả về (thị trường Việt Nam, nhiều khả năng là VND). Kiểm tra lại trước khi dùng."},
        "products": products})
    write_json(DATA_DIR / "bd-reviews.json", {
        "meta": {"source": LOOX, "fetchedAt": now, "count": len(reviews)},
        "reviews": reviews})

    log("4/4 Tải ảnh...")
    ok, failed = download_all(jobs_p + jobs_r)
    log(f"Xong: {ok} ảnh OK, {len(failed)} lỗi.")
    for f in failed[:20]:
        log("  LỖI", f)
    if failed:
        log("Chạy lại lệnh để tải nốt các ảnh lỗi (ảnh đã có sẽ được bỏ qua).")


if __name__ == "__main__":
    main()
