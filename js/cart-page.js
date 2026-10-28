// Trang giỏ hàng: đọc giỏ từ localStorage + products.json (fetch), vẽ danh sách bằng DOM,
// sửa số lượng/xoá món, tính tiền, kiểm tra form thanh toán rồi lưu đơn hàng giả lập.
import { loadShipping, calcCosts } from "./shipping.js";
import { loadProducts, createProductImage, renderGrid, isColorAvailable, canBuy, stockAfter, applyStock, OVERRIDES_KEY } from "./products.js";
import { getCart, saveCart, qtyInCart } from "./cart.js";
import { readList, writeAll, isValidOrder } from "./storage.js";
import { REGIONS, loadRates, formatPrice, getSavedCurrency, saveCurrency } from "./currency.js";
import { rules, validateForm, liveValidate } from "./form-validate.js";
import { updateCartCount } from "./header.js";
import { initProductPopup } from "./product-popup.js";
import { getCurrentUser, updateProfile } from "./auth.js";
import { openAuth } from "./auth-ui.js";

const ORDERS_KEY = "sanctuary_orders";

const $ = (id) => document.getElementById(id);
const list = $("cart-list");
const form = $("checkout-form");

let products = {};
let discount = null;        // { code, pct } khi đã áp mã athlete
let athletes = [];          // danh sách athlete + mã lấy từ data/access.json
let shippingData = null;   // dữ liệu phí ship/thuế từ data/shipping.json
let rates = { USD: 1 };
let currency = getSavedCurrency();
let lastTotalUsd = 0;        // tổng tiền (USD) lần tính gần nhất, lưu vào đơn hàng để trang Account hiện lại
let loaded = false;          // đã tải xong dữ liệu sản phẩm chưa (chưa xong thì không được kiểm tra giỏ, kẻo xoá nhầm)

const fmt = (usd) => formatPrice(usd, currency, rates);

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

// ---------- Kiểm tra giỏ ----------
// Giỏ "đã kiểm tra": chỉ giữ món còn bán (sản phẩm chưa bị ẩn, màu còn bán, còn hàng) và số lượng không vượt kho.
// Giỏ này dùng CHUNG cho hiển thị, tính tiền và lưu đơn, nên số tiền khách thấy luôn khớp với đơn được lưu.
// Trả về { cart, changed }: changed = true nếu phải bỏ bớt hoặc giảm món so với giỏ đang lưu.
function checkedCart() {
  const stored = getCart();
  const used = {};                          // số đã xếp vào giỏ của từng sản phẩm (cộng mọi màu/size)
  const cart = [];
  stored.forEach((item) => {
    const p = products[item.id];
    const color = p && p.colors.find((c) => c.name === item.color);
    if (!p || !color || !isColorAvailable(color)) return;
    const qty = Math.min(item.qty, p.stock - (used[p.id] || 0));
    if (qty <= 0) return;
    used[p.id] = (used[p.id] || 0) + qty;
    cart.push({ ...item, qty });
  });
  // Cùng số dòng nghĩa là không bỏ dòng nào, nên so số lượng theo đúng vị trí là được
  const changed = cart.length !== stored.length || cart.some((item, k) => item.qty !== stored[k].qty);
  return { cart, changed };
}

// Dòng thông báo phía trên giỏ hàng
const notice = (text) => { $("cart-notice").textContent = text; };

