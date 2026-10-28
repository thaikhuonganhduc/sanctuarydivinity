// Trang quản trị (chỉ vai trò admin vào được, xem guard.js).
// Web không có backend nên mọi dữ liệu đọc/ghi ở localStorage của trình duyệt:
//   sanctuary_orders (đơn hàng), sanctuary_users (khách), sanctuary_messages (tin nhắn),
//   sanctuary_product_overrides (thay đổi giá/tồn kho/ẩn/xoá sản phẩm, xem products.js),
//   sanctuary_custom_products (sản phẩm admin thêm mới).
// Sản phẩm gốc và mã athlete đọc từ file JSON bằng fetch.
// An toàn: mọi chữ do người dùng nhập (tên, tin nhắn...) đều ghi bằng textContent, không dùng innerHTML.
import { logout } from "./guard.js";
import { loadProducts, createProductImage, OVERRIDES_KEY, CUSTOM_PRODUCTS_KEY, getProductOverrides, stockAfter, applyStock } from "./products.js";
import { listUsers, addSampleUser } from "./auth.js";
import { readList as readStored, writeJSON, writeAll, isObject, isValidOrder, isValidUser, isValidMessage, isValidProduct } from "./storage.js";
import { getLaunchDate, setLaunchDate, resetLaunchDate, isLaunchOverridden, DEFAULT_LAUNCH, toVietnamInput, fromVietnamInput, formatLaunch } from "./countdown.js";
import { rules, validateForm, liveValidate } from "./form-validate.js";
import { SIZES } from "./size-finder.js";

const KEYS = { orders: "sanctuary_orders", users: "sanctuary_users", messages: "sanctuary_messages", overrides: OVERRIDES_KEY, custom: CUSTOM_PRODUCTS_KEY };
// Luật kiểm tra cấu trúc của từng danh sách (dùng khi đọc localStorage và khi khôi phục file backup)
const VALIDATORS = { [KEYS.orders]: isValidOrder, [KEYS.users]: isValidUser, [KEYS.messages]: isValidMessage, [KEYS.custom]: isValidProduct };
const SAVE_ERROR = "Could not save. Browser storage may be full.";
const STATUSES = ["Processing", "Shipped", "Delivered", "Cancelled"];
const LOW_STOCK = 10;

const $ = (id) => document.getElementById(id);
let products = [];          // tất cả sản phẩm (kể cả đã ẩn / đã xoá), đã áp thay đổi của admin
let productById = {};       // giữ cả sản phẩm đã xoá để đơn hàng cũ vẫn hiện đúng tên
let athletes = [];

// Sản phẩm còn trong danh mục (chưa bị admin xoá)
const listed = () => products.filter((p) => !p.deleted);

// ---------- Tiện ích ----------
function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}
// Bản ghi sai cấu trúc bị bỏ qua (xem storage.js), không làm lỗi trang admin
function readList(key) {
  return readStored(key, VALIDATORS[key]);
}
// Trả về true nếu lưu được; lỗi thì báo bằng toast
function writeList(key, list) {
  if (writeJSON(key, list)) return true;
  toast(SAVE_ERROR);
  return false;
}
const money = (usd) => usd.toLocaleString("en-US", { style: "currency", currency: "USD" });
const formatDate = (iso) => new Date(iso).toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });

// Thông báo nhỏ góc dưới, tự ẩn sau 1,8 giây
let toastTimer;
function toast(text) {
  const box = $("admin-toast");
  box.textContent = text;
  box.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { box.hidden = true; }, 1800);
}

// Tạo bảng: headers = mảng tiêu đề, rows = mảng hàng, mỗi ô là chuỗi hoặc phần tử DOM
function table(headers, rows, emptyText = "Nothing here yet.") {
  const wrap = el("div", "admin-table-wrap");
  if (rows.length === 0) { wrap.appendChild(el("p", "admin-empty", emptyText)); return wrap; }
  const t = el("table", "admin-table");
  const headRow = el("tr");
  headers.forEach((h) => headRow.appendChild(el("th", "", h)));
  t.appendChild(el("thead")).appendChild(headRow);
  const body = el("tbody");
  rows.forEach((cells) => {
    const tr = el("tr");
    cells.forEach((c) => {
      const td = el("td");
      if (c instanceof Node) td.appendChild(c); else td.textContent = c;
      tr.appendChild(td);
    });
    body.appendChild(tr);
  });
  t.appendChild(body);
  wrap.appendChild(t);
  return wrap;
}

// ---------- Tính toán đơn hàng ----------
const orderStatus = (o) => o.status || "Processing";
const orderUnits = (o) => o.items.reduce((n, i) => n + i.qty, 0);
// Tổng tiền: đơn mới có totalUsd; đơn cũ thì cộng giá hàng
function orderTotal(o) {
  if (typeof o.totalUsd === "number") return o.totalUsd;
  return o.items.reduce((sum, i) => sum + (productById[i.id] ? productById[i.id].price * i.qty : 0), 0);
}
// Đơn bị huỷ không tính vào doanh thu
const countsForRevenue = (o) => orderStatus(o) !== "Cancelled";

