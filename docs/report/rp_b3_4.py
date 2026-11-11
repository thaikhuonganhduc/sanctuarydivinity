# -*- coding: utf-8 -*-
"""PHẦN B - CHƯƠNG 3. HIỆU CHỈNH SƠ ĐỒ BPMN (kèm lưu đồ giải thuật) và CHƯƠNG 4. MÔ HÌNH DFD VÀ YÊU CẦU HỆ THỐNG"""

BPMN = [
    ("Quy trình vào website qua trang cổng", 1, "BPMN quy trình vào website qua trang cổng", [
        "Quy trình bắt đầu khi người dùng mở trang cổng của website. Người dùng bấm nút “Enter using password” ở góc phải trên "
        "để mở hộp nhập mã, nhập mã truy cập rồi nhấn Enter.",
        "Nhận được yêu cầu, website kiểm tra mã có trống hay không; nếu trống thì báo “Please enter a password.” và người dùng "
        "nhập lại. Nếu có mã, website băm mã bằng SHA-256 và so sánh với giá trị băm của mã quản trị. Trường hợp trùng khớp, vai "
        "trò quản trị được lưu vào sessionStorage và người dùng được chuyển vào trang quản trị.",
        "Nếu không phải mã quản trị, website đọc danh sách mã athlete đang bật (kho D3) và tìm mã khớp, không phân biệt chữ hoa, "
        "chữ thường. Có mã khớp thì website lưu vai trò khách cùng tên athlete giới thiệu và chuyển người dùng vào trang chủ; "
        "không có thì hiện “Incorrect password.” để người dùng nhập lại. Quy trình kết thúc khi người dùng vào được trang chủ "
        "hoặc trang quản trị."]),
    ("Quy trình đăng ký tài khoản", 2, "BPMN quy trình đăng ký tài khoản", [
        "Quy trình bắt đầu khi khách bấm biểu tượng tài khoản trên đầu trang và chọn thẻ “Create account”. Khách nhập họ tên, "
        "email, mật khẩu và xác nhận mật khẩu rồi bấm nút tạo tài khoản.",
        "Website kiểm tra form: họ tên ít nhất 2 ký tự, email đúng định dạng, mật khẩu ít nhất 8 ký tự có cả chữ và số, ô xác "
        "nhận trùng mật khẩu. Nếu sai, lỗi hiện ngay dưới từng ô để khách sửa. Nếu hợp lệ, website kiểm tra email đã có tài "
        "khoản hay chưa; email trùng thì báo để khách dùng email khác hoặc đăng nhập.",
        "Với email mới, website tạo salt ngẫu nhiên 16 byte, băm SHA-256 của (salt + mật khẩu), rồi lưu tài khoản vào kho D8. "
        "Nếu lưu thất bại (bộ nhớ trình duyệt đầy hoặc bị chặn), website báo lỗi. Lưu thành công thì khách được đăng nhập luôn, "
        "biểu tượng tài khoản đổi trạng thái và quy trình kết thúc."]),
    ("Quy trình đăng nhập", 3, "BPMN quy trình đăng nhập", [
        "Quy trình bắt đầu khi thành viên bấm biểu tượng tài khoản và chọn thẻ “Sign in”, nhập email và mật khẩu. Website kiểm "
        "tra hai ô không trống và email đúng định dạng; nếu chưa hợp lệ thì yêu cầu nhập lại.",
        "Website tìm tài khoản theo email trong kho D8, băm lại mật khẩu vừa nhập với salt đã lưu và so sánh với giá trị băm "
        "đã lưu. Nếu không có tài khoản hoặc không khớp, website báo chung một câu “Incorrect email or password.” để không lộ "
        "email nào đã đăng ký.",
        "Đăng nhập thành công, website lưu phiên đăng nhập và phát sự kiện `auth-change` để các phần khác của trang (biểu tượng "
        "tài khoản, form thanh toán) tự cập nhật; form thanh toán tự điền thông tin giao hàng của thành viên."]),
    ("Quy trình thêm sản phẩm vào giỏ hàng", 4, "BPMN quy trình thêm sản phẩm vào giỏ hàng", [
        "Khách mở popup chi tiết sản phẩm, chọn màu, size, số lượng rồi bấm “Add to cart”. Website kiểm tra khách đã chọn size "
        "chưa; nếu chưa thì báo “Please select a size.”.",
        "Tiếp theo, website kiểm tra màu đang chọn còn bán hay không, rồi tính số lượng còn có thể thêm bằng tồn kho trừ đi số "
        "lượng sản phẩm đó (mọi màu, size) đã có trong giỏ. Nếu không còn thêm được, website báo khách đã có đủ hàng trong giỏ.",
        "Còn thêm được thì website thêm vào giỏ tối đa bằng số còn lại và lưu vào kho D6. Lưu thành công, số trên biểu tượng giỏ "
        "được cập nhật qua sự kiện `cart-change` và nút đổi thành “Added ✓”; lưu thất bại thì báo lỗi lưu giỏ."]),
    ("Quy trình đặt hàng", 5, "BPMN quy trình đặt hàng", [
        "Khi khách mở trang giỏ hàng, website kiểm tra giỏ: bỏ món bị ẩn, bị xoá, hết màu, giảm số lượng vượt tồn kho, rồi tính "
        "tạm tính. Khách có thể nhập mã athlete; mã đang bật thì được giảm 10%, mã sai thì hiện “This code is not valid.”.",
        "Khách điền thông tin giao hàng, chọn nước nhận và cách thanh toán. Website đọc bảng phí trong kho D4 (shipping.xml) để "
        "tính phí vận chuyển, thuế nhập khẩu và VAT/GST theo nước. Khi khách bấm “Place order”, website kiểm tra form, với thẻ "
        "thì kiểm tra thêm thuật toán Luhn, hạn thẻ, mã CVC; lỗi hiện dưới từng ô.",
        "Form hợp lệ, website kiểm tra lại giỏ một lần nữa; nếu giỏ vừa đổi (ví dụ ở tab khác) thì dừng để khách xem tổng mới. "
        "Nếu không đổi, website tạo đơn mã “SD-...” ở trạng thái Processing, rồi ghi đơn hàng (D7) và tồn kho đã trừ (D1) "
        "**cùng một lần** bằng hàm `writeAll()`. Ghi lỗi thì báo lỗi và giữ nguyên giỏ; ghi thành công thì xoá giỏ, cập nhật "
        "hồ sơ nếu đang đăng nhập và hiện xác nhận kèm mã đơn."]),
    ("Quy trình quản trị viên xử lý đơn hàng", 6, "BPMN quy trình quản trị viên xử lý đơn hàng", [
        "Quản trị viên mở mục Orders, tìm và lọc đơn theo trạng thái, xem chi tiết rồi chọn trạng thái mới cho đơn.",
        "Nếu đơn đã trừ kho và được đổi sang Cancelled, website tính cộng lại tồn kho cho các món trong đơn. Ngược lại, nếu mở "
        "lại một đơn đã huỷ, website trừ kho lần nữa. Sau đó đơn và tồn kho được lưu cùng lúc vào D7 và D1.",
        "Nếu lưu thất bại, ô chọn trạng thái trở về giá trị cũ để màn hình luôn khớp với dữ liệu. Lưu thành công thì quản trị "
        "viên thấy thông báo nhỏ, và khách thấy trạng thái mới ở trang Account của mình."]),
    ("Quy trình liên hệ", 7, "BPMN quy trình liên hệ và trả lời", [
        "Phía khách: khách mở trang Info, tab Contact, điền tên, email, chủ đề, nội dung và bấm “Send”. Website kiểm tra dữ liệu, "
        "lỗi hiện dưới từng ô. Hợp lệ thì tin nhắn được lưu vào kho D9 với trạng thái chưa đọc; lưu được thì hiện “Message sent”, "
        "lưu lỗi thì báo lỗi và giữ nguyên nội dung để khách thử lại.",
        "Phía quản trị: quản trị viên thấy số tin chưa đọc trên menu, mở mục Messages, đọc và đánh dấu đã đọc. Nếu cần trả lời, "
        "quản trị viên bấm Reply để mở ứng dụng email với địa chỉ của khách (liên kết `mailto:`); sau đó có thể xoá tin nhắn."]),
    ("Quy trình quản trị viên thêm sản phẩm", 8, "BPMN quy trình quản trị viên thêm sản phẩm", [
        "Quản trị viên bấm “Add product”, điền tên, dòng sản phẩm, danh mục, giá, tồn kho, màu, size và chọn ảnh. Website kiểm "
        "tra ảnh là JPG, PNG hoặc WebP và không quá 10 MB; sai thì báo lỗi.",
        "Ảnh hợp lệ được đọc bằng FileReader, vẽ lên canvas thu nhỏ còn tối đa 800 px rồi xuất WebP, giúp vừa dung lượng bộ nhớ "
        "trình duyệt. Khi bấm “Save product”, website kiểm tra giá > 0, tồn kho ≥ 0, có ít nhất một size, có ảnh và tên không "
        "trùng sản phẩm khác.",
        "Hợp lệ thì sản phẩm mới (mã bắt đầu bằng “c”, gắn nhãn New) được lưu vào kho D1; bảng sản phẩm được vẽ lại và sản phẩm "
        "xuất hiện ngay trên cửa hàng. Nếu bộ nhớ trình duyệt đầy, website báo lỗi để quản trị viên chọn ảnh nhỏ hơn."]),
]