// ---------- Vẽ giỏ hàng ----------
// Trả về kết quả checkedCart() để nút "Place order" dùng lại đúng giỏ vừa vẽ
function render() {
  if (!loaded) return { cart: [], changed: false };
  const checked = checkedCart();
  const { cart } = checked;
  if (checked.changed) {
    saveCart(cart);                          // lưu lại giỏ đã sửa, lần sau khỏi phải sửa nữa
    notice("Some items in your cart were removed or reduced because they are no longer available in that amount.");
  }
  const hasItems = cart.length > 0;
  $("cart-empty").hidden = hasItems || !$("order-done").hidden;
  $("cart-content").hidden = !hasItems;
  updateCartCount();
  renderSuggest(cart);
  if (!hasItems) return checked;

  list.replaceChildren();
  let subtotal = 0;

  cart.forEach((item) => {
    const p = products[item.id];
    subtotal += p.price * item.qty;
    const color = p.colors.find((c) => c.name === item.color);
    // Dòng này được tối đa bao nhiêu: số trong kho trừ các dòng khác (màu/size khác) của cùng sản phẩm
    const maxForLine = p.stock - qtyInCart(cart, p.id) + item.qty;

    const media = el("div", "product-card__media cart-item__media");
    media.appendChild(createProductImage(p, color));

    const minus = el("button", "qty__btn", "−");
    const plus = el("button", "qty__btn", "+");
    minus.type = plus.type = "button";
    minus.setAttribute("aria-label", "Decrease quantity");
    plus.setAttribute("aria-label", "Increase quantity");
    minus.disabled = item.qty <= 1;
    plus.disabled = item.qty >= maxForLine;          // không vượt quá số trong kho
    minus.addEventListener("click", () => changeQty(item, item.qty - 1));
    plus.addEventListener("click", () => changeQty(item, item.qty + 1));
    const qty = el("div", "qty");
    qty.append(minus, el("span", "qty__value", String(item.qty)), plus);

    const remove = el("button", "cart-item__remove", "Remove");
    remove.type = "button";
    remove.addEventListener("click", () => removeItem(item));
    const actions = el("div", "cart-item__actions");
    actions.append(qty, remove);

    // Số còn trong kho: dưới 10 thì báo sắp hết (số tô đỏ)
    const stock = el("p", "cart-item__stock");
    if (p.stock < 10) {
      stock.append("Only ", el("strong", "stock-number", String(p.stock)), " left in stock");
    } else {
      stock.append(el("strong", "stock-number", String(p.stock)), " in stock");
    }

    const info = el("div", "cart-item__info");
    info.append(
      el("h3", "product-card__name", p.name),
      el("p", "review-card__item", item.color + " · Size " + item.size),
      stock, actions
    );

    const price = el("div", "cart-item__price");
    price.appendChild(el("p", "", fmt(p.price * item.qty)));
    if (item.qty > 1) price.appendChild(el("p", "cart-item__each", fmt(p.price) + " each"));

    const li = el("li", "cart-item");
    li.append(media, info, price);
    list.appendChild(li);
  });

  // Phí ship (theo cân nặng + vùng), thuế nhập khẩu và VAT/GST theo nước đang chọn
  const costs = calcCosts(shippingData, cart, products, $("co-country").value, discount ? discount.pct : 0);
  $("sum-subtotal").textContent = fmt(subtotal);
  const discountUsd = discount ? subtotal * discount.pct / 100 : 0;
  $("row-discount").hidden = !discount;
  if (discount) {
    $("sum-discount-label").textContent = "Discount (" + discount.code + ")";
    $("sum-discount").textContent = "−" + fmt(discountUsd);
  }
  $("sum-shipping-label").textContent = "Shipping (" + costs.weightKg.toFixed(2) + " kg)";
  $("sum-shipping").textContent = fmt(costs.shipping);
  $("row-duty").hidden = costs.duty === 0;
  $("sum-duty").textContent = fmt(costs.duty);
  $("sum-tax-label").textContent = costs.taxLabel + " (" + costs.taxRate + "%)";
  $("sum-tax").textContent = costs.taxRate === 0 ? "None" : fmt(costs.tax);
  lastTotalUsd = subtotal - discountUsd + costs.shipping + costs.duty + costs.tax;
  $("sum-total").textContent = fmt(lastTotalUsd);
  $("shipping-note").textContent = "";
  return checked;
}

function sameItem(a, b) { return a.id === b.id && a.color === b.color && a.size === b.size; }

function changeQty(item, qty) {
  const cart = getCart();
  const found = cart.find((i) => sameItem(i, item));
  if (found) {
    const max = products[item.id].stock - qtyInCart(cart, item.id) + found.qty;   // tính cả các dòng khác của sản phẩm
    found.qty = Math.min(Math.max(qty, 1), max);
  }
  if (!saveCart(cart)) notice("We couldn't save your cart. Please try again.");
  render();
}

function removeItem(item) {
  if (!saveCart(getCart().filter((i) => !sameItem(i, item)))) notice("We couldn't save your cart. Please try again.");
  render();
}

// ---------- Form thanh toán ----------
const cardRules = {
  "co-card": [rules.required, rules.card],
  "co-expiry": [rules.required, rules.expiry],
  "co-cvc": [rules.required, rules.cvc]
};
const baseRules = {
  "co-name": [rules.required, rules.minLength(2)],
  "co-email": [rules.required, rules.email],
  "co-phone": [rules.required, rules.phone],
  "co-address": [rules.required, rules.minLength(5)],
  "co-city": [rules.required]
};
liveValidate(form, { ...baseRules, ...cardRules });

// Nhận diện hãng thẻ từ các số đầu và làm sáng nhãn tương ứng
function detectBrand(number) {
  const n = number.replace(/\s/g, "");
  if (/^4/.test(n)) return "visa";
  if (/^(5[1-5]|2[2-7])/.test(n)) return "mastercard";
  if (/^3[47]/.test(n)) return "amex";
  if (/^35/.test(n)) return "jcb";
  return "";
}
$("co-card").addEventListener("input", (e) => {
  const brand = detectBrand(e.target.value);
  document.querySelectorAll(".pay-brands span").forEach((s) => s.classList.toggle("is-active", s.dataset.brand === brand));
});

