# SANCTUARY — Website thương mại điện tử bán quần áo gym

Đồ án cuối kỳ môn **Phát triển Web kinh doanh (BIE5030)**, Đại học Kinh tế - Luật (UEL), Khoa Hệ thống thông tin.

> Đây là đồ án môn học, **không phải cửa hàng thật** ("student project, not a real store").
> Phong cách và dữ liệu mẫu tham khảo từ breathedivinity.com. Logo và tên thương hiệu SANCTUARY là của nhóm.

## 1. Dự án làm gì?

Một website bán quần áo gym theo phong cách tối, gothic, underground. Toàn bộ giao diện bằng **tiếng Anh**, mã nguồn và comment bằng **tiếng Việt**.

Luồng người dùng:

1. **Trang cổng** (`index.html`): đồng hồ đếm ngược tới ngày ra mắt bộ sưu tập, lookbook, và một ô nhỏ ở góc phải trên để nhập mật khẩu.
2. Nhập mã của athlete/influencer (ví dụ `SANCTUARY-DEMO`) thì vào **trang chủ** (`pages/home.html`).
3. **Trang chủ**: ảnh bộ sưu tập, nút **Reviews** bên phải (popup đánh giá thật, lọc theo sao, slideshow ảnh), bấm "Collection X Is Out Now" hoặc **Shop** để cuộn xuống cửa hàng.
4. **Cửa hàng** (dưới ảnh trang chủ): 3 khu Sanctuary (nam), Sanctuary Selene (nữ), Accessories, mỗi khu chia nhóm sản phẩm. Menu **Collections** bên trái và hai thẻ Men's/Women's Line để cuộn tới từng khu; đổi tiền theo vùng; bấm sản phẩm để xem popup (slideshow ảnh, chọn màu, size, gợi ý size, thêm vào giỏ).
5. **Cart**: sửa số lượng, mã giảm giá 10% của athlete, phí ship + thuế ước tính theo nước, form thanh toán có kiểm tra bằng JavaScript.
6. **Contact** (form liên hệ có kiểm tra) và **About** (câu chuyện thương hiệu).

## 2. Công nghệ

