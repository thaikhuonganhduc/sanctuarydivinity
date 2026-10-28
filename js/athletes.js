// Mã athlete: vừa là mật khẩu vào web (trang cổng), vừa là mã giảm 10% ở giỏ hàng.
// Danh sách gốc nằm trong data/access.json. Khi admin thêm / bật-tắt / xoá mã (trang Admin → Athlete codes),
// cả danh sách mới được lưu vào localStorage và dùng THAY cho file gốc. Xoá key này (nút Reset) là quay về file gốc.
import { readList, writeJSON, isValidAthlete } from "./storage.js";

export const ATHLETES_KEY = "sanctuary_athletes";

// Danh sách admin đã lưu; null nếu admin chưa sửa gì (khi đó dùng data/access.json)
export function getSavedAthletes() {
  if (localStorage.getItem(ATHLETES_KEY) === null) return null;
  return readList(ATHLETES_KEY, isValidAthlete);
}

export function saveAthletes(list) {
  return writeJSON(ATHLETES_KEY, list);
}

// url: đường dẫn tới access.json, khác nhau tuỳ trang (trang cổng ở gốc: "data/access.json", trang trong pages/: "../data/access.json")
export async function loadAthletes(url) {
  const saved = getSavedAthletes();
  if (saved) return saved;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Cannot load access list");
  const data = await res.json();
  return (data.influencers || []).filter(isValidAthlete);
}

// Tìm mã đang bật (không phân biệt hoa thường); không có thì trả về undefined
export function findActiveCode(athletes, code) {
  return athletes.find((a) => a.active && a.code.toLowerCase() === code.trim().toLowerCase());
}