// ---------- Chuyển mục (giống trang Info: mục đang xem nằm trên địa chỉ #...) ----------
const navLinks = document.querySelectorAll(".admin-nav a");
const RENDERERS = {
  overview: renderOverview, orders: renderOrders, products: renderProducts,
  customers: renderCustomers, messages: renderMessages, codes: renderCodes, launch: renderLaunch, backup: () => {}
};
function showPanel() {
  let id = location.hash.slice(1) || "overview";
  if (!RENDERERS[id]) id = "overview";
  document.querySelectorAll(".admin-panel").forEach((p) => { p.hidden = p.id !== "panel-" + id; });
  navLinks.forEach((a) => {
    if (a.dataset.panel === id) a.setAttribute("aria-current", "page");
    else a.removeAttribute("aria-current");
  });
  RENDERERS[id]();                      // vẽ lại mục vừa mở để luôn thấy dữ liệu mới nhất
}
navLinks.forEach((a) => a.addEventListener("click", (e) => {
  e.preventDefault();
  history.pushState(null, "", a.getAttribute("href"));
  showPanel();
}));
window.addEventListener("popstate", showPanel);

// Số nhỏ cạnh tên mục trong menu
function updateCounts() {
  $("count-orders").textContent = readList(KEYS.orders).length || "";
  $("count-products").textContent = listed().length || "";
  $("count-customers").textContent = listUsers().length || "";
  const unread = readList(KEYS.messages).filter((m) => !m.read).length;
  $("count-messages").textContent = unread || "";
}

// ---------- Overview ----------
function renderOverview() {
  const orders = readList(KEYS.orders);
  const valid = orders.filter(countsForRevenue);
  const revenue = valid.reduce((s, o) => s + orderTotal(o), 0);
  const unread = readList(KEYS.messages).filter((m) => !m.read).length;
  const low = listed().filter((p) => !p.hidden && p.stock <= LOW_STOCK);

  const plural = (n, word) => n + " " + word + (n === 1 ? "" : "s");
  const guests = orders.filter((o) => !o.userEmail).length;
  const kpis = [
    ["Revenue", money(revenue), "Excludes cancelled orders"],
    ["Orders", String(orders.length), orders.filter((o) => orderStatus(o) === "Processing").length + " to process"],
    ["Average order", money(valid.length ? revenue / valid.length : 0), "Per paid order"],
    ["Customers", String(listUsers().length), plural(guests, "guest order")],
    ["Unread messages", String(unread), "From the Info page"],
    ["Low stock", String(low.length), LOW_STOCK + " pieces or fewer"]
  ];
  $("kpis").replaceChildren(...kpis.map(([label, value, note]) => {
    const card = el("div", "kpi");
    card.append(el("p", "kpi__label", label), el("p", "kpi__value", value), el("p", "kpi__note", note));
    return card;
  }));

  // 5 đơn mới nhất
  const recent = orders.slice(-5).reverse().map((o) => [o.number, formatDate(o.date), o.customer.name, money(orderTotal(o)), statusBadge(orderStatus(o))]);
  $("recent-orders").replaceChildren(table(["Order", "Date", "Customer", "Total", "Status"], recent, "No orders yet."));

  // Sắp hết hàng: ít nhất lên đầu
  const lowRows = low.sort((a, b) => a.stock - b.stock).slice(0, 8).map((p) => [p.name, stockBadge(p.stock)]);
  $("low-stock").replaceChildren(table(["Product", "Stock"], lowRows, "Every product has enough stock."));

  // Bán chạy: cộng số lượng theo sản phẩm từ các đơn không bị huỷ
  const sold = {};
  valid.forEach((o) => o.items.forEach((i) => { sold[i.id] = (sold[i.id] || 0) + i.qty; }));
  const best = Object.entries(sold).sort((a, b) => b[1] - a[1]).slice(0, 5)
    .map(([id, units]) => [productById[id] ? productById[id].name : id, String(units), money(units * (productById[id] ? productById[id].price : 0))]);
  $("best-sellers").replaceChildren(table(["Product", "Units", "Sales (list price)"], best, "No sales yet."));
}

function statusBadge(status) {
  return el("span", "badge badge--" + status.toLowerCase(), status);
}
function stockBadge(stock) {
  return el("span", "badge " + (stock === 0 ? "badge--cancelled" : stock <= LOW_STOCK ? "badge--processing" : "badge--delivered"), stock === 0 ? "Sold out" : String(stock));
}

// ---------- Orders ----------
STATUSES.forEach((s) => $("order-filter").add(new Option(s, s)));
$("order-filter").prepend(new Option("All statuses", ""));
$("order-filter").value = "";
$("order-filter").addEventListener("change", renderOrders);
$("order-search").addEventListener("input", renderOrders);

