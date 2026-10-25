// Tính phí vận chuyển, thuế nhập khẩu và VAT/GST (ước tính) theo nước nhận.
// Dữ liệu nằm trong data/shipping.json để sau này admin hoặc nhóm chỉnh số dễ dàng.
export async function loadShipping() {
  const res = await fetch("../data/shipping.json");
  if (!res.ok) throw new Error("Cannot load shipping data");
  return res.json();
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
