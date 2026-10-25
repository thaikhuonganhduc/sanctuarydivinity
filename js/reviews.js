// Phần đánh giá của khách: đọc reviews.json + products.json bằng fetch,
// hiện từng đợt (nút "Show more"), bấm vào thẻ thì mở popup chi tiết.
const PAGE_SIZE = 6;                       // mỗi lần hiện 6 đánh giá
const IMAGE_EXTENSIONS = [".jpg", ".png"]; // thử .jpg trước, không có thì thử .png

const list = document.getElementById("review-list");
const summary = document.getElementById("review-summary");
const moreBtn = document.getElementById("review-more");
const dialog = document.getElementById("review-dialog");
const detail = document.getElementById("review-detail");
const filterButtons = document.querySelectorAll("#review-filter button");

let reviews = [];    // tất cả đánh giá
let filtered = [];   // các đánh giá đang hiển thị theo bộ lọc sao
let products = {};   // tra sản phẩm theo id: products["p03"]
let shown = 0;

// ---------- Hàm dùng chung ----------

// Sao có phần lẻ: lớp sao xám bên dưới, lớp sao trắng bên trên cắt theo % điểm
function createStars(rating) {
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

// Ảnh feedback của khách: thử .jpg -> .png -> khung chờ
function createPhoto(review) {
  const box = document.createElement("div");
  box.className = "review-card__photo";
  const img = document.createElement("img");
  img.alt = "Photo from " + review.name;
  img.loading = "lazy";
  let tries = 0;
  img.src = "../" + review.image + IMAGE_EXTENSIONS[tries];
  img.addEventListener("error", () => {
    tries++;
    if (tries < IMAGE_EXTENSIONS.length) {
      img.src = "../" + review.image + IMAGE_EXTENSIONS[tries];
    } else {
      const ph = document.createElement("span");
      ph.textContent = "Photo soon";
      img.replaceWith(ph);
    }
  });
  box.appendChild(img);
  return box;
}

// dd/mm/yy từ chuỗi "2026-08-03"
function formatDate(iso) {
  const [y, m, d] = iso.split("-");
  return d + "/" + m + "/" + y.slice(2);
}

// Tạo 1 phần tử với class và nội dung chữ (cho gọn code)
function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

// ---------- Thẻ đánh giá ----------
function createCard(review) {
  const product = products[review.productId];
  const card = el("article", "review-card glass");
  card.tabIndex = 0;                         // cho phép bấm bằng bàn phím
  card.setAttribute("role", "button");
  card.setAttribute("aria-label", "Open review by " + review.name);

  const head = el("div", "review-card__rating");
  head.append(createStars(review.rating), el("span", "", review.rating.toFixed(1)));

  const text = el("blockquote", "review-card__text", "“" + review.text + "”");
  text.lang = review.lang;                   // để trình duyệt chọn đúng font cho từng ngôn ngữ

  card.append(
    createPhoto(review),
    head,
    text,
    el("p", "review-card__meta", review.name + " · " + review.country),
    el("p", "review-card__item", product.name + " · " + formatDate(review.date))
  );

  card.addEventListener("click", () => openDetail(review));
  card.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openDetail(review); }
  });
  return card;
}

// ---------- Popup chi tiết: ảnh bên trái, thông tin bên phải ----------
function addRow(table, label, value) {
  const row = el("div", "spec-row");
  row.append(el("dt", "", label), el("dd", "", value));
  table.appendChild(row);
}

function openDetail(review) {
  const product = products[review.productId];
  detail.replaceChildren();

  const photo = createPhoto(review);
  photo.classList.add("review-detail__photo");

  const info = el("div", "review-detail__info");

  const rating = el("div", "review-card__rating");
  rating.append(createStars(review.rating), el("span", "", review.rating.toFixed(1)));

  const text = el("blockquote", "review-detail__text", "“" + review.text + "”");
  text.lang = review.lang;

  const who = el("p", "review-card__meta", review.name + " · " + review.country);
  const when = el("p", "review-card__item", "Reviewed on " + formatDate(review.date));

  // Thông tin sản phẩm đã mua
  const productTitle = el("h3", "glass__title", product.name);
  const specs = el("dl", "spec-list");
  addRow(specs, "Price", "$" + product.price.toFixed(2));
  addRow(specs, "Size bought", review.size);
  addRow(specs, "Color", review.color);
  addRow(specs, "Material", product.specs.material);
  addRow(specs, "Weight", product.specs.weight);
  addRow(specs, "Fit", product.specs.fit);
  addRow(specs, "Care", product.specs.care);

  const close = el("button", "review-detail__close", "×");
  close.type = "button";
  close.setAttribute("aria-label", "Close");
  close.addEventListener("click", () => dialog.close());

  info.append(rating, text, who, when, productTitle, specs);
  detail.append(photo, info, close);
  dialog.showModal();                         // <dialog> tự xử lý phím Esc và khóa nền
}

// Bấm ra ngoài vùng nội dung (vào lớp nền mờ) thì đóng popup
dialog.addEventListener("click", (e) => { if (e.target === dialog) dialog.close(); });

// ---------- Hiện từng đợt ----------
function showMore() {
  const next = filtered.slice(shown, shown + PAGE_SIZE);
  next.forEach((r) => list.appendChild(createCard(r)));
  shown += next.length;
  moreBtn.hidden = shown >= filtered.length; // hết đánh giá thì ẩn nút
}

// Nhóm sao của 1 đánh giá: làm tròn xuống (4.7 -> 4, 5.0 -> 5)
const starGroup = (review) => Math.floor(review.rating);

// Lọc theo sao: "all" hoặc "1".."5". Vẽ lại danh sách từ đầu.
function applyFilter(value) {
  filtered = value === "all" ? reviews : reviews.filter((r) => starGroup(r) === Number(value));
  filterButtons.forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.stars === value)));
  list.replaceChildren();
  shown = 0;
  if (filtered.length === 0) {
    list.appendChild(el("p", "review-empty", "No reviews in this range yet."));
  }
  showMore();
}

// Ghi số lượng đánh giá của từng nhóm sao lên nút, ví dụ "4 ★ (17)"
function labelFilterButtons() {
  filterButtons.forEach((b) => {
    if (b.dataset.stars === "all") return;
    const count = reviews.filter((r) => starGroup(r) === Number(b.dataset.stars)).length;
    b.textContent = b.dataset.stars + " ★ (" + count + ")";
  });
}

async function fetchJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error("Cannot load " + url);
  return res.json();
}

Promise.all([fetchJson("../data/reviews.json"), fetchJson("../data/products.json")])
  .then(([reviewData, productData]) => {
    productData.products.forEach((p) => { products[p.id] = p; });
    reviews = reviewData.reviews;
    const avg = reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length;
    summary.textContent = avg.toFixed(1) + " / 5 · " + reviews.length + " reviews";
    labelFilterButtons();
    applyFilter("all");
  })
  .catch((err) => { list.textContent = "Unable to load reviews."; console.error(err); });

moreBtn.addEventListener("click", showMore);
filterButtons.forEach((b) => b.addEventListener("click", () => applyFilter(b.dataset.stars)));