function renderOrders() {
  const all = readList(KEYS.orders);
  const status = $("order-filter").value;
  const q = $("order-search").value.trim().toLowerCase();
  const shown = all
    .map((o, index) => ({ o, index }))                 // nhớ vị trí gốc để lưu lại đúng đơn
    .filter(({ o }) => !status || orderStatus(o) === status)
    .filter(({ o }) => !q || [o.number, o.customer.name, o.customer.email].some((v) => v.toLowerCase().includes(q)))
    .reverse();

  const wrap = el("div", "admin-table-wrap");
  if (shown.length === 0) {
    wrap.appendChild(el("p", "admin-empty", all.length ? "No orders match." : "No orders yet."));
    $("orders-table").replaceChildren(wrap);
    return;
  }
  const t = el("table", "admin-table");
  const head = el("tr");
  ["Order", "Date", "Customer", "Items", "Total", "Status", ""].forEach((h) => head.appendChild(el("th", "", h)));
  t.appendChild(el("thead")).appendChild(head);
  const body = el("tbody");

  shown.forEach(({ o, index }) => {
    const tr = el("tr");
    const who = el("div");
    who.append(el("p", "", o.customer.name), el("p", "admin-sub", o.customer.email + (o.userEmail ? "" : " · guest")));

    // Đổi trạng thái: lưu ngay vào localStorage, khách thấy ở trang Account
    const select = el("select", "input input--compact");
    select.setAttribute("aria-label", "Status of " + o.number);
    STATUSES.forEach((s) => select.add(new Option(s, s)));
    select.value = orderStatus(o);
    select.addEventListener("change", () => {
      const orders = readList(KEYS.orders);
      const order = orders[index];
      const before = orderStatus(order);
      const after = select.value;
      // Tồn kho (chỉ với đơn đã trừ kho lúc đặt, xem cart-page.js):
      // huỷ đơn -> cộng hàng lại vào kho; mở lại đơn đã huỷ -> trừ kho lần nữa
      let sign = 0;
      if (order.stockDeducted && before !== "Cancelled" && after === "Cancelled") sign = 1;
      if (order.stockDeducted && before === "Cancelled" && after !== "Cancelled") sign = -1;

      order.status = after;
      const entries = [[KEYS.orders, orders]];
      const change = sign ? stockAfter(productById, order.items, sign) : null;
      if (change) entries.push([KEYS.overrides, change.overrides]);
      // Ghi đơn + tồn kho cùng lúc; lỗi thì trả ô chọn về trạng thái cũ
      if (!writeAll(entries)) { select.value = before; toast(SAVE_ERROR); return; }
      if (change) applyStock(productById, change.stock);
      toast(o.number + " marked " + after + (sign > 0 ? " · stock returned" : sign < 0 ? " · stock taken again" : ""));
      updateCounts();
    });

    const toggle = el("button", "link-btn", "Details");
    toggle.type = "button";
    toggle.setAttribute("aria-expanded", "false");

    [o.number, formatDate(o.date), who, String(orderUnits(o)), money(orderTotal(o)), select, toggle].forEach((c) => {
      const td = el("td");
      if (c instanceof Node) td.appendChild(c); else td.textContent = c;
      tr.appendChild(td);
    });

    // Hàng chi tiết (ẩn, bấm Details để mở): các món + địa chỉ + thanh toán
    const detail = el("tr", "order-detail");
    detail.hidden = true;
    const td = el("td");
    td.colSpan = 7;
    const items = el("ul", "admin-items");
    o.items.forEach((i) => {
      const p = productById[i.id];
      items.appendChild(el("li", "", (p ? p.name : i.id) + " · " + i.color + " · Size " + i.size + " × " + i.qty));
    });
    const c = o.customer;
    const info = el("dl", "admin-dl");
    [["Phone", c.phone], ["Ship to", [c.address, c.city, c.country].filter(Boolean).join(", ")],
     ["Payment", o.payment], ["Athlete code", o.discountCode || "None"], ["Shown currency", o.currency]].forEach(([k, v]) => {
      info.append(el("dt", "", k), el("dd", "", v || "-"));
    });
    td.append(items, info);
    detail.appendChild(td);
    toggle.addEventListener("click", () => {
      detail.hidden = !detail.hidden;
      toggle.setAttribute("aria-expanded", String(!detail.hidden));
      toggle.textContent = detail.hidden ? "Details" : "Hide";
    });

    body.append(tr, detail);
  });
  t.appendChild(body);
  wrap.appendChild(t);
  $("orders-table").replaceChildren(wrap);
}

// ---------- Products ----------
$("product-search").addEventListener("input", renderProducts);
$("product-category").addEventListener("change", renderProducts);
// Đưa về đúng products.json: bỏ mọi thay đổi và xoá luôn các sản phẩm admin đã thêm
$("products-reset").addEventListener("click", async () => {
  if (!confirm("Reset every product change back to products.json? Products you added will be removed too.")) return;
  if (!writeAll([[KEYS.overrides, null], [KEYS.custom, null]])) { toast(SAVE_ERROR); return; }
  await reloadProducts();
  renderProducts();
  updateCounts();
  toast("Product changes reset");
});

// Khôi phục mọi sản phẩm đã xoá (bỏ dấu deleted, giữ nguyên các thay đổi khác như giá, tồn kho)
$("products-restore").addEventListener("click", async () => {
  const overrides = getProductOverrides();
  Object.keys(overrides).forEach((id) => {
    if (!isObject(overrides[id])) return;
    delete overrides[id].deleted;
    if (Object.keys(overrides[id]).length === 0) delete overrides[id];
  });
  if (!writeJSON(KEYS.overrides, overrides)) { toast(SAVE_ERROR); return; }
  await reloadProducts();
  renderProducts();
  updateCounts();
  toast("Deleted products restored");
});

