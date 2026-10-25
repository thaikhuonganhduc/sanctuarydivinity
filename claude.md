# CLAUDE.md — Đồ án môn Phát triển Web kinh doanh (BIE5030)

> File này mô tả toàn bộ yêu cầu môn học và định hướng dự án. Claude hãy đọc kỹ trước khi viết bất kỳ dòng code nào.

## 1. Thông tin môn học

- **Trường/Khoa:** Đại học Kinh tế - Luật (UEL), Khoa Hệ thống thông tin, Bộ môn Thương mại điện tử
- **Học phần:** Phát triển Web kinh doanh (Business Web Development), mã BIE5030
- **Số tín chỉ:** 3 (2 lý thuyết, 1 thực hành)
- **Môn học trước:** Tư duy lập trình
- **Giảng viên:** TS. Trần Duy Thanh, NCS.ThS. Nguyễn Quang Phúc, NCS.ThS. Trần Thị Ánh
- **Giáo trình chính:** Ben Frain (2020), *Responsive Web Design with HTML5 and CSS*, 3rd Edition
- **Tham khảo:** *Eloquent JavaScript* (Marijn Haverbeke, 4th Ed.); *CSS in Depth* (Keith J. Grant, 2nd Ed.)
- **Công cụ thống nhất trong lớp:** Visual Studio Code

## 2. Mục tiêu và chuẩn đầu ra

- **CLO1:** Nắm vững khái niệm thiết kế và phát triển website TMĐT, đề xuất được kỹ thuật phù hợp.
- **CLO2:** Ứng dụng kỹ thuật thiết kế và lập trình **HTML, CSS, JavaScript, XML, DOM** để xây dựng website TMĐT.
- **CLO3:** Sử dụng, cài đặt web TMĐT mã nguồn mở (Adobe Commerce, PrestaShop, WooCommerce) và biết quản trị website.
- **CLO4:** Làm việc nhóm, thuyết trình, tư duy phản biện độc lập.

## 3. Cách tính điểm

| Thành phần | Bài đánh giá | Trọng số |
|---|---|---|
| Quá trình | A1.1 Bài tập thực hành trên lớp | 15% |
| Quá trình | A1.2 Bài tập về nhà | 15% |
| Giữa kỳ | A2.1 Kiểm tra thực hành (75/90 phút) | 20% |
| **Cuối kỳ** | **A3.1 Đồ án nhóm** | **50%** |

- Thang điểm 10, đạt từ 5.0 trở lên.
- Quy định: cấm thi nếu vắng quá 3 buổi; cấm thi nếu không nộp bài tập trên LMS quá 2 lần.

## 4. Rubric chấm đồ án cuối kỳ (A3.1)

### 4.1. Nội dung (40%)
- Đầy đủ nội dung theo yêu cầu
- Code chuẩn
- Chính xác

### 4.2. Cấu trúc, bố cục, hình thức báo cáo và đúng hạn (30%) — 6 yếu tố
1. Có kế hoạch thực hiện đồ án rõ ràng
2. Nộp bài đúng hạn theo kế hoạch
3. Slides có cấu trúc rõ ràng, dễ theo dõi, sinh động, đầy đủ các phần của một báo cáo
4. Không sai lỗi chính tả
5. Trích dẫn, tài liệu tham khảo đầy đủ
6. Có bảng phân công công việc

### 4.3. Thuyết trình (30%) — 5 yếu tố
1. Có kịch bản trình bày tốt
2. Tất cả thành viên tham gia trình bày và trả lời vấn đáp
3. Tự tin, trôi chảy, hạn chế đọc slides
4. Không vượt thời gian quy định
5. Trả lời tốt các câu hỏi

## 5. Phạm vi kiến thức môn học (website phải thể hiện được)

1. **Tổng quan Internet và Website TMĐT:** client/server, giao thức, IP, tên miền, web server, web browser
2. **Thiết kế web:** xác định yêu cầu, front-end/back-end, admin/customer, các bước xây dựng, đưa web chạy online
3. **HTML5:** heading, thẻ phân vùng (semantic), hình ảnh, danh sách, liên kết, bảng, iframe, **form**
4. **CSS:** selector, thuộc tính, **box model**, CSS3, reset/normalize, LESS, **responsive web**, CSS framework
5. **JavaScript:** nhúng vào trang, biến, kiểu dữ liệu, toán tử, cấu trúc điều khiển, hàm, đối tượng
6. **XML và DOM:** thuộc tính/phương thức DOM, **xử lý sự kiện**, XML, **AJAX**
7. **Mã nguồn mở:** Adobe Commerce, PrestaShop, WooCommerce (cài đặt, quản lý sản phẩm/đơn hàng/khách hàng, tùy biến giao diện)
8. **Quản trị website:** mối đe dọa bảo mật, kế hoạch sao lưu, kế hoạch nâng cấp

