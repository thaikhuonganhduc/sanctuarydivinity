// Kiểm tra dữ liệu form bằng JavaScript (dùng cho trang Cart/Checkout và Contact).
// Mỗi ô nhập có id="x" và 1 thẻ <p class="form-error" id="error-x"> bên dưới để hiện lỗi.

// Mỗi hàm kiểm tra trả về true nếu hợp lệ, hoặc chuỗi thông báo lỗi
export const rules = {
  required: (v) => v.trim() !== "" || "This field is required.",
  email: (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()) || "Enter a valid email address.",
  // SĐT: chỉ gồm chữ số, khoảng trắng, dấu "-" (có thể có "+" ở đầu) và phải có 8-15 CHỮ SỐ
  // (đếm chữ số riêng, để chuỗi toàn dấu "--------" không lọt qua)
  phone: (v) => {
    const text = v.trim();
    const digits = text.replace(/\D/g, "").length;
    return (/^\+?[\d\s-]+$/.test(text) && digits >= 8 && digits <= 15) || "Enter a valid phone number.";
  },
  minLength: (n) => (v) => v.trim().length >= n || "Please enter at least " + n + " characters.",
  // Số thẻ: 13-19 chữ số và đúng thuật toán Luhn
  card: (v) => {
    const digits = v.replace(/\s/g, "");
    if (!/^\d{13,19}$/.test(digits)) return "Enter a valid card number.";
    let sum = 0;
    for (let i = 0; i < digits.length; i++) {
      let d = Number(digits[digits.length - 1 - i]);
      if (i % 2 === 1) { d *= 2; if (d > 9) d -= 9; }
      sum += d;
    }
    return sum % 10 === 0 || "Enter a valid card number.";
  },
  // Hạn thẻ dạng MM/YY, chưa hết hạn
  expiry: (v) => {
    const m = /^(\d{2})\/(\d{2})$/.exec(v.trim());
    if (!m || Number(m[1]) < 1 || Number(m[1]) > 12) return "Use the format MM/YY.";
    const end = new Date(2000 + Number(m[2]), Number(m[1]), 1); // đầu tháng sau
    return end > new Date() || "This card has expired.";
  },
  cvc: (v) => /^\d{3,4}$/.test(v.trim()) || "Enter the 3 or 4 digit code."
};

// Kiểm tra 1 ô: hiện lỗi dưới ô, trả về true/false
export function validateField(input, fieldRules) {
  let result = true;
  for (const rule of fieldRules) {
    result = rule(input.value);
    if (result !== true) break;
  }
  const box = document.getElementById("error-" + input.id);
  if (box) box.textContent = result === true ? "" : result;
  input.setAttribute("aria-invalid", String(result !== true));
  return result === true;
}

// Kiểm tra cả form theo bảng { idÔ: [các luật] }; focus vào ô lỗi đầu tiên
export function validateForm(form, ruleMap) {
  let firstBad = null;
  Object.keys(ruleMap).forEach((id) => {
    const input = form.querySelector("#" + id);
    if (!input || input.closest("[hidden]")) return;     // bỏ qua ô đang ẩn (vd: thẻ khi chọn COD)
    if (!validateField(input, ruleMap[id]) && !firstBad) firstBad = input;
  });
  if (firstBad) firstBad.focus();
  return !firstBad;
}

// Kiểm tra từng ô ngay khi người dùng rời khỏi ô đó
export function liveValidate(form, ruleMap) {
  Object.keys(ruleMap).forEach((id) => {
    const input = form.querySelector("#" + id);
    if (input) input.addEventListener("blur", () => validateField(input, ruleMap[id]));
  });
}
