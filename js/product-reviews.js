// Phần "Reviews" trong popup sản phẩm: đọc data/reviews.json (fetch) rồi lọc ra đánh giá liên quan tới sản phẩm đang xem.
// Dữ liệu review được crawl theo tên sản phẩm của shop gốc, nhiều tên không trùng với 32 sản phẩm của web, nên:
//   1. Có review đúng tên sản phẩm -> hiện các review đó.
//   2. Không có -> hiện review của các mẫu CÙNG LOẠI (vd: cùng là compression nam) và ghi rõ điều này cho khách.

const PAGE_SIZE = 3;            // mỗi lần hiện 3 review, bấm "Show more" để xem tiếp

let reviewsPromise = null;
// Đọc reviews.json 1 lần rồi dùng lại; lỗi thì xoá promise để lần mở popup sau được tải lại
function loadReviews() {
  if (!reviewsPromise) {
    reviewsPromise = fetch("../data/reviews.json")
      .then((res) => {
        if (!res.ok) throw new Error("Cannot load reviews");
        return res.json();
      })
      .then((data) => flatten(data.reviews || []))
      .catch((err) => {
        reviewsPromise = null;
        throw err;
      });
  }
  return reviewsPromise;
}

// Mỗi người có thể đánh giá nhiều sản phẩm (entries) -> tách thành từng lời đánh giá riêng.
// Ảnh trong dữ liệu gắn theo NGƯỜI, không theo từng sản phẩm: người chỉ có 1 lời đánh giá thì ảnh đi kèm lời đó;
// người có nhiều lời thì ảnh gắn vào lời dài nhất (giống thẻ đánh giá ở trang chủ), tránh lặp ảnh ở nhiều lời.
function flatten(reviews) {
  const list = [];
  reviews.forEach((r) => {
    const entries = r.entries || [];
    const main = entries.reduce((a, b) => (b.text.length > a.text.length ? b : a), entries[0]);
    entries.forEach((e) => {
      list.push({
        name: r.name, verified: r.verified, rating: e.rating, text: e.text, lang: e.lang, product: e.product || "",
        images: e === main ? r.images || [] : []
      });
    });
  });
  return list;
}

