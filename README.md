# SANCTUARY — Website thương mại điện tử bán quần áo gym

Đồ án cuối kỳ môn **Phát triển Web kinh doanh (BIE5030)**, Đại học Kinh tế - Luật (UEL), Khoa Hệ thống thông tin.

> Đây là đồ án môn học, **không phải cửa hàng thật** ("student project, not a real store").
> Phong cách và dữ liệu mẫu tham khảo từ breathedivinity.com. Logo và tên thương hiệu SANCTUARY là của nhóm.

## 1. Dự án làm gì?

Một website bán quần áo gym theo phong cách tối, gothic, underground. Toàn bộ giao diện bằng **tiếng Anh**, mã nguồn và comment bằng **tiếng Việt**.

Luồng người dùng:

1. **Trang cổng** (`index.html`): đồng hồ đếm ngược tới ngày ra mắt bộ sưu tập, lookbook, và một ô nhỏ ở góc phải trên để nhập mật khẩu.
2. Nhập mã của athlete/influencer (ví dụ `SANCTUARY-DEMO`) thì vào **trang chủ** (`pages/home.html`). Nhập **mã admin** thì vào thẳng **trang quản trị** (`pages/admin.html`).
3. **Trang chủ**: video hero, nút **Reviews** bên phải (popup đánh giá thật, lọc theo sao, slideshow ảnh), bấm "Collection X Is Out Now" hoặc **Shop** để cuộn xuống cửa hàng. Giữa trang có các đoạn video ngắn xen kẽ.
4. **Cửa hàng** (dưới ảnh trang chủ): 3 khu Sanctuary (nam), Sanctuary Selene (nữ), Accessories, mỗi khu chia nhóm sản phẩm. Menu **Collections** bên trái và hai thẻ Men's/Women's Line để cuộn tới từng khu; đổi tiền theo vùng; bấm sản phẩm để xem popup (slideshow ảnh theo màu, chọn màu, size, gợi ý size, thêm vào giỏ).
5. **Tài khoản**: icon người trên header mở popup **Sign in / Create account**. Đăng nhập rồi thì vào trang **Account** (`pages/account.html`): sửa thông tin cá nhân, đổi mật khẩu, xem lịch sử đơn hàng và trạng thái đơn. Khách chưa đăng ký vẫn mua được (đơn khách vãng lai).
6. **Cart**: sửa số lượng, mã giảm giá 10% của athlete, phí ship + thuế ước tính theo nước, form thanh toán có kiểm tra bằng JavaScript (tự điền nếu đã đăng nhập), mục gợi ý **You may also like**.
7. **Info** (`pages/contact.html`): các tab Contact (form có kiểm tra), Shipping/Returns, Terms and Conditions, Terms of Service, Privacy Policy, Accessibility. Và **About** (câu chuyện thương hiệu).
8. **Admin** (`pages/admin.html`): tổng quan doanh thu, đơn hàng (đổi trạng thái), sản phẩm (sửa giá, tồn kho, nổi bật, ẩn/hiện), khách hàng, tin nhắn liên hệ, mã athlete, sao lưu/khôi phục dữ liệu và dữ liệu mẫu để thuyết trình.

## 2. Công nghệ

- **HTML5 semantic, CSS3, JavaScript thuần** (ES modules), không dùng framework.
- Dữ liệu lưu bằng **JSON**, đọc bằng `fetch` (AJAX), vẽ giao diện bằng **DOM**.
- Không có backend. Trạng thái (giỏ hàng, vai trò, tài khoản, đơn hàng, tin nhắn, thay đổi của admin) lưu bằng `localStorage` / `sessionStorage`.
- **Web Crypto API** (`crypto.subtle`): băm SHA-256 mã admin và mật khẩu tài khoản (có salt ngẫu nhiên), không lưu mật khẩu chữ thô.
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
- Mã admin chỉ lưu dạng hash trong `js/config.js` (xem comment trong file). Nhập mã admin ở trang cổng để vào trang admin. Muốn có dữ liệu demo: vào Admin → **Backup** → **Add sample data** (3 khách, 8 đơn, 3 tin nhắn; khách mẫu đăng nhập bằng mật khẩu `Sanctuary1`).
- Dữ liệu admin và tài khoản nằm trong `localStorage` của **từng trình duyệt**, nên đổi máy hoặc đổi trình duyệt là không thấy (dùng **Backup → Download backup** để mang đi).

