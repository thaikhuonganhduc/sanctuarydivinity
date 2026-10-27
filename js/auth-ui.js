// Giao diện tài khoản dùng chung cho mọi trang:
//  - Icon người trên header (cạnh icon giỏ hàng). Chưa đăng nhập: bấm mở popup. Đã đăng nhập: sang trang Account.
//  - Popup 2 tab: Sign in / Create account, kiểm tra dữ liệu bằng form-validate.js.
// Đăng nhập/đăng xuất xong sẽ phát sự kiện "auth-change" để trang đang mở tự cập nhật (vd: Checkout tự điền thông tin).
import { register, login, getCurrentUser } from "./auth.js";
import { rules, validateForm, liveValidate } from "./form-validate.js";

let dialog = null;
let accountLink = null;

// Khung popup: chỉ là HTML tĩnh (không chứa dữ liệu người dùng) nên viết bằng template cho dễ đọc
const TEMPLATE = `
  <div class="glass auth-box">
    <button type="button" class="review-detail__close" data-close aria-label="Close">×</button>
    <div class="auth-tabs" role="tablist">
      <button type="button" role="tab" id="tab-signin" aria-controls="auth-signin" aria-selected="true">Sign in</button>
      <button type="button" role="tab" id="tab-register" aria-controls="auth-register" aria-selected="false">Create account</button>
    </div>

    <form id="auth-signin" class="form" role="tabpanel" aria-labelledby="tab-signin" novalidate>
      <div class="field"><label for="si-email">Email</label>
        <input id="si-email" class="input" type="email" autocomplete="email">
        <p class="form-error" id="error-si-email"></p></div>
      <div class="field"><label for="si-password">Password</label>
        <input id="si-password" class="input" type="password" autocomplete="current-password">
        <p class="form-error" id="error-si-password"></p></div>
      <p class="form-error auth-message" role="alert"></p>
      <button type="submit" class="btn">Sign in</button>
    </form>

    <form id="auth-register" class="form" role="tabpanel" aria-labelledby="tab-register" novalidate hidden>
      <div class="field"><label for="ru-name">Full name</label>
        <input id="ru-name" class="input" type="text" autocomplete="name">
        <p class="form-error" id="error-ru-name"></p></div>
      <div class="field"><label for="ru-email">Email</label>
        <input id="ru-email" class="input" type="email" autocomplete="email">
        <p class="form-error" id="error-ru-email"></p></div>
      <div class="field"><label for="ru-password">Password</label>
        <input id="ru-password" class="input" type="password" autocomplete="new-password">
        <p class="form-error" id="error-ru-password"></p></div>
      <div class="field"><label for="ru-confirm">Confirm password</label>
        <input id="ru-confirm" class="input" type="password" autocomplete="new-password">
        <p class="form-error" id="error-ru-confirm"></p></div>
      <p class="form-error auth-message" role="alert"></p>
      <button type="submit" class="btn">Create account</button>
      <p class="cart-note">Demo account: saved only in this browser.</p>
    </form>
  </div>`;

const ICON = `<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">
  <circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/></svg>`;

// Chuyển tab Sign in <-> Create account
function showTab(name) {
  const isSignIn = name === "signin";
  dialog.querySelector("#tab-signin").setAttribute("aria-selected", String(isSignIn));
  dialog.querySelector("#tab-register").setAttribute("aria-selected", String(!isSignIn));
  dialog.querySelector("#auth-signin").hidden = !isSignIn;
  dialog.querySelector("#auth-register").hidden = isSignIn;
  dialog.querySelectorAll(".auth-message").forEach((m) => { m.textContent = ""; });
}

// Mở popup (các trang khác gọi được, vd: trang Account khi chưa đăng nhập)
export function openAuth(tab = "signin") {
  if (!dialog) buildDialog();
  showTab(tab);
  dialog.showModal();
  dialog.querySelector(tab === "signin" ? "#si-email" : "#ru-name").focus();
}

