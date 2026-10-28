// Phần đánh giá của khách: đọc reviews.json bằng fetch,
// lọc theo số sao / dòng nam-nữ / loại sản phẩm, hiện từng đợt (nút "Show more"), bấm vào thẻ thì mở popup chi tiết.
import { buildSlideshow } from "./slideshow.js";
import { createStars, createImage, guessCategory, guessGender } from "./product-reviews.js";

const PAGE_SIZE = 6;                       // mỗi lần hiện 6 đánh giá

const list = document.getElementById("review-list");
const summary = document.getElementById("review-summary");
const moreBtn = document.getElementById("review-more");
const dialog = document.getElementById("review-dialog");
const detail = document.getElementById("review-detail");
const filterBox = document.getElementById("review-filters");

let reviews = [];    // tất cả đánh giá
let filtered = [];   // các đánh giá đang hiển thị theo bộ lọc
let shown = 0;

// ---------- Bộ lọc ----------
// Loại sản phẩm (category trong products.json) -> nhóm hiện trên nút lọc
const TYPE_OF = {
  compression: "compression", tops: "tops", oversize: "tops", hoodies: "outerwear",
  bottoms: "bottoms", bodysuits: "bodysuits", accessories: "accessories"
};

// Mỗi hàng lọc: nhãn, các lựa chọn [giá trị, chữ trên nút], và hàm kiểm tra 1 đánh giá có khớp lựa chọn không.
// 1 người có thể đánh giá nhiều sản phẩm (entries): khớp nếu ÍT NHẤT 1 sản phẩm khớp.
const FILTERS = {
  stars: {
    label: "Rating",
    options: [["5", "5 ★"], ["4", "4 ★"], ["3", "3 ★"], ["2", "2 ★"], ["1", "1 ★"]],
    test: (r, value) => Math.floor(r.rating) === Number(value)          // 4.7 sao tính vào nhóm 4 (làm tròn xuống)
  },
  line: {
    label: "Line",
    options: [["him", "Men's"], ["her", "Women's"]],
    test: (r, value) => r.genders.has(value)
  },
  type: {
    label: "Type",
    options: [["compression", "Compression"], ["tops", "Tees & Tops"], ["outerwear", "Hoodies & Jackets"],
              ["bottoms", "Bottoms"], ["bodysuits", "Bodysuits"], ["accessories", "Accessories"]],
    test: (r, value) => r.types.has(value)
  }
};
const state = { stars: "all", line: "all", type: "all" };     // "all" = không lọc hàng đó

// Đánh giá có qua mọi bộ lọc không. skip: bỏ qua 1 hàng (dùng khi đếm số cho các nút của chính hàng đó)
function passes(review, skip) {
  return Object.keys(FILTERS).every((key) =>
    key === skip || state[key] === "all" || FILTERS[key].test(review, state[key]));
}

// ---------- Hàm dùng chung ----------
// (createStars: vẽ sao có phần lẻ; createImage: ảnh feedback thử .webp -> .jpg.
//  Hai hàm nằm ở product-reviews.js để popup sản phẩm dùng chung)

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

// Tạo các nút lọc bằng DOM: mỗi hàng = nhãn + nút "All" + các lựa chọn
function buildFilters() {
  Object.keys(FILTERS).forEach((key) => {
    const row = filterBox.querySelector('[data-filter="' + key + '"]');
    row.appendChild(el("span", "review-filter__label", FILTERS[key].label));
    [["all", "All"], ...FILTERS[key].options].forEach(([value, text]) => {
      const btn = el("button", "", text);
      btn.type = "button";
      btn.dataset.value = value;
      btn.dataset.text = text;                 // chữ gốc, để ghép thêm số lượng "(12)"
      btn.addEventListener("click", () => { state[key] = value; applyFilters(); });
      row.appendChild(btn);
    });
  });
}

// Cập nhật nút: nút đang chọn sáng lên; mỗi nút ghi số đánh giá sẽ còn lại nếu bấm nó
// (tính theo các hàng lọc khác đang chọn), 0 thì làm mờ và không bấm được
function updateFilterButtons() {
  Object.keys(FILTERS).forEach((key) => {
    const pool = reviews.filter((r) => passes(r, key));
    filterBox.querySelectorAll('[data-filter="' + key + '"] button').forEach((btn) => {
      const value = btn.dataset.value;
      btn.setAttribute("aria-pressed", String(state[key] === value));
      if (value === "all") return;
      const count = pool.filter((r) => FILTERS[key].test(r, value)).length;
      btn.textContent = btn.dataset.text + " (" + count + ")";
      btn.disabled = count === 0 && state[key] !== value;
    });
  });
}

// Áp bộ lọc: vẽ lại danh sách từ đầu
function applyFilters() {
  filtered = reviews.filter((r) => passes(r));
  updateFilterButtons();
  list.replaceChildren();
  shown = 0;
  const active = Object.values(state).some((v) => v !== "all");
  summary.textContent = summaryText(filtered) + (active ? " (filtered)" : "");
  if (filtered.length === 0) {
    list.appendChild(el("p", "review-empty", "No reviews match these filters."));
  }
  showMore();
}

// Dòng tóm tắt: điểm trung bình + số đánh giá (của nhóm đang xem)
function summaryText(items) {
  if (items.length === 0) return "0 reviews";
  const avg = items.reduce((sum, r) => sum + r.rating, 0) / items.length;
  return avg.toFixed(1) + " / 5 · " + items.length + " review" + (items.length === 1 ? "" : "s");
}

async function fetchJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error("Cannot load " + url);
  return res.json();
}

fetchJson("../data/reviews.json")
  .then((reviewData) => {
    // Đoán sẵn dòng (nam/nữ) và loại của các sản phẩm mà mỗi người đã đánh giá (từ tên sản phẩm), lưu dạng Set để lọc nhanh
    reviews = reviewData.reviews.map((r) => ({
      ...r,
      genders: new Set(r.entries.map((e) => guessGender(e.product || ""))),
      types: new Set(r.entries.map((e) => TYPE_OF[guessCategory(e.product || "")]).filter(Boolean))
    }));
    // Chưa có đánh giá nào: chỉ báo "No reviews yet", ẩn bộ lọc và nút Show more
    if (reviews.length === 0) {
      summary.textContent = "No reviews yet.";
      filterBox.hidden = true;
      moreBtn.hidden = true;
      return;
    }
    buildFilters();
    applyFilters();
  })
  .catch((err) => { list.textContent = "Unable to load reviews."; console.error(err); });

moreBtn.addEventListener("click", showMore);