// Lưu 1 thay đổi của 1 sản phẩm (chỉ lưu phần khác với dữ liệu gốc). Trả về true nếu lưu được
function saveOverride(product, field, value) {
  const overrides = getProductOverrides();
  overrides[product.id] = { ...(overrides[product.id] || {}), [field]: value };
  if (!writeJSON(KEYS.overrides, overrides)) {
    toast(SAVE_ERROR);
    renderProducts();                       // vẽ lại để ô nhập trở về giá trị cũ (chưa lưu được)
    return false;
  }
  product[field] = value;
  if (field === "stock") product.inStock = value > 0;
  toast("Saved: " + product.name);
  return true;
}

// Xoá sản phẩm: chỉ đánh dấu deleted (không xoá hẳn) để đơn hàng cũ vẫn tra được tên, và bấm Restore là lấy lại.
// Cửa hàng và giỏ hàng bỏ qua sản phẩm có deleted (xem loadProducts trong products.js).
function deleteProduct(product) {
  if (!confirm("Delete \"" + product.name + "\"? It disappears from the store and from shopping carts. You can bring it back with Restore deleted.")) return;
  if (!saveOverride(product, "deleted", true)) return;
  renderProducts();
  updateCounts();
  toast("Deleted: " + product.name);
}

function renderProducts() {
  const q = $("product-search").value.trim().toLowerCase();
  const cat = $("product-category").value;
  const overrides = getProductOverrides();

  // Nút Restore chỉ hiện khi có sản phẩm đã xoá
  const deletedCount = products.length - listed().length;
  $("products-restore").hidden = deletedCount === 0;
  $("products-restore").textContent = "Restore deleted (" + deletedCount + ")";

  const rows = listed()
    .filter((p) => (!cat || p.category === cat) && (!q || p.name.toLowerCase().includes(q) || p.id.includes(q)))
    .map((p) => {
      const thumb = el("div", "admin-thumb");
      thumb.appendChild(createProductImage(p, p.colors[0]));

      const name = el("div");
      name.append(el("p", "", p.name), el("p", "admin-sub", p.id + " · " + p.gender + (p.custom ? " · added" : "") + (overrides[p.id] ? " · edited" : "")));

      // Giá: số dương, tối đa 2 chữ số thập phân
      const price = el("input", "input input--compact input--num");
      price.type = "number"; price.min = "1"; price.step = "0.01"; price.value = p.price;
      price.setAttribute("aria-label", "Price of " + p.name);
      price.addEventListener("change", () => {
        const v = Math.round(Number(price.value) * 100) / 100;
        if (!(v > 0)) { price.value = p.price; toast("Price must be above 0"); return; }
        saveOverride(p, "price", v);
      });

      // Tồn kho: số nguyên >= 0
      const stock = el("input", "input input--compact input--num");
      stock.type = "number"; stock.min = "0"; stock.step = "1"; stock.value = p.stock;
      stock.setAttribute("aria-label", "Stock of " + p.name);
      stock.addEventListener("change", () => {
        const v = Math.floor(Number(stock.value));
        if (!(v >= 0)) { stock.value = p.stock; toast("Stock must be 0 or more"); return; }
        saveOverride(p, "stock", v);
      });

      const featured = el("input");
      featured.type = "checkbox"; featured.checked = Boolean(p.featured);
      featured.setAttribute("aria-label", "Feature " + p.name);
      featured.addEventListener("change", () => saveOverride(p, "featured", featured.checked));

      // "On sale" = hiện trên cửa hàng; bỏ tick là ẩn sản phẩm
      const visible = el("input");
      visible.type = "checkbox"; visible.checked = !p.hidden;
      visible.setAttribute("aria-label", "Show " + p.name + " in the store");
      visible.addEventListener("change", () => saveOverride(p, "hidden", !visible.checked));

      const del = el("button", "link-btn link-btn--danger", "Delete");
      del.type = "button";
      del.setAttribute("aria-label", "Delete " + p.name);
      del.addEventListener("click", () => deleteProduct(p));

      return [thumb, name, p.category, price, stock, featured, visible, del];
    });
  $("products-table").replaceChildren(table(["", "Product", "Category", "Price (USD)", "Stock", "Featured", "On sale", ""], rows, "No products match."));
}

// ---------- Thêm sản phẩm ----------
// Danh mục được chọn theo dòng sản phẩm, đúng với các nhóm mà cửa hàng chia (LINES trong shop.js),
// để sản phẩm mới luôn có chỗ hiện trên trang shop
const CATEGORIES = {
  him: [["compression", "Compression"], ["hoodies", "Zip-ups and crewnecks"], ["oversize", "T-shirts"], ["tops", "Stringers and beaters"], ["bottoms", "Cargos, sweatpants and jeans"]],
  her: [["hoodies", "Zip-ups"], ["tops", "Baby tees and sports bras"], ["bodysuits", "Bodysuits"], ["bottoms", "Leggings, shorts and sweatpants"]],
  unisex: [["accessories", "Accessories"]]
};
const ONE_SIZE = "One size";
const PHOTO_MAX_WIDTH = 800;               // bằng ảnh sản phẩm có sẵn; ảnh nhỏ thì localStorage mới chứa được
const PHOTO_MAX_BYTES = 10 * 1024 * 1024;

