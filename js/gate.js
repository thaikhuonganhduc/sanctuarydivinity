// Xử lý cổng nhập mật khẩu:
//  - Mã admin (so hash)  -> vai trò admin
//  - Mật khẩu influencer (data/access.json, hoặc danh sách admin đã sửa, xem athletes.js) -> vai trò customer
import { ADMIN_CODE_HASH, ROLE_KEY, PAGES, SHOW_DEMO_HINTS, DEMO_ADMIN_CODE } from "./config.js";
import { loadAthletes, findActiveCode } from "./athletes.js";

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

// Lấy danh sách mật khẩu influencer đang bật
async function loadInfluencerCodes() {
  return (await loadAthletes("data/access.json")).filter((i) => i.active);
}

// ---------- Gợi ý mật khẩu để test nhanh ----------
// Hiện 2 nút "Customer" / "Admin": bấm là điền mật khẩu vào ô rồi gửi form luôn.
// Mã customer lấy từ data/access.json (mã đầu tiên đang bật), mã admin lấy từ config.js.
async function showDemoHints() {
  const box = document.getElementById("gate-demo");
  const hints = [["Admin", DEMO_ADMIN_CODE]];
  try {
    const first = (await loadInfluencerCodes())[0];
    if (first) hints.unshift(["Customer", first.code]);
  } catch (err) { console.warn("Demo hint: cannot load customer code", err); }

  box.appendChild(Object.assign(document.createElement("p"), { className: "gate-demo__title", textContent: "Test logins (click to enter)" }));
  hints.forEach(([role, code]) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "gate-demo__btn";
    const name = document.createElement("strong");
    name.textContent = role;
    btn.append(name, " " + code);
    btn.addEventListener("click", () => {
      input.value = code;
      form.requestSubmit();
    });
    box.appendChild(btn);
  });
  box.hidden = false;
}
if (SHOW_DEMO_HINTS) showDemoHints();

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
    const match = findActiveCode(await loadInfluencerCodes(), code);
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
