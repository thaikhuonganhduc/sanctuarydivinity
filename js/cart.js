// Giỏ hàng lưu trong localStorage (key "sanctuary_cart"): mảng { id, color, size, qty }
const CART_KEY = "sanctuary_cart";

export function getCart() {
  try { return JSON.parse(localStorage.getItem(CART_KEY)) || []; } catch (e) { return []; }
}

export function saveCart(cart) {
  try { localStorage.setItem(CART_KEY, JSON.stringify(cart)); } catch (e) { /* bỏ qua */ }
}

// Thêm 1 sản phẩm: nếu đã có cùng mẫu + màu + size thì chỉ tăng số lượng
export function addToCart(id, color, size, qty = 1) {
  const cart = getCart();
  const found = cart.find((i) => i.id === id && i.color === color && i.size === size);
  if (found) found.qty += qty;
  else cart.push({ id, color, size, qty });
  saveCart(cart);
}
