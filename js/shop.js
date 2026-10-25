// Trang cửa hàng: đọc products.json (fetch), lọc/sắp xếp bằng JavaScript rồi vẽ lại lưới bằng DOM.
import { loadProducts, renderGrid, createProductImage } from "./products.js";
import { addToCart } from "./cart.js";
import { REGIONS, loadRates, formatPrice, getSavedCurrency, saveCurrency } from "./currency.js";

const grid = document.getElementById("product-grid");
const count = document.getElementById("shop-count");
const empty = document.getElementById("shop-empty");
const audienceButtons = document.querySelectorAll("#shop-audience button");
const categorySelect = document.getElementById("filter-category");
const sortSelect = document.getElementById("filter-sort");
const currencySelect = document.getElementById("filter-currency");
const header = document.querySelector(".site-header");
const dialog = document.getElementById("product-dialog");
const detail = document.getElementById("product-detail");
const SIZES = ["XXS", "XS", "S", "M", "L", "XL"];

let products = [];
let rates = { USD: 1 };
const state = { audience: "him", category: "all", sort: "featured", currency: getSavedCurrency() };

// Đồ unisex hiện ở cả mục Him lẫn Her
function matchAudience(p) {
  return p.gender === state.audience || p.gender === "unisex";
}

function getVisible() {
  const list = products.filter((p) =>
    matchAudience(p) &&
    (state.category === "all" || p.category === state.category)
  );
  if (state.sort === "price-asc") list.sort((a, b) => a.price - b.price);
  if (state.sort === "price-desc") list.sort((a, b) => b.price - a.price);
  if (state.sort === "featured") list.sort((a, b) => Number(b.featured) - Number(a.featured));
  return list;
}

function render() {
  const list = getVisible();
  renderGrid(grid, list, (usd) => formatPrice(usd, state.currency, rates), openProduct);
  const available = list.filter((p) => p.stock > 0).length; // chỉ đếm mẫu còn hàng
  count.textContent = available + (available === 1 ? " piece" : " pieces") + " available";
  empty.hidden = list.length > 0;
}

// Đổ danh sách loại vào ô chọn, chỉ lấy loại có sản phẩm của mục đang chọn
// (For Him không có bikini/bodysuit vì không có sản phẩm nam thuộc loại đó)
function fillCategories() {
  categorySelect.replaceChildren(new Option("All", "all"));
  state.category = "all";
  const names = { hoodies: "Hoodies", oversize: "Oversized Shirts", compression: "Compression", bodysuits: "Bodysuits",
    bikinis: "Bikinis", bottoms: "Bottoms", accessories: "Accessories" };
  [...new Set(products.filter(matchAudience).map((p) => p.category))].forEach((c) => {
    categorySelect.add(new Option(names[c] || c, c));
  });
}