const productForm = $("product-form");
const PRODUCT_RULES = {
  "pf-name": [rules.required, rules.minLength(3)],
  "pf-price": [(v) => Number(v) > 0 || "Enter a price above 0."],
  "pf-stock": [(v) => (v.trim() !== "" && Number.isInteger(Number(v)) && Number(v) >= 0) || "Enter a whole number, 0 or more."],
  "pf-color": [rules.required]
};
liveValidate(productForm, PRODUCT_RULES);
let photoTask = null;                      // Promise trả về ảnh đã thu nhỏ (dạng data URL), null = chưa chọn ảnh

// Ô chọn size: XXS → XXL và One size (cho phụ kiện), tạo bằng DOM
[...SIZES, ONE_SIZE].forEach((size) => {
  const label = el("label");
  const box = el("input");
  box.type = "checkbox"; box.name = "pf-size"; box.value = size;
  label.append(box, document.createTextNode(size));
  $("pf-sizes").appendChild(label);
});

// Đổi dòng sản phẩm: đổi danh sách danh mục và tick sẵn size hợp lý (quần áo: XXS-XXL, phụ kiện: One size)
function fillCategories() {
  const line = $("pf-line").value;
  $("pf-category").replaceChildren(...CATEGORIES[line].map(([value, label]) => new Option(label, value)));
  productForm.querySelectorAll("input[name='pf-size']").forEach((box) => {
    box.checked = line === "unisex" ? box.value === ONE_SIZE : box.value !== ONE_SIZE;
  });
}
$("pf-line").addEventListener("change", fillCategories);

// Thu nhỏ ảnh trước khi lưu: FileReader đọc file -> vẽ lên canvas rộng tối đa 800px -> xuất WebP (trình duyệt
// không hỗ trợ WebP thì xuất JPEG). Ảnh gốc từ điện thoại có thể vài MB, lưu thẳng sẽ làm đầy localStorage (~5 MB).
function readPhoto(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.addEventListener("error", () => reject(new Error("Could not read this file.")));
    reader.addEventListener("load", () => {
      const img = new Image();
      img.addEventListener("error", () => reject(new Error("This file is not a readable image.")));
      img.addEventListener("load", () => {
        const scale = Math.min(1, PHOTO_MAX_WIDTH / img.width);
        const canvas = document.createElement("canvas");
        canvas.width = Math.round(img.width * scale);
        canvas.height = Math.round(img.height * scale);
        canvas.getContext("2d").drawImage(img, 0, 0, canvas.width, canvas.height);
        let url = canvas.toDataURL("image/webp", 0.85);
        if (!url.startsWith("data:image/webp")) url = canvas.toDataURL("image/jpeg", 0.85);
        resolve(url);
      });
      img.src = reader.result;
    });
    reader.readAsDataURL(file);
  });
}

$("pf-image").addEventListener("change", () => {
  const file = $("pf-image").files[0];
  const preview = $("pf-preview");
  $("error-pf-image").textContent = "";
  preview.hidden = true;
  photoTask = null;
  if (!file) return;
  if (!/^image\/(jpeg|png|webp)$/.test(file.type) || file.size > PHOTO_MAX_BYTES) {
    $("error-pf-image").textContent = "Choose a JPG, PNG or WebP photo up to 10 MB.";
    $("pf-image").value = "";
    return;
  }
  photoTask = readPhoto(file);
  photoTask.then((url) => { preview.src = url; preview.hidden = false; })
    .catch((err) => { $("error-pf-image").textContent = err.message; $("pf-image").value = ""; photoTask = null; });
});

function openProductForm(open) {
  productForm.hidden = !open;
  $("product-add").setAttribute("aria-expanded", String(open));
  if (!open) return;
  productForm.reset();
  productForm.querySelectorAll(".form-error").forEach((p) => { p.textContent = ""; });
  productForm.querySelectorAll("[aria-invalid]").forEach((i) => i.removeAttribute("aria-invalid"));
  $("pf-preview").hidden = true;
  photoTask = null;
  fillCategories();
  $("pf-name").focus();
}
$("product-add").addEventListener("click", () => openProductForm(productForm.hidden));
$("pf-cancel").addEventListener("click", () => openProductForm(false));

productForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  let ok = validateForm(productForm, PRODUCT_RULES);

  // Không cho trùng tên với sản phẩm đang có
  const name = $("pf-name").value.trim().replace(/\s+/g, " ");
  if (ok && listed().some((p) => p.name.toLowerCase() === name.toLowerCase())) {
    $("error-pf-name").textContent = "A product with this name already exists.";
    $("pf-name").setAttribute("aria-invalid", "true");
    $("pf-name").focus();
    ok = false;
  }
  const sizes = [...productForm.querySelectorAll("input[name='pf-size']:checked")].map((box) => box.value);
  $("error-pf-sizes").textContent = sizes.length ? "" : "Pick at least one size.";
  if (!photoTask) $("error-pf-image").textContent = "Add a photo of the product.";
  if (!ok || !sizes.length || !photoTask) return;

  let photo;
  try { photo = await photoTask; } catch (err) { return; }   // lỗi ảnh đã được báo dưới ô chọn ảnh

  const stock = Number($("pf-stock").value);
  const product = {
    id: "c" + Date.now().toString(36),     // id riêng cho sản phẩm thêm mới (sản phẩm gốc là p01, p02...)
    name,
    category: $("pf-category").value,
    gender: $("pf-line").value,
    price: Math.round(Number($("pf-price").value) * 100) / 100,
    currency: "USD",
    colors: [{ name: $("pf-color").value.trim(), hex: $("pf-hex").value, images: [photo], available: true }],
    sizes,
    featured: $("pf-featured").checked,
    inStock: stock > 0,
    stock,
    tag: "New",
    specs: { material: "", weight: "", fit: "", care: "" },
    description: "",
    features: $("pf-features").value.split("\n").map((line) => line.trim()).filter(Boolean),
    custom: true
  };
  if (!isValidProduct(product)) { toast("Some product details are missing."); return; }

  const list = readList(KEYS.custom);
  list.push(product);
  if (!writeList(KEYS.custom, list)) return;          // thường do ảnh làm đầy localStorage
  await reloadProducts();
  openProductForm(false);
  renderProducts();
  updateCounts();
  toast("Added: " + product.name);
});

