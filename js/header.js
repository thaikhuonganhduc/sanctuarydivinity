// Header dùng chung: hiện số món trong giỏ cạnh chữ "Cart", ví dụ "Cart (3)"
import { getCart } from "./cart.js";

export function updateCartCount() {
  const link = document.querySelector('.site-nav a[href="cart.html"]');
  if (!link) return;
  const total = getCart().reduce((sum, item) => sum + item.qty, 0);
  link.textContent = total > 0 ? "Cart (" + total + ")" : "Cart";
}
updateCartCount();
