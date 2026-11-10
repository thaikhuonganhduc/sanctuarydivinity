# Bản cài thử WooCommerce (Chương VII – mã nguồn mở)

Chạy WordPress + WooCommerce **ngay trên máy**, không cần XAMPP/PHP/MySQL, bằng [WordPress Playground](https://wordpress.github.io/wordpress-playground/) (chạy bằng Node.js).

| Thành phần | Phiên bản khi nhóm chạy thử (11/11/2026) |
|---|---|
| WordPress | 7.1.4 (PHP 8.3, CSDL SQLite do Playground cung cấp) |
| WooCommerce | 11.2.2 |
| Theme | Storefront |

## Các file

| File | Việc làm |
|---|---|
| `blueprint.json` | Các bước cài đặt: đăng nhập admin, cài WooCommerce + Storefront, đặt tên shop, tiền tệ USD, địa chỉ cửa hàng, bỏ màn hình hướng dẫn ban đầu |
| `build_seed.py` | Lấy 12 sản phẩm từ `data/products.json`, đổi ảnh đầu tiên sang JPG, ghi ra `seed/` |
| `run.php` | Nhập dữ liệu vào WooCommerce: danh mục, thuộc tính Size, 12 sản phẩm có biến thể, 3 khách, vùng giao hàng + thuế, 6 đơn hàng, tùy biến màu Storefront và logo |
| `seed/` | Dữ liệu do `build_seed.py` tạo (`seed.json` + ảnh) |

## Cách chạy

```bash
# 1. (Chỉ khi đổi sản phẩm) tạo lại dữ liệu mẫu
python tools/woocommerce/build_seed.py

# 2. Khởi động WordPress (lần đầu mất vài phút để tải WordPress, WooCommerce, Storefront)
#    Git Bash: thêm MSYS_NO_PATHCONV=1 ở đầu lệnh để Git Bash không tự đổi đường dẫn /wordpress/...
npx @wp-playground/cli@3.1.59 server --port=9400 --login \
  --blueprint=tools/woocommerce/blueprint.json \
  --mount-dir "C:\PTWEB_FINALPROJECT\tools\woocommerce" /wordpress/sanctuary-seed
```

3. Khi thấy `Ready! WordPress is running on http://127.0.0.1:9400`, mở trình duyệt vào **http://127.0.0.1:9400/sanctuary-seed/run.php** (chạy 1 lần) để nhập dữ liệu.
4. Trang quản trị: http://127.0.0.1:9400/wp-admin (tài khoản `admin` / `password`). Cửa hàng: http://127.0.0.1:9400/?post_type=product

Lưu ý:

- Playground **không lưu lại** sau khi tắt server: mỗi lần chạy là một bản cài mới, phải chạy lại bước 3.
- `run.php` không kiểm tra quyền, **chỉ dùng trên máy cá nhân**, không đưa lên hosting thật.
- Khách mẫu đăng nhập bằng mật khẩu `Sanctuary1`.
