// Phần đánh giá của khách: đọc reviews.json bằng fetch,
// hiện từng đợt (nút "Show more"), bấm vào thẻ thì mở popup chi tiết.
import { buildSlideshow } from "./slideshow.js";

const PAGE_SIZE = 6;                       // mỗi lần hiện 6 đánh giá
const IMAGE_EXTENSIONS = [".webp", ".jpg"]; // thử .webp (nhẹ) trước, không có thì thử .jpg

const list = document.getElementById("review-list");
const summary = document.getElementById("review-summary");
const moreBtn = document.getElementById("review-more");
const dialog = document.getElementById("review-dialog");
const detail = document.getElementById("review-detail");
const filterButtons = document.querySelectorAll("#review-filter button");

let reviews = [];    // tất cả đánh giá
let filtered = [];   // các đánh giá đang hiển thị theo bộ lọc sao
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

// 1 ảnh feedback của khách: thử .webp -> .jpg -> khung chờ. base = đường dẫn không có đuôi file
function createImage(base, alt, lazy) {
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

// Khung ảnh của 1 đánh giá: 1 ảnh thì hiện ảnh, nhiều ảnh thì thành slideshow
function createPhoto(review) {
  const box = document.createElement("div");
  box.className = "review-card__photo";
  const alt = "Photo from " + review.name;
  if (review.images.length === 1) {
    box.appendChild(createImage(review.images[0], alt, true));
    return box;
  }
  const nodes = review.images.map((base, i) =>
    // Chỉ ảnh đầu tải lười; các ảnh sau tải sẵn để lúc trượt không bị trống
    createImage(base, alt + " (" + (i + 1) + "/" + review.images.length + ")", i === 0));
  return buildSlideshow(box, nodes);
}

// Tạo 1 phần tử với class và nội dung chữ (cho gọn code)
function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

// Lời đánh giá dài nhất của 1 người (dùng làm nội dung chính trên thẻ)
function mainEntry(review) {
  return review.entries.reduce((a, b) => (b.text.length > a.text.length ? b : a));
}

// ---------- Thẻ đánh giá ----------
function createCard(review) {
  const card = el("article", "review-card glass");
  card.tabIndex = 0;                         // cho phép bấm bằng bàn phím (Enter mở popup)
  card.setAttribute("role", "group");        // không dùng role="button" vì trong thẻ có nút của slideshow
  card.setAttribute("aria-label", "Review by " + review.name + ". Press Enter to open.");

  const head = el("div", "review-card__rating");
  head.append(createStars(review.rating), el("span", "", review.rating.toFixed(1)));

  // Người có nhiều đánh giá: thẻ hiện lời đánh giá dài nhất, các lời còn lại xem trong popup
  const main = mainEntry(review);
  const text = el("blockquote", "review-card__text", "“" + main.text + "”");
  text.lang = main.lang;                     // để trình duyệt chọn đúng font cho từng ngôn ngữ
  const more = review.entries.length - 1;

  card.append(
    createPhoto(review),
    head,
    text,
    el("p", "review-card__meta", review.name),
    el("p", "review-card__item", main.product + (more > 0 ? "  + " + more + " more" : ""))
  );

  card.addEventListener("click", () => openDetail(review));
  card.addEventListener("keydown", (e) => {
    if (e.target === card && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); openDetail(review); }
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
  detail.replaceChildren();

  const photo = createPhoto(review);
  photo.classList.add("review-detail__photo");

  const info = el("div", "review-detail__info");

  const rating = el("div", "review-card__rating");
  rating.append(createStars(review.rating), el("span", "", review.rating.toFixed(1)));
  const count = review.entries.length;
  const who = el("p", "review-card__meta", review.name + (count > 1 ? " · " + count + " reviews" : ""));
  info.append(rating, who);

  // Mỗi lần đánh giá của người này: sao, lời đánh giá, sản phẩm đã mua
  review.entries.forEach((entry) => {
    const block = el("div", "review-entry");
    if (count > 1) {
      const head = el("div", "review-card__rating");
      head.append(createStars(entry.rating), el("span", "", entry.rating.toFixed(1)));
      block.appendChild(head);
    }
    const text = el("blockquote", "review-detail__text", "“" + entry.text + "”");
    text.lang = entry.lang;
    block.append(text, el("h3", "glass__title", entry.product));
    info.appendChild(block);
  });

  if (review.verified) {
    const specs = el("dl", "spec-list");
    addRow(specs, "Purchase", "Verified buyer");
    info.appendChild(specs);
  }

  const close = el("button", "review-detail__close", "×");
  close.type = "button";
  close.setAttribute("aria-label", "Close");
  close.addEventListener("click", () => dialog.close());

  detail.append(photo, info, close);
  dialog.showModal();                         // <dialog> tự xử lý phím Esc và khóa nền
}

// Bấm ra ngoài vùng nội dung (vào lớp nền mờ) thì đóng popup
dialog.addEventListener("click", (e) => { if (e.target === dialog) dialog.close(); });
// Đóng popup thì gỡ nội dung đi (slideshow trong popup nhờ vậy tự dừng chạy)
dialog.addEventListener("close", () => detail.replaceChildren());

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

fetchJson("../data/reviews.json")
  .then((reviewData) => {
    reviews = reviewData.reviews;
    // Chưa có đánh giá nào: chỉ báo "No reviews yet", ẩn bộ lọc và nút Show more
    if (reviews.length === 0) {
      summary.textContent = "No reviews yet.";
      document.getElementById("review-filter").style.display = "none";
      moreBtn.hidden = true;
      return;
    }
    const avg = reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length;
    summary.textContent = avg.toFixed(1) + " / 5 · " + reviews.length + " reviews";
    labelFilterButtons();
    applyFilter("all");
  })
  .catch((err) => { list.textContent = "Unable to load reviews."; console.error(err); });

moreBtn.addEventListener("click", showMore);
filterButtons.forEach((b) => b.addEventListener("click", () => applyFilter(b.dataset.stars)));
