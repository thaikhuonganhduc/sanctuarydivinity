// Slideshow dùng chung (đánh giá của khách trên trang chủ + popup sản phẩm ở trang Shop).
// Các ảnh xếp ngang trong 1 dải (track), đổi ảnh bằng cách trượt dải sang trái (CSS transition cho mượt).
// Có nút trước/sau, chấm điều hướng, vuốt trên điện thoại, phím mũi tên và (tuỳ chọn) tự chạy.
//   box        : phần tử khung ảnh (sẽ được thêm class "slideshow")
//   slideNodes : mảng phần tử ảnh đã tạo sẵn (mỗi phần tử là 1 trang của slideshow)
//   autoplay   : true thì tự đổi ảnh mỗi 4,5 giây (tạm dừng khi rê chuột); popup sản phẩm để false
export function buildSlideshow(box, slideNodes, { autoplay = true } = {}) {
  box.classList.add("slideshow");
  const count = slideNodes.length;

  const track = document.createElement("div");
  track.className = "slideshow__track";
  slideNodes.forEach((node) => {
    const slide = document.createElement("div");
    slide.className = "slideshow__slide";
    slide.appendChild(node);
    track.appendChild(slide);
  });

  const dots = document.createElement("div");
  dots.className = "slideshow__dots";
  const dotButtons = slideNodes.map((_, i) => {
    const dot = document.createElement("button");
    dot.type = "button";
    dot.className = "slideshow__dot";
    dot.setAttribute("aria-label", "Show photo " + (i + 1));
    dot.addEventListener("click", (e) => { e.stopPropagation(); go(i, true); });
    dots.appendChild(dot);
    return dot;
  });

  function arrow(direction, label, symbol) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "slideshow__btn slideshow__btn--" + (direction > 0 ? "next" : "prev");
    btn.setAttribute("aria-label", label);
    btn.textContent = symbol;
    btn.addEventListener("click", (e) => { e.stopPropagation(); go(index + direction, true); });
    return btn;
  }

  let index = 0;
  let timer = null;
  function go(n, byUser) {
    index = (n + count) % count;                           // đi vòng: sau ảnh cuối quay lại ảnh đầu
    track.style.transform = "translateX(" + (-index * 100) + "%)";
    dotButtons.forEach((d, i) => d.classList.toggle("is-active", i === index));
    if (byUser) startTimer();                              // người dùng bấm thì tính lại giờ tự chạy
  }

  // Tự chạy: tắt nếu không bật autoplay hoặc người dùng chọn giảm chuyển động
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function startTimer() {
    stopTimer();
    if (!autoplay || reduceMotion) return;
    timer = setInterval(() => {
      if (!box.isConnected) { stopTimer(); return; }       // khung ảnh đã bị gỡ khỏi trang
      if (box.offsetParent === null) return;               // đang ẩn (popup đóng) thì không đổi ảnh
      go(index + 1);
    }, 4500);
  }
  function stopTimer() { clearInterval(timer); timer = null; }
  box.addEventListener("mouseenter", stopTimer);
  box.addEventListener("mouseleave", startTimer);
  box.addEventListener("focusin", stopTimer);
  box.addEventListener("focusout", startTimer);

  // Vuốt ngang trên điện thoại
  let startX = null;
  box.addEventListener("touchstart", (e) => { startX = e.touches[0].clientX; }, { passive: true });
  box.addEventListener("touchend", (e) => {
    if (startX === null) return;
    const dx = e.changedTouches[0].clientX - startX;
    startX = null;
    if (Math.abs(dx) > 40) go(index + (dx < 0 ? 1 : -1), true);
  });

  // Phím mũi tên khi đang focus trong khung ảnh
  box.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") { e.preventDefault(); go(index - 1, true); }
    if (e.key === "ArrowRight") { e.preventDefault(); go(index + 1, true); }
  });

  box.append(track, arrow(-1, "Previous photo", "‹"), arrow(1, "Next photo", "›"), dots);
  go(0);
  startTimer();
  return box;
}