## 4. Cấu trúc thư mục

```
/
├── index.html            # Trang cổng: đếm ngược, lookbook, ô nhập mật khẩu
├── README.md
├── vercel.json           # Trên Vercel: "/" chuyển sang "/password" (trang cổng)
├── claude.md             # Yêu cầu môn học + hướng dẫn cho Claude (đọc nếu dùng Claude Code)
├── pages/
│   ├── home.html         # Trang chủ: video hero, cửa hàng (3 khu + popup sản phẩm), nút Reviews
│   ├── cart.html         # Giỏ hàng + thanh toán
│   ├── contact.html      # Trang Info: Contact, Shipping/Returns, điều khoản, chính sách (chuyển tab bằng #)
│   ├── about.html        # Câu chuyện thương hiệu
│   ├── account.html      # Tài khoản khách: thông tin, đổi mật khẩu, lịch sử đơn
│   └── admin.html        # Trang quản trị (chỉ vai trò admin)
├── css/
│   ├── reset.css         # Reset mặc định của trình duyệt
│   ├── base.css          # Biến màu, font, kiểu chữ cơ bản
│   ├── components.css    # Nút, ô nhập, select dùng lại nhiều trang
│   ├── pages.css         # Giao diện từng trang
│   └── admin.css         # Giao diện riêng của trang admin
├── js/
│   ├── config.js         # Hash mã admin, khoá lưu trữ, đường dẫn trang
│   ├── gate.js           # Xử lý nhập mật khẩu ở trang cổng
│   ├── guard.js          # Chặn vào trang nếu chưa nhập mật khẩu (trang admin cần đúng vai trò admin)
│   ├── countdown.js      # Đồng hồ đếm ngược + ngày ra mắt
│   ├── reviews.js        # Đánh giá: lọc sao, hiện thêm, popup chi tiết
│   ├── reviews-panel.js  # Nút Reviews bên phải: mở/đóng popup đánh giá
│   ├── slideshow.js      # Slideshow dùng chung (đánh giá, popup sản phẩm)
│   ├── products.js       # Đọc products.json, áp thay đổi của admin, vẽ thẻ sản phẩm
│   ├── shop.js           # Cửa hàng trên trang chủ: chia khu/nhóm, lọc size/màu, sắp xếp giá, menu Collections
│   ├── product-popup.js  # Popup chi tiết sản phẩm (dùng ở trang chủ và giỏ hàng): màu, size XXS-XXL, bảng size, gợi ý size
│   ├── product-reviews.js # Review trong popup sản phẩm: đúng sản phẩm, không có thì review mẫu cùng loại
│   ├── home-ui.js        # Video hero, chữ mờ dần khi cuộn, nút bên cạnh trang chủ
│   ├── currency.js       # Tỷ giá + định dạng tiền theo vùng
│   ├── storage.js        # Đọc/ghi localStorage an toàn, kiểm tra cấu trúc dữ liệu, ghi nhiều key cùng lúc
│   ├── cart.js           # Giỏ hàng trong localStorage (không vượt tồn kho)
│   ├── cart-page.js      # Trang giỏ hàng: tính tiền, mã giảm giá, đặt hàng, gợi ý sản phẩm
│   ├── shipping.js       # Tính phí ship, thuế nhập khẩu, VAT/GST (ước tính)
│   ├── size-finder.js    # Gợi ý size từ chiều cao + cân nặng (dùng data/size-chart.json)
│   ├── form-validate.js  # Các luật kiểm tra form dùng chung
│   ├── contact.js        # Form liên hệ
│   ├── info.js           # Chuyển tab trên trang Info
│   ├── auth.js           # Tài khoản: đăng ký, đăng nhập, đổi mật khẩu (hash SHA-256 + salt)
│   ├── auth-ui.js        # Icon tài khoản trên header + popup Sign in / Create account
│   ├── account-page.js   # Trang Account
│   ├── admin.js          # Trang admin: đơn hàng, sản phẩm, khách, tin nhắn, sao lưu
│   └── header.js         # Số món trong giỏ "Cart (n)", icon tài khoản, header ghim cố định trên trang chủ
├── data/
│   ├── products.json     # 32 sản phẩm thật (crawl, tạo bằng `tools/build_products.py`): giá USD, màu, size, tồn kho `stock` giả lập
│   ├── reviews.json      # 157 đánh giá thật (crawl, gộp theo người, tạo bằng `tools/build_reviews.py`): có nhiều ảnh thì hiện slideshow
│   ├── access.json       # Mã athlete: vừa để vào web, vừa là mã giảm giá 10%
│   ├── shipping.json     # Phí ship, thuế, thuế nhập khẩu theo nước (ước tính)
│   ├── size-chart.json   # Hệ số gợi ý size + bảng size (ngực, eo, cao, nặng theo size), tính từ ANSUR II bằng tools/build_size_chart.py
│   ├── bd-products.json  # Dữ liệu thô crawl sản phẩm (đầu vào của build_products.py)
│   ├── bd-reviews.json   # Dữ liệu thô crawl đánh giá (đầu vào của build_reviews.py)
│   └── ANSUR_II_*.csv    # Số đo cơ thể (bộ dữ liệu ANSUR II) để tính bảng size
├── assets/               # logo, fonts, images (lookbook WebP trang cổng, bg), products (ảnh WebP theo sản phẩm/màu), reviews (ảnh feedback), videos (hero + 3 đoạn break, đã nén)
│                         # assets/_source/ = ảnh lookbook + video gốc chưa nén (chỉ trên máy, không đưa lên Git)
├── tools/                # Script Python: crawl dữ liệu, tạo products.json và reviews.json, tạo bảng size, đổi ảnh sang WebP,
│                         # compress_media.py: nén ảnh lookbook (WebP q94) + video (H.264 CRF 20)
└── docs/                 # Kế hoạch, phân công, báo cáo, slides, kịch bản thuyết trình (hiện còn trống)
```

