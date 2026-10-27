// Trang cửa hàng: đọc products.json (fetch), chia sản phẩm thành 3 khu (nam, nữ, phụ kiện) + các nhóm nhỏ, vẽ bằng DOM.
import { loadProducts, renderGrid } from "./products.js";
import { initProductPopup, el } from "./product-popup.js";
import { REGIONS, loadRates, formatPrice, getSavedCurrency, saveCurrency } from "./currency.js";

const sections = document.querySelectorAll(".shop-section");
const header = document.querySelector(".site-header");
const empty = document.getElementById("shop-empty");
const lineCards = document.querySelectorAll("#shop-audience button");        // 2 thẻ Men's / Women's Line
const lineItems = document.querySelectorAll("#lines-menu .line-item");      // 3 mục chính trong menu bên trái
const menu = document.getElementById("lines-menu");
const linesTab = document.getElementById("lines-tab");
const currencySelect = document.getElementById("filter-currency");
const dialog = document.getElementById("product-dialog");
const detail = document.getElementById("product-detail");

let products = [];
let rates = { USD: 1 };
const state = { currency: getSavedCurrency() };
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

// 3 khu sản phẩm. Mỗi khu chia thành các nhóm nhỏ: nhóm hiện thành tiêu đề + lưới trên trang,
// đồng thời thành mục con trong menu Collections (bấm vào thì cuộn tới nhóm đó).
const LINES = {
  sanctuary: {
    match: (p) => p.gender === "him" && p.category !== "accessories",
    groups: [
      { id: "compression", title: "Men's Doom Tech™ and Void Tech™ Compressions", match: (p) => p.category === "compression" },
      { id: "zipups", title: "Men's Zip-ups and Crewnecks", match: (p) => p.category === "hoodies" },
      { id: "tees", title: "Men's T-Shirts and Cut-offs", videoBefore: "break-1", match: (p) => p.category === "oversize" || /cut-off/i.test(p.name) },
      { id: "cargos", title: "Men's Cargos and Sweatpants", match: (p) => p.category === "bottoms" && !/jeans/i.test(p.name) },
      { id: "jeans", title: "Distressed Jeans", match: (p) => p.category === "bottoms" && /jeans/i.test(p.name) },
      { id: "stringers", title: "Men's Stringers and Beaters", match: (p) => p.category === "tops" && !/cut-off/i.test(p.name) }
    ]
  },
  selene: {
    match: (p) => p.gender === "her" && p.category !== "accessories",
    groups: [
      { id: "zipups", title: "Women's Zip-ups", videoBefore: "break-2", videoRatio: "10 / 16", match: (p) => p.category === "hoodies" },
      { id: "tops", title: "Women's Baby Tees and Sports Bras", match: (p) => p.category === "tops" },
      { id: "bodysuits", title: "Women's Void Tech™ Bodysuits", match: (p) => p.category === "bodysuits" },
      { id: "bottoms", title: "Women's Leggings, Shorts and Sweatpants", videoBefore: "break-3", match: (p) => p.category === "bottoms" }
    ]
  },
  accessories: {
    match: (p) => p.category === "accessories",
    groups: [
      { id: "caps", title: "Tarnished Metallic Logo Caps", match: (p) => /\bcap\b/i.test(p.name) },
      { id: "beanies", title: "Essential Embroidery Beanies", match: (p) => /\bbeanie\b/i.test(p.name) }
    ]
  }
};

const byFeatured = (a, b) => Number(b.featured) - Number(a.featured);

// Sản phẩm của 1 nhóm (món nổi bật xếp trước)
function groupItems(line, group) {
  return products.filter((p) => LINES[line].match(p) && group.match(p)).sort(byFeatured);
}