// Chọn PayPal / Apple Pay / Google Pay thì ẩn phần nhập thẻ (ví điện tử thanh toán ở cổng riêng)
form.querySelectorAll('input[name="pay"]').forEach((radio) => {
  radio.addEventListener("change", () => {
    $("card-fields").hidden = form.pay.value !== "card";
  });
});

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const errorBox = $("checkout-error");
  errorBox.textContent = "";
  const useCard = form.pay.value === "card";
  if (!validateForm(form, useCard ? { ...baseRules, ...cardRules } : baseRules)) return;

  // Kiểm tra lại giỏ ngay lúc đặt (giỏ có thể vừa đổi ở tab khác). Có thay đổi thì dừng để khách xem lại tổng tiền mới.
  const { cart, changed } = render();
  if (cart.length === 0) return;
  if (changed) {
    errorBox.textContent = "Your cart was updated. Please check the new total and place your order again.";
    return;
  }

  const user = getCurrentUser();
  const number = "SD-" + Date.now().toString(36).toUpperCase();
  const order = {
    number, date: new Date().toISOString(), items: cart, currency,     // đúng giỏ đã dùng để tính tiền
    customer: { name: $("co-name").value.trim(), email: $("co-email").value.trim(),
      phone: $("co-phone").value.trim(), address: $("co-address").value.trim(),
      city: $("co-city").value.trim(), country: $("co-country").value },
    payment: form.pay.value,
    discountCode: discount ? discount.code : null,
    totalUsd: lastTotalUsd,
    status: "Processing",
    stockDeducted: true,                          // đơn này đã trừ kho -> admin huỷ đơn thì cộng lại (xem admin.js)
    userEmail: user ? user.email : null           // đang đăng nhập thì gắn đơn vào tài khoản (trang Account đọc lại)
  };

  // Lưu đơn + trừ kho cùng lúc: chỉ cần 1 trong 2 lỗi là không lưu gì, giữ nguyên giỏ và báo lỗi
  const orders = readList(ORDERS_KEY, isValidOrder);
  orders.push(order);
  const { overrides, stock } = stockAfter(products, cart, -1);
  if (!writeAll([[ORDERS_KEY, orders], [OVERRIDES_KEY, overrides]])) {
    errorBox.textContent = "We couldn't save your order. Your cart is unchanged, please try again.";
    return;
  }
  applyStock(products, stock);

  // Tài khoản chưa có địa chỉ thì lưu luôn địa chỉ vừa nhập, lần sau khỏi gõ lại (lỗi ở bước này không ảnh hưởng đơn hàng)
  if (user) {
    const c = order.customer;
    try {
      updateProfile({
        phone: user.phone || c.phone, address: user.address || c.address,
        city: user.city || c.city, country: user.country || c.country
      });
    } catch (err) { console.warn("Cannot update profile", err); }
  }

  saveCart([]);                                  // đơn đã lưu xong mới xoá giỏ
  notice("");
  $("order-number").textContent = number;
  $("order-email").textContent = order.customer.email;
  $("cart-content").hidden = true;
  $("order-done").hidden = false;
  updateCartCount();
  window.scrollTo({ top: 0 });
});

// ---------- Gợi ý "You may also like": mọi sản phẩm chưa có trong giỏ, xếp ngẫu nhiên, lướt ngang bằng 2 nút ----------
let suggestOrder = null;                               // thứ tự ngẫu nhiên, xáo 1 lần mỗi lần mở trang (đổi số lượng không làm đảo lại)
let suggestKey = "";                                   // nhớ bộ gợi ý đang hiện để khỏi vẽ lại ảnh mỗi lần đổi số lượng
const suggestTrack = $("suggest-grid");
// Popup sản phẩm dùng chung với trang chủ. Thêm món vào giỏ thì vẽ lại giỏ; "Buy now" chỉ cần đóng popup vì đang ở trang giỏ hàng
const productDialog = $("product-dialog");
const openProduct = initProductPopup({
  dialog: productDialog, detail: $("product-detail"),
  getCurrency: () => currency, getRates: () => rates,
  onAddToCart: () => render(),
  onBuyNow: () => productDialog.close()
});
function shuffle(arr) {                                // Fisher-Yates: xáo trộn đều
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}
function updateSuggestButtons() {                      // hết đường lướt thì làm mờ nút
  $("suggest-prev").disabled = suggestTrack.scrollLeft <= 2;
  $("suggest-next").disabled = suggestTrack.scrollLeft + suggestTrack.clientWidth >= suggestTrack.scrollWidth - 2;
}
function renderSuggest(cart) {
  if (!suggestOrder) suggestOrder = shuffle(Object.values(products).filter(canBuy));
  const inCart = new Set(cart.map((i) => i.id));
  const picks = suggestOrder.filter((p) => !inCart.has(p.id));
  $("cart-suggest").hidden = picks.length === 0;
  const key = picks.map((p) => p.id).join(",") + "|" + currency;
  if (key === suggestKey) return;
  suggestKey = key;
  // Bấm thẻ -> mở popup sản phẩm ngay trên trang giỏ hàng (đóng popup là về lại đúng chỗ đang xem)
  renderGrid(suggestTrack, picks, fmt, (p) => openProduct(p));
  suggestTrack.scrollLeft = 0;
  updateSuggestButtons();
}
// Mỗi lần bấm lướt gần hết 1 trang (còn chừa 1 phần để người dùng thấy nối tiếp)
$("suggest-prev").addEventListener("click", () => suggestTrack.scrollBy({ left: -suggestTrack.clientWidth * 0.9, behavior: "smooth" }));
$("suggest-next").addEventListener("click", () => suggestTrack.scrollBy({ left: suggestTrack.clientWidth * 0.9, behavior: "smooth" }));
suggestTrack.addEventListener("scroll", updateSuggestButtons, { passive: true });
window.addEventListener("resize", updateSuggestButtons);