// ---------- Customers ----------
$("customer-search").addEventListener("input", renderCustomers);

function renderCustomers() {
  const q = $("customer-search").value.trim().toLowerCase();
  const orders = readList(KEYS.orders);
  const rows = listUsers()
    .filter((u) => !q || u.name.toLowerCase().includes(q) || u.email.includes(q))
    .map((u) => {
      const mine = orders.filter((o) => o.userEmail === u.email);
      const spent = mine.filter(countsForRevenue).reduce((s, o) => s + orderTotal(o), 0);
      const who = el("div");
      who.append(el("p", "", u.name), el("p", "admin-sub", u.email));
      return [who, u.phone || "-", [u.city, u.country].filter(Boolean).join(", ") || "-", formatDate(u.createdAt), String(mine.length), money(spent)];
    });
  $("customers-table").replaceChildren(table(["Customer", "Phone", "Location", "Joined", "Orders", "Spent"], rows, "No customer accounts yet."));
}

// ---------- Messages ----------
function renderMessages() {
  const messages = readList(KEYS.messages);
  const list = $("messages-list");
  list.replaceChildren();
  if (messages.length === 0) { list.appendChild(el("p", "admin-empty", "No messages yet.")); return; }

  // Mới nhất lên đầu; index giữ vị trí gốc để sửa/xoá đúng tin
  messages.map((m, index) => ({ m, index })).reverse().forEach(({ m, index }) => {
    const card = el("article", "message-card" + (m.read ? "" : " is-unread"));
    const head = el("div", "message-card__head");
    const who = el("div");
    who.append(el("p", "message-card__name", m.name), el("p", "admin-sub", m.email + " · " + formatDate(m.date)));
    head.append(who, el("span", "badge badge--shipped", m.topic));
    const body = el("p", "message-card__body", m.message);

    const actions = el("div", "message-card__actions");
    const reply = el("a", "btn btn--small btn--ghost", "Reply");
    reply.href = "mailto:" + encodeURIComponent(m.email) + "?subject=" + encodeURIComponent("Re: " + m.topic);
    const readBtn = el("button", "btn btn--small btn--ghost", m.read ? "Mark unread" : "Mark read");
    readBtn.type = "button";
    readBtn.addEventListener("click", () => {
      const all = readList(KEYS.messages);
      all[index].read = !all[index].read;
      if (!writeList(KEYS.messages, all)) return;
      renderMessages();
      updateCounts();
    });
    const del = el("button", "btn btn--small btn--danger", "Delete");
    del.type = "button";
    del.addEventListener("click", () => {
      if (!confirm("Delete this message from " + m.name + "?")) return;
      const all = readList(KEYS.messages);
      all.splice(index, 1);
      if (!writeList(KEYS.messages, all)) return;
      renderMessages();
      updateCounts();
    });
    actions.append(reply, readBtn, del);
    card.append(head, body, actions);
    list.appendChild(card);
  });
}

// ---------- Athlete codes ----------
function renderCodes() {
  const orders = readList(KEYS.orders);
  const rows = athletes.map((a) => {
    const used = orders.filter((o) => o.discountCode && o.discountCode.toLowerCase() === a.code.toLowerCase());
    const sales = used.filter(countsForRevenue).reduce((s, o) => s + orderTotal(o), 0);
    return [a.name, a.code, el("span", "badge " + (a.active ? "badge--delivered" : "badge--cancelled"), a.active ? "Active" : "Off"), String(used.length), money(sales)];
  });
  $("codes-table").replaceChildren(table(["Athlete", "Code", "Status", "Orders", "Sales"], rows, "No athlete codes in data/access.json."));
}

// ---------- Launch date ----------
// Ô chọn ngày giờ hiểu theo giờ Việt Nam (UTC+7); lưu bằng setLaunchDate() trong countdown.js
function renderLaunch() {
  const launch = getLaunchDate();
  $("launch-input").value = toVietnamInput(launch);
  $("launch-error").textContent = "";

  // Còn bao lâu nữa tới ngày drop (hoặc đã qua)
  const diff = launch - Date.now();
  const days = Math.floor(diff / 86400000);
  const hours = Math.floor((diff % 86400000) / 3600000);
  const left = diff <= 0 ? "Launched (countdown shows 00)" : days + " days " + hours + " hours left";

  const info = $("launch-info");
  info.replaceChildren();
  [["Drop time", formatLaunch(launch) + " (UTC+7)"], ["Source", isLaunchOverridden() ? "Set by admin" : "Default"],
   ["Countdown", left], ["Default", formatLaunch(DEFAULT_LAUNCH)]].forEach(([k, v]) => {
    info.append(el("dt", "", k), el("dd", "", v));
  });
}