# Bảng đối chiếu từng quy trình BPMN với quy tắc nghiệp vụ (mã BR ở Chương 2), kho dữ liệu (mã D ở Chương 4) và file code
STEP_RULES = {
    1: [("Kiểm tra mã trống", "BR-A02", "-", "gate.js"),
        ("So khớp mã quản trị bằng SHA-256", "BR-A02, BR-A03", "config.js (giá trị băm)", "gate.js"),
        ("Tìm mã athlete đang bật", "BR-A02, BR-A05", "D3 Mã athlete", "gate.js, athletes.js"),
        ("Lưu vai trò, athlete giới thiệu", "BR-A06", "sessionStorage", "gate.js"),
        ("Chặn trang khi chưa qua cổng", "BR-A01, BR-A03", "sessionStorage", "guard.js")],
    2: [("Kiểm tra form đăng ký", "BR-F01, BR-F02", "-", "auth-ui.js, form-validate.js"),
        ("Kiểm tra email đã tồn tại", "BR-F01", "D8 Tài khoản", "auth.js"),
        ("Tạo salt, băm mật khẩu, lưu", "BR-F03", "D8 Tài khoản", "auth.js, storage.js"),
        ("Đăng nhập ngay sau khi đăng ký", "BR-F05", "D8 (sanctuary_session)", "auth.js")],
    3: [("Kiểm tra form đăng nhập", "BR-F01", "-", "auth-ui.js"),
        ("Băm lại với salt đã lưu, so sánh", "BR-F03, BR-F04", "D8 Tài khoản", "auth.js"),
        ("Lưu phiên, phát auth-change", "-", "D8 (sanctuary_session)", "auth.js, header.js")],
    4: [("Kiểm tra đã chọn size", "BR-B03", "-", "product-popup.js"),
        ("Kiểm tra màu còn bán", "BR-B02", "D1 Sản phẩm", "product-popup.js"),
        ("Tính số còn thêm được", "BR-C01, BR-C02", "D1, D6", "cart.js"),
        ("Lưu giỏ, cập nhật biểu tượng", "BR-C05", "D6 Giỏ hàng", "cart.js, header.js")],
    5: [("Kiểm tra lại giỏ khi mở trang", "BR-C04", "D1, D6", "cart-page.js"),
        ("Áp mã giảm giá", "BR-D03", "D3 Mã athlete", "cart-page.js, athletes.js"),
        ("Tính phí ship, thuế", "BR-E01 - BR-E05", "D4 Phí ship, thuế", "shipping.js"),
        ("Kiểm tra form, thẻ", "BR-D01, BR-D02", "-", "form-validate.js"),
        ("Kiểm tra lại giỏ lúc đặt", "BR-D04", "D1, D6", "cart-page.js"),
        ("Tạo đơn, ghi đơn + kho cùng lúc", "BR-D05, BR-D06", "D1, D7", "cart-page.js, storage.js")],
    6: [("Tìm, lọc, xem chi tiết đơn", "BR-H01", "D7 Đơn hàng", "admin.js"),
        ("Huỷ đơn: cộng lại kho", "BR-H02", "D1, D7", "admin.js"),
        ("Mở lại đơn huỷ: trừ kho", "BR-H02", "D1, D7", "admin.js"),
        ("Lưu lỗi: trả ô chọn về giá trị cũ", "-", "D7", "admin.js, storage.js")],
    7: [("Kiểm tra form liên hệ", "BR-G03", "-", "contact.js, form-validate.js"),
        ("Lưu tin nhắn chưa đọc", "BR-G04", "D9 Tin nhắn", "contact.js"),
        ("Đọc, đánh dấu, trả lời, xoá", "BR-G04", "D9 Tin nhắn", "admin.js")],
    8: [("Kiểm tra loại, dung lượng ảnh", "BR-B06", "-", "admin.js"),
        ("Thu nhỏ ảnh 800 px, xuất WebP", "BR-H03", "-", "admin.js"),
        ("Kiểm tra form, tên không trùng", "BR-B05, BR-B06", "D1 Sản phẩm", "admin.js"),
        ("Lưu sản phẩm mới, hiện trên cửa hàng", "BR-B01", "D1 (sanctuary_custom_products)", "admin.js, products.js")],
}

