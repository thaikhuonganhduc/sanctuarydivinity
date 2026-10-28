// Đọc/ghi dữ liệu trong localStorage an toàn, dùng chung cho mọi trang.
// Dữ liệu trong localStorage có thể bị sửa tay (F12) hoặc bị hỏng: JSON sai cú pháp, hoặc đúng cú pháp nhưng sai kiểu
// (vd: cần mảng mà lại là {}). Khi đó .find / .filter / .reduce sẽ báo lỗi và làm hỏng cả trang,
// nên mọi chỗ đọc đều đi qua đây: sai kiểu thì trả về giá trị rỗng, bản ghi sai cấu trúc thì bỏ qua.

export const isObject = (x) => x !== null && typeof x === "object" && !Array.isArray(x);
const isText = (x) => typeof x === "string";
const isPositiveInt = (x) => Number.isInteger(x) && x > 0;

// ---------- Kiểm tra cấu trúc từng loại bản ghi (chỉ các trường mà web thật sự dùng tới) ----------
export function isValidCartItem(i) {
  return isObject(i) && isText(i.id) && isText(i.color) && isText(i.size) && isPositiveInt(i.qty);
}
export function isValidOrder(o) {
  return isObject(o) && isText(o.number) && isText(o.date)
    && isObject(o.customer) && isText(o.customer.name) && isText(o.customer.email)
    && Array.isArray(o.items) && o.items.every((i) => isObject(i) && isText(i.id) && isPositiveInt(i.qty));
}
export function isValidUser(u) {
  return isObject(u) && isText(u.name) && isText(u.email) && isText(u.salt) && isText(u.passwordHash);
}
export function isValidMessage(m) {
  return isObject(m) && isText(m.name) && isText(m.email) && isText(m.message) && isText(m.date);
}
export function isValidAthlete(a) {
  return isObject(a) && isText(a.name) && isText(a.code) && a.code.trim() !== "" && typeof a.active === "boolean";
}
// Sản phẩm admin tự thêm: cần đủ các trường mà thẻ sản phẩm, popup và giỏ hàng dùng tới
export function isValidProduct(p) {
  return isObject(p) && isText(p.id) && isText(p.name) && isText(p.category) && isText(p.gender)
    && typeof p.price === "number" && p.price > 0 && Number.isInteger(p.stock) && p.stock >= 0
    && Array.isArray(p.sizes) && p.sizes.length > 0 && p.sizes.every(isText)
    && Array.isArray(p.colors) && p.colors.length > 0
    && p.colors.every((c) => isObject(c) && isText(c.name) && isText(c.hex) && Array.isArray(c.images) && c.images.every(isText));
}

// ---------- Đọc ----------
function readRaw(key) {
  try { return JSON.parse(localStorage.getItem(key)); } catch (e) { return null; }
}

// Đọc 1 danh sách: không phải mảng -> []; phần tử sai cấu trúc -> bỏ qua
export function readList(key, isValid = isObject) {
  const value = readRaw(key);
  return Array.isArray(value) ? value.filter(isValid) : [];
}

// Đọc 1 object dạng { khoá: object }: không phải object -> {}; giá trị không phải object -> bỏ qua
export function readMap(key) {
  const value = readRaw(key);
  if (!isObject(value)) return {};
  return Object.fromEntries(Object.entries(value).filter(([, v]) => isObject(v)));
}

// ---------- Ghi ----------
// Trả về true nếu lưu được, false nếu lỗi (vd: bộ nhớ đầy hoặc trình duyệt chặn lưu trữ)
export function writeJSON(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch (e) {
    console.warn("Cannot save " + key, e);
    return false;
  }
}

// Ghi nhiều key "cùng lúc": nếu 1 key lỗi thì trả lại giá trị cũ cho các key đã ghi, tránh dữ liệu "nửa vời".
// entries: mảng [key, value]; value = null nghĩa là xoá key đó. Trả về true/false.
export function writeAll(entries) {
  let before;
  try { before = entries.map(([key]) => [key, localStorage.getItem(key)]); } catch (e) { return false; }   // trình duyệt chặn lưu trữ
  try {
    entries.forEach(([key, value]) => {
      if (value === null) localStorage.removeItem(key);
      else localStorage.setItem(key, JSON.stringify(value));
    });
    return true;
  } catch (e) {
    console.warn("Cannot save, rolling back", e);
    before.forEach(([key, raw]) => {
      try {
        if (raw === null) localStorage.removeItem(key);
        else localStorage.setItem(key, raw);
      } catch (err) { /* không trả lại được thì thôi */ }
    });
    return false;
  }
}
