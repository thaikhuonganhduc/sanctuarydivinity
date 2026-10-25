// Guard: đặt ở mọi trang bên trong. Chưa nhập mật khẩu -> đá về cổng index.html.
import { ROLE_KEY, PAGES } from "./config.js";

export function getRole() {
  return sessionStorage.getItem(ROLE_KEY); // null nếu chưa qua cổng
}

// requiredRole = "admin" nếu trang chỉ dành cho admin
export function requireAccess(requiredRole) {
  const role = getRole();
  if (!role || (requiredRole === "admin" && role !== "admin")) {
    window.location.replace(PAGES.gate);
  }
}

export function logout() {
  sessionStorage.removeItem(ROLE_KEY);
  window.location.replace(PAGES.gate);
}