## 5. Dữ liệu nằm ở đâu?

| Dữ liệu | Nơi lưu | Ghi chú |
|---|---|---|
| Sản phẩm, tồn kho | `data/products.json` | Sửa `stock` để đổi số hàng còn |
| Đánh giá | `data/reviews.json` | Ảnh feedback đặt trong `assets/reviews/` |
| Mã athlete / giảm giá | `data/access.json` | Thêm dòng mới là có mã mới |
| Phí ship, thuế | `data/shipping.json` | **Ước tính**, không phải báo giá thật |
| Giỏ hàng | `localStorage` khoá `sanctuary_cart` | |
| Đơn hàng giả lập | `localStorage` khoá `sanctuary_orders` | Admin đổi trạng thái đơn, khách thấy ở trang Account |
| Tin nhắn liên hệ | `localStorage` khoá `sanctuary_messages` | Admin xem, đánh dấu đã đọc, xoá |
| Tiền tệ đã chọn | `localStorage` khoá `sanctuary_currency` | |
| Tài khoản khách | `localStorage` khoá `sanctuary_users` | Chỉ lưu hash mật khẩu + salt |
| Người đang đăng nhập | `localStorage` khoá `sanctuary_session` | Lưu email |
| Thay đổi sản phẩm của admin | `localStorage` khoá `sanctuary_product_overrides` | Giá, tồn kho, nổi bật, ẩn, xoá (`deleted`); đè lên `products.json` |
| Sản phẩm admin thêm mới | `localStorage` khoá `sanctuary_custom_products` | Ảnh tải lên được thu nhỏ còn 800px, lưu dạng data URL |
| Ngày ra mắt (ghi đè) | `localStorage` khoá `sanctuary_launch_override` | Mặc định 01/12/2026 trong `js/countdown.js`; admin đổi ở Admin → Launch date |
| Vai trò (customer/admin) | `sessionStorage` khoá `sanctuary_role` | |
| Athlete đã dùng để vào web | `sessionStorage` khoá `sanctuary_source` | |

