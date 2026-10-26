// Header dùng chung: hiện số món trong giỏ cạnh chữ "Cart", ví dụ "Cart (3)"
import { getCart } from "./cart.js";
import { logout } from "./guard.js";

export function updateCartCount() {
  const link = document.querySelector('.site-nav a[href="cart.html"]');
  if (!link) return;
  const total = getCart().reduce((sum, item) => sum + item.qty, 0);
  link.textContent = total > 0 ? "Cart (" + total + ")" : "Cart";
}
updateCartCount();

// Nút Exit (trang chủ): xoá vai trò đã đăng nhập rồi quay về trang nhập mật khẩu
const exitBtn = document.getElementById("exit-btn");
if (exitBtn) exitBtn.addEventListener("click", logout);