- **HTML5 semantic, CSS3, JavaScript thuần** (ES modules), không dùng framework.
- Dữ liệu lưu bằng **JSON**, đọc bằng `fetch` (AJAX), vẽ giao diện bằng **DOM**.
- Không có backend. Trạng thái (giỏ hàng, vai trò, đơn hàng, tin nhắn) lưu bằng `localStorage` / `sessionStorage`.
- **API ngoài:** [open.er-api.com](https://open.er-api.com) để lấy tỷ giá (không cần key). Mất mạng thì dùng tỷ giá dự phòng trong `js/currency.js`.
- **Font:** Angel Wish (file `assets/fonts/Angel wish.ttf`) cho tiêu đề, Times New Roman cho phần còn lại.
- Triển khai dự kiến: GitHub → Vercel.

## 3. Cách chạy trên máy

Yêu cầu: **Visual Studio Code** + extension **Live Server**.

1. Clone hoặc pull code về, mở thư mục dự án bằng VS Code (thư mục gốc là nơi có `index.html`).
2. Chuột phải vào `index.html` → **Open with Live Server** (địa chỉ dạng `http://127.0.0.1:5500`).
3. Trên Vercel, trang cổng có địa chỉ `/password` (cấu hình trong `vercel.json`); chạy local bằng Live Server vẫn là `index.html`.
4. Ở trang cổng, bấm "Enter using password" (góc phải trên) và nhập mã athlete: **`SANCTUARY-DEMO`**.

Lưu ý quan trọng:

- **Phải chạy bằng Live Server**, không mở file trực tiếp bằng đúp chuột. Vì web dùng `fetch` và ES modules nên cần chạy qua `http://`.
- Muốn thử lại luồng cổng: xoá `sessionStorage`/`localStorage` trong DevTools (F12 → Application).
- Mã admin chỉ lưu dạng hash trong `js/config.js` (xem comment trong file). Trang admin chưa làm.

## 4. Cấu trúc thư mục

```
/
├── index.html            # Trang cổng: đếm ngược, lookbook, ô nhập mật khẩu
├── README.md
├── claude.md             # Yêu cầu môn học + hướng dẫn cho Claude (đọc nếu dùng Claude Code)
├── pages/
│   ├── home.html         # Trang chủ: ảnh hero, cửa hàng (3 khu + popup sản phẩm), nút Reviews
│   ├── cart.html         # Giỏ hàng + thanh toán
│   ├── contact.html      # Liên hệ
│   └── about.html        # Câu chuyện thương hiệu
├── css/
│   ├── reset.css         # Reset mặc định của trình duyệt
│   ├── base.css          # Biến màu, font, kiểu chữ cơ bản
│   ├── components.css    # Nút, ô nhập, select dùng lại nhiều trang
│   └── pages.css         # Giao diện từng trang
├── js/
│   ├── config.js         # Hash mã admin, khoá lưu trữ, đường dẫn trang
│   ├── gate.js           # Xử lý nhập mật khẩu ở trang cổng
│   ├── guard.js          # Chặn vào trang nếu chưa nhập mật khẩu
│   ├── countdown.js      # Đồng hồ đếm ngược + ngày ra mắt
│   ├── reviews.js        # Đánh giá: lọc sao, hiện thêm, popup chi tiết
│   ├── products.js       # Đọc products.json, vẽ thẻ sản phẩm
│   ├── shop.js           # Cửa hàng trên trang chủ: chia khu/nhóm, menu Collections, popup chi tiết
│   ├── currency.js       # Tỷ giá + định dạng tiền theo vùng
│   ├── cart.js           # Giỏ hàng trong localStorage
│   ├── cart-page.js      # Trang giỏ hàng: tính tiền, mã giảm giá, đặt hàng
│   ├── shipping.js       # Tính phí ship, thuế nhập khẩu, VAT/GST (ước tính)
│   ├── size-finder.js    # Gợi ý size từ chiều cao + cân nặng (dùng data/size-chart.json)
│   ├── form-validate.js  # Các luật kiểm tra form dùng chung
│   ├── contact.js        # Form liên hệ
│   └── header.js         # Số món trong giỏ "Cart (n)", header ghim cố định trên trang chủ
├── data/
│   ├── products.json     # 32 sản phẩm thật (crawl, tạo bằng `tools/build_products.py`): giá USD, màu, size, tồn kho `stock` giả lập
│   ├── reviews.json      # 157 đánh giá thật (crawl, gộp theo người, tạo bằng `tools/build_reviews.py`): có nhiều ảnh thì hiện slideshow
│   ├── access.json       # Mã athlete: vừa để vào web, vừa là mã giảm giá 10%
│   └── shipping.json     # Phí ship, thuế, thuế nhập khẩu theo nước (ước tính)
│   ├── size-chart.json   # Hệ số gợi ý size, tính từ ANSUR II bằng tools/build_size_chart.py
├── assets/               # logo, fonts, images (lookbook, bg, about), reviews (ảnh feedback)
├── tools/                # Script Python: crawl dữ liệu, tạo products.json và reviews.json, tạo bảng size, đổi ảnh sang WebP
└── docs/                 # Kế hoạch, phân công, báo cáo, slides, kịch bản thuyết trình
```

## 5. Dữ liệu nằm ở đâu?

| Dữ liệu | Nơi lưu | Ghi chú |
|---|---|---|
| Sản phẩm, tồn kho | `data/products.json` | Sửa `stock` để đổi số hàng còn |
| Đánh giá | `data/reviews.json` | Ảnh feedback đặt trong `assets/reviews/` |
| Mã athlete / giảm giá | `data/access.json` | Thêm dòng mới là có mã mới |
| Phí ship, thuế | `data/shipping.json` | **Ước tính**, không phải báo giá thật |
| Giỏ hàng | `localStorage` khoá `sanctuary_cart` | |
| Đơn hàng giả lập | `localStorage` khoá `sanctuary_orders` | |
| Tin nhắn liên hệ | `localStorage` khoá `sanctuary_messages` | |
| Tiền tệ đã chọn | `localStorage` khoá `sanctuary_currency` | |
| Vai trò (customer/admin) | `sessionStorage` khoá `sanctuary_role` | |

## 6. Quy ước làm việc nhóm

- **Một tính năng, một commit**, message rõ ràng bằng tiếng Anh hoặc tiếng Việt theo dạng `loại: nội dung`, ví dụ `feat: cart discount code`, `fix: footer position`, `style: about page layout`, `content: brand story`.
- Commit nhỏ, thường xuyên: lịch sử commit là **bằng chứng phân công công việc** trong báo cáo.
- Trước khi làm, `git pull` để lấy code mới nhất. Tránh hai người sửa cùng một file cùng lúc (đặc biệt `css/pages.css`).
- Code **dễ hiểu hơn code "thông minh"**, comment tiếng Việt ở các đoạn quan trọng, vì cả nhóm phải giải thích được khi vấn đáp.
- Giao diện (chữ hiển thị) viết bằng tiếng Anh; thư viện ngoài, nếu dùng, tải về `js/lib/` và ghi vào báo cáo.

## 7. Trạng thái hiện tại

**Đã có:** trang cổng, trang chủ, đánh giá (lọc sao, popup), Cửa hàng trên trang chủ (khu/nhóm sản phẩm, đổi tiền thật theo tỷ giá, popup chi tiết, gợi ý size), Cart (mã giảm giá, ship/thuế ước tính, thanh toán có kiểm tra), Contact, About.

**Chưa có / còn lại:**

- Trang admin (`pages/admin.html`): thêm/xoá/sửa sản phẩm và tồn kho, đặt ngày ra mắt, xem đơn hàng và tin nhắn.
- Ảnh sản phẩm thật (đang hiện khung chờ). Đặt tên theo mẫu `assets/images/p01-black.jpg` (mã sản phẩm + màu).
- Trang đăng ký / đăng nhập (mô phỏng phía client).
- Nén ảnh lookbook ở trang cổng (khoảng 13 MB) trước khi đưa lên Vercel.
- Tài liệu trong `docs/`: kế hoạch, bảng phân công, báo cáo, slides, kịch bản thuyết trình.
- **Đổi mã admin** trong `js/config.js` trước khi nộp bài.

## 8. Lưu ý về bảo mật

Đây là web tĩnh không có backend, nên mọi "bảo mật" (mật khẩu athlete, mã admin, thanh toán) chỉ là **mô phỏng phía client** và ai cũng xem được bằng F12. Điều này cần nêu rõ trong báo cáo (mục quản trị website: mối đe dọa bảo mật). **Không** đưa mật khẩu thật hay khoá API bí mật vào repo.
