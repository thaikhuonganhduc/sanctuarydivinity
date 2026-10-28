// Header dùng chung: hiện số món trong giỏ cạnh chữ "Cart", ví dụ "Cart (3)"
import { getCart } from "./cart.js";
import { logout } from "./guard.js";
import { initAccountUI } from "./auth-ui.js";

export function updateCartCount() {
  const total = getCart().reduce((sum, item) => sum + item.qty, 0);

  // Trang chủ: giỏ hàng là icon, số món hiện ở huy hiệu nhỏ
  const badge = document.querySelector(".cart-badge");
  if (badge) {
    badge.textContent = String(total);
    badge.hidden = total === 0;
    badge.closest("a").setAttribute("aria-label", total > 0 ? "Cart, " + total + " items" : "Cart");
    return;
  }

  // Các trang khác: chữ "Cart (n)" trên menu
  const link = document.querySelector('.site-nav a[href="cart.html"]');
  if (!link) return;
  link.textContent = total > 0 ? "Cart (" + total + ")" : "Cart";
}
updateCartCount();
// Giỏ đổi (thêm từ popup sản phẩm, sửa ở trang Cart...) thì cập nhật số ngay, không cần tải lại trang
window.addEventListener("cart-change", updateCartCount);
// Giỏ đổi ở tab khác của cùng trình duyệt: sự kiện "storage" chỉ báo cho các tab còn lại
window.addEventListener("storage", (e) => { if (e.key === "sanctuary_cart") updateCartCount(); });
initAccountUI();   // icon tài khoản + popup đăng nhập (js/auth-ui.js)

// Nút Exit (trang chủ): xoá vai trò đã đăng nhập rồi quay về trang nhập mật khẩu
const exitBtn = document.getElementById("exit-btn");
if (exitBtn) exitBtn.addEventListener("click", logout);

// Header trang chủ được ghim cố định: cuộn xuống quá 40px thì đổi sang nền kính mờ và thu nhỏ logo
const pinnedHeader = document.querySelector(".site-header--pinned");
if (pinnedHeader) {
  const updatePinned = () => pinnedHeader.classList.toggle("is-scrolled", window.scrollY > 40);
  window.addEventListener("scroll", updatePinned, { passive: true });
  updatePinned();
}