$("launch-form").addEventListener("submit", (e) => {
  e.preventDefault();
  const time = fromVietnamInput($("launch-input").value);
  const year = time === null ? 0 : new Date(time).getUTCFullYear();
  if (time === null || year < 2020 || year > 2100) {
    $("launch-error").textContent = "Choose a valid date and time.";
    return;
  }
  if (!setLaunchDate(time)) { toast(SAVE_ERROR); return; }
  renderLaunch();
  toast("Launch date saved");
});

$("launch-reset").addEventListener("click", () => {
  if (!resetLaunchDate()) { toast(SAVE_ERROR); return; }
  renderLaunch();
  toast("Launch date reset to default");
});

// ---------- Backup ----------
// Xuất: gom dữ liệu cửa hàng trong localStorage thành 1 file JSON rồi tải về (Blob + thẻ <a download>).
// Đọc qua readList / getProductOverrides nên dữ liệu hỏng không làm lỗi nút xuất.
$("backup-export").addEventListener("click", () => {
  const data = {
    [KEYS.orders]: readList(KEYS.orders),
    [KEYS.users]: readList(KEYS.users),
    [KEYS.messages]: readList(KEYS.messages),
    [KEYS.overrides]: getProductOverrides(),
    [KEYS.custom]: readList(KEYS.custom)
  };
  const backup = { app: "sanctuary", version: 1, exportedAt: new Date().toISOString(), data };
  const blob = new Blob([JSON.stringify(backup, null, 2)], { type: "application/json" });
  const link = el("a");
  link.href = URL.createObjectURL(blob);
  link.download = "sanctuary-backup-" + new Date().toISOString().slice(0, 10) + ".json";
  link.click();
  URL.revokeObjectURL(link.href);
  $("backup-status").textContent = "Backup downloaded.";
});

// Kiểm tra file backup TRƯỚC khi ghi bất cứ thứ gì: đúng app, đúng phiên bản, từng phần dữ liệu đúng cấu trúc.
// Sai ở đâu thì ném lỗi nói rõ phần đó, dữ liệu hiện tại giữ nguyên.
function checkBackup(backup) {
  if (!isObject(backup) || backup.app !== "sanctuary") throw new Error("Not a SANCTUARY backup file.");
  if (backup.version !== 1) throw new Error("This backup version is not supported.");
  if (!isObject(backup.data)) throw new Error("The file has no store data.");
  [[KEYS.orders, "orders"], [KEYS.users, "customers"], [KEYS.messages, "messages"], [KEYS.custom, "added products"]].forEach(([key, label]) => {
    const list = backup.data[key];
    if (list !== undefined && !(Array.isArray(list) && list.every(VALIDATORS[key]))) {
      throw new Error("The " + label + " in this file are damaged.");
    }
  });
  const overrides = backup.data[KEYS.overrides];
  if (overrides !== undefined && !(isObject(overrides) && Object.values(overrides).every(isObject))) {
    throw new Error("The product changes in this file are damaged.");
  }
}

// Nhập: đọc file bằng FileReader, kiểm tra toàn bộ rồi mới ghi đè (ghi cùng lúc, lỗi giữa chừng thì trả lại như cũ)
$("backup-import").addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.addEventListener("load", async () => {
    try {
      let backup;
      try { backup = JSON.parse(reader.result); } catch (err) { throw new Error("The file is not valid JSON."); }
      checkBackup(backup);
      if (!confirm("Replace the current store data with this backup from " + formatDate(backup.exportedAt) + "?")) return;
      // Key không có trong file thì xoá (null), giống trạng thái lúc xuất file
      const entries = Object.values(KEYS).map((key) => [key, key in backup.data ? backup.data[key] : null]);
      if (!writeAll(entries)) throw new Error("Browser storage is full. Nothing was changed.");
      await reloadProducts();
      updateCounts();
      $("backup-status").textContent = "Backup restored.";
    } catch (err) {
      $("backup-status").textContent = "Could not restore: " + err.message;
    } finally {
      e.target.value = "";                      // cho phép chọn lại cùng 1 file
    }
  });
  reader.readAsText(file);
});

$("backup-clear").addEventListener("click", async () => {
  if (!confirm("Delete all orders, customers, messages, product changes and added products in this browser? This cannot be undone.")) return;
  Object.values(KEYS).forEach((key) => localStorage.removeItem(key));
  localStorage.removeItem("sanctuary_session");           // tài khoản đã xoá thì đăng xuất luôn
  await reloadProducts();
  updateCounts();
  $("backup-status").textContent = "Store data cleared.";
});

