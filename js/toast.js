// Popup thông báo nhỏ (toast): hiện ở góc trên màn hình khi làm xong một việc
// (đặt hàng, đăng nhập, tạo tài khoản, gửi tin nhắn) rồi tự biến mất sau vài giây.
// Dùng: import { showToast } from "./toast.js";  showToast("Order placed", "Thank you...");

let box = null;   // khung chứa các toast, tạo 1 lần cho cả trang

function getBox() {
  if (!box) {
    box = document.createElement("div");
    box.className = "toast-box";
    // role="status" + aria-live: trình đọc màn hình sẽ tự đọc nội dung toast mới
    box.setAttribute("role", "status");
    box.setAttribute("aria-live", "polite");
    document.body.appendChild(box);
  }
  return box;
}

// Tạo 1 toast. ms = thời gian hiển thị (mặc định 2.5 giây)
export function showToast(title, text = "", ms = 2500) {
  const toast = document.createElement("div");
  toast.className = "toast";
  // Dùng textContent (không dùng innerHTML) cho chữ để tránh chèn mã HTML lạ
  toast.innerHTML = `
    <svg class="toast__icon" width="28" height="28" viewBox="0 0 28 28" fill="none" aria-hidden="true">
      <circle cx="14" cy="14" r="13" stroke="currentColor" stroke-width="1.5"/>
      <path d="M8.5 14.5l3.5 3.5 7.5-8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    <div class="toast__content"><strong class="toast__title"></strong><p class="toast__text"></p></div>`;
  toast.querySelector(".toast__title").textContent = title;
  toast.querySelector(".toast__text").textContent = text;
  getBox().appendChild(toast);

  // Hết giờ: thêm class để chạy hiệu ứng mờ dần, rồi xoá khỏi DOM
  setTimeout(() => {
    toast.classList.add("toast--hide");
    setTimeout(() => toast.remove(), 300);   // 300ms = thời gian hiệu ứng trong CSS
  }, ms);
  return toast;
}
