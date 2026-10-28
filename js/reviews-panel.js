// Nút "Reviews" bên trái trang chủ (dưới nút Armory): bấm để mở popup chứa phần đánh giá, bấm × / Esc / ra ngoài để đóng.
const tab = document.getElementById("reviews-tab");
const panel = document.getElementById("reviews-panel");
const closeBtn = document.getElementById("reviews-close");

tab.addEventListener("click", () => panel.showModal());   // <dialog> tự khóa nền và xử lý phím Esc
closeBtn.addEventListener("click", () => panel.close());

// Bấm ra ngoài vùng nội dung (vào lớp nền mờ) thì đóng
panel.addEventListener("click", (e) => { if (e.target === panel) panel.close(); });
