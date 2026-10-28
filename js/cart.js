// Giỏ hàng lưu trong localStorage (key "sanctuary_cart"): mảng { id, color, size, qty }
import { readList, writeJSON, isValidCartItem } from "./storage.js";

const CART_KEY = "sanctuary_cart";

// Món sai cấu trúc (dữ liệu hỏng / sửa tay) bị bỏ qua, không làm lỗi trang
export function getCart() {
  return readList(CART_KEY, isValidCartItem);
}

// Lưu giỏ; trả về true nếu lưu được. Lưu xong phát sự kiện "cart-change" để header cập nhật số món ngay
export function saveCart(cart) {
  const ok = writeJSON(CART_KEY, cart);
  if (ok) window.dispatchEvent(new CustomEvent("cart-change"));
  return ok;
}

// Tổng số lượng của 1 sản phẩm trong giỏ (cộng mọi màu + size), vì tồn kho tính theo sản phẩm
export function qtyInCart(cart, id) {
  return cart.filter((i) => i.id === id).reduce((sum, i) => sum + i.qty, 0);
}

// Thêm 1 sản phẩm: nếu đã có cùng mẫu + màu + size thì chỉ tăng số lượng.
// stock: số còn trong kho -> tổng số trong giỏ không được vượt quá (bấm thêm nhiều lần cũng không vượt).
// Trả về { added: số thật sự thêm được, saved: lưu thành công hay không }
export function addToCart(id, color, size, qty = 1, stock = Infinity) {
  const cart = getCart();
  const room = Math.max(0, stock - qtyInCart(cart, id));   // còn được thêm bao nhiêu
  const added = Math.min(qty, room);
  if (added === 0) return { added: 0, saved: true };
  const found = cart.find((i) => i.id === id && i.color === color && i.size === size);
  if (found) found.qty += added;
  else cart.push({ id, color, size, qty: added });
  return { added, saved: saveCart(cart) };
}