// Dữ liệu mẫu để thuyết trình: 3 khách, 8 đơn đủ trạng thái, 3 tin nhắn.
// Bấm nhiều lần không tạo trùng: khách trùng email, đơn trùng số, tin nhắn trùng nội dung đều được bỏ qua.
// Đơn mẫu không trừ kho (không có stockDeducted), nên huỷ đơn mẫu cũng không cộng kho.
$("backup-sample").addEventListener("click", async () => {
  const people = [
    { name: "Minh Tran", email: "minh.tran@example.com", phone: "0903 456 789", address: "45 Le Loi Street", city: "Ho Chi Minh City", country: "Vietnam" },
    { name: "Jordan Reyes", email: "jordan.reyes@example.com", phone: "+1 415 555 0142", address: "820 Mission Street", city: "San Francisco", country: "United States" },
    { name: "Hana Sato", email: "hana.sato@example.com", phone: "+81 90 1234 5678", address: "2-11-3 Shibuya", city: "Tokyo", country: "Japan" }
  ];
  const day = 24 * 60 * 60 * 1000;
  let addedUsers = 0;
  try {
    for (const [i, p] of people.entries()) {
      if (await addSampleUser({ ...p, password: "Sanctuary1", createdAt: new Date(Date.now() - (40 - i * 10) * day).toISOString() })) addedUsers++;
    }
  } catch (err) {
    $("backup-status").textContent = err.message;
    return;
  }

  // Đơn mẫu: chọn ngẫu nhiên sản phẩm đang bán
  const forSale = listed().filter((p) => !p.hidden);
  const pick = () => forSale[Math.floor(Math.random() * forSale.length)];
  const statuses = ["Delivered", "Delivered", "Shipped", "Shipped", "Processing", "Processing", "Processing", "Cancelled"];
  const orders = readList(KEYS.orders);
  const existingNumbers = new Set(orders.map((o) => o.number));
  let addedOrders = 0;
  statuses.forEach((status, i) => {
    const number = "SD-DEMO" + (i + 1);
    if (existingNumbers.has(number) || forSale.length === 0) return;   // đã có đơn số này thì bỏ qua
    addedOrders++;
    const person = people[i % people.length];
    const items = [pick(), pick()].slice(0, 1 + (i % 2)).map((p) => ({ id: p.id, color: p.colors[0].name, size: p.sizes[Math.min(2, p.sizes.length - 1)], qty: 1 + (i % 3 === 0 ? 1 : 0) }));
    const subtotal = items.reduce((s, it) => s + productById[it.id].price * it.qty, 0);
    orders.push({
      number, date: new Date(Date.now() - (14 - i * 1.5) * day).toISOString(), items, currency: "USD",
      customer: { ...person }, payment: i % 3 === 0 ? "paypal" : "card",
      discountCode: i === 2 && athletes[0] ? athletes[0].code : null,
      // tổng = giá hàng (đơn số 3 dùng mã athlete giảm 10%) + 24 USD phí ship ước tính
      totalUsd: Math.round(subtotal * (i === 2 ? 0.9 : 1) * 100) / 100 + 24, status,
      userEmail: i === 7 ? null : person.email         // 1 đơn khách vãng lai (không có tài khoản)
    });
  });
  const sampleMessages = [
    { date: new Date(Date.now() - 3 * day).toISOString(), name: "Jordan Reyes", email: "jordan.reyes@example.com", topic: "Sizing help", message: "I'm 183 cm and 82 kg. Should I take M or L in the Doom Tech compression?" },
    { date: new Date(Date.now() - 1 * day).toISOString(), name: "Hana Sato", email: "hana.sato@example.com", topic: "Order and shipping", message: "Hi, my tracking has not updated for two days. Is my parcel still in Vietnam?" },
    { date: new Date().toISOString(), name: "Leo Martins", email: "leo.martins@example.com", topic: "Collaboration", message: "I run a powerlifting page with 40k followers and would love to work with SANCTUARY." }
  ];
  const messages = readList(KEYS.messages);
  const newMessages = sampleMessages.filter((s) => !messages.some((m) => m.email === s.email && m.message === s.message));
  messages.push(...newMessages);

  if (!writeAll([[KEYS.orders, orders], [KEYS.messages, messages]])) {
    $("backup-status").textContent = SAVE_ERROR;
    return;
  }
  updateCounts();
  const plural = (n, word) => n + " " + word + (n === 1 ? "" : "s");
  $("backup-status").textContent = addedUsers + addedOrders + newMessages.length === 0
    ? "Sample data is already loaded."
    : "Sample data added: " + plural(addedUsers, "customer") + ", " + plural(addedOrders, "order") + ", " + plural(newMessages.length, "message") + ".";
});

// ---------- Khởi động ----------
$("admin-exit").addEventListener("click", logout);

async function reloadProducts() {
  products = await loadProducts({ includeHidden: true });
  productById = Object.fromEntries(products.map((p) => [p.id, p]));
}

(async function init() {
  try {
    const [, access] = await Promise.all([reloadProducts(), fetch("../data/access.json").then((r) => r.json())]);
    athletes = access.influencers || [];
  } catch (err) {
    console.error(err);
    toast("Could not load store data");
  }
  // Danh mục cho bộ lọc sản phẩm
  const cats = [...new Set(listed().map((p) => p.category))].sort();
  $("product-category").add(new Option("All categories", ""));
  cats.forEach((c) => $("product-category").add(new Option(c, c)));
  updateCounts();
  showPanel();
})();
