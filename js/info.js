// Trang Info: các mục (Contact, Shipping/Returns, điều khoản...) hiện từng cái một, đổi bằng thanh tab.
// Mục đang xem nằm trong địa chỉ (#shipping...) nên gửi link hoặc bấm Back đều đúng mục.
const tabs = document.querySelectorAll(".info-tabs a");
const panels = document.querySelectorAll(".info-panel");

function show() {
  let id = location.hash.slice(1) || "contact";
  if (!document.getElementById("info-" + id)) id = "contact";      // địa chỉ lạ thì về Contact
  panels.forEach((p) => { p.hidden = p.id !== "info-" + id; });
  tabs.forEach((a) => {
    if (a.dataset.panel === id) a.setAttribute("aria-current", "page");
    else a.removeAttribute("aria-current");
  });
}

tabs.forEach((a) => a.addEventListener("click", (e) => {
  e.preventDefault();                                             // không để trình duyệt tự cuộn nhảy tới mục
  history.pushState(null, "", a.getAttribute("href"));
  show();
}));
window.addEventListener("popstate", show);
show();
