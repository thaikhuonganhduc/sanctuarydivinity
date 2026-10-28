// Tài khoản khách hàng (mô phỏng phía trình duyệt, không có backend):
//  - Danh sách tài khoản lưu trong localStorage (key "sanctuary_users").
//  - Mật khẩu KHÔNG lưu chữ thô: chỉ lưu hash SHA-256 của (salt + mật khẩu), mỗi tài khoản 1 salt ngẫu nhiên riêng.
//  - Người đang đăng nhập lưu email trong localStorage (key "sanctuary_session") để tắt trình duyệt mở lại vẫn còn đăng nhập.
// Lưu ý khi vấn đáp: web tĩnh nên ai mở F12 cũng xem được localStorage; đây là mô phỏng để học, web thật phải có server.

import { readList, writeJSON, isValidUser } from "./storage.js";

const USERS_KEY = "sanctuary_users";
const SESSION_KEY = "sanctuary_session";

// Tài khoản sai cấu trúc (dữ liệu hỏng / sửa tay) bị bỏ qua
function readUsers() {
  return readList(USERS_KEY, isValidUser);
}
// Lưu lỗi thì ném lỗi có câu thông báo dễ hiểu, để popup / trang Account hiện cho người dùng
function writeUsers(users) {
  if (!writeJSON(USERS_KEY, users)) throw new Error("We couldn't save your account. Please try again.");
}

// Băm chuỗi bằng SHA-256 (Web Crypto API), trả về chuỗi hex
async function sha256(text) {
  const bytes = new TextEncoder().encode(text);
  const hash = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(hash)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

// Salt: 16 byte ngẫu nhiên -> 2 người cùng mật khẩu vẫn ra 2 hash khác nhau
function makeSalt() {
  return [...crypto.getRandomValues(new Uint8Array(16))].map((b) => b.toString(16).padStart(2, "0")).join("");
}

const normalizeEmail = (email) => email.trim().toLowerCase();

// Bỏ các trường bí mật trước khi đưa thông tin ra ngoài
function publicUser(user) {
  const { passwordHash, salt, ...rest } = user;
  return rest;
}

// Đăng ký: trả về người dùng mới, hoặc ném lỗi nếu email đã có
export async function register({ name, email, password }) {
  const users = readUsers();
  const key = normalizeEmail(email);
  if (users.some((u) => u.email === key)) throw new Error("An account with this email already exists.");
  const user = await makeUser({ name, email: key, password });
  users.push(user);
  writeUsers(users);
  localStorage.setItem(SESSION_KEY, key);           // đăng ký xong thì đăng nhập luôn
  return publicUser(user);
}

// Tạo bản ghi tài khoản (có salt + hash), chưa lưu
async function makeUser({ name, email, password, phone = "", address = "", city = "", country = "", createdAt = new Date().toISOString() }) {
  const salt = makeSalt();
  return {
    name: name.trim(), email: normalizeEmail(email), salt, passwordHash: await sha256(salt + password),
    phone, address, city, country, createdAt
  };
}

// Admin: thêm tài khoản mẫu để demo (không đăng nhập vào tài khoản đó). Email đã có thì bỏ qua.
export async function addSampleUser(data) {
  const users = readUsers();
  if (users.some((u) => u.email === normalizeEmail(data.email))) return false;
  users.push(await makeUser(data));
  writeUsers(users);
  return true;
}

// Admin: danh sách khách hàng (đã bỏ salt + hash mật khẩu)
export function listUsers() {
  return readUsers().map(publicUser);
}

// Đăng nhập: băm lại mật khẩu vừa nhập với salt của tài khoản rồi so với hash đã lưu
export async function login(email, password) {
  const user = readUsers().find((u) => u.email === normalizeEmail(email));
  // Báo chung 1 câu cho cả 2 trường hợp, không để lộ email nào đã có tài khoản
  if (!user || (await sha256(user.salt + password)) !== user.passwordHash) throw new Error("Incorrect email or password.");
  localStorage.setItem(SESSION_KEY, user.email);
  return publicUser(user);
}

export function logout() {
  localStorage.removeItem(SESSION_KEY);
}

// Người đang đăng nhập (null nếu chưa)
export function getCurrentUser() {
  const email = localStorage.getItem(SESSION_KEY);
  if (!email) return null;
  const user = readUsers().find((u) => u.email === email);
  return user ? publicUser(user) : null;
}

// Cập nhật thông tin cá nhân / địa chỉ (không cho đổi email và mật khẩu ở đây)
export function updateProfile(changes) {
  const email = localStorage.getItem(SESSION_KEY);
  const users = readUsers();
  const user = users.find((u) => u.email === email);
  if (!user) throw new Error("You are not signed in.");
  ["name", "phone", "address", "city", "country"].forEach((k) => {
    if (k in changes) user[k] = String(changes[k]).trim();
  });
  writeUsers(users);
  return publicUser(user);
}

// Đổi mật khẩu: phải nhập đúng mật khẩu cũ
export async function changePassword(oldPassword, newPassword) {
  const email = localStorage.getItem(SESSION_KEY);
  const users = readUsers();
  const user = users.find((u) => u.email === email);
  if (!user) throw new Error("You are not signed in.");
  if ((await sha256(user.salt + oldPassword)) !== user.passwordHash) throw new Error("Your current password is incorrect.");
  user.salt = makeSalt();
  user.passwordHash = await sha256(user.salt + newPassword);
  writeUsers(users);
}