FLOWS = [
    ("Lưu đồ kiểm tra mã ở trang cổng", 1, "js/gate.js", 17,
     "Mã được kiểm tra theo thứ tự: rỗng → mã quản trị → mã athlete. Mã quản trị không lưu dạng chữ trong mã nguồn mà chỉ lưu "
     "giá trị băm SHA-256; trình duyệt băm chuỗi vừa nhập rồi so sánh hai giá trị băm. Mã athlete so khớp không phân biệt hoa "
     "thường và chỉ tính các mã đang bật."),
    ("Lưu đồ gợi ý size", 2, "js/size-finder.js", 18, None),
    ("Lưu đồ tính tổng tiền đơn hàng", 3, "js/shipping.js, js/cart-page.js", 17,
     "Khối lượng đơn bằng 0,15 kg bao bì cộng khối lượng ước tính theo loại của từng món, làm tròn lên mỗi 0,5 kg để tính cước. "
     "Ví dụ: một áo Doom Tech (0,25 kg) và hai mũ len (0,4 kg mỗi chiếc) gửi đi Mỹ có khối lượng 1,20 kg, làm tròn lên 1,5 kg, "
     "phí ship = 24 + 10 × 1,5 = 39 USD, đúng với số hiển thị trên trang giỏ hàng."),
    ("Lưu đồ đặt hàng", 4, "js/cart-page.js", 18,
     "Lưu đồ có ba lớp bảo vệ dữ liệu: kiểm tra form, kiểm tra lại giỏ hàng, và ghi đơn cùng tồn kho bằng `writeAll()`. Hàm này "
     "lưu giá trị cũ của các khoá trước khi ghi; nếu một lần ghi lỗi thì khôi phục toàn bộ, mô phỏng tính nguyên tử của "
     "transaction trong cơ sở dữ liệu."),
    ("Lưu đồ kiểm tra số thẻ bằng thuật toán Luhn", 5, "js/form-validate.js", 17,
     "Thuật toán Luhn phát hiện lỗi gõ nhầm số thẻ: đi từ chữ số cuối về đầu, nhân đôi các chữ số ở vị trí lẻ (lớn hơn 9 thì "
     "trừ 9), cộng tất cả lại; số thẻ hợp lệ khi tổng chia hết cho 10. Số thẻ thử 4242 4242 4242 4242 có tổng 80 nên hợp lệ; "
     "đổi chữ số cuối thành 1 thì tổng 79, bị báo lỗi."),
]