## 6. Quy ước làm việc nhóm

- **Một tính năng, một commit**, message rõ ràng bằng tiếng Anh hoặc tiếng Việt theo dạng `loại: nội dung`, ví dụ `feat: cart discount code`, `fix: footer position`, `style: about page layout`, `content: brand story`.
- Commit nhỏ, thường xuyên: lịch sử commit là **bằng chứng phân công công việc** trong báo cáo.
- Trước khi làm, `git pull` để lấy code mới nhất. Tránh hai người sửa cùng một file cùng lúc (đặc biệt `css/pages.css`).
- Code **dễ hiểu hơn code "thông minh"**, comment tiếng Việt ở các đoạn quan trọng, vì cả nhóm phải giải thích được khi vấn đáp.
- Giao diện (chữ hiển thị) viết bằng tiếng Anh; thư viện ngoài, nếu dùng, tải về `js/lib/` và ghi vào báo cáo.

## 7. Trạng thái hiện tại

**Đã có:**

- Trang cổng (đếm ngược, lookbook, nhập mật khẩu athlete/admin) và trang chủ (video hero, đánh giá lọc sao + popup + slideshow ảnh).
- Cửa hàng trên trang chủ: khu/nhóm sản phẩm, **lọc theo size/màu, sắp xếp theo giá**, đổi tiền theo tỷ giá thật, popup chi tiết (size XXS–XXL, bảng size, gợi ý size, review có ảnh + lọc sao). **Ảnh sản phẩm thật** (WebP, 32 sản phẩm) đã có đủ.
- Cart: mã giảm giá, ship/thuế ước tính, thanh toán có kiểm tra, gợi ý "You may also like".
- **Đăng ký / đăng nhập** mô phỏng phía client, trang Account (sửa thông tin, đổi mật khẩu, lịch sử đơn).
- **Trang admin**: tổng quan, đơn hàng (đổi trạng thái), sản phẩm (**thêm mới có ảnh**, sửa giá, tồn kho, nổi bật, ẩn/hiện, **xoá + khôi phục**), khách hàng, tin nhắn, mã athlete, **đặt ngày ra mắt**, sao lưu/khôi phục, dữ liệu mẫu.
- Trang Info (Contact + các trang chính sách) và About.
- **Ảnh lookbook và video đã nén** bằng `tools/compress_media.py`: 96 MB → 23 MB, gần như không thấy khác bản gốc (ảnh PSNR 45–48 dB, video SSIM ≥ 0.995).

**Chưa có / còn lại:**

- Tài liệu trong `docs/`: kế hoạch, bảng phân công, báo cáo, slides, kịch bản thuyết trình (thư mục đang trống).
- **Đổi mã admin** trong `js/config.js` trước khi nộp bài (hiện vẫn là mã tạm ghi trong comment của file).

## 8. Lưu ý về bảo mật

Đây là web tĩnh không có backend, nên mọi "bảo mật" (mật khẩu athlete, mã admin, tài khoản khách, thanh toán) chỉ là **mô phỏng phía client** và ai cũng xem được bằng F12. Mật khẩu tài khoản và mã admin chỉ lưu dạng hash SHA-256 (tài khoản có thêm salt), nhưng `guard.js` chỉ chặn ở giao diện, ai tự sửa `sessionStorage` vẫn vào được trang admin. Điều này cần nêu rõ trong báo cáo (mục quản trị website: mối đe dọa bảo mật). **Không** đưa mật khẩu thật hay khoá API bí mật vào repo.
