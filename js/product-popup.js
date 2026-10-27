// Popup chi tiết sản phẩm (ảnh theo màu bên trái, thông tin + nút mua bên phải), dùng chung cho trang chủ và trang giỏ hàng.
// initProductPopup nhận khung <dialog> và vài hàm của trang gọi nó, rồi trả về hàm openProduct(product).
import { createProductImage } from "./products.js";
import { addToCart } from "./cart.js";
import { buildSlideshow } from "./slideshow.js";
import { parseHeight, parseWeight, recommendSize, fitNote, loadSizeChart } from "./size-finder.js";
import { formatPrice } from "./currency.js";

const SIZES = ["XXS", "XS", "S", "M", "L", "XL"];

export function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

// getCurrency / getRates: lấy tiền tệ + tỷ giá đang dùng của trang
// onAddToCart: chạy sau khi thêm món vào giỏ (trang giỏ hàng dùng để vẽ lại)
// onBuyNow: chạy khi bấm Buy now (mặc định sang trang giỏ hàng; trang giỏ hàng thì chỉ đóng popup)
export function initProductPopup({ dialog, detail, getCurrency, getRates, onAddToCart = () => {}, onBuyNow = () => { location.href = "cart.html"; } }) {
  // Bấm ra ngoài vùng nội dung thì đóng popup
  dialog.addEventListener("click", (e) => { if (e.target === dialog) dialog.close(); });

  function openProduct(product) {
    let color = product.colors[0];
    let size = null;
    detail.replaceChildren();

    // Bên trái: ảnh theo màu đang chọn
    const media = el("div", "review-detail__photo product-card__media product-detail__media");
    // Màu có nhiều ảnh thì hiện slideshow (tự xem ảnh khác bằng nút/chấm/vuốt), 1 ảnh thì hiện ảnh thường
    const showImage = () => {
      media.replaceChildren();
      media.classList.remove("slideshow");
      const nodes = color.images.map((_, i) => createProductImage(product, color, i));
      if (nodes.length === 1) media.appendChild(nodes[0]);
      else buildSlideshow(media, nodes, { autoplay: false });
    };
    showImage();

    // Bên phải: thông tin
    const info = el("div", "review-detail__info");
    const price = el("p", "product-detail__price", formatPrice(product.price, getCurrency(), getRates()));
    const message = el("p", "form-error");
    message.setAttribute("role", "alert");

    // Chọn màu
    const colorName = el("span", "", color.name);
    const colorRow = el("div", "product-detail__options");
    product.colors.forEach((c) => {
      const btn = el("button", "swatch-btn");
      btn.type = "button";
      btn.style.background = c.hex;
      btn.title = c.name;
      btn.setAttribute("aria-label", c.name);
      btn.setAttribute("aria-pressed", String(c === color));
      btn.addEventListener("click", () => {
        color = c;
        colorName.textContent = c.name;
        colorRow.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
        showImage();
      });
      colorRow.appendChild(btn);
    });

    // Chọn size XXS -> XL
    const sizeRow = el("div", "product-detail__options");
    const sizeList = product.sizes.length ? product.sizes : SIZES;
    sizeList.forEach((sz) => {
      const btn = el("button", "size-btn", sz);
      btn.type = "button";
      btn.setAttribute("aria-pressed", "false");
      btn.addEventListener("click", () => selectSize(sz));
      sizeRow.appendChild(btn);
    });
    // Chọn 1 size (dùng cho cả bấm nút lẫn nút "Use this size" của bộ gợi ý)
    function selectSize(sz) {
      size = sz;
      message.textContent = "";
      sizeRow.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", String(b.textContent === sz)));
    }

    // ---- Gợi ý size theo chiều cao + cân nặng ----
    const finder = buildSizeFinder(product, selectSize);

    // Số lượng muốn mua (tối đa bằng số còn trong kho)
    let qty = 1;
    const qtyValue = el("span", "qty__value", "1");
    const minus = el("button", "qty__btn", "−");
    const plus = el("button", "qty__btn", "+");
    minus.type = plus.type = "button";
    minus.setAttribute("aria-label", "Decrease quantity");
    plus.setAttribute("aria-label", "Increase quantity");
    function setQty(n) {
      qty = Math.min(Math.max(n, 1), product.stock);
      qtyValue.textContent = qty;
      minus.disabled = qty <= 1;
      plus.disabled = qty >= product.stock;
    }
    minus.addEventListener("click", () => setQty(qty - 1));
    plus.addEventListener("click", () => setQty(qty + 1));
    setQty(1);
    const qtyRow = el("div", "qty");
    qtyRow.append(minus, qtyValue, plus);

    // Dòng số hàng còn trong kho (con số tô đỏ)
    const stockLine = el("p", "product-detail__stock");
    if (product.stock > 0) {
      stockLine.append(el("strong", "stock-number", String(product.stock)), " in stock");
    } else {
      stockLine.textContent = "Out of stock";
    }

    // Nút thêm vào giỏ / mua ngay (bắt buộc chọn size)
    const addBtn = el("button", "btn", "Add to cart");
    const buyBtn = el("button", "btn btn--ghost", "Buy now");
    addBtn.type = buyBtn.type = "button";
    function checkSize() {
      if (!size) { message.textContent = "Please select a size."; return false; }
      return true;
    }
    addBtn.addEventListener("click", () => {
      if (!checkSize()) return;
      addToCart(product.id, color.name, size, qty);
      onAddToCart();
      addBtn.textContent = "Added ✓";
      setTimeout(() => { addBtn.textContent = "Add to cart"; }, 1500);
    });
    buyBtn.addEventListener("click", () => {
      if (!checkSize()) return;
      addToCart(product.id, color.name, size, qty);
      onAddToCart();
      onBuyNow();
    });
    const actions = el("div", "product-detail__actions");
    if (product.stock > 0) {
      actions.append(addBtn, buyBtn);
    } else {
      actions.appendChild(el("p", "product-card__tag", "Sold out"));
    }

    // Thông số
    const specs = el("dl", "spec-list");
    [["Material", product.specs.material], ["Weight", product.specs.weight],
     ["Fit", product.specs.fit], ["Care", product.specs.care]].filter(([, value]) => value).forEach(([label, value]) => {
      const row = el("div", "spec-row");
      row.append(el("dt", "", label), el("dd", "", value));
      specs.appendChild(row);
    });

    // Các ý mô tả sản phẩm (từ products.json) hiện thành danh sách
    const featureList = el("ul", "product-detail__features");
    (product.features || []).forEach((f) => featureList.appendChild(el("li", "", f)));
    if (product.description) featureList.prepend(el("li", "", product.description));

    const colorLabel = el("p", "product-detail__label", "Color · ");
    colorLabel.appendChild(colorName);

    const close = el("button", "review-detail__close", "×");
    close.type = "button";
    close.setAttribute("aria-label", "Close");
    close.addEventListener("click", () => dialog.close());

    info.append(
      el("h2", "glass__title", product.name), price, featureList,
      colorLabel, colorRow, el("p", "product-detail__label", "Size"), sizeRow, finder,
      ...(product.stock > 0 ? [el("p", "product-detail__label", "Quantity"), qtyRow] : []), stockLine, message, actions, specs
    );
    detail.append(media, info, close);
    dialog.showModal();
  }

  // Khối "Find your size": nhập chiều cao + cân nặng -> hiện size gợi ý (số to, màu đỏ)
  function buildSizeFinder(product, selectSize) {
    if (product.sizes.length === 1 && product.sizes[0] === "One size") return el("span");   // mũ, nón: không cần

    const box = el("details", "size-finder");
    box.appendChild(el("summary", "", "Find your size"));

    const heightInput = el("input", "input");
    heightInput.id = "sf-height";
    heightInput.placeholder = "5'11\" or 180 cm";
    const weightInput = el("input", "input");
    weightInput.id = "sf-weight";
    weightInput.placeholder = "165 lbs or 75 kg";
    const fields = el("div", "size-finder__fields");
    [["Height", heightInput], ["Weight", weightInput]].forEach(([label, input]) => {
      const wrap = el("div", "field");
      const lab = el("label", "", label);
      lab.htmlFor = input.id;
      wrap.append(lab, input);
      fields.appendChild(wrap);
    });

    const result = el("div", "size-finder__result");
    result.setAttribute("role", "status");
    const calcBtn = el("button", "btn btn--small", "Calculate");
    calcBtn.type = "button";

    async function calculate() {
      result.replaceChildren();
      const heightCm = parseHeight(heightInput.value);
      const weightKg = parseWeight(weightInput.value);
      if (heightCm === null || weightKg === null || heightCm < 120 || heightCm > 230 || weightKg < 30 || weightKg > 200) {
        result.appendChild(el("p", "form-error", "Enter a height like 5'11\" or 180 cm, and a weight like 165 lbs or 75 kg."));
        return;
      }
      // Sản phẩm unisex: dùng thang nam; còn lại theo him/her của sản phẩm
      const gender = product.gender === "her" ? "her" : "him";
      let chart;
      try { chart = await loadSizeChart(); } catch (err) {
        result.appendChild(el("p", "form-error", "Size data is unavailable right now."));
        return;
      }
      const rec = recommendSize({ chart, gender, heightCm, weightKg, category: product.category, available: product.sizes });
      const useBtn = el("button", "btn btn--small btn--ghost", "Use size " + rec.size);
      useBtn.type = "button";
      useBtn.addEventListener("click", () => selectSize(rec.size));
      result.append(el("p", "size-finder__label", "Your size"), el("p", "size-finder__size", rec.size));
      if (rec.between) result.appendChild(el("p", "size-finder__note", "You are between two sizes, so we picked the larger one."));
      if (rec.outOfRange) result.appendChild(el("p", "size-finder__note", "Your measurements are outside the range of our data, so treat this as a rough guess."));
      const note = fitNote(product.category);
      if (note) result.appendChild(el("p", "size-finder__note", note));
      result.append(el("p", "size-finder__source", "Based on ANSUR II body measurements (" + chart[gender].sampleSize.toLocaleString("en-US") + " adults). Fit varies by style."), useBtn);
    }
    calcBtn.addEventListener("click", calculate);
    [heightInput, weightInput].forEach((i) => i.addEventListener("keydown", (e) => { if (e.key === "Enter") calculate(); }));

    box.append(fields, calcBtn, result);
    return box;
  }

  return openProduct;
}
