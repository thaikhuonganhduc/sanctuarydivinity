// Trang giỏ hàng: đọc giỏ từ localStorage + products.json (fetch), vẽ danh sách bằng DOM,
// sửa số lượng/xoá món, tính tiền, kiểm tra form thanh toán rồi lưu đơn hàng giả lập.
import { loadShipping, calcCosts } from "./shipping.js";
import { loadProducts, createProductImage } from "./products.js";
import { getCart, saveCart } from "./cart.js";
import { REGIONS, loadRates, formatPrice, getSavedCurrency, saveCurrency } from "./currency.js";
import { rules, validateForm, liveValidate } from "./form-validate.js";
import { updateCartCount } from "./header.js";

const ORDERS_KEY = "sanctuary_orders";

const $ = (id) => document.getElementById(id);
const list = $("cart-list");
const currencySelect = $("filter-currency");
const form = $("checkout-form");

let products = {};
let discount = null;        // { code, pct } khi đã áp mã athlete
let athletes = [];          // danh sách athlete + mã lấy từ data/access.json
let shippingData = null;   // dữ liệu phí ship/thuế từ data/shipping.json
let rates = { USD: 1 };
let currency = getSavedCurrency();

const fmt = (usd) => formatPrice(usd, currency, rates);

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

// ---------- Vẽ giỏ hàng ----------
function render() {
  const cart = getCart().filter((i) => products[i.id]);   // bỏ món không còn trong dữ liệu
  const hasItems = cart.length > 0;
  $("cart-empty").hidden = hasItems || !$("order-done").hidden;
  $("cart-content").hidden = !hasItems;
  updateCartCount();
  if (!hasItems) return;

  list.replaceChildren();
  let subtotal = 0;

  cart.forEach((item) => {
    const p = products[item.id];
    subtotal += p.price * item.qty;
    const color = p.colors.find((c) => c.name === item.color) || p.colors[0];

    const media = el("div", "product-card__media cart-item__media");
    media.appendChild(createProductImage(p, color));

    const minus = el("button", "qty__btn", "−");
    const plus = el("button", "qty__btn", "+");
    minus.type = plus.type = "button";
    minus.setAttribute("aria-label", "Decrease quantity");
    plus.setAttribute("aria-label", "Increase quantity");
    minus.disabled = item.qty <= 1;
    plus.disabled = item.qty >= p.stock;             // không vượt quá số trong kho
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
  $("sum-total").textContent = fmt(subtotal - discountUsd + costs.shipping + costs.duty + costs.tax);
  $("shipping-note").textContent = "";
}

function sameItem(a, b) { return a.id === b.id && a.color === b.color && a.size === b.size; }

function changeQty(item, qty) {
  const cart = getCart();
  const found = cart.find((i) => sameItem(i, item));
  if (found) found.qty = Math.min(Math.max(qty, 1), products[item.id].stock);
  saveCart(cart);
  render();
}

function removeItem(item) {
  saveCart(getCart().filter((i) => !sameItem(i, item)));
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
  const useCard = form.pay.value === "card";
  if (!validateForm(form, useCard ? { ...baseRules, ...cardRules } : baseRules)) return;

  // Lưu đơn hàng giả lập vào localStorage (sau này admin có thể xem)
  const number = "SD-" + Date.now().toString(36).toUpperCase();
  const order = {
    number, date: new Date().toISOString(), items: getCart(), currency,
    customer: { name: $("co-name").value.trim(), email: $("co-email").value.trim(),
      phone: $("co-phone").value.trim(), address: $("co-address").value.trim(),
      city: $("co-city").value.trim(), country: $("co-country").value },
    payment: form.pay.value,
    discountCode: discount ? discount.code : null
  };
  try {
    const orders = JSON.parse(localStorage.getItem(ORDERS_KEY)) || [];
    orders.push(order);
    localStorage.setItem(ORDERS_KEY, JSON.stringify(orders));
  } catch (err) { console.warn("Cannot save order", err); }

  saveCart([]);                                  // xoá giỏ sau khi đặt
  $("order-number").textContent = number;
  $("order-email").textContent = order.customer.email;
  $("cart-content").hidden = true;
  $("order-done").hidden = false;
  updateCartCount();
  window.scrollTo({ top: 0 });
});

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
  currencySelect.add(new Option(r.name + " (" + r.code + ")", r.code));
  $("co-country").add(new Option(r.name, r.name));
});
currencySelect.value = currency;
$("co-country").value = (REGIONS.find((r) => r.code === currency) || REGIONS[0]).name;
// Liên kết 2 chiều: đổi Country trong form thì tiền tệ ở góc trên đổi theo, và ngược lại
$("co-country").addEventListener("change", () => {
  const region = REGIONS.find((r) => r.name === $("co-country").value);
  if (region) {
    currency = region.code;
    currencySelect.value = currency;
    saveCurrency(currency);
  }
  render();
});
currencySelect.addEventListener("change", () => {
  currency = currencySelect.value;
  const region = REGIONS.find((r) => r.code === currency);
  if (region) $("co-country").value = region.name;
  saveCurrency(currency);
  render();
});

Promise.all([loadProducts(), loadRates(), loadShipping(), fetch("../data/access.json").then((r) => r.json())])
  .then(([items, rateInfo, shipping, access]) => {
    athletes = access.influencers || [];
    shippingData = shipping;
    items.forEach((p) => { products[p.id] = p; });
    rates = rateInfo.rates;
    render();
  })
  .catch((err) => { $("cart-empty").hidden = false; console.error(err); });
