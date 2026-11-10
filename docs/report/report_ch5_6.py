# -*- coding: utf-8 -*-
"""Chương 5. Thảo luận (kèm quản trị website) và Chương 6. Kết luận và đề xuất."""


def vn(x):
    return str(x).replace(".", ",")


def build(R, ctx):
    sc = ctx["size_chart"]
    lh = ctx["lighthouse"]
    tests = ctx["tests"]
    passed = sum(t["ok"] for t in tests)

    # ================= CHƯƠNG 5 =================
    R.h1("CHƯƠNG 5. THẢO LUẬN", chapter=5)
    R.h2("5.1. So sánh kết quả với mục tiêu ban đầu")
    R.table(["Mục tiêu", "Tiêu chí", "Kết quả", "Đánh giá"], [
        ("MT1. Luồng mua hàng", "Mọi ca kiểm thử của luồng mua hàng đạt", "TC01 - TC38: %d/%d ca đạt" % (passed - 3, len(tests) - 3), ("Đạt", "E2EFDA")),
        ("MT2. Đáp ứng", "Không cuộn ngang ở 390, 820, 1440 px", "TC39 - TC41 đạt; lưới 2, 3, 4 cột", ("Đạt", "E2EFDA")),
        ("MT3. Kỹ thuật đề cương", "Mỗi kỹ thuật có chỗ dùng thật", "Đủ 8 chương đề cương (mục 3.6)", ("Đạt", "E2EFDA")),
        ("MT4. Gợi ý size", "Đúng ≥ 50%, lệch ≤ 1 size ≥ 95%",
         "Đúng " + vn(sc["him"]["exactSizePct"]) + "% / " + vn(sc["her"]["exactSizePct"]) + "%; lệch ≤ 1 size " +
         vn(sc["him"]["withinOneSizePct"]) + "% / " + vn(sc["her"]["withinOneSizePct"]) + "% (nam/nữ)", ("Đạt", "E2EFDA")),
        ("MT5. Trang quản trị", "8 chức năng chạy được", "TC33 - TC38 đạt; đủ 8 trang chức năng", ("Đạt", "E2EFDA")),
        ("MT6. Chất lượng kỹ thuật", "Accessibility ≥ 90; LCP desktop ≤ 2,5 s; HTML hợp lệ",
         "Accessibility 100/100; LCP desktop ≤ " + vn(max(float(r["LCP"].split()[0]) for r in lh if r["mode"] == "desktop")) +
         " s ở cả 5 trang; W3C 0 lỗi (sau một vòng sửa)", ("Đạt", "E2EFDA")),
        ("MT7. Mã nguồn mở", "Cài và quản trị được WooCommerce", "Cài đặt, sản phẩm, đơn, khách, ship/thuế, giao diện", ("Đạt", "E2EFDA")),
    ], widths=[3.6, 4.2, 6.0, 2.2], caption="Đối chiếu kết quả với mục tiêu", size=11, center_cols=(3,))
    R.p("Cả bảy mục tiêu đều đạt. Riêng MT6 không đạt ở lần đo đầu (trang cổng có LCP " +
        vn([r for r in ctx["lighthouse_before"] if r["mode"] == "desktop" and r["name"] == "Gate"][0]["LCP"]) +
        " và CLS cao, còn 5 lỗi W3C) và chỉ đạt sau một vòng đo - sửa - đo lại (mục 4.7.2, 4.7.3).")

    R.h2("5.2. Điểm mạnh của dự án")
    R.bullets([
        "**Bao phủ đủ kiến thức học phần trên một sản phẩm thống nhất:** HTML5 semantic, form, bảng, iframe; CSS3, box "
        "model, reset, LESS, responsive; JavaScript, DOM, sự kiện; XML và AJAX bằng cả `XMLHttpRequest` lẫn `fetch`; mã "
        "nguồn mở; quản trị website.",
        "**Giải quyết vấn đề thật của thời trang trực tuyến:** gợi ý size dựa trên dữ liệu số đo cơ thể thật, có đánh "
        "giá độ chính xác bằng số liệu, thay vì chỉ có một bảng size tĩnh.",
        "**Trải nghiệm thương hiệu rõ nét:** cổng drop có đếm ngược, mã athlete kiêm mã giảm giá, giao diện tối thống "
        "nhất, tối ưu cho điện thoại.",
        "**Chú trọng tính đúng của dữ liệu:** kiểm tra lại giỏ lúc đặt hàng, không cho vượt tồn kho, ghi đơn và tồn kho "
        "cùng lúc có hoàn tác, kiểm tra cấu trúc dữ liệu khi đọc localStorage.",
        "**Đánh giá bằng số liệu khách quan, lặp lại được:** 41 ca kiểm thử tự động, Lighthouse, W3C, độ chính xác mô hình; "
        "mọi script đo và dựng dữ liệu đều nằm trong kho mã nguồn.",
        "**Khả năng truy cập tốt:** Accessibility 100 trên mọi trang dù dùng giao diện nền tối.",
    ])

    R.h2("5.3. Hạn chế của dự án")
    R.bullets([
        "**Không có máy chủ và CSDL:** đơn hàng, tài khoản, thay đổi của quản trị viên chỉ nằm trong trình duyệt đang "
        "dùng; khách đặt hàng trên máy A thì quản trị viên trên máy B không thấy. Việc chuyển dữ liệu phải qua file sao lưu.",
        "**Bảo mật chỉ là mô phỏng:** mọi mã JavaScript, kể cả giá trị băm của mã admin, đều xem được bằng công cụ của "
        "trình duyệt; `guard.js` chỉ chặn ở giao diện, ai sửa `sessionStorage` vẫn vào được trang quản trị. Giá trị băm "
        "SHA-256 của một mã ngắn có thể bị dò bằng tấn công từ điển.",
        "**Thanh toán giả lập:** chỉ kiểm tra định dạng số thẻ, không kết nối cổng thanh toán, không xác thực 3-D Secure.",
        "**Hiệu năng trên điện thoại** của trang chủ (video hero nặng) và trang About (ảnh lớn đầu trang) chưa đạt ngưỡng "
        "LCP tốt 2,5 s; trang Info nặng thêm khoảng 600 KB do bản đồ nhúng.",
        "**Giao diện điện thoại:** hai tab Armory và Reviews ở mép trái che một phần tên sản phẩm ở cột trái (thấy trong ảnh "
        "chụp ở mục 4.4).",
        "**Dữ liệu mẫu lấy từ một thương hiệu khác:** phù hợp mục đích học tập nhưng không dùng được cho kinh doanh thật.",
    ])

    R.h2("5.4. Những phát hiện đáng chú ý")
    R.bullets([
        "**Kiểm tra dữ liệu khi đọc có giá trị thực tế:** cả ba ca kiểm thử “không đạt” ở lần chạy đầu đều do dữ liệu thử "
        "sai cấu trúc hoặc sai giả định, và website đã xử lý đúng: bỏ qua đơn thiếu trường, ẩn màu đã ngừng bán.",
        "**Hồi quy tuyến tính đơn giản đã đủ dùng:** chỉ với chiều cao và cân nặng, mô hình lệch không quá một size với "
        "gần như toàn bộ người trong dữ liệu; đây là lựa chọn hợp lý cho cửa hàng mới chưa có lịch sử mua hàng, khác với "
        "các mô hình học máy cần nhiều dữ liệu (Chatterjee và cộng sự, 2022).",
        "**Ảnh và video quyết định hiệu năng:** cùng mã nguồn, trang không có video tải khoảng 450 KB còn trang chủ tải "
        "khoảng 8.700 KiB; tối ưu tài nguyên đã giảm 70% dung lượng nhưng video vẫn là phần nặng nhất.",
        "**Đo lường cần cẩn thận:** lần đo Lighthouse đầu tiên cho điểm trang cổng cao bất thường vì bộ nhớ đệm chưa được "
        "xoá; nhóm phát hiện nhờ con số tổng dung lượng chỉ 2 KiB, rồi đo lại sau khi xoá cache. Số liệu trong báo cáo là "
        "số đo lại.",
        "**Phải tìm đúng nguyên nhân trước khi sửa:** khai báo kích thước ảnh, cách sửa CLS thường được khuyên, không làm "
        "CLS trang cổng giảm chút nào. Chỉ khi ghi lại từng lần dịch chuyển bố cục và đo kích thước ảnh lúc chưa tải, nhóm "
        "mới thấy nguyên nhân là flex container co theo nội dung; một dòng CSS đã đưa CLS từ 0,316 về 0.",
    ])

    R.h2("5.5. Quản trị website: bảo mật, sao lưu và nâng cấp")
    R.h3("5.5.1. Các mối đe doạ và biện pháp")
    R.table(["Mối đe doạ", "Rủi ro với SANCTUARY", "Biện pháp hiện có", "Biện pháp khi kinh doanh thật"], [
        ("Kiểm soát truy cập kém", "Sửa sessionStorage để vào trang admin", "guard.js chặn giao diện; mã admin chỉ lưu dạng băm", "Xác thực phía máy chủ, phiên đăng nhập, phân quyền"),
        ("Lộ, dò mật khẩu", "Dò giá trị băm bằng từ điển", "SHA-256 + salt 16 byte riêng từng tài khoản", "Băm chậm (bcrypt/Argon2) ở máy chủ, giới hạn số lần thử"),
        ("Chèn mã (XSS)", "Tin nhắn, tên khách chứa mã độc", "Ghi bằng textContent, không dùng innerHTML cho dữ liệu nhập", "Thêm Content-Security-Policy, lọc dữ liệu ở máy chủ"),
        ("Sửa dữ liệu phía máy khách", "Sửa giá, tồn kho trong localStorage", "Kiểm tra cấu trúc khi đọc", "Tính giá, tồn kho ở máy chủ"),
        ("Mất dữ liệu", "Xoá dữ liệu trình duyệt, đổi máy", "Sao lưu/khôi phục JSON trong trang admin", "Sao lưu CSDL tự động hằng ngày"),
        ("Gián đoạn dịch vụ", "Hosting hoặc API tỷ giá lỗi", "CDN của Vercel; tỷ giá dự phòng", "Giám sát uptime, phương án dự phòng"),
        ("Lộ thông tin cấu hình", "Mã demo, mã admin trong mã nguồn", "Chỉ lưu băm; tắt gợi ý mã demo khi nộp", "Biến môi trường, không đưa bí mật lên kho mã"),
    ], widths=[3.0, 4.0, 4.5, 4.5], caption="Mối đe doạ và biện pháp bảo mật", size=10.5)
    R.h3("5.5.2. Kế hoạch sao lưu")
    R.p("Nhóm áp dụng nguyên tắc 3-2-1: ít nhất **3 bản** dữ liệu, trên **2 loại** nơi lưu khác nhau, **1 bản** ở ngoài "
        "máy làm việc.")
    R.table(["Đối tượng", "Cách sao lưu", "Tần suất", "Nơi lưu", "Khôi phục"], [
        ("Mã nguồn, dữ liệu gốc", "Commit Git, đẩy lên GitHub", "Mỗi tính năng", "Máy cá nhân + GitHub", "git checkout / revert"),
        ("Bản triển khai", "Vercel giữ lịch sử từng lần triển khai", "Tự động", "Vercel", "Promote bản cũ (rollback)"),
        ("Dữ liệu vận hành (đơn, khách, tin nhắn, thay đổi sản phẩm)", "Admin → Backup → Download backup (file JSON)", "Cuối mỗi ngày bán", "Ổ đám mây của nhóm", "Admin → Backup → Restore, có kiểm tra file"),
        ("Ảnh, video gốc chưa nén", "Lưu riêng ngoài kho Git", "Khi có tài nguyên mới", "Ổ đám mây", "Nén lại bằng tools/compress_media.py"),
    ], widths=[3.6, 4.2, 2.4, 2.8, 3.0], caption="Kế hoạch sao lưu", size=10.5)
    R.h3("5.5.3. Kế hoạch nâng cấp")
    R.table(["Giai đoạn", "Nội dung nâng cấp", "Lý do"], [
        ("Đã làm (11/11/2026)", "Sửa 5 lỗi W3C; thêm meta description; sửa xô lệch bố cục trang cổng; sửa nhãn thẻ sản phẩm", "MT6 đạt; CLS 0; SEO 100"),
        ("Ngắn hạn", "Dời tab Armory/Reviews trên điện thoại; chỉ tải bản đồ khi khách bấm “Show map”", "Không che sản phẩm; trang Info nhẹ hơn ~600 KB"),
        ("Ngắn hạn", "Video trang chủ: ảnh poster nhẹ, tải video sau; bản video riêng cho điện thoại; nén ảnh đầu trang About", "Giảm LCP trên mobile"),
        ("Trung hạn", "Thêm máy chủ (Node.js hoặc PHP) và CSDL; chuyển đơn, tài khoản, tồn kho về máy chủ", "Dữ liệu dùng chung, bảo mật thật"),
        ("Trung hạn", "Tích hợp cổng thanh toán (VNPay, MoMo, Stripe) và email xác nhận đơn", "Bán hàng thật"),
        ("Dài hạn", "Hoặc chuyển cửa hàng lên WooCommerce, giữ giao diện SANCTUARY làm theme riêng", "Tận dụng hệ sinh thái plugin, giảm công bảo trì"),
        ("Thường xuyên", "Theo dõi Lighthouse sau mỗi lần triển khai; cập nhật thư viện, kiểm tra bảo mật", "Giữ chất lượng ổn định"),
    ], widths=[2.6, 8.6, 4.8], caption="Kế hoạch nâng cấp website", size=10.5)
    R.p("Mỗi lần nâng cấp thực hiện trên nhánh Git riêng, chạy lại bộ kiểm thử tự động và Lighthouse, rồi mới gộp vào "
        "nhánh `main` để Vercel triển khai; nếu có sự cố thì quay lại bản triển khai trước trên Vercel.")

    # ================= CHƯƠNG 6 =================
    R.h1("CHƯƠNG 6. KẾT LUẬN VÀ ĐỀ XUẤT", chapter=6)
    R.h2("6.1. Tổng kết các nội dung chính")
    R.p("Đồ án đã xây dựng hoàn chỉnh website TMĐT SANCTUARY cho thương hiệu quần áo gym bán theo đợt drop, chạy trực "
        "tuyến trên Vercel. Các đóng góp chính gồm:")
    R.bullets([
        "Một website front-end gồm 7 trang, " + str(ctx["js_files"]) + " mô-đun JavaScript, đủ luồng từ trang cổng, cửa "
        "hàng, chi tiết sản phẩm, giỏ hàng, thanh toán, tài khoản tới trang quản trị 8 chức năng, chỉ dùng HTML5, CSS3/LESS "
        "và JavaScript thuần.",
        "Bộ tài liệu phân tích thiết kế: kiến trúc, sơ đồ trang, Use case (24 use case), ERD (18 thực thể), DFD hai mức, "
        "8 quy trình BPMN và 5 lưu đồ giải thuật bám sát mã nguồn.",
        "Công cụ gợi ý size dựa trên hồi quy tuyến tính từ " + "{:,}".format(sc["him"]["sampleSize"] + sc["her"]["sampleSize"]).replace(",", ".") +
        " người trong ANSUR II, đúng size " + vn(sc["him"]["exactSizePct"]) + "% (nam) và lệch không quá một size " +
        vn(sc["him"]["withinOneSizePct"]) + "%.",
        "Bản cài thử WooCommerce với dữ liệu SANCTUARY và bảng so sánh với cách tự lập trình.",
        "Bộ đánh giá lặp lại được: " + str(len(tests)) + " ca kiểm thử tự động (đạt 100%), kết quả Lighthouse, W3C và kế "
        "hoạch quản trị website.",
    ])
    R.h2("6.2. Ý nghĩa khoa học và thực tiễn")
    R.p("**Về học tập và khoa học:** đồ án cho thấy cách hiện thực các yếu tố đã được nghiên cứu về TMĐT thời trang (tính "
        "khan hiếm của sản phẩm giới hạn, giảm trả hàng nhờ thông tin size, khả năng truy cập) bằng công nghệ phía máy "
        "khách, kèm phương pháp đo lường cụ thể. Việc dùng song song XML/`XMLHttpRequest` và JSON/`fetch`, cũng như so sánh "
        "tự lập trình với WooCommerce, giúp thấy rõ ưu nhược của từng cách.")
    R.p("**Về thực tiễn:** mô hình website tĩnh có chi phí vận hành gần như bằng 0, phù hợp để một thương hiệu nhỏ thử "
        "nghiệm một đợt drop trước khi đầu tư hệ thống đầy đủ. Công cụ gợi ý size và bảng size theo số đo thật có thể "
        "dùng lại cho cửa hàng thời trang khác. Kế hoạch sao lưu, nâng cấp và lộ trình chuyển sang WooCommerce là căn cứ "
        "nếu nhóm muốn đưa ý tưởng thành cửa hàng thật.")
    R.h2("6.3. Hướng phát triển")
    R.bullets([
        "Bổ sung máy chủ ứng dụng và CSDL để dữ liệu dùng chung, xác thực và tính giá ở phía máy chủ.",
        "Tích hợp cổng thanh toán trong nước (VNPay, MoMo) và quốc tế, gửi email xác nhận đơn hàng.",
        "Nâng cấp gợi ý size: kết hợp phản hồi “vừa/chật/rộng” trong đánh giá của khách sau khi cửa hàng có lịch sử bán "
        "hàng, theo hướng của Chatterjee và cộng sự (2022).",
        "Tối ưu hiệu năng trên điện thoại (ảnh có kích thước, video riêng cho mobile) và hoàn thiện SEO.",
        "Đo trải nghiệm người dùng thật: khảo sát, kiểm thử khả dụng với khách hàng mục tiêu, phân tích hành vi bằng "
        "công cụ thống kê truy cập.",
    ])
    R.h2("6.4. Kiến nghị")
    R.p("Nhóm kiến nghị học phần có thể giới thiệu thêm các công cụ kiểm thử tự động (như Playwright) và công cụ đo chất "
        "lượng (Lighthouse, W3C Validator) trong các buổi thực hành, vì chúng giúp sinh viên đánh giá sản phẩm bằng số "
        "liệu thay vì cảm nhận. Ngoài ra, WordPress Playground là cách nhanh để cả lớp cài thử WooCommerce mà không cần "
        "cấu hình XAMPP trên từng máy.")