## 6. Dự án của nhóm

- **Chủ đề:** Website thương mại điện tử bán quần áo gym
- **Thương hiệu:** **SANCTUARY** (logo chữ gothic/metal gai góc, đen trắng, file logo nằm trong `/assets/`)
- **Tham khảo phong cách:** breathedivinity.com (luxury gym brand, thiết kế hoa văn cầu kỳ, đồ cut-and-sew, các đợt drop giới hạn, luxury basics). Đây là đồ án môn học (không kinh doanh thật) nên **được phép sao chép/mô phỏng** danh mục sản phẩm, tên, mô tả và bố cục của site này để làm dữ liệu mẫu. Riêng **logo, thương hiệu và tên thương hiệu của họ thì không dùng** (web dùng thương hiệu SANCTUARY). Phải ghi nguồn tham khảo (breathedivinity.com) trong báo cáo/slides, và ghi chú ở footer web là "student project, not a real store".
- **Tông thương hiệu gợi ý:** tối, mạnh, underground, cao cấp. Nền đen/than, chữ trắng, điểm nhấn tối giản, ảnh sản phẩm lớn.

### Tính năng dự kiến (điều chỉnh sau khi chốt với giảng viên)
- Trang chủ: banner drop, đồng hồ đếm ngược, sản phẩm nổi bật
- Danh sách sản phẩm: lọc theo loại, size, màu, giới tính; sắp xếp theo giá
- Chi tiết sản phẩm: đổi ảnh theo màu, chọn size, bảng size
- Giỏ hàng: thêm/xóa/sửa số lượng, tính tổng tiền, lưu bằng `localStorage`
- Thanh toán: form có validate bằng JavaScript
- Đăng ký / đăng nhập (mô phỏng phía client)
- Trang giới thiệu thương hiệu, liên hệ, chính sách
- Responsive: mobile, tablet, desktop

## 7. Ràng buộc kỹ thuật

- Ưu tiên **HTML5, CSS3, JavaScript thuần** (vanilla). Được phép dùng **bất kỳ thư viện/công cụ nào** (ví dụ Three.js cho hình 3D) nếu cần để hoàn thành yêu cầu. Thư viện nên tải về lưu trong `js/lib/` (không phụ thuộc CDN) và phải ghi trong báo cáo.
- Dữ liệu sản phẩm lưu ở file **XML hoặc JSON**, đọc bằng AJAX/`fetch`.
- Thao tác giao diện bằng **DOM**, có xử lý sự kiện rõ ràng.
- Dùng **semantic HTML**, CSS tổ chức theo module, đặt tên class nhất quán.
- Code sạch, có comment tiếng Việt ở các đoạn quan trọng, dễ giải thích khi vấn đáp.
- Thiết kế mobile-first, kiểm tra các độ rộng phổ biến.
- Chạy được bằng Live Server, không cần backend (trừ khi chốt khác).

### Cấu trúc thư mục đề xuất
```
/
├── CLAUDE.md
├── index.html
├── pages/            # products.html, product-detail.html, cart.html, checkout.html, about.html, contact.html
├── css/              # reset.css, base.css, components.css, pages.css
├── js/               # main.js, cart.js, products.js, filter.js, form-validate.js
├── data/             # products.xml hoặc products.json
├── assets/           # logo, images, fonts
└── docs/             # kế hoạch, phân công, báo cáo, slides, kịch bản thuyết trình
```


## 8. Sản phẩm cần nộp

1. Mã nguồn website hoàn chỉnh
2. Báo cáo + slides (cấu trúc rõ, có trích dẫn, có bảng phân công công việc)
3. Kế hoạch thực hiện đồ án
4. Kịch bản thuyết trình (mọi thành viên đều có phần nói)
5. (Nếu yêu cầu) Phần cài đặt và quản trị thử một hệ thống mã nguồn mở (CLO3)

## 9. Hướng dẫn cho Claude khi làm việc trong dự án này

- Đọc file này trước, bám sát rubric ở mục 4 và phạm vi ở mục 5.
- Luôn trả lời và comment bằng **tiếng Việt**, giải thích đơn giản vì người dùng là sinh viên cần hiểu để vấn đáp.
- Ưu tiên code **dễ hiểu** hơn code "thông minh". Mỗi tính năng nên dùng kỹ thuật có trong đề cương.
- Trước khi viết tính năng lớn, nêu ngắn gọn kế hoạch và các file sẽ tạo/sửa.
- Được dùng mọi thư viện/công cụ cần thiết, không cần hỏi trước (xem mục 7). Được phép sao chép sản phẩm/nội dung từ breathedivinity.com làm dữ liệu mẫu cho đồ án (xem mục 6), nhưng không dùng logo/tên thương hiệu của họ.
- Sau mỗi phần hoàn thành, nhắc người dùng commit Git với message rõ ràng (để làm bằng chứng phân công công việc).