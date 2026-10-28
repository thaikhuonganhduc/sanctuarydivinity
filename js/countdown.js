// Đồng hồ đếm ngược đến ngày mở bán (drop).
// Ngày mặc định cố định cho MỌI người xem: 00:00 ngày 01/12/2026 giờ Việt Nam (UTC+7).
// Admin đổi ngày ở trang Admin -> Launch date: giá trị đó lưu trong localStorage (chỉ trình duyệt đó thấy)
// và được ưu tiên hơn mặc định.
const LAUNCH_KEY = "sanctuary_launch_override";
export const DEFAULT_LAUNCH = new Date("2026-12-01T00:00:00+07:00").getTime();
const TIME_ZONE = "Asia/Ho_Chi_Minh";
const VN_OFFSET_MS = 7 * 60 * 60 * 1000;   // Việt Nam luôn là UTC+7 (không đổi giờ mùa hè)

// Ngày admin đã đặt (số mili giây), hoặc null nếu chưa đặt / dữ liệu hỏng
function savedLaunch() {
  try {
    const raw = localStorage.getItem(LAUNCH_KEY);
    const saved = Number(raw);
    return raw !== null && Number.isFinite(saved) && saved > 0 ? saved : null;
  } catch (e) { return null; }
}

export function getLaunchDate() {
  return savedLaunch() ?? DEFAULT_LAUNCH;
}

// Admin đã đổi ngày chưa (để trang admin ghi "Set by admin" hay "Default")
export function isLaunchOverridden() {
  return savedLaunch() !== null;
}

// Admin đổi ngày mở bán; trả về true nếu lưu được
export function setLaunchDate(timestamp) {
  try { localStorage.setItem(LAUNCH_KEY, String(timestamp)); return true; } catch (e) { return false; }
}

// Admin quay về ngày mặc định
export function resetLaunchDate() {
  try { localStorage.removeItem(LAUNCH_KEY); return true; } catch (e) { return false; }
}

// Đổi qua lại giữa mốc thời gian và giá trị của ô <input type="datetime-local"> ("2026-12-01T00:00"),
// luôn hiểu theo giờ Việt Nam để admin ở đâu cũng đặt đúng giờ drop.
export function toVietnamInput(timestamp) {
  return new Date(timestamp + VN_OFFSET_MS).toISOString().slice(0, 16);
}
export function fromVietnamInput(value) {
  if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/.test(value)) return null;
  const time = new Date(value + ":00+07:00").getTime();
  return Number.isFinite(time) ? time : null;
}

// Ngày giờ đầy đủ theo giờ Việt Nam, ví dụ "01 Dec 2026, 00:00"
export function formatLaunch(timestamp) {
  return new Intl.DateTimeFormat("en-GB", {
    timeZone: TIME_ZONE, day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit", hour12: false
  }).format(new Date(timestamp));
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
