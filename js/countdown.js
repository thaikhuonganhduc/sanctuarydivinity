// Đồng hồ đếm ngược đến ngày mở bán (drop).
// Ngày mặc định cố định cho MỌI người xem: 00:00 ngày 01/12/2026 giờ Việt Nam (UTC+7).
// Sau này admin có thể đổi bằng setLaunchDate(): giá trị đó lưu trong localStorage và được ưu tiên hơn mặc định.
const LAUNCH_KEY = "sanctuary_launch_override";
const DEFAULT_LAUNCH = new Date("2026-12-01T00:00:00+07:00").getTime();
const TIME_ZONE = "Asia/Ho_Chi_Minh";

export function getLaunchDate() {
  const saved = localStorage.getItem(LAUNCH_KEY);
  return saved ? Number(saved) : DEFAULT_LAUNCH;
}

// Admin dùng hàm này để đổi ngày mở bán (làm ở bước admin)
export function setLaunchDate(timestamp) {
  localStorage.setItem(LAUNCH_KEY, String(timestamp));
}

// Hiển thị ngày mở bán dạng dd/mm/yy theo giờ Việt Nam, ví dụ "01/12/26"
export function showLaunchDate(element) {
  const parts = new Intl.DateTimeFormat("en-GB", { timeZone: TIME_ZONE, day: "2-digit", month: "2-digit", year: "2-digit" })
    .formatToParts(new Date(getLaunchDate()));
  const get = (type) => parts.find((p) => p.type === type).value;
  element.textContent = get("day") + "/" + get("month") + "/" + get("year");
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
