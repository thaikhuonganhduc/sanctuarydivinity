// Trang Account: chưa đăng nhập thì mời đăng nhập; đã đăng nhập thì hiện thông tin cá nhân (sửa được),
// đổi mật khẩu, đăng xuất và lịch sử đơn hàng (đọc từ localStorage "sanctuary_orders", lọc theo email tài khoản).
import { getCurrentUser, updateProfile, changePassword, logout } from "./auth.js";
import { openAuth } from "./auth-ui.js";
import { rules, validateForm, liveValidate } from "./form-validate.js";
import { loadProducts, createProductImage } from "./products.js";
import { REGIONS, loadRates, formatPrice, getSavedCurrency } from "./currency.js";
import { readList, isValidOrder } from "./storage.js";

const ORDERS_KEY = "sanctuary_orders";
const $ = (id) => document.getElementById(id);

let products = {};
let rates = { USD: 1 };

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

const formatDate = (iso) => new Date(iso).toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });

// ---------- Vẽ trang theo trạng thái đăng nhập ----------
function render() {
  const user = getCurrentUser();
  $("account-guest").hidden = Boolean(user);
  $("account-content").hidden = !user;
  if (!user) return;

  $("account-name").textContent = user.name;
  $("account-email").textContent = user.email;
  $("account-since").textContent = formatDate(user.createdAt);
  $("pf-name").value = user.name;
  $("pf-phone").value = user.phone;
  $("pf-address").value = user.address;
  $("pf-city").value = user.city;
  $("pf-country").value = user.country || REGIONS[0].name;
  renderOrders(user);
}

// ---------- Lịch sử đơn hàng ----------
function renderOrders(user) {
  let orders = [];
  orders = readList(ORDERS_KEY, isValidOrder);      // đơn sai cấu trúc bị bỏ qua, không làm lỗi trang
  orders = orders.filter((o) => o.userEmail === user.email).reverse();     // đơn mới nhất lên đầu

  const list = $("order-list");
  list.replaceChildren();
  $("orders-empty").hidden = orders.length > 0;
  const currency = getSavedCurrency();

  orders.forEach((order) => {
    const li = el("li", "order-card");
    const head = el("div", "order-card__head");
    head.append(el("p", "order-card__number", order.number), el("p", "order-card__date", formatDate(order.date)));

    // Các món trong đơn: ảnh nhỏ + tên + màu/size/số lượng
    const items = el("ul", "order-card__items");
    let subtotal = 0;
    order.items.forEach((item) => {
      const p = products[item.id];
      if (!p) return;                                // sản phẩm không còn trong dữ liệu
      subtotal += p.price * item.qty;
      const color = p.colors.find((c) => c.name === item.color) || p.colors[0];
      const row = el("li", "order-item");
      const media = el("div", "product-card__media order-item__media");
      media.appendChild(createProductImage(p, color));
      const info = el("div", "order-item__info");
      info.append(el("p", "order-item__name", p.name), el("p", "cart-note", item.color + " · Size " + item.size + " · Qty " + item.qty));
      row.append(media, info);
      items.appendChild(row);
    });

    // Đơn cũ (trước khi có tài khoản) chưa lưu tổng tiền thì hiện tạm tổng giá hàng
    const total = typeof order.totalUsd === "number" ? order.totalUsd : subtotal;
    const foot = el("div", "order-card__foot");
    const status = order.status || "Processing";           // admin đổi trạng thái ở trang Admin
    foot.append(el("span", "order-card__status order-card__status--" + status.toLowerCase(), status), el("span", "order-card__total", "Total " + formatPrice(total, currency, rates)));

    li.append(head, items, foot);
    list.appendChild(li);
  });
}

// ---------- Sửa thông tin ----------
const profileForm = $("profile-form");
const profileRules = {
  "pf-name": [rules.required, rules.minLength(2)],
  // SĐT, địa chỉ có thể để trống; đã nhập thì phải đúng dạng
  "pf-phone": [(v) => v.trim() === "" || rules.phone(v)],
  "pf-address": [(v) => v.trim() === "" || rules.minLength(5)(v)]
};
liveValidate(profileForm, profileRules);
profileForm.addEventListener("submit", (e) => {
  e.preventDefault();
  $("profile-saved").hidden = true;
  if (!validateForm(profileForm, profileRules)) return;
  try {
    updateProfile({
      name: $("pf-name").value, phone: $("pf-phone").value, address: $("pf-address").value,
      city: $("pf-city").value, country: $("pf-country").value
    });
  } catch (err) {
    alert(err.message);                                       // lưu lỗi: báo và giữ nguyên nội dung đang sửa
    return;
  }
  render();
  window.dispatchEvent(new CustomEvent("auth-change"));      // cập nhật tên trên icon tài khoản
  $("profile-saved").hidden = false;
});

// ---------- Đổi mật khẩu ----------
const passwordForm = $("password-form");
const passwordRules = {
  "pw-old": [rules.required],
  "pw-new": [rules.required, rules.minLength(8), (v) => (/[a-z]/i.test(v) && /\d/.test(v)) || "Use both letters and numbers."]
};
liveValidate(passwordForm, passwordRules);
passwordForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const msg = $("password-msg");
  msg.textContent = "";
  msg.className = "form-error";
  if (!validateForm(passwordForm, passwordRules)) return;
  try {
    await changePassword($("pw-old").value, $("pw-new").value);
    passwordForm.reset();
    msg.textContent = "Password updated.";
    msg.className = "contact-success";
  } catch (err) {
    msg.textContent = err.message;
  }
});

// ---------- Đăng xuất / đăng nhập ----------
$("sign-out").addEventListener("click", () => {
  logout();
  window.dispatchEvent(new CustomEvent("auth-change"));
});
$("guest-signin").addEventListener("click", () => openAuth("signin"));
$("guest-register").addEventListener("click", () => openAuth("register"));
window.addEventListener("auth-change", render);

// ---------- Khởi động ----------
REGIONS.forEach((r) => $("pf-country").add(new Option(r.name, r.name)));
Promise.all([loadProducts({ includeHidden: true }), loadRates()])
  .then(([items, rateInfo]) => {
    items.forEach((p) => { products[p.id] = p; });
    rates = rateInfo.rates;
    render();
  })
  .catch((err) => { console.error(err); render(); });
