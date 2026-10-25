// Quy đổi tiền: giá gốc trong products.json là USD. Tỷ giá lấy bằng fetch từ API miễn phí
// (open.er-api.com, không cần key). Lưu cache 1 giờ trong localStorage; nếu mất mạng thì dùng tỷ giá dự phòng.
const API_URL = "https://open.er-api.com/v6/latest/USD";
const CACHE_KEY = "sanctuary_rates";
const CURRENCY_KEY = "sanctuary_currency";
const CACHE_MS = 60 * 60 * 1000;

// Danh sách vùng lãnh thổ -> tiền tệ
export const REGIONS = [
  { name: "United States", code: "USD" },
  { name: "European Union", code: "EUR" },
  { name: "United Kingdom", code: "GBP" },
  { name: "Vietnam", code: "VND" },
  { name: "Japan", code: "JPY" },
  { name: "South Korea", code: "KRW" },
  { name: "China", code: "CNY" },
  { name: "Australia", code: "AUD" },
  { name: "Canada", code: "CAD" },
  { name: "Singapore", code: "SGD" },
  { name: "Thailand", code: "THB" },
  { name: "India", code: "INR" },
  { name: "Switzerland", code: "CHF" },
  { name: "Brazil", code: "BRL" },
  { name: "Mexico", code: "MXN" }
];

// Tỷ giá gần đúng, chỉ dùng khi không gọi được API
const FALLBACK_RATES = {
  USD: 1, EUR: 0.92, GBP: 0.78, VND: 25400, JPY: 150, KRW: 1350, CNY: 7.2, AUD: 1.52,
  CAD: 1.36, SGD: 1.34, THB: 35.5, INR: 83, CHF: 0.88, BRL: 5.0, MXN: 17
};

// Trả về { rates, live, updated }: live = true nếu là tỷ giá thật từ API
export async function loadRates() {
  try {
    const cached = JSON.parse(localStorage.getItem(CACHE_KEY));
    if (cached && Date.now() - cached.time < CACHE_MS) {
      return { rates: cached.rates, live: true, updated: new Date(cached.time) };
    }
  } catch (e) { /* cache hỏng thì bỏ qua */ }

  try {
    const res = await fetch(API_URL);
    if (!res.ok) throw new Error("Rate API error");
    const data = await res.json();
    try { localStorage.setItem(CACHE_KEY, JSON.stringify({ time: Date.now(), rates: data.rates })); } catch (e) { /* bỏ qua */ }
    return { rates: data.rates, live: true, updated: new Date() };
  } catch (e) {
    console.warn("Using fallback exchange rates", e);
    return { rates: FALLBACK_RATES, live: false, updated: null };
  }
}

// Đổi USD -> tiền đã chọn và định dạng đúng kiểu (VND, JPY, KRW tự bỏ số lẻ)
export function formatPrice(usd, code, rates) {
  const value = usd * (rates[code] || 1);
  return new Intl.NumberFormat("en-US", { style: "currency", currency: code }).format(value);
}

export function getSavedCurrency() {
  try { return localStorage.getItem(CURRENCY_KEY) || "USD"; } catch (e) { return "USD"; }
}
export function saveCurrency(code) {
  try { localStorage.setItem(CURRENCY_KEY, code); } catch (e) { /* bỏ qua */ }
}