// Dải video chèn giữa 2 nhóm sản phẩm (tỷ lệ 4:5, tự chạy khi cuộn tới, tắt tiếng, lặp lại).
// Tạo 1 lần rồi dùng lại, để đổi tiền tệ (vẽ lại lưới) không làm video tải lại từ đầu.
const breakVideos = {};
function getBreakVideo(name, ratio) {
  if (!breakVideos[name]) {
    const figure = el("figure", "shop-break");
    const video = document.createElement("video");
    video.className = "shop-break__video";
    if (ratio) video.style.aspectRatio = ratio;        // mỗi video 1 tỷ lệ riêng (mặc định 4:5 trong CSS)
    video.src = "../assets/videos/" + name + ".mp4";
    video.poster = "../assets/videos/" + name + "-poster.jpg";
    video.muted = true; video.loop = true; video.playsInline = true; video.preload = "metadata";
    video.setAttribute("aria-hidden", "true");
    figure.appendChild(video);
    if (reduceMotion) {
      // người dùng chọn giảm chuyển động: chỉ hiện ảnh poster
    } else if ("IntersectionObserver" in window) {
      // Chạy khi còn thấy dù chỉ 1 góc video (threshold 0); chỉ dừng khi đã hoàn toàn ra khỏi màn hình, cho đỡ tốn pin/CPU
      new IntersectionObserver((entries) => {
        entries.forEach((e) => { if (e.isIntersecting) video.play().catch(() => {}); else video.pause(); });
      }, { threshold: 0 }).observe(video);
    }
    breakVideos[name] = figure;
  }
  return breakVideos[name];
}

// Vẽ cả 3 khu lên cùng 1 trang. animate = false khi chỉ đổi tiền tệ (không cần cho các thẻ hiện lại từ đầu)
function renderSections(animate = true) {
  const format = (usd) => formatPrice(usd, state.currency, rates);
  Object.keys(LINES).forEach((line) => {
    const wrap = document.getElementById("groups-" + line);
    wrap.replaceChildren();
    LINES[line].groups.forEach((group) => {
      const items = groupItems(line, group);
      if (items.length === 0) return;                    // nhóm trống thì không hiện
      if (group.videoBefore) wrap.appendChild(getBreakVideo(group.videoBefore, group.videoRatio));   // video nằm ngay trên tiêu đề nhóm
      const block = document.createElement("div");
      block.className = "shop-group";
      block.id = line + "-" + group.id;                  // điểm neo, ví dụ "sanctuary-compression"
      const title = document.createElement("h3");
      title.className = "shop-group__title";
      title.textContent = group.title;
      const grid = document.createElement("div");
      grid.className = "product-grid";
      renderGrid(grid, items, format, openProduct);
      block.append(title, grid);
      wrap.appendChild(block);
    });
  });

  empty.hidden = products.length > 0;

  // Hiệu ứng: các thẻ lần lượt hiện lên (trễ dần theo thứ tự, tối đa 12 thẻ đầu)
  if (!animate) return;
  document.querySelectorAll(".product-card").forEach((card, i) => {
    card.style.animationDelay = Math.min(i, 12) * 45 + "ms";
    card.classList.add("is-entering");
  });
}

// Cuộn mượt tới 1 điểm neo (khu hoặc nhóm)
function scrollToId(id) {
  const target = document.getElementById(id);
  if (target) target.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
}

// ---------- Popup chi tiết sản phẩm: nằm ở js/product-popup.js (dùng chung với trang giỏ hàng) ----------
const openProduct = initProductPopup({ dialog, detail, getCurrency: () => state.currency, getRates: () => rates });

function fillCurrencies() {
  REGIONS.forEach((r) => currencySelect.add(new Option(r.name + " (" + r.code + ")", r.code)));
  currencySelect.value = state.currency;
}

// Đánh dấu khu đang xem: thẻ Men's/Women's Line, mục menu Collections và logo header (trắng <-> đỏ khi ở khu nữ)
function markActive(line) {
  lineCards.forEach((c) => c.setAttribute("aria-pressed", String(c.dataset.line === line)));
  lineItems.forEach((i) => i.classList.toggle("is-active", i.dataset.line === line));
  header.classList.toggle("is-her", line === "selene");      // CSS làm mờ chéo logo trắng <-> logo đỏ
}

