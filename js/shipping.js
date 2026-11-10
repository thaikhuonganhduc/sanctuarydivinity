// Tính phí vận chuyển, thuế nhập khẩu và VAT/GST (ước tính) theo nước nhận.
// Dữ liệu nằm trong file XML data/shipping.xml, đọc bằng AJAX "cổ điển" (XMLHttpRequest).
// Các dữ liệu khác của web (sản phẩm, đánh giá...) là JSON đọc bằng fetch: nhóm dùng cả hai cách để so sánh.

// Bước 1: gửi yêu cầu AJAX lấy file XML. Trả về Promise để trang giỏ hàng dùng chung với Promise.all.
export function loadShipping() {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "../data/shipping.xml");        // true (bất đồng bộ) là mặc định
    xhr.onload = () => {
      // status 200 = thành công; responseXML là cây DOM của file XML (trình duyệt tự phân tích)
      if (xhr.status === 200 && xhr.responseXML) resolve(parseShippingXml(xhr.responseXML));
      else reject(new Error("Cannot load shipping data (status " + xhr.status + ")"));
    };
    xhr.onerror = () => reject(new Error("Network error while loading shipping data"));
    xhr.send();
  });
}

// Bước 2: duyệt cây DOM của XML, chuyển thành object JavaScript để hàm calcCosts bên dưới dùng.
// Dùng các phương thức DOM giống HTML: getElementsByTagName, getAttribute, textContent.
function parseShippingXml(doc) {
  const num = (el, name) => Number(el.getAttribute(name));   // thuộc tính XML luôn là chuỗi -> đổi sang số
  const data = { categoryKg: {}, zones: {}, countries: {} };

  data.packagingKg = num(doc.getElementsByTagName("packaging")[0], "kg");

  for (const c of doc.getElementsByTagName("category")) {
    data.categoryKg[c.getAttribute("id")] = num(c, "kg");
  }
  for (const z of doc.getElementsByTagName("zone")) {
    data.zones[z.getAttribute("id")] = { base: num(z, "base"), perKg: num(z, "perKg") };
  }
  for (const c of doc.getElementsByTagName("country")) {
    const tax = c.getElementsByTagName("tax")[0];
    const duty = c.getElementsByTagName("duty")[0];
    data.countries[c.getAttribute("name")] = {
      zone: c.getAttribute("zone"),
      taxLabel: tax.getAttribute("label"),
      tax: Number(tax.textContent),                // % thuế nằm trong nội dung thẻ <tax>
      dutyPct: num(duty, "pct"),
      dutyPerItemUsd: num(duty, "perItemUsd"),
    };
  }
  return data;
}

// cart: [{id, color, size, qty}], products: tra theo id, country: tên nước (vd "Vietnam")
// Trả về { weightKg, shipping, duty, tax, taxRate, taxLabel } (tất cả tính bằng USD)
// discountPct: % giảm giá từ mã athlete (0 nếu không có); thuế và thuế nhập khẩu tính trên giá đã giảm
export function calcCosts(data, cart, products, country, discountPct = 0) {
  const info = data.countries[country] || data.countries["United States"];
  const zone = data.zones[info.zone];

  let weightKg = data.packagingKg;
  let subtotal = 0;
  let items = 0;
  cart.forEach((i) => {
    const p = products[i.id];
    weightKg += (data.categoryKg[p.category] || 0.4) * i.qty;
    subtotal += p.price * i.qty;
    items += i.qty;
  });

  subtotal *= 1 - discountPct / 100;

  // Phí ship = phí gốc của vùng + giá mỗi kg (làm tròn lên mỗi 0.5 kg như hãng vận chuyển)
  const billedKg = Math.ceil(weightKg * 2) / 2;
  const shipping = zone.base + zone.perKg * billedKg;
  // Thuế nhập khẩu: % theo giá hàng + mức cố định mỗi món (vd EU)
  const duty = subtotal * (info.dutyPct / 100) + info.dutyPerItemUsd * items;
  // VAT/GST tính trên (hàng + ship + thuế nhập khẩu)
  const tax = (subtotal + shipping + duty) * (info.tax / 100);

  return { weightKg, shipping, duty, tax, taxRate: info.tax, taxLabel: info.taxLabel };
}
