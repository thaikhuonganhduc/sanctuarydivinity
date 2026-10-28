// Form liên hệ: kiểm tra bằng JavaScript rồi lưu tin nhắn giả lập vào localStorage
// (web không có backend nên chưa gửi email thật; admin đọc danh sách này ở trang Admin).
import { rules, validateForm, liveValidate } from "./form-validate.js";
import { readList, writeJSON, isValidMessage } from "./storage.js";

const MESSAGES_KEY = "sanctuary_messages";
const form = document.getElementById("contact-form");
const success = document.getElementById("contact-success");
const errorBox = document.getElementById("contact-error");

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
  success.hidden = false;
});
