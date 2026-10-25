// Hiệu ứng logo: rê chuột vào logo thì vùng quanh con trỏ chuyển sang gradient đỏ.
// Cách làm: lưu vị trí chuột vào biến CSS --mx, --my; CSS dùng nó làm tâm của mặt nạ (mask) cho logo đỏ.
const brand = document.getElementById("brand-link");

brand.addEventListener("mousemove", (e) => {
  const box = brand.getBoundingClientRect();
  brand.style.setProperty("--mx", e.clientX - box.left + "px");
  brand.style.setProperty("--my", e.clientY - box.top + "px");
});
