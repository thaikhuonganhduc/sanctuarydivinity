// Popup chi tiết sản phẩm (ảnh theo màu bên trái, thông tin + nút mua bên phải), dùng chung cho trang chủ và trang giỏ hàng.
// initProductPopup nhận khung <dialog> và vài hàm của trang gọi nó, rồi trả về hàm openProduct(product).
import { createProductImage, isColorAvailable, canBuy } from "./products.js";
import { addToCart, getCart, qtyInCart } from "./cart.js";
import { buildSlideshow } from "./slideshow.js";
import { parseHeight, parseWeight, recommendSize, fitNote, loadSizeChart, SIZES } from "./size-finder.js";
import { formatPrice } from "./currency.js";
import { buildProductReviews } from "./product-reviews.js";

export function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

// ---------- Đơn vị của bảng size ----------
// Số liệu gốc là cm/kg; chọn "IN / LB" thì đổi sang inch / pound, chiều cao ghi kiểu feet-inch (5'7").
const CM_PER_INCH = 2.54;
const LB_PER_KG = 2.20462;
function feetInches(cm) {
  const inches = Math.round(cm / CM_PER_INCH);
  return Math.floor(inches / 12) + "'" + (inches % 12) + "\"";
}
const UNITS = {
  metric: { button: "CM / KG", length: "cm", height: "cm", weight: "kg", caption: "centimetres and kilograms",
            toLength: (cm) => cm, toHeight: (cm) => cm, toWeight: (kg) => kg },
  imperial: { button: "IN / LB", length: "in", height: "ft", weight: "lb", caption: "inches and pounds",
              toLength: (cm) => Math.round(cm / CM_PER_INCH), toHeight: feetInches, toWeight: (kg) => Math.round(kg * LB_PER_KG) }
};
// Nhớ đơn vị khách chọn (mở sản phẩm khác vẫn giữ); không đọc/ghi được localStorage thì dùng cm/kg
const UNIT_KEY = "sanctuary_size_units";
let sizeUnit = "metric";
try { if (UNITS[localStorage.getItem(UNIT_KEY)]) sizeUnit = localStorage.getItem(UNIT_KEY); } catch (e) { /* bỏ qua */ }
function setSizeUnit(unit) {
  sizeUnit = unit;
  try { localStorage.setItem(UNIT_KEY, unit); } catch (e) { /* bỏ qua: chỉ là tiện ích */ }
}