// ---------- Mã giảm giá của athlete (giảm 10%) ----------
const DISCOUNT_PCT = 10;
const discountForm = $("discount-form");
const discountInput = $("discount-code");
const discountBtn = $("discount-btn");
const discountMsg = $("discount-msg");

discountForm.addEventListener("submit", (e) => {
  e.preventDefault();
  if (discount) {                       // đang áp mã -> bấm để gỡ
    discount = null;
    discountInput.value = "";
    discountInput.readOnly = false;
    discountBtn.textContent = "Apply";
    discountMsg.textContent = "";
    render();
    return;
  }
  const code = discountInput.value.trim();
  const athlete = athletes.find((a) => a.active && a.code.toLowerCase() === code.toLowerCase());
  if (!code) { discountMsg.textContent = "Enter a code first."; discountMsg.className = "discount__msg is-error"; return; }
  if (!athlete) { discountMsg.textContent = "This code is not valid."; discountMsg.className = "discount__msg is-error"; return; }
  discount = { code: athlete.code, pct: DISCOUNT_PCT, athlete: athlete.name };
  discountInput.readOnly = true;
  discountBtn.textContent = "Remove";
  discountMsg.textContent = DISCOUNT_PCT + "% off applied with " + athlete.name + "'s code.";
  discountMsg.className = "discount__msg is-ok";
  render();
});

// ---------- Khởi động ----------
REGIONS.forEach((r) => {
  $("co-country").add(new Option(r.name, r.name));
});
$("co-country").value = (REGIONS.find((r) => r.code === currency) || REGIONS[0]).name;
// Đổi Country trong form thì tiền tệ đổi theo (và được lưu cho các trang khác)
$("co-country").addEventListener("change", () => {
  const region = REGIONS.find((r) => r.name === $("co-country").value);
  if (region) {
    currency = region.code;
    saveCurrency(currency);
  }
  render();
});
// ---------- Tài khoản: tự điền form Checkout ----------
// Chỉ điền vào ô còn trống, không ghi đè thứ người dùng đã gõ
function fillFromAccount() {
  const user = getCurrentUser();
  $("checkout-signin").hidden = Boolean(user);
  if (!user) return;
  const map = { "co-name": user.name, "co-email": user.email, "co-phone": user.phone, "co-address": user.address, "co-city": user.city };
  Object.keys(map).forEach((id) => { if (!$(id).value && map[id]) $(id).value = map[id]; });
  // Nước trong tài khoản: chọn sẵn và đổi tiền tệ/phí ship theo (dùng lại sự kiện change của ô Country)
  if (user.country && REGIONS.some((r) => r.name === user.country) && $("co-country").value !== user.country) {
    $("co-country").value = user.country;
    $("co-country").dispatchEvent(new Event("change"));
  }
}
$("checkout-signin-btn").addEventListener("click", () => openAuth("signin"));
window.addEventListener("auth-change", fillFromAccount);

// Tải dữ liệu. Lỗi thì hiện thông báo lỗi + nút "Try again" (không giả làm "giỏ trống")
function loadData() {
  $("cart-error").hidden = true;
  const loadAccess = fetch("../data/access.json").then((r) => {
    if (!r.ok) throw new Error("Cannot load access list");
    return r.json();
  });
  Promise.all([loadProducts(), loadRates(), loadShipping(), loadAccess])
    .then(([items, rateInfo, shipping, access]) => {
      athletes = access.influencers || [];
      shippingData = shipping;
      products = {};
      items.forEach((p) => { products[p.id] = p; });
      rates = rateInfo.rates;
      loaded = true;
      render();
      fillFromAccount();
    })
    .catch((err) => { $("cart-error").hidden = false; console.error(err); });
}
$("cart-retry").addEventListener("click", loadData);
loadData();