// Cuộn trang thì tự cập nhật khu đang xem (khu nào đi qua giữa màn hình)
function watchSections() {
  if (!("IntersectionObserver" in window)) return;
  const spy = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) markActive(e.target.dataset.line); });
  }, { rootMargin: "-40% 0px -55% 0px" });
  sections.forEach((section) => spy.observe(section));
}

// 2 thẻ Men's / Women's Line: bấm để cuộn xuống khu tương ứng
lineCards.forEach((c) => c.addEventListener("click", () => scrollToId(c.dataset.line)));

// ---------- Menu Collections bên trái: khung nhỏ trượt ra cạnh nút ----------
function openMenu() {
  menu.classList.remove("is-closing");
  menu.hidden = false;
  linesTab.setAttribute("aria-expanded", "true");
}
function closeMenu() {
  if (menu.hidden) return;
  linesTab.setAttribute("aria-expanded", "false");
  if (reduceMotion) { menu.hidden = true; return; }
  menu.classList.add("is-closing");                      // chạy hiệu ứng thu vào rồi mới ẩn thật
}
// Hết hiệu ứng thu vào thì ẩn (chỉ tính hiệu ứng của chính khung, không tính của các mục bên trong)
menu.addEventListener("animationend", (e) => {
  if (e.target === menu && menu.classList.contains("is-closing")) {
    menu.classList.remove("is-closing");
    menu.hidden = true;
  }
});

linesTab.addEventListener("click", () => (menu.hidden ? openMenu() : closeMenu()));
// Bấm ra ngoài khung hoặc nhấn Esc thì đóng
document.addEventListener("click", (e) => {
  if (!menu.hidden && !menu.contains(e.target) && !linesTab.contains(e.target)) closeMenu();
});
document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeMenu(); });

// Mục chính: bấm thì mở danh sách mục con (các mục khác tự thu lại) và cuộn xuống khu đó. Menu vẫn mở để chọn tiếp mục con.
lineItems.forEach((item) => item.addEventListener("click", () => {
  const group = item.closest(".line-group");
  const willOpen = !group.classList.contains("is-open");
  document.querySelectorAll("#lines-menu .line-group").forEach((g) => {
    g.classList.remove("is-open");
    g.querySelector(".line-item").setAttribute("aria-expanded", "false");
  });
  if (willOpen) {
    group.classList.add("is-open");
    item.setAttribute("aria-expanded", "true");
  }
  scrollToId(item.dataset.line);
}));

// Mục con (Compression, T-Shirts, ...): lấy từ các nhóm có sản phẩm; bấm thì cuộn tới nhóm và đóng menu
function buildMenuSubs() {
  Object.keys(LINES).forEach((line) => {
    const inner = document.querySelector('#lines-menu .line-group[data-line="' + line + '"] .line-sub__inner');
    inner.replaceChildren();
    LINES[line].groups.forEach((group) => {
      if (groupItems(line, group).length === 0) return;
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "line-sub__item";
      btn.textContent = group.title;
      btn.addEventListener("click", () => { scrollToId(line + "-" + group.id); closeMenu(); });
      inner.appendChild(btn);
    });
  });
}

currencySelect.addEventListener("change", () => {
  state.currency = currencySelect.value;
  saveCurrency(state.currency);   // nhớ lựa chọn cho các trang khác
  renderSections(false);
});

async function init() {
  try {
    fillCurrencies();
    const [list, rateInfo] = await Promise.all([loadProducts(), loadRates()]);
    products = list;
    rates = rateInfo.rates;
    renderSections(true);
    buildMenuSubs();
    markActive("sanctuary");
    watchSections();
  } catch (err) {
    empty.textContent = "Unable to load products.";
    empty.hidden = false;
    console.error(err);
  }
}
init();
