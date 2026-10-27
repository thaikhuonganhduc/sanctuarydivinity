// Gợi ý size từ chiều cao + cân nặng.
// Cách làm (xem tools/build_size_chart.py): từ dữ liệu đo cơ thể ANSUR II (~6.000 người), học công thức
//   vòng_ngực ≈ intercept + perKg * cân_nặng + perCm * chiều_cao
// rồi tra vòng ngực vào bảng mốc của các hãng để ra size. Hệ số nằm trong data/size-chart.json.

const SIZES = ["XXS", "XS", "S", "M", "L", "XL"];

let chartPromise = null;
// Đọc data/size-chart.json 1 lần rồi dùng lại (fetch)
export function loadSizeChart() {
  if (!chartPromise) {
    chartPromise = fetch("../data/size-chart.json").then((res) => {
      if (!res.ok) throw new Error("Cannot load size chart");
      return res.json();
    });
  }
  return chartPromise;
}

// Đọc chiều cao: "5'11", "5'11\"", "5 ft 11", "180", "180 cm", "1.8 m" -> cm (hoặc null nếu không hiểu)
export function parseHeight(text) {
  const t = text.trim().toLowerCase().replace(/[”″]/g, '"').replace(/[’′]/g, "'");
  let m = t.match(/^(\d)\s*(?:'|ft|feet)\s*(\d{1,2})?\s*(?:"|in|inch|inches)?$/);
  if (m) return Math.round((Number(m[1]) * 12 + Number(m[2] || 0)) * 2.54);
  m = t.match(/^(\d(?:[.,]\d+)?)\s*m$/);
  if (m) return Math.round(Number(m[1].replace(",", ".")) * 100);
  m = t.match(/^(\d{2,3}(?:[.,]\d+)?)\s*(?:cm)?$/);
  if (m) return Math.round(Number(m[1].replace(",", ".")));
  return null;
}

// Đọc cân nặng: "165 lbs", "165lb", "75 kg", "75" (mặc định kg) -> kg
export function parseWeight(text) {
  const m = text.trim().toLowerCase().match(/^(\d{2,3}(?:[.,]\d+)?)\s*(kg|kgs|lb|lbs|pounds?)?$/);
  if (!m) return null;
  const n = Number(m[1].replace(",", "."));
  const isPounds = m[2] && (m[2].startsWith("lb") || m[2].startsWith("pound"));
  return isPounds ? n * 0.45359237 : n;
}

// Trả về { size, between, outOfRange, chestCm }
//   chart: nội dung size-chart.json; gender: "him" | "her"
//   category: category của sản phẩm; available: các size sản phẩm có bán
export function recommendSize({ chart, gender, heightCm, weightKg, category, available }) {
  const g = chart[gender] || chart.him;
  const chest = g.intercept + g.perKg * weightKg + g.perCm * heightCm;   // vòng ngực dự đoán (cm)

  let index = g.chestLimitsCm.findIndex((limit) => chest < limit);
  if (index === -1) index = SIZES.length - 1;                            // vượt mốc cuối -> XL

  // Ngoài khoảng số liệu của bộ dữ liệu (P1-P99) thì kết quả kém tin cậy
  const outOfRange = heightCm < g.heightRangeCm[0] || heightCm > g.heightRangeCm[1] ||
                     weightKg < g.weightRangeKg[0] || weightKg > g.weightRangeKg[1];

  // Đồ ôm: vòng ngực nằm sát mốc trên (trong 1 cm) thì gợi ý size lớn hơn cho thoải mái
  const snug = ["compression", "bodysuits", "tops", "bottoms"].includes(category);
  const upper = g.chestLimitsCm[index];
  const between = snug && upper !== undefined && upper - chest < 1 && index < SIZES.length - 1;
  if (between) index += 1;

  // Chỉ gợi ý size mà sản phẩm có bán: lấy size gần nhất
  const pool = (available && available.length ? available : SIZES).filter((s) => SIZES.includes(s));
  let best = pool.length ? pool[0] : SIZES[index];
  pool.forEach((s) => {
    if (Math.abs(SIZES.indexOf(s) - index) < Math.abs(SIZES.indexOf(best) - index)) best = s;
  });
  return { size: best, between, outOfRange, chestCm: chest };
}

// Câu lưu ý theo kiểu dáng sản phẩm
export function fitNote(category) {
  if (["oversize", "hoodies", "bottoms"].includes(category)) {
    return "Oversized cut: this size gives the intended relaxed look. Size down one for a closer fit.";
  }
  if (["compression", "bodysuits", "tops"].includes(category)) {
    return "Second-skin fit: if you are between sizes, size up for comfort.";
  }
  return "";
}
