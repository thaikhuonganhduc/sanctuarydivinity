// Form liên hệ: kiểm tra bằng JavaScript rồi lưu tin nhắn giả lập vào localStorage
// (web không có backend nên chưa gửi email thật; admin đọc danh sách này ở trang Admin).
import { rules, validateForm, liveValidate } from "./form-validate.js";
import { readList, writeJSON, isValidMessage } from "./storage.js";
import { getCurrentUser } from "./auth.js";

const MESSAGES_KEY = "sanctuary_messages";
const form = document.getElementById("contact-form");
const success = document.getElementById("contact-success");
const errorBox = document.getElementById("contact-error");
const messageBox = document.getElementById("ct-message");
const counter = document.getElementById("ct-count");

// Khách đã đăng nhập: điền sẵn tên + email từ tài khoản (vẫn sửa được)
function prefill() {
  const user = getCurrentUser();
  if (!user) return;
  const name = form.querySelector("#ct-name");
  const email = form.querySelector("#ct-email");
  if (!name.value) name.value = user.name;
  if (!email.value) email.value = user.email;
}
prefill();
window.addEventListener("auth-change", prefill);   // đăng nhập ngay trên trang này (icon tài khoản) thì điền luôn

// Đếm ký tự của ô Message (tối đa 1000, đặt bằng maxlength trong HTML)
function updateCount() {
  counter.textContent = messageBox.value.length + " / " + messageBox.maxLength;
}
messageBox.addEventListener("input", updateCount);
// Gõ tin mới thì ẩn dòng "Message sent" của lần gửi trước
form.addEventListener("input", () => { success.hidden = true; });

const ruleMap = {
  "ct-name": [rules.required, rules.minLength(2)],
  "ct-email": [rules.required, rules.email],
  "ct-message": [rules.required, rules.minLength(10)]
};
liveValidate(form, ruleMap);

form.addEventListener("submit", (e) => {
  e.preventDefault();
  success.hidden = true;
  errorBox.textContent = "";
  if (!validateForm(form, ruleMap)) return;

  const message = {
    date: new Date().toISOString(),
    name: form.querySelector("#ct-name").value.trim(),
    email: form.querySelector("#ct-email").value.trim(),
    topic: form.querySelector("#ct-topic").value,
    message: form.querySelector("#ct-message").value.trim()
  };
  const all = readList(MESSAGES_KEY, isValidMessage);
  all.push(message);

  // Lưu lỗi thì giữ nguyên nội dung khách đã gõ và báo lỗi, không báo "đã gửi"
  if (!writeJSON(MESSAGES_KEY, all)) {
    errorBox.textContent = "We couldn't send your message. Please try again.";
    return;
  }
  form.reset();
  prefill();                                   // giữ lại tên + email của tài khoản cho lần gửi sau
  updateCount();
  success.hidden = false;
});