// ---------- Popup chi tiết sản phẩm: ảnh bên trái, thông tin + nút mua bên phải ----------
function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function openProduct(product) {
  let color = product.colors[0];
  let size = null;
  detail.replaceChildren();

  // Bên trái: ảnh theo màu đang chọn
  const media = el("div", "review-detail__photo product-card__media product-detail__media");
  const showImage = () => media.replaceChildren(createProductImage(product, color));
  showImage();

  // Bên phải: thông tin
  const info = el("div", "review-detail__info");
  const price = el("p", "product-detail__price", formatPrice(product.price, state.currency, rates));
  const message = el("p", "form-error");
  message.setAttribute("role", "alert");

  // Chọn màu
  const colorName = el("span", "", color.name);
  const colorRow = el("div", "product-detail__options");
  product.colors.forEach((c) => {
    const btn = el("button", "swatch-btn");
    btn.type = "button";
    btn.style.background = c.hex;
    btn.title = c.name;
    btn.setAttribute("aria-label", c.name);
    btn.setAttribute("aria-pressed", String(c === color));
    btn.addEventListener("click", () => {
      color = c;
      colorName.textContent = c.name;
      colorRow.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
      showImage();
    });
    colorRow.appendChild(btn);
  });

  // Chọn size XXS -> XL
  const sizeRow = el("div", "product-detail__options");
  const sizeList = product.sizes.length ? product.sizes : SIZES;
  sizeList.forEach((sz) => {
    const btn = el("button", "size-btn", sz);
    btn.type = "button";
    btn.setAttribute("aria-pressed", "false");
    btn.addEventListener("click", () => {
      size = sz;
      message.textContent = "";
      sizeRow.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
    });
    sizeRow.appendChild(btn);
  });

  // Số lượng muốn mua (tối đa bằng số còn trong kho)
  let qty = 1;
  const qtyValue = el("span", "qty__value", "1");
  const minus = el("button", "qty__btn", "−");
  const plus = el("button", "qty__btn", "+");
  minus.type = plus.type = "button";
  minus.setAttribute("aria-label", "Decrease quantity");
  plus.setAttribute("aria-label", "Increase quantity");
  function setQty(n) {
    qty = Math.min(Math.max(n, 1), product.stock);
    qtyValue.textContent = qty;
    minus.disabled = qty <= 1;
    plus.disabled = qty >= product.stock;
  }
  minus.addEventListener("click", () => setQty(qty - 1));
  plus.addEventListener("click", () => setQty(qty + 1));
  setQty(1);
  const qtyRow = el("div", "qty");
  qtyRow.append(minus, qtyValue, plus);

  // Dòng số hàng còn trong kho (con số tô đỏ)
  const stockLine = el("p", "product-detail__stock");
  if (product.stock > 0) {
    stockLine.append(el("strong", "stock-number", String(product.stock)), " in stock");
  } else {
    stockLine.textContent = "Out of stock";
  }

  // Nút thêm vào giỏ / mua ngay (bắt buộc chọn size)
  const addBtn = el("button", "btn", "Add to cart");
  const buyBtn = el("button", "btn btn--ghost", "Buy now");
  addBtn.type = buyBtn.type = "button";
  function checkSize() {
    if (!size) { message.textContent = "Please select a size."; return false; }
    return true;
  }
  addBtn.addEventListener("click", () => {
    if (!checkSize()) return;
    addToCart(product.id, color.name, size, qty);
    addBtn.textContent = "Added ✓";
    setTimeout(() => { addBtn.textContent = "Add to cart"; }, 1500);
  });
  buyBtn.addEventListener("click", () => {
    if (!checkSize()) return;
    addToCart(product.id, color.name, size, qty);
    location.href = "cart.html";
  });
  const actions = el("div", "product-detail__actions");
  if (product.stock > 0) {
    actions.append(addBtn, buyBtn);
  } else {
    actions.appendChild(el("p", "product-card__tag", "Sold out"));
  }

  // Thông số
  const specs = el("dl", "spec-list");
  [["Material", product.specs.material], ["Weight", product.specs.weight],
   ["Fit", product.specs.fit], ["Care", product.specs.care]].forEach(([label, value]) => {
    const row = el("div", "spec-row");
    row.append(el("dt", "", label), el("dd", "", value));
    specs.appendChild(row);
  });

  const colorLabel = el("p", "product-detail__label", "Color · ");
  colorLabel.appendChild(colorName);

  const close = el("button", "review-detail__close", "×");
  close.type = "button";
  close.setAttribute("aria-label", "Close");
  close.addEventListener("click", () => dialog.close());

  info.append(
    el("h2", "glass__title", product.name), price, el("p", "review-card__item", product.description),
    colorLabel, colorRow, el("p", "product-detail__label", "Size"), sizeRow,
    ...(product.stock > 0 ? [el("p", "product-detail__label", "Quantity"), qtyRow] : []), stockLine, message, actions, specs
  );
  detail.append(media, info, close);
  dialog.showModal();
}

// Bấm ra ngoài vùng nội dung thì đóng popup
dialog.addEventListener("click", (e) => { if (e.target === dialog) dialog.close(); });

function fillCurrencies() {
  REGIONS.forEach((r) => currencySelect.add(new Option(r.name + " (" + r.code + ")", r.code)));
  currencySelect.value = state.currency;
}

audienceButtons.forEach((b) => b.addEventListener("click", () => {
  state.audience = b.dataset.audience;
  audienceButtons.forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
  header.classList.toggle("is-her", state.audience === "her"); // đổi logo trắng <-> đỏ
  fillCategories();
  render();
}));
categorySelect.addEventListener("change", () => { state.category = categorySelect.value; render(); });
sortSelect.addEventListener("change", () => { state.sort = sortSelect.value; render(); });
currencySelect.addEventListener("change", () => {
  state.currency = currencySelect.value;
  saveCurrency(state.currency);   // nhớ lựa chọn cho các trang khác
  render();
});

async function init() {
  try {
    fillCurrencies();
    const [list, rateInfo] = await Promise.all([loadProducts(), loadRates()]);
    products = list;
    rates = rateInfo.rates;
    fillCategories();
    render();
  } catch (err) {
    grid.textContent = "Unable to load products.";
    console.error(err);
  }
}
init();
