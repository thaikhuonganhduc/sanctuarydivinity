// Đồng hồ đếm ngược đến ngày mở bán (drop).
// Ngày mở bán lưu trong localStorage để sau này admin có thể chỉnh.
// Lần đầu chưa có -> giả lập mở bán sau 10 ngày.
const LAUNCH_KEY = "sanctuary_launch_date";
const DEFAULT_DAYS = 10;

export function getLaunchDate() {
  let saved = localStorage.getItem(LAUNCH_KEY);
  if (!saved) {
    saved = String(Date.now() + DEFAULT_DAYS * 24 * 60 * 60 * 1000);
    localStorage.setItem(LAUNCH_KEY, saved);
  }
  return Number(saved);
}

// Admin dùng hàm này để đổi ngày mở bán (làm ở bước admin)
export function setLaunchDate(timestamp) {
  localStorage.setItem(LAUNCH_KEY, String(timestamp));
}

// Hiển thị ngày mở bán dạng dd/mm/yy, ví dụ "04/11/26"
export function showLaunchDate(element) {
  const d = new Date(getLaunchDate());
  element.textContent = [d.getDate(), d.getMonth() + 1, d.getFullYear() % 100]
    .map((n) => String(n).padStart(2, "0"))
    .join("/");
}

const pad = (n) => String(n).padStart(2, "0");

// Gắn đồng hồ vào phần tử container có 4 thẻ con data-unit="days|hours|mins|secs"
export function startCountdown(container) {
  const target = getLaunchDate();
  const units = {
    days: container.querySelector('[data-unit="days"]'),
    hours: container.querySelector('[data-unit="hours"]'),
    mins: container.querySelector('[data-unit="mins"]'),
    secs: container.querySelector('[data-unit="secs"]'),
  };

  function tick() {
    const diff = Math.max(0, target - Date.now()); // ms còn lại, không để âm
    const totalSecs = Math.floor(diff / 1000);
    units.days.textContent = pad(Math.floor(totalSecs / 86400));
    units.hours.textContent = pad(Math.floor((totalSecs % 86400) / 3600));
    units.mins.textContent = pad(Math.floor((totalSecs % 3600) / 60));
    units.secs.textContent = pad(totalSecs % 60);
  }

  tick();
  setInterval(tick, 1000); // cập nhật mỗi giây
}