def build(R, ctx):
    D = ctx["diag"]
    sc = ctx["size_chart"]
    # ======================= CHƯƠNG 3 =======================
    R.chapter(3, "HIỆU CHỈNH SƠ ĐỒ BPMN")
    R.p("Chương này mô tả 8 quy trình nghiệp vụ chính của SANCTUARY bằng ký pháp BPMN 2.0. Mỗi quy trình là một pool, chia "
        "lane theo người hoặc bộ phận thực hiện; hình tròn xanh là sự kiện bắt đầu, hình tròn đỏ là sự kiện kết thúc (có tia sét "
        "là kết thúc do lỗi), hình thoi là cổng rẽ nhánh loại trừ, hình trụ là kho dữ liệu. Các bước bám đúng mã nguồn hiện tại. "
        "Cuối chương là lưu đồ của các thuật toán xử lý chính.")
    for i, (title, page, cap, paras) in enumerate(BPMN, 1):
        R.h3("3.%d. %s" % (i, title))
        R.figure(D / ("04-bpmn-p%d.png" % page), cap, width=17)
        R.h4("3.%d.1. Mô tả quy trình" % i)
        R.ps(*paras)
        R.h4("3.%d.2. Đối chiếu quy tắc nghiệp vụ và dữ liệu" % i)
        R.table(["Bước / điểm quyết định", "Quy tắc áp dụng", "Kho dữ liệu", "File mã nguồn"], STEP_RULES[page],
                widths=[5.2, 3.4, 3.6, 4.8], caption="Đối chiếu " + cap[5:] + " với SRS", size=11)
    n = len(BPMN) + 1
    R.h3("3.%d. Lưu đồ giải thuật các xử lý chính" % n)
    R.p("Ngoài quy trình nghiệp vụ, nhóm vẽ lưu đồ cho năm thuật toán quyết định tính đúng đắn của website. Ký hiệu: hình bầu "
        "dục là bắt đầu/kết thúc, chữ nhật là xử lý, hình thoi là điều kiện, hình bình hành là nhập/xuất, hình trụ là dữ liệu, "
        "ô đỏ là thông báo lỗi.")
    for k, (title, page, file, h, text) in enumerate(FLOWS, 1):
        R.h4("3.%d.%d. %s" % (n, k, title))
        if page == 2:
            hm, hf = sc["him"], sc["her"]
            text = ("Thuật toán gồm ba phần. Thứ nhất, đổi đơn vị (chấp nhận 5'11, 180 cm, 1.8 m, 165 lbs, 75 kg) và loại giá "
                    "trị vô lý (ngoài 120 - 230 cm, 30 - 200 kg). Thứ hai, ước lượng vòng ngực bằng hồi quy tuyến tính học từ "
                    "ANSUR II: nam `ngực = %s + %s × kg − %s × cm`, nữ `ngực = %s + %s × kg − %s × cm`. Thứ ba, tra vòng ngực "
                    "vào các mốc của bảng size; với đồ bó sát, nếu cách mốc trên dưới 1 cm thì tăng một size, cuối cùng chỉ "
                    "gợi ý size sản phẩm đang bán." % tuple(str(x).replace(".", ",") for x in
                    (hm["intercept"], hm["perKg"], abs(hm["perCm"]), hf["intercept"], hf["perKg"], abs(hf["perCm"]))))
        R.p(R.next_fig() + " trình bày " + title.lower() + " (`" + file + "`). " + text)
        R.figure(D / ("05-flowchart-p%d.png" % page), title + " (" + file + ")", height=h)

    # ======================= CHƯƠNG 4 =======================
    R.chapter(4, "MÔ HÌNH DFD VÀ YÊU CẦU HỆ THỐNG")
    R.h3("4.1. DFD")
    R.h4("4.1.1. Ký hiệu sử dụng")
    R.table(["Ký hiệu", "Ý nghĩa"], [
        ("Chữ nhật bo góc (vàng), có số", "Tiến trình: nơi dữ liệu được xử lý"),
        ("Chữ nhật (xanh)", "Tác nhân ngoài: người hoặc hệ thống bên ngoài gửi/nhận dữ liệu"),
        ("Chữ nhật hở một đầu, có mã D", "Kho dữ liệu"),
        ("Mũi tên có nhãn", "Luồng dữ liệu: vào kho là ghi, ra khỏi kho là đọc, hai đầu là đọc và ghi"),
    ], widths=[6.0, 11.0], caption="Ký hiệu DFD theo Gane-Sarson", size=12)
    R.h4("4.1.2. DFD mức ngữ cảnh")
    R.p("Ở mức ngữ cảnh (" + R.next_fig() + "), cả website là một tiến trình trao đổi dữ liệu với ba tác nhân ngoài. **Khách "
        "hàng** gửi mã athlete, lựa chọn sản phẩm, giỏ hàng, thông tin giao hàng, tin nhắn; nhận lại sản phẩm, gợi ý size, tổng "
        "tiền, xác nhận đơn. **Quản trị viên** gửi mã quản trị và các thao tác quản trị; nhận doanh thu, danh sách đơn, khách, "
        "tin nhắn, file sao lưu. **Dịch vụ tỷ giá** cung cấp tỷ giá để quy đổi giá USD.")
    R.figure(D / "03-dfd-p1.png", "DFD mức ngữ cảnh của website SANCTUARY", width=15)
    R.h4("4.1.3. DFD mức 0")
    R.p("Ở mức 0 (" + R.next_fig() + "), hệ thống được tách thành 7 tiến trình và 10 kho dữ liệu.")
    R.figure(D / "03-dfd-p2.png", "DFD mức 0 của website SANCTUARY", width=17)
    R.table(["Tiến trình", "Việc xử lý", "Kho đọc", "Kho ghi", "File mã nguồn"], [
        ("1.0 Xác thực truy cập", "So mã quản trị (băm SHA-256), rồi mã athlete đang bật", "D3", "(sessionStorage)", "gate.js"),
        ("2.0 Duyệt, lọc sản phẩm và đánh giá", "Lọc, sắp xếp, popup, bảng size, gợi ý size, đánh giá, đổi tiền", "D1, D2, D5, D10", "D10", "shop.js, product-popup.js, reviews.js"),
        ("3.0 Quản lý giỏ hàng", "Thêm, sửa số lượng, xoá; không vượt tồn kho", "D1, D6", "D6", "cart.js, cart-page.js"),
        ("4.0 Đặt hàng", "Kiểm tra form, áp mã, tính ship/thuế, lưu đơn, trừ kho", "D1, D3, D4, D6, D8", "D1, D6, D7", "cart-page.js, shipping.js"),
        ("5.0 Quản lý tài khoản", "Đăng ký, đăng nhập, hồ sơ, mật khẩu, lịch sử đơn", "D7, D8", "D8", "auth.js, account-page.js"),
        ("6.0 Gửi liên hệ", "Kiểm tra form rồi lưu tin nhắn", "-", "D9", "contact.js"),
        ("7.0 Quản trị cửa hàng", "Đơn, sản phẩm, khách, tin nhắn, mã athlete, ngày ra mắt, sao lưu", "D1, D3, D7, D8, D9", "D1, D3, D7, D9", "admin.js"),
    ], widths=[3.4, 5.0, 2.6, 2.4, 3.6], caption="Mô tả các tiến trình của DFD mức 0", size=11)
    R.h4("4.1.4. Mô tả kho dữ liệu")
    R.table(["Mã", "Kho dữ liệu", "Nơi lưu thực tế", "Dữ liệu chính"], [
        ("D1", "Sản phẩm", "data/products.json + sanctuary_product_overrides + sanctuary_custom_products", "Tên, giá, màu, ảnh, size, tồn kho, trạng thái ẩn/xoá"),
        ("D2", "Đánh giá", "data/reviews.json", "Người viết, điểm, nội dung, ảnh, sản phẩm được đánh giá"),
        ("D3", "Mã athlete", "data/access.json hoặc sanctuary_athletes", "Tên athlete, mã, trạng thái bật/tắt"),
        ("D4", "Phí ship, thuế", "data/shipping.xml", "Vùng, nước, thuế suất, thuế nhập khẩu, khối lượng theo loại"),
        ("D5", "Bảng size", "data/size-chart.json", "Hệ số hồi quy, mốc vòng ngực, bảng số đo theo size"),
        ("D6", "Giỏ hàng", "sanctuary_cart", "Sản phẩm, màu, size, số lượng"),
        ("D7", "Đơn hàng", "sanctuary_orders", "Mã đơn, khách, món hàng, tổng tiền, trạng thái"),
        ("D8", "Tài khoản", "sanctuary_users, sanctuary_session", "Họ tên, email, salt, giá trị băm mật khẩu, địa chỉ"),
        ("D9", "Tin nhắn", "sanctuary_messages", "Người gửi, email, chủ đề, nội dung, đã đọc"),
        ("D10", "Tỷ giá", "sanctuary_rates", "Tỷ giá theo mã tiền, thời điểm lấy (lưu tạm 1 giờ)"),
    ], widths=[1.4, 2.8, 6.8, 6.0], caption="Mô tả Data Store của hệ thống từ DFD", size=11, center_cols=(0,))
    R.h3("4.2. Yêu cầu hệ thống")
    R.h4("4.2.1. Kiến trúc hệ thống")
    R.p(R.next_fig() + " mô tả kiến trúc client/server của SANCTUARY. Máy chủ Vercel chỉ phục vụ file tĩnh qua HTTPS và CDN, "
        "không có cơ sở dữ liệu hay mã chạy phía máy chủ. Trình duyệt tải HTML, CSS, JavaScript; JavaScript đọc dữ liệu JSON "
        "bằng `fetch`, XML bằng `XMLHttpRequest`, gọi API tỷ giá và lưu trạng thái bằng Web Storage.")
    R.figure(D / "06-architecture-p1.png", "Kiến trúc hệ thống SANCTUARY", width=16.5)
    R.h4("4.2.2. Yêu cầu phía người dùng")
    R.table(["Thành phần", "Yêu cầu"], [
        ("Thiết bị", "Máy tính, máy tính bảng hoặc điện thoại; màn hình rộng từ 360 px"),
        ("Trình duyệt", "Chrome, Edge, Firefox, Safari phiên bản hiện hành (hỗ trợ ES modules, dialog, Web Crypto)"),
        ("Thiết lập", "Bật JavaScript; cho phép lưu trữ cục bộ (localStorage, sessionStorage)"),
        ("Kết nối", "Internet để tải trang, ảnh, video, tỷ giá và bản đồ; mất mạng vẫn xem giá bằng tỷ giá dự phòng"),
    ], widths=[3.6, 13.4], caption="Yêu cầu phía người dùng", size=12, bold_first=True)
    R.h4("4.2.3. Môi trường phát triển và triển khai")
    R.table(["Thành phần", "Môi trường phát triển", "Môi trường triển khai"], [
        ("Máy chủ web", "VS Code Live Server (http://127.0.0.1:5500)", "Vercel (HTTPS, CDN, tự triển khai)"),
        ("Mã nguồn", "Git, kho cục bộ", "GitHub, nhánh main"),
        ("Biên dịch", "Node.js + less 4.2.0 (npm run build:css)", "Không cần, đẩy file CSS đã biên dịch"),
        ("Dữ liệu", "Script Python tạo JSON, ảnh WebP", "File tĩnh trong data/ và assets/"),
        ("Tên miền", "localhost", "sanctuarydivinity.vercel.app"),
    ], widths=[3.4, 6.8, 6.8], caption="Môi trường phát triển và triển khai", size=12, bold_first=True)
    R.h4("4.2.4. Yêu cầu về dung lượng dữ liệu")
    R.p("Vì dữ liệu phát sinh lưu trong localStorage (khoảng 5 MB cho mỗi website trên mỗi trình duyệt), nhóm ước lượng dung "
        "lượng từng loại dữ liệu để bảo đảm không vượt giới hạn; dữ liệu gốc và tài nguyên tĩnh được phục vụ qua CDN nên không bị "
        "giới hạn này.")
    R.table(["Loại dữ liệu", "Nơi lưu", "Dung lượng", "Ghi chú"], [
        ("Danh mục sản phẩm", "data/products.json", "103 KB", "32 sản phẩm, 103 biến thể màu"),
        ("Đánh giá", "data/reviews.json", "85 KB", "157 đánh giá"),
        ("Bảng size, phí ship, mã athlete", "size-chart.json, shipping.xml, access.json", "khoảng 9 KB", "Đọc một lần mỗi trang"),
        ("Ảnh sản phẩm, đánh giá, lookbook", "assets/ (WebP)", "khoảng 37 MB", "Tải lười, chỉ tải ảnh đang xem"),
        ("Video", "assets/videos (H.264)", "khoảng 20 MB", "Chỉ trang chủ"),
        ("Một đơn hàng", "localStorage", "khoảng 0,5 - 1 KB", "~5.000 đơn mới chạm giới hạn 5 MB"),
        ("Một tài khoản", "localStorage", "khoảng 0,3 KB", "Gồm salt và giá trị băm"),
        ("Một sản phẩm do quản trị viên thêm", "localStorage", "khoảng 30 - 80 KB", "Chủ yếu là ảnh WebP 800 px dạng data URL"),
    ], widths=[4.4, 4.8, 2.8, 5.0], caption="Ước lượng dung lượng dữ liệu", size=12)
    R.p("Từ bảng trên, phần dễ làm đầy bộ nhớ trình duyệt nhất là ảnh của sản phẩm do quản trị viên thêm. Đây là lý do website "
        "thu nhỏ ảnh còn tối đa 800 px và xuất WebP trước khi lưu (quy tắc BR-H03), đồng thời báo lỗi rõ ràng khi bộ nhớ đầy.")
