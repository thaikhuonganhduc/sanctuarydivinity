// Đọc data/products.json bằng fetch (AJAX) và vẽ sản phẩm bằng DOM.
// File này là module: shop.js import các hàm bên dưới để dùng.

export async function loadProducts() {
  const res = await fetch("../data/products.json");
  if (!res.ok) throw new Error("Cannot load products");
  const data = await res.json();
  return data.products;
}

// Ảnh sản phẩm theo màu; chưa có ảnh thật thì hiện khung chờ ghi tên mẫu thay vì ảnh lỗi
export function createProductImage(product, color) {
  const img = document.createElement("img");
  img.src = "../" + color.images[0];
  img.alt = product.name + " - " + color.name;
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