// getCurrency / getRates: lấy tiền tệ + tỷ giá đang dùng của trang
// onAddToCart: chạy sau khi thêm món vào giỏ (trang giỏ hàng dùng để vẽ lại)
// onBuyNow: chạy khi bấm Buy now (mặc định sang trang giỏ hàng; trang giỏ hàng thì chỉ đóng popup)
export function initProductPopup({ dialog, detail, getCurrency, getRates, onAddToCart = () => {}, onBuyNow = () => { location.href = "cart.html"; } }) {
  // Bấm ra ngoài vùng nội dung thì đóng popup
  dialog.addEventListener("click", (e) => { if (e.target === dialog) dialog.close(); });

  function openProduct(product) {
    let color = product.colors.find(isColorAvailable) || product.colors[0];   // mở sẵn màu đầu tiên còn bán
    let size = null;
    const buyable = canBuy(product);
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
      btn.style.backgroundColor = c.hex;           // chỉ đặt màu nền, để CSS còn vẽ được gạch chéo cho màu ngừng bán
      btn.title = c.name;
      btn.setAttribute("aria-label", c.name);
      btn.setAttribute("aria-pressed", String(c === color));
      // Màu đã ngừng bán: vẫn hiện để khách biết, nhưng làm mờ và không bấm được
      if (!isColorAvailable(c)) {
        btn.disabled = true;
        btn.title = c.name + " (sold out)";
        btn.setAttribute("aria-label", c.name + ", sold out");
      }
      btn.addEventListener("click", () => {
        color = c;
        colorName.textContent = c.name;
        colorRow.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
        showImage();
      });
      colorRow.appendChild(btn);
    });

    // Chọn size XXS -> XXL
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
      // Tô sáng dòng của size vừa chọn trong bảng size
      sizeChart.querySelectorAll("tr[data-size]").forEach((tr) => tr.classList.toggle("is-selected", tr.dataset.size === sz));
    }

    // ---- Bảng size (số liệu từ data/size-chart.json) ----
    const sizeChart = buildSizeChart(product);

    // ---- Gợi ý size theo chiều cao + cân nặng ----
    const finder = buildSizeFinder(product, selectSize);

    // Số lượng muốn mua: tối đa = số trong kho trừ đi số đã có trong giỏ (tính cả màu/size khác của sản phẩm này)
    let qty = 1;
    const qtyValue = el("span", "qty__value", "1");
    const minus = el("button", "qty__btn", "−");
    const plus = el("button", "qty__btn", "+");
    minus.type = plus.type = "button";
    minus.setAttribute("aria-label", "Decrease quantity");
    plus.setAttribute("aria-label", "Increase quantity");
    const maxQty = () => Math.max(1, product.stock - qtyInCart(getCart(), product.id));
    function setQty(n) {
      qty = Math.min(Math.max(n, 1), maxQty());
      qtyValue.textContent = qty;
      minus.disabled = qty <= 1;
      plus.disabled = qty >= maxQty();
    }
    minus.addEventListener("click", () => setQty(qty - 1));
    plus.addEventListener("click", () => setQty(qty + 1));
    setQty(1);
    const qtyRow = el("div", "qty");
    qtyRow.append(minus, qtyValue, plus);

    // Dòng số hàng còn trong kho (con số tô đỏ)
    const stockLine = el("p", "product-detail__stock");
    if (buyable) {
      stockLine.append(el("strong", "stock-number", String(product.stock)), " in stock");
    } else {
      stockLine.textContent = "Out of stock";
    }

    // Nút thêm vào giỏ / mua ngay (bắt buộc chọn size)
    const addBtn = el("button", "btn", "Add to cart");
    const buyBtn = el("button", "btn btn--ghost", "Buy now");
    addBtn.type = buyBtn.type = "button";

    // Thử thêm vào giỏ, trả về: "ok" (đã thêm), "full" (giỏ đã có đủ số trong kho), "error" (chưa thêm được)
    function tryAdd() {
      if (!size) { message.textContent = "Please select a size."; return "error"; }
      if (!isColorAvailable(color)) { message.textContent = "This color is sold out."; return "error"; }
      const { added, saved } = addToCart(product.id, color.name, size, qty, product.stock);
      if (!saved) { message.textContent = "We couldn't save your cart. Please try again."; return "error"; }
      if (added === 0) {
        message.textContent = "You already have all " + product.stock + " in your cart.";
        return "full";
      }
      // Thêm được ít hơn số muốn mua (do giới hạn kho) thì báo cho khách biết
      message.textContent = added < qty ? "Only " + added + " more could be added: that is all we have in stock." : "";
      onAddToCart();
      setQty(1);                                     // giỏ đổi -> số tối đa được mua thêm cũng đổi
      return "ok";
    }
    addBtn.addEventListener("click", () => {
      if (tryAdd() !== "ok") return;
      addBtn.textContent = "Added ✓";
      setTimeout(() => { addBtn.textContent = "Add to cart"; }, 1500);
    });
    // Mua ngay: giỏ đã đủ hàng ("full") thì vẫn sang thanh toán
    buyBtn.addEventListener("click", () => {
      if (tryAdd() !== "error") onBuyNow();
    });
    const actions = el("div", "product-detail__actions");
    if (buyable) {
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

    // Thứ tự: tên, giá -> chọn màu, size (bảng size, gợi ý size) -> số lượng, nút mua -> thông số -> mô tả -> review
    info.append(
      el("h2", "glass__title", product.name), price,
      colorLabel, colorRow, el("p", "product-detail__label", "Size"), sizeRow, sizeChart, finder,
      ...(buyable ? [el("p", "product-detail__label", "Quantity"), qtyRow] : []), stockLine, message, actions,
      specs, featureList, buildProductReviews(product)
    );
    detail.append(media, info, close);
    dialog.showModal();
  }

  // Khối "Size chart": bảng số đo theo từng size, mở/đóng bằng thẻ <details>.
  // Số liệu đọc từ data/size-chart.json (tính từ dữ liệu ANSUR II bằng tools/build_size_chart.py):
  //   - Vòng ngực: khoảng của từng size (theo bảng size công bố của các hãng)
  //   - Vòng eo, chiều cao, cân nặng: khoảng phổ biến (50% ở giữa) của những người thuộc size đó trong dữ liệu
  function buildSizeChart(product) {
    if (product.sizes.length === 1 && product.sizes[0] === "One size") return el("span");   // mũ, nón: không cần

    const box = el("details", "size-finder size-chart");
    const gender = product.gender === "her" ? "her" : "him";              // unisex dùng thang nam
    const label = gender === "her" ? "Women's" : "Men's";
    box.appendChild(el("summary", "", "Size chart"));
    const body = el("div", "size-chart__body");
    body.appendChild(el("p", "cart-note", "Loading size chart..."));
    box.appendChild(body);

    // Khoảng số "a–b" sau khi đổi đơn vị (fmt); không có số liệu thì "–"
    const range = (pair, fmt) => (pair ? fmt(pair[0]) + "–" + fmt(pair[1]) : "–");
    // Vòng ngực: thiếu cận dưới thì "< b", thiếu cận trên thì "a+"
    const chestRange = (row, fmt) => {
      if (row.chestMinCm === null) return "< " + fmt(row.chestMaxCm);
      if (row.chestMaxCm === null) return fmt(row.chestMinCm) + "+";
      return fmt(row.chestMinCm) + "–" + fmt(row.chestMaxCm);
    };

    // Vẽ bảng theo đơn vị đang chọn (vẽ lại mỗi lần bấm nút đổi đơn vị)
    function fillTable(table, data) {
      const u = UNITS[sizeUnit];
      table.replaceChildren(el("caption", "visually-hidden", label + " size chart in " + u.caption));
      const headRow = el("tr");
      ["Size", "Chest (" + u.length + ")", "Waist (" + u.length + ")", "Height (" + u.height + ")", "Weight (" + u.weight + ")"].forEach((h) => {
        const th = el("th", "", h);
        th.scope = "col";
        headRow.appendChild(th);
      });
      table.appendChild(el("thead")).appendChild(headRow);

      const tbody = el("tbody");
      data.table.filter((row) => product.sizes.includes(row.size)).forEach((row) => {
        const tr = el("tr");
        tr.dataset.size = row.size;
        const th = el("th", "", row.size);
        th.scope = "row";
        tr.appendChild(th);
        [chestRange(row, u.toLength), range(row.waistCm, u.toLength), range(row.heightCm, u.toHeight), range(row.weightKg, u.toWeight)]
          .forEach((v) => tr.appendChild(el("td", "", v)));
        tbody.appendChild(tr);
      });
      table.appendChild(tbody);

      // Khách đã chọn size (trước khi mở bảng hoặc trước khi đổi đơn vị): tô sáng dòng đó
      const pressed = box.closest(".review-detail__info")?.querySelector(".size-btn[aria-pressed='true']");
      if (pressed) tbody.querySelector('tr[data-size="' + pressed.textContent + '"]')?.classList.add("is-selected");
    }

    // Chỉ tải dữ liệu khi khách mở bảng lần đầu
    let loaded = false;
    box.addEventListener("toggle", async () => {
      if (!box.open || loaded) return;
      try {
        const chart = await loadSizeChart();
        const data = chart[gender];
        loaded = true;

        const table = el("table", "size-chart__table");
        fillTable(table, data);

        // Nút đổi đơn vị: CM / KG <-> IN / LB
        const unitGroup = el("div", "size-chart__units");
        unitGroup.setAttribute("role", "group");
        unitGroup.setAttribute("aria-label", "Units");
        Object.keys(UNITS).forEach((key) => {
          const btn = el("button", "size-chart__unit", UNITS[key].button);
          btn.type = "button";
          btn.setAttribute("aria-pressed", String(key === sizeUnit));
          btn.addEventListener("click", () => {
            setSizeUnit(key);
            unitGroup.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
            fillTable(table, data);
          });
          unitGroup.appendChild(btn);
        });
        const head = el("div", "size-chart__head");
        head.append(el("p", "size-chart__title", label + " sizes"), unitGroup);

        const wrap = el("div", "size-chart__scroll");                         // màn hình hẹp: bảng cuộn ngang
        wrap.appendChild(table);
        body.replaceChildren(
          head,
          wrap,
          el("p", "size-finder__source", "Chest ranges follow common apparel size charts. Waist, height and weight show the middle 50% of people in each size in the ANSUR II body survey (" +
            data.sampleSize.toLocaleString("en-US") + " adults). \"–\" means too few people in the data to show a range. Inches and pounds are rounded from the metric values.")
        );
      } catch (err) {
        body.replaceChildren(el("p", "form-error", "Size data is unavailable right now. Close and open the chart to try again."));
      }
    });
    return box;
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
