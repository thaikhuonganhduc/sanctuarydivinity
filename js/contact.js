// Form liên hệ: kiểm tra bằng JavaScript rồi lưu tin nhắn giả lập vào localStorage
// (web không có backend nên chưa gửi email thật; sau này admin có thể đọc danh sách này).
import { rules, validateForm, liveValidate } from "./form-validate.js";

const MESSAGES_KEY = "sanctuary_messages";
const form = document.getElementById("contact-form");
const success = document.getElementById("contact-success");

const ruleMap = {
  "ct-name": [rules.required, rules.minLength(2)],
  "ct-email": [rules.required, rules.email],
  "ct-message": [rules.required, rules.minLength(10)]
};
liveValidate(form, ruleMap);

form.addEventListener("submit", (e) => {
  e.preventDefault();
  success.hidden = true;
  if (!validateForm(form, ruleMap)) return;

  const message = {
    date: new Date().toISOString(),
    name: form.querySelector("#ct-name").value.trim(),
    email: form.querySelector("#ct-email").value.trim(),
    topic: form.querySelector("#ct-topic").value,
    message: form.querySelector("#ct-message").value.trim()
  };
  try {
    const all = JSON.parse(localStorage.getItem(MESSAGES_KEY)) || [];
    all.push(message);
    localStorage.setItem(MESSAGES_KEY, JSON.stringify(all));
  } catch (err) { console.warn("Cannot save message", err); }

  form.reset();
  success.hidden = false;
});
