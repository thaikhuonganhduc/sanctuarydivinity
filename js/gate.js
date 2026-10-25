// Xử lý cổng nhập mật khẩu:
//  - Mã admin (so hash)  -> vai trò admin
//  - Mật khẩu influencer (đọc từ data/access.json bằng fetch) -> vai trò customer
import { ADMIN_CODE_HASH, ROLE_KEY, PAGES } from "./config.js";

import { startCountdown, showLaunchDate } from "./countdown.js";

startCountdown(document.getElementById("countdown"));
showLaunchDate(document.getElementById("launch-date"));

// Bấm nút góc phải để mở/đóng hộp nhập mật khẩu
const toggleBtn = document.getElementById("gate-toggle");
const dialog = document.getElementById("gate-dialog");
toggleBtn.addEventListener("click", () => {
  dialog.hidden = !dialog.hidden;
  toggleBtn.setAttribute("aria-expanded", String(!dialog.hidden));
  if (!dialog.hidden) document.getElementById("gate-password").focus();
});

const form = document.getElementById("gate-form");
const input = document.getElementById("gate-password");
const errorBox = document.getElementById("gate-error");

// Đã qua cổng rồi thì vào thẳng
const savedRole = sessionStorage.getItem(ROLE_KEY);
if (savedRole) goTo(savedRole);

// Băm chuỗi bằng SHA-256, trả về chuỗi hex
async function sha256(text) {
  const bytes = new TextEncoder().encode(text);
  const hash = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(hash)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function goTo(role) {
  window.location.replace(role === "admin" ? PAGES.admin : PAGES.home);
}

// Lấy danh sách mật khẩu influencer từ JSON
async function loadInfluencerCodes() {
  const res = await fetch("data/access.json");
  if (!res.ok) throw new Error("Cannot load access list");
  const data = await res.json();
  return data.influencers.filter((i) => i.active);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorBox.textContent = "";
  const code = input.value.trim();

  if (!code) {
    errorBox.textContent = "Please enter a password.";
    return;
  }

  try {
    // 1. Thử mã admin trước
    if ((await sha256(code)) === ADMIN_CODE_HASH) {
      sessionStorage.setItem(ROLE_KEY, "admin");
      goTo("admin");
      return;
    }

    // 2. Thử mật khẩu influencer (không phân biệt hoa thường)
    const influencers = await loadInfluencerCodes();
    const match = influencers.find((i) => i.code.toLowerCase() === code.toLowerCase());
    if (match) {
      sessionStorage.setItem(ROLE_KEY, "customer");
      sessionStorage.setItem("sanctuary_source", match.name); // biết khách đến từ influencer nào
      goTo("customer");
      return;
    }

    errorBox.textContent = "Incorrect password.";
  } catch (err) {
    errorBox.textContent = "Something went wrong. Please try again.";
    console.error(err);
  }
});
