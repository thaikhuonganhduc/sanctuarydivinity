// Hành vi giao diện riêng của trang chủ: video hero và 2 nút bên cạnh (Reviews, Armory).

// ---------- Video hero ----------
const video = document.querySelector(".hero-stage__video");
if (video) {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduceMotion) {
    video.pause();                       // người dùng chọn giảm chuyển động: chỉ hiện ảnh poster
  } else if ("IntersectionObserver" in window) {
    // Chạy khi còn thấy dù chỉ 1 góc video (threshold 0); chỉ dừng khi đã hoàn toàn ra khỏi màn hình, cho đỡ tốn pin/CPU
    new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) video.play().catch(() => {}); else video.pause(); });
    }, { threshold: 0 }).observe(video);
  }
}

// ---------- Chữ "Collection X" ghim trên video, mờ dần khi gần hết video ----------
const heroSection = document.querySelector(".hero-visual");
const heroOverlay = document.querySelector(".hero-overlay");
if (heroSection && heroOverlay) {
  let ticking = false;
  const updateOverlay = () => {
    ticking = false;
    const rect = heroSection.getBoundingClientRect();
    const vh = window.innerHeight;
    const scrollable = rect.height - vh;                    // quãng video nằm dưới màn hình đầu tiên
    let opacity = 1;
    if (scrollable > 0) {
      const remaining = rect.bottom - vh;                   // còn bao nhiêu px nữa thì đáy video chạm đáy màn hình
      const range = Math.min(0.8 * vh, scrollable * 0.5);   // đoạn cuối dùng để mờ dần
      opacity = Math.max(0, Math.min(1, remaining / range));
    }
    heroOverlay.style.opacity = opacity;
    heroOverlay.style.visibility = opacity === 0 ? "hidden" : "visible";   // mờ hẳn thì không bấm nhầm vào link
  };
  // requestAnimationFrame: gom nhiều sự kiện cuộn thành 1 lần cập nhật mỗi khung hình cho mượt
  const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(updateOverlay); } };
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  updateOverlay();
}

// ---------- Nút Reviews / Armory ----------
// Ẩn lúc đầu; khi người dùng kéo xuống tới 2 thẻ Men's / Women's Line thì trượt ra (CSS: body.has-side-tabs).
// Kéo ngược lên đầu trang thì ẩn lại.
const audienceCards = document.getElementById("shop-audience");
if (audienceCards) {
  const updateSideTabs = () => {
    const reached = audienceCards.getBoundingClientRect().top < window.innerHeight * 0.9;
    document.body.classList.toggle("has-side-tabs", reached);
  };
  window.addEventListener("scroll", updateSideTabs, { passive: true });
  window.addEventListener("resize", updateSideTabs);
  updateSideTabs();
}