// Đăng nhập/đăng ký xong: đóng popup, cập nhật icon, báo cho trang biết
function onSignedIn() {
  dialog.close();
  dialog.querySelectorAll("form").forEach((f) => f.reset());
  updateAccountIcon();
  window.dispatchEvent(new CustomEvent("auth-change"));
}

function buildDialog() {
  dialog = document.createElement("dialog");
  dialog.className = "review-dialog auth-dialog";
  dialog.setAttribute("aria-label", "Account");
  dialog.innerHTML = TEMPLATE;
  document.body.appendChild(dialog);

  // Đóng: nút ×, hoặc bấm ra ngoài khung (Esc thì <dialog> tự đóng)
  dialog.querySelector("[data-close]").addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", (e) => { if (e.target === dialog) dialog.close(); });
  dialog.querySelector("#tab-signin").addEventListener("click", () => showTab("signin"));
  dialog.querySelector("#tab-register").addEventListener("click", () => showTab("register"));

  // ---- Form đăng nhập ----
  const signinForm = dialog.querySelector("#auth-signin");
  const signinRules = { "si-email": [rules.required, rules.email], "si-password": [rules.required] };
  liveValidate(signinForm, signinRules);
  signinForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = signinForm.querySelector(".auth-message");
    message.textContent = "";
    if (!validateForm(signinForm, signinRules)) return;
    try {
      await login(signinForm.querySelector("#si-email").value, signinForm.querySelector("#si-password").value);
      onSignedIn();
    } catch (err) {
      message.textContent = err.message;
    }
  });

  // ---- Form đăng ký ----
  const registerForm = dialog.querySelector("#auth-register");
  const password = registerForm.querySelector("#ru-password");
  const registerRules = {
    "ru-name": [rules.required, rules.minLength(2)],
    "ru-email": [rules.required, rules.email],
    // Mật khẩu: ít nhất 8 ký tự, có cả chữ và số
    "ru-password": [rules.required, rules.minLength(8), (v) => (/[a-z]/i.test(v) && /\d/.test(v)) || "Use both letters and numbers."],
    "ru-confirm": [rules.required, (v) => v === password.value || "Passwords do not match."]
  };
  liveValidate(registerForm, registerRules);
  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = registerForm.querySelector(".auth-message");
    message.textContent = "";
    if (!validateForm(registerForm, registerRules)) return;
    try {
      await register({
        name: registerForm.querySelector("#ru-name").value,
        email: registerForm.querySelector("#ru-email").value,
        password: password.value
      });
      onSignedIn();
    } catch (err) {
      message.textContent = err.message;
    }
  });
}

// Icon người: đã đăng nhập thì có chấm nhỏ và nhãn ghi tên
export function updateAccountIcon() {
  if (!accountLink) return;
  const user = getCurrentUser();
  accountLink.classList.toggle("is-signed-in", Boolean(user));
  accountLink.setAttribute("aria-label", user ? "Account, signed in as " + user.name : "Sign in");
  accountLink.title = user ? user.name : "Sign in";
}

// Gắn icon vào header (trang nào chưa có nhóm .header-tools thì tạo mới)
export function initAccountUI() {
  const header = document.querySelector(".site-header");
  if (!header) return;
  let tools = header.querySelector(".header-tools");
  if (!tools) {
    tools = document.createElement("div");
    tools.className = "header-tools";
    header.appendChild(tools);
  }
  accountLink = document.createElement("a");
  accountLink.href = "account.html";
  accountLink.className = "cart-link account-link";
  accountLink.innerHTML = ICON;
  accountLink.addEventListener("click", (e) => {
    if (getCurrentUser()) return;            // đã đăng nhập: đi tới trang Account như link bình thường
    e.preventDefault();
    openAuth("signin");
  });
  tools.prepend(accountLink);                // nằm bên trái icon giỏ hàng
  updateAccountIcon();
  window.addEventListener("auth-change", updateAccountIcon);
}
