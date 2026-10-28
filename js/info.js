// Trang Info: các mục (Contact, Shipping/Returns, điều khoản...) hiện từng cái một, đổi bằng thanh tab.
// Mục đang xem nằm trong địa chỉ (#shipping...) nên gửi link hoặc bấm Back đều đúng mục.
const tabs = document.querySelectorAll(".info-tabs a");
const panels = document.querySelectorAll(".info-panel");
const tabBar = document.querySelector(".info-tabs");

function show() {
  let id = location.hash.slice(1) || "contact";
  if (!document.getElementById("info-" + id)) id = "contact";      // địa chỉ lạ thì về Contact
  panels.forEach((p) => { p.hidden = p.id !== "info-" + id; });
  let current = null;
  tabs.forEach((a) => {
    if (a.dataset.panel === id) { a.setAttribute("aria-current", "page"); current = a; }
    else a.removeAttribute("aria-current");
  });
  // Tiêu đề tab trình duyệt theo mục đang xem, vd "SANCTUARY | Shipping/Returns"
  document.title = "SANCTUARY | " + (current ? current.textContent : "Info");
  // Điện thoại: thanh tab lướt ngang, nên kéo tab đang chọn vào tầm nhìn
  if (current) current.scrollIntoView({ block: "nearest", inline: "center" });
}

// Đổi mục: ghi #mục lên địa chỉ rồi hiện mục đó.
// Áp dụng cho cả thanh tab lẫn các link "#..." nằm trong nội dung (vd: "explained in Shipping/Returns", Quick answers)
document.addEventListener("click", (e) => {
  const link = e.target.closest('a[href^="#"]');
  if (!link || !document.getElementById("info-" + link.getAttribute("href").slice(1))) return;
  e.preventDefault();                                             // không để trình duyệt tự cuộn nhảy tới mục
  history.pushState(null, "", link.getAttribute("href"));
  show();
  // Bấm từ giữa một trang chính sách dài: cuộn lên thanh tab để thấy mục mới từ đầu
  if (!tabBar.contains(link)) tabBar.scrollIntoView({ behavior: "smooth", block: "start" });
});
window.addEventListener("popstate", show);
show();