// Chuẩn hoá tên để so sánh: bỏ màu trong [ ], bỏ ™, bỏ chữ "Women's", chữ thường, gộp khoảng trắng
function normalizeName(name) {
  return name.toLowerCase()
    .replace(/\[.*?\]/g, "")
    .replace(/™/g, "")
    .replace(/[’']/g, "'")
    .replace(/^women'?s\s+|^womens\s+|^mens\s+/, "")
    .replace(/\s+/g, " ")
    .trim();
}

// Đoán loại sản phẩm từ tên trong review (cùng cách chia category với products.json)
function guessCategory(name) {
  const n = name.toLowerCase();
  if (/bodysuit/.test(n)) return "bodysuits";
  if (/compression|shrug/.test(n)) return "compression";
  if (/beanie|\bcap\b/.test(n)) return "accessories";
  if (/sweatpants|cargos|jeans|shorts|leggings|capri/.test(n)) return "bottoms";
  if (/hoodie|zip-up|jacket|crewneck/.test(n)) return "hoodies";
  if (/stringer|beater|tank|bra|cut-off|baby tee/.test(n)) return "tops";
  if (/t-shirt|\btee\b/.test(n)) return "oversize";
  return null;
}

const guessGender = (name) => (/^wom[ae]n/i.test(name.trim()) ? "her" : "him");

const CATEGORY_LABEL = {
  compression: "compression", bodysuits: "bodysuit", bottoms: "bottoms", hoodies: "hoodie and jacket",
  tops: "stringer and top", oversize: "oversized tee", accessories: "accessory"
};

// Trả về { items, exact }: exact = true nếu là review đúng sản phẩm này
export function matchReviews(all, product) {
  const target = normalizeName(product.name);
  const exact = all.filter((r) => normalizeName(r.product) === target);
  if (exact.length) return { items: exact, exact: true };

  const sameCategory = all.filter((r) => guessCategory(r.product) === product.category);
  // Ưu tiên cùng giới tính (nam/nữ); sản phẩm unisex hoặc không có review cùng giới tính thì lấy cả hai
  const sameGender = sameCategory.filter((r) => guessGender(r.product) === product.gender);
  return { items: sameGender.length ? sameGender : sameCategory, exact: false };
}

// ---------- Vẽ giao diện ----------
function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

// Sao có phần lẻ: lớp sao xám bên dưới, lớp sao trắng bên trên cắt theo % điểm (dùng chung với reviews.js)
export function createStars(rating) {
  const wrap = document.createElement("span");
  wrap.className = "stars";
  wrap.setAttribute("aria-label", rating.toFixed(1) + " out of 5");
  wrap.textContent = "★★★★★";
  const fill = document.createElement("span");
  fill.className = "stars__fill";
  fill.style.width = (rating / 5) * 100 + "%";
  fill.textContent = "★★★★★";
  wrap.appendChild(fill);
  return wrap;
}

// 1 ảnh feedback của khách: thử .webp (nhẹ) -> .jpg -> chữ "Photo soon". base = đường dẫn không có đuôi file
// (dùng chung với reviews.js)
const IMAGE_EXTENSIONS = [".webp", ".jpg"];
export function createImage(base, alt, lazy) {
  const img = document.createElement("img");
  img.alt = alt;
  img.loading = lazy ? "lazy" : "eager";
  let tries = 0;
  img.src = "../" + base + IMAGE_EXTENSIONS[tries];
  img.addEventListener("error", () => {
    tries++;
    if (tries < IMAGE_EXTENSIONS.length) {
      img.src = "../" + base + IMAGE_EXTENSIONS[tries];
    } else {
      const ph = document.createElement("span");
      ph.textContent = "Photo soon";
      img.replaceWith(ph);
    }
  });
  return img;
}

// Ảnh của 1 review: hàng ảnh nhỏ; bấm ảnh nhỏ thì hiện ảnh lớn bên dưới, bấm lại đúng ảnh đó thì thu lại
function createPhotos(review) {
  const wrap = el("div", "product-review__photos");
  const thumbs = el("div", "product-review__thumbs");
  const big = el("div", "product-review__big");
  big.hidden = true;
  let openIndex = -1;

  review.images.forEach((base, i) => {
    const btn = el("button", "product-review__thumb");
    btn.type = "button";
    btn.setAttribute("aria-label", "View photo " + (i + 1) + " of " + review.images.length + " from " + review.name);
    btn.setAttribute("aria-pressed", "false");
    btn.appendChild(createImage(base, "", true));
    btn.addEventListener("click", () => {
      openIndex = openIndex === i ? -1 : i;          // bấm lại ảnh đang mở -> đóng
      thumbs.querySelectorAll("button").forEach((b, k) => b.setAttribute("aria-pressed", String(k === openIndex)));
      big.hidden = openIndex === -1;
      big.replaceChildren();
      if (openIndex !== -1) big.appendChild(createImage(base, "Photo " + (i + 1) + " from " + review.name, false));
    });
    thumbs.appendChild(btn);
  });
  wrap.append(thumbs, big);
  return wrap;
}

function createItem(review) {
  const item = el("li", "product-review");
  const head = el("div", "review-card__rating");
  head.append(createStars(review.rating), el("span", "", review.rating.toFixed(1)));
  const text = el("blockquote", "product-review__text", "“" + review.text + "”");
  text.lang = review.lang;                  // để trình duyệt chọn đúng font cho từng ngôn ngữ
  const who = el("p", "product-review__meta", review.name + (review.verified ? " · Verified buyer" : ""));
  item.append(head, text);
  if (review.images.length) item.appendChild(createPhotos(review));
  item.appendChild(who);
  // Review của mẫu cùng loại: ghi tên sản phẩm khách đã mua để không gây hiểu nhầm
  if (review.showProduct) item.appendChild(el("p", "product-review__product", review.product));
  return item;
}

// Nhóm sao của 1 review: làm tròn xuống (4.7 -> 4), giống bộ lọc ở trang chủ
const starGroup = (review) => Math.floor(review.rating);

// Tạo khối Reviews cho 1 sản phẩm. Trả về phần tử ngay, nội dung được điền sau khi tải xong dữ liệu.
export function buildProductReviews(product) {
  const section = el("section", "product-reviews");
  section.appendChild(el("h3", "product-detail__label", "Reviews"));
  const body = el("div", "product-reviews__body");
  body.appendChild(el("p", "cart-note", "Loading reviews..."));
  section.appendChild(body);

  loadReviews()
    .then((all) => {
      const { items, exact } = matchReviews(all, product);
      body.replaceChildren();
      if (items.length === 0) {
        body.appendChild(el("p", "cart-note", "No reviews for this style yet."));
        return;
      }
      // Lời đánh giá dài (nhiều thông tin) lên trước
      const sorted = [...items].sort((a, b) => b.text.length - a.text.length)
        .map((r) => ({ ...r, showProduct: !exact }));

      const avg = sorted.reduce((sum, r) => sum + r.rating, 0) / sorted.length;
      const summary = el("div", "review-card__rating product-reviews__summary");
      summary.append(createStars(avg), el("span", "", avg.toFixed(1) + " · " + sorted.length + " review" + (sorted.length === 1 ? "" : "s")));
      body.appendChild(summary);
      if (!exact) {
        body.appendChild(el("p", "cart-note", "No reviews for this exact item yet. Showing reviews of similar " +
          (CATEGORY_LABEL[product.category] || "") + " styles."));
      }

      // Bộ lọc theo sao: All, 5★ ... 1★ (kèm số lượng); nhóm không có review thì làm mờ nút
      const filter = el("div", "review-filter product-reviews__filter");
      filter.setAttribute("role", "group");
      filter.setAttribute("aria-label", "Filter reviews by stars");
      const options = [["all", "All (" + sorted.length + ")"]];
      [5, 4, 3, 2, 1].forEach((n) => {
        options.push([String(n), n + " ★ (" + sorted.filter((r) => starGroup(r) === n).length + ")"]);
      });
      options.forEach(([value, label]) => {
        const btn = el("button", "", label);
        btn.type = "button";
        btn.dataset.stars = value;
        btn.disabled = value !== "all" && !sorted.some((r) => starGroup(r) === Number(value));
        btn.addEventListener("click", () => applyFilter(value));
        filter.appendChild(btn);
      });

      const list = el("ul", "product-reviews__list");
      const more = el("button", "btn btn--small btn--ghost", "Show more reviews");
      more.type = "button";
      let filtered = sorted;
      let shown = 0;
      const showMore = () => {
        filtered.slice(shown, shown + PAGE_SIZE).forEach((r) => list.appendChild(createItem(r)));
        shown = Math.min(shown + PAGE_SIZE, filtered.length);
        more.hidden = shown >= filtered.length;
      };
      // Đổi bộ lọc: vẽ lại danh sách từ đầu
      function applyFilter(value) {
        filtered = value === "all" ? sorted : sorted.filter((r) => starGroup(r) === Number(value));
        filter.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.stars === value)));
        list.replaceChildren();
        shown = 0;
        showMore();
      }
      more.addEventListener("click", showMore);
      body.append(filter, list, more);
      applyFilter("all");
    })
    .catch((err) => {
      console.error(err);
      body.replaceChildren(el("p", "form-error", "Reviews are unavailable right now."));
    });

  return section;
}
