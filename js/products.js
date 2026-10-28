// Đọc data/products.json bằng fetch (AJAX) và vẽ sản phẩm bằng DOM.
// File này là module: shop.js import các hàm bên dưới để dùng.
import { readMap, readList, isValidProduct } from "./storage.js";

// Thay đổi của admin (giá, tồn kho, nổi bật, ẩn, xoá) lưu trong localStorage, đè lên dữ liệu gốc của products.json.
// Web tĩnh không ghi được vào file JSON, nên đây là cách mô phỏng "cập nhật sản phẩm" phía trình duyệt.
export const OVERRIDES_KEY = "sanctuary_product_overrides";
// Sản phẩm admin thêm mới (trang Admin → Products → Add product), nối vào sau danh sách của products.json
export const CUSTOM_PRODUCTS_KEY = "sanctuary_custom_products";

export function getProductOverrides() {
  return readMap(OVERRIDES_KEY);
}

export function getCustomProducts() {
  return readList(CUSTOM_PRODUCTS_KEY, isValidProduct);
}

// Đường dẫn ảnh: ảnh trong thư mục assets cần thêm "../" (trang nằm trong pages/);
// ảnh admin tải lên được lưu thẳng dạng "data:image/..." nên dùng nguyên
export const imageUrl = (path) => (path.startsWith("data:") ? path : "../" + path);

// Màu còn bán không (products.json đánh dấu "available": false cho màu đã ngừng bán)
export const isColorAvailable = (color) => color.available !== false;

// Mua được không: còn hàng trong kho và còn ít nhất 1 màu đang bán
export const canBuy = (product) => product.stock > 0 && product.colors.some(isColorAvailable);

// ---------- Tồn kho mô phỏng ----------
// Quy tắc: đặt hàng thì trừ kho (sign = -1); admin huỷ đơn thì cộng lại (sign = +1).
// Làm 2 bước để nơi gọi ghi đơn hàng + tồn kho cùng lúc (xem writeAll trong storage.js):
//   1. stockAfter(): tính tồn kho mới, CHƯA ghi gì
//   2. ghi xong thì applyStock(): cập nhật sản phẩm đang hiện trên trang

// productsById: { id: sản phẩm } đang dùng trên trang; items: các món của đơn { id, qty }
// Trả về { overrides: bản overrides mới để ghi vào localStorage, stock: { id: số tồn mới } }
export function stockAfter(productsById, items, sign) {
  // Gộp số lượng theo sản phẩm (1 sản phẩm có thể nằm ở nhiều dòng: khác màu/size)
  const totals = {};
  items.forEach((i) => { if (productsById[i.id]) totals[i.id] = (totals[i.id] || 0) + i.qty; });

  const overrides = getProductOverrides();
  const stock = {};
  Object.keys(totals).forEach((id) => {
    stock[id] = Math.max(0, productsById[id].stock + sign * totals[id]);   // không để kho âm
    overrides[id] = { ...(overrides[id] || {}), stock: stock[id] };
  });
  return { overrides, stock };
}

export function applyStock(productsById, stock) {
  Object.keys(stock).forEach((id) => {
    productsById[id].stock = stock[id];
    productsById[id].inStock = stock[id] > 0;
  });
}

// includeHidden: trang admin và lịch sử đơn cần cả sản phẩm đã ẩn / đã xoá (để đơn cũ vẫn hiện đúng tên);
// cửa hàng và giỏ hàng thì bỏ cả 2 loại này
export async function loadProducts({ includeHidden = false } = {}) {
  const res = await fetch("../data/products.json");
  if (!res.ok) throw new Error("Cannot load products");
  const data = await res.json();
  const overrides = getProductOverrides();
  return [...data.products, ...getCustomProducts()]
    .map((p) => {
      const merged = { ...p, ...(overrides[p.id] || {}) };
      merged.inStock = merged.stock > 0;          // tồn kho đổi thì trạng thái còn hàng đổi theo
      return merged;
    })
    .filter((p) => includeHidden || (!p.hidden && !p.deleted));
}

// Ảnh sản phẩm theo màu; chưa có ảnh thật thì hiện khung chờ ghi tên mẫu thay vì ảnh lỗi
export function createProductImage(product, color, index = 0) {
  const img = document.createElement("img");
  img.src = imageUrl(color.images[index] || "");
  img.alt = product.name + " - " + color.name + (color.images.length > 1 ? " (" + (index + 1) + "/" + color.images.length + ")" : "");
  img.loading = "lazy";
  img.addEventListener("error", () => {
    const ph = document.createElement("span");
    ph.className = "product-card__placeholder";
    ph.textContent = product.name.split(" ")[0];
    img.replaceWith(ph);
  });
  return img;
}

// Tạo 1 thẻ sản phẩm (dùng createElement để dễ giải thích DOM khi vấn đáp)
// formatPrice: hàm đổi giá USD sang tiền đang chọn; onOpen: hàm chạy khi bấm vào thẻ (mở popup)
export function createCard(product, formatPrice = (usd) => "$" + usd.toFixed(2), onOpen) {
  const card = document.createElement("article");
  card.className = "product-card";
  card.tabIndex = 0;                         // cho phép bấm bằng bàn phím
  card.setAttribute("role", "button");
  card.setAttribute("aria-label", "View " + product.name);
  if (onOpen) {
    card.addEventListener("click", () => onOpen(product));
    card.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); onOpen(product); }
    });
  }

  const media = document.createElement("div");
  media.className = "product-card__media";
  media.appendChild(createProductImage(product, product.colors[0]));

  // Có ảnh thứ 2 của sản phẩm thì xếp chồng lên, hiện ra khi rê chuột (CSS) và ẩn lại khi rời chuột
  const firstColor = product.colors[0];
  if (firstColor.images.length > 1) {
    const hover = document.createElement("img");
    hover.className = "product-card__hover";
    hover.src = imageUrl(firstColor.images[1]);
    hover.alt = "";
    hover.loading = "lazy";
    hover.addEventListener("error", () => hover.remove());   // ảnh lỗi thì bỏ, không ảnh hưởng ảnh chính
    media.appendChild(hover);
  }

  const name = document.createElement("h3");
  name.className = "product-card__name";
  name.textContent = product.name;

  const price = document.createElement("p");
  price.className = "product-card__price";
  price.textContent = formatPrice(product.price);

  // Chấm màu có sẵn
  const swatches = document.createElement("div");
  swatches.className = "product-card__swatches";
  product.colors.forEach((c) => {
    const dot = document.createElement("span");
    dot.style.background = c.hex;
    dot.title = c.name;
    swatches.appendChild(dot);
  });

  card.append(media, name, price, swatches);

  if (product.tag) {
    const tag = document.createElement("p");
    tag.className = "product-card__tag";
    tag.textContent = product.tag;
    card.appendChild(tag);
  }
  return card;
}

export function renderGrid(grid, products, formatPrice, onOpen) {
  grid.replaceChildren(...products.map((p) => createCard(p, formatPrice, onOpen)));
}
