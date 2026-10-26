// Cấu hình chung của website.
// Lưu ý: web tĩnh (không backend) nên MỌI thứ trong file JS đều xem được bằng F12.
// Vì vậy mã admin chỉ lưu dạng hash SHA-256, không lưu chữ thô.
// Mã admin tạm hiện tại: SANCTUARY-ADMIN-2026  -> HÃY ĐỔI trước khi nộp bài.
// Cách tạo hash mới (PowerShell):
//   $h=[Security.Cryptography.SHA256]::Create().ComputeHash([Text.Encoding]::UTF8.GetBytes("MÃ_MỚI")); ($h|%{$_.ToString("x2")}) -join ""
export const ADMIN_CODE_HASH = "fc7e67d62ceb2b7133d3126a7bde80565ac7ed7b807e5caa44805d54cc3996f1";

export const ROLE_KEY = "sanctuary_role";   // lưu vai trò trong sessionStorage: "customer" | "admin"
export const PAGES = {
  gate: "/",   // trang cổng: trên Vercel "/" tự chuyển sang /password (xem vercel.json)
  home: "/pages/home.html",
  admin: "/pages/admin.html",
};
