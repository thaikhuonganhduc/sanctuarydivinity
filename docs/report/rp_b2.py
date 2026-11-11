# -*- coding: utf-8 -*-
"""PHẦN B - CHƯƠNG 2. INSIGHT KHÁCH HÀNG VÀ QUY TRÌNH NGHIỆP VỤ (chân dung, hành trình khách hàng, SRS)"""

BLUE, GREEN, RED, GRAY = "DDEBF7", "E2EFDA", "FBE5D6", "D9D9D9"

PERSONAS = [
    {
        "title": "Nguyễn Hoàng Khang - Sinh viên tập gym",
        "info": "Nguyễn Hoàng Khang\n**Tuổi**\n21\n**Giới tính**\nNam\n**Nơi ở**\nKý túc xá khu B, ĐHQG TP.HCM\n**Nghề nghiệp**\nSinh viên năm 3",
        "goals": "- Tập gym 5 buổi/tuần, muốn có bộ đồ tập vừa thoải mái vừa thể hiện cá tính, không “đụng hàng” với bạn cùng phòng tập.\n"
                 "- Theo dõi một số athlete trên mạng xã hội, thích mua đồ theo các đợt ra mắt giới hạn.\n"
                 "- Muốn mua online nhanh, biết rõ tổng tiền ngay từ đầu, không phải nhắn tin hỏi giá.",
        "pains": "- Ngân sách có hạn nên rất sợ mua sai size rồi không đổi được.\n"
                 "- Đã từng đặt áo nước ngoài, chờ ba tuần rồi nhận một chiếc áo chật.\n"
                 "- Không thích website rườm rà, nhiều bước, phải tạo tài khoản mới mua được.",
        "journey": [
            ("Hành động", "Thấy athlete đăng ảnh Collection X kèm mã truy cập", "Nhập mã, xem cửa hàng, lọc size M, màu đen", "Dùng công cụ gợi ý size, thêm vào giỏ, nhập mã giảm 10%", "Theo dõi trạng thái đơn trong tài khoản"),
            ("Điểm chạm", "Mạng xã hội, trang cổng có đếm ngược", "Trang chủ, menu Armory, popup sản phẩm", "Popup sản phẩm, giỏ hàng, thanh toán", "Trang Account, email"),
            ("Suy nghĩ", "“Drop này có giới hạn, phải vào sớm”", "“Mẫu nào hợp với mình, size nào vừa?”", "“Tổng bao nhiêu tiền, có phí gì thêm không?”", "“Bao giờ hàng tới?”"),
            ("Cảm xúc", "Tò mò, háo hức", "Thích thú nhưng còn phân vân về size", "Yên tâm khi thấy gợi ý size và tổng tiền rõ ràng", "Hài lòng, muốn chờ drop sau"),
            ("SANCTUARY đáp ứng", "Đồng hồ đếm ngược, lookbook, mã athlete", "Lọc theo size/màu, ảnh theo màu, đánh giá có ảnh", "Gợi ý size ANSUR II, mã giảm giá, phí ship hiển thị trước", "Lịch sử đơn, trạng thái do quản trị viên cập nhật"),
        ],
    },
    {
        "title": "Trịnh Mai Anh - Nhân viên văn phòng yêu thích tập luyện",
        "info": "Trịnh Mai Anh\n**Tuổi**\n26\n**Giới tính**\nNữ\n**Nơi ở**\nQuận 3, TP.HCM\n**Nghề nghiệp**\nNhân viên marketing",
        "goals": "- Tập gym và pilates sau giờ làm, muốn bộ đồ ôm dáng, đẹp đủ để mặc đi cà phê sau buổi tập.\n"
                 "- Thích phong cách tối, huyền bí; sẵn sàng chi tiền cho món đồ chất lượng, ít người có.\n"
                 "- Muốn xem đánh giá có ảnh thật của người mặc trước khi mua.",
        "pains": "- Đồ tập nữ trên sàn thương mại điện tử thường mỏng, nhanh xù, màu sắc khác ảnh.\n"
                 "- Bảng size mỗi hãng một kiểu, khó so với số đo của mình.\n"
                 "- Lo ngại việc để lộ thông tin cá nhân khi tạo tài khoản ở website lạ.",
        "journey": [
            ("Hành động", "Xem bạn bè mặc dòng Selene, hỏi mã truy cập", "Vào khu Sanctuary Selene, xem bodysuit, legging", "Lọc đánh giá dòng nữ 5 sao, xem bảng size, đặt hàng", "Lưu thông tin giao hàng cho lần sau"),
            ("Điểm chạm", "Bạn bè, mạng xã hội", "Khu Selene, popup sản phẩm, popup đánh giá", "Bảng size cm/kg, giỏ hàng, form thanh toán", "Trang Account"),
            ("Suy nghĩ", "“Thương hiệu này có gì khác?”", "“Chất vải có dày không, mặc lên trông thế nào?”", "“Size S hay M?”", "“Lần sau mua nhanh hơn”"),
            ("Cảm xúc", "Tò mò", "Ấn tượng với ảnh và câu chuyện thương hiệu", "Tin tưởng hơn nhờ đánh giá có ảnh thật", "Hài lòng"),
            ("SANCTUARY đáp ứng", "Trang About kể câu chuyện thương hiệu", "Ảnh lớn theo từng màu, thông số chất liệu, cách giặt", "Đánh giá lọc theo dòng và số sao; bảng size theo số đo thật", "Tài khoản lưu hồ sơ, tự điền khi thanh toán; mật khẩu được băm"),
        ],
    },
    {
        "title": "Jordan Reyes - Khách hàng quốc tế",
        "info": "Jordan Reyes\n**Tuổi**\n29\n**Giới tính**\nNam\n**Nơi ở**\nSan Francisco, Hoa Kỳ\n**Nghề nghiệp**\nHuấn luyện viên cá nhân",
        "goals": "- Là huấn luyện viên, cần đồ tập bền, co giãn tốt cho cả ngày đứng lớp.\n"
                 "- Theo dõi một athlete Việt Nam và muốn ủng hộ thương hiệu của cộng đồng đó.\n"
                 "- Muốn biết giá bằng đô la, phí vận chuyển và thuế nhập khẩu trước khi quyết định.",
        "pains": "- Từng bị tính thêm thuế khi nhận hàng quốc tế mà không được báo trước.\n"
                 "- Bảng size châu Á thường nhỏ hơn, lại chỉ có đơn vị cm.\n"
                 "- Thời gian giao hàng quốc tế dài, khó theo dõi.",
        "journey": [
            ("Hành động", "Thấy bài đăng của athlete, vào website bằng mã", "Chọn vùng United States (USD), xem compression", "Nhập chiều cao 6'0\", cân nặng 180 lbs để gợi ý size, xem phí ship, thuế", "Gửi tin nhắn hỏi về thời gian giao"),
            ("Điểm chạm", "Mạng xã hội, trang cổng", "Bộ chọn vùng ở chân trang, cửa hàng", "Gợi ý size (ft-in/lbs), bảng size in/lb, giỏ hàng", "Form liên hệ, trang Shipping/Returns"),
            ("Suy nghĩ", "“Có giao tới Mỹ không?”", "“Giá bao nhiêu đô?”", "“Tổng cộng phải trả bao nhiêu, có thuế không?”", "“Bao lâu thì tới?”"),
            ("Cảm xúc", "Tò mò, hơi e ngại", "Thuận tiện khi giá hiện bằng USD", "Yên tâm khi phí và thuế được ước tính trước", "Được hỗ trợ"),
            ("SANCTUARY đáp ứng", "Giao 15 nước, giao diện tiếng Anh", "Đổi 15 loại tiền tệ theo tỷ giá thật", "Đơn vị ft-in/lbs, phí ship theo khối lượng, thuế nhập khẩu 15% (Mỹ) hiển thị trong giỏ", "Form liên hệ, chính sách thời gian giao theo vùng"),
        ],
    },
]

BR = [
    ("BR-A: Quy tắc truy cập và mã athlete (Access Rules)", "Nhóm quy tắc này quy định ai được vào cửa hàng, vào trang quản trị và cách dùng mã athlete.", [
        ("BR-A01", "Người dùng phải nhập đúng mã ở trang cổng mới xem được các trang bên trong; mở thẳng trang bên trong khi chưa qua cổng sẽ bị chuyển về cổng."),
        ("BR-A02", "Mã nhập vào được kiểm tra theo thứ tự: rỗng → mã quản trị (so sánh giá trị băm SHA-256) → mã athlete đang bật (không phân biệt hoa thường)."),
        ("BR-A03", "Mã quản trị chỉ mở trang quản trị; người có vai trò khách mở trang quản trị sẽ bị chặn."),
        ("BR-A04", "Mã athlete gồm 4 - 30 ký tự: chữ in hoa, số, dấu gạch ngang; không trùng với mã đã có."),
        ("BR-A05", "Chỉ mã đang bật (active) mới dùng được; khi tắt mã cuối cùng đang bật, hệ thống hỏi xác nhận vì sẽ không ai vào được cửa hàng."),
        ("BR-A06", "Vai trò sau khi qua cổng lưu trong phiên làm việc (sessionStorage), đóng tab là phải nhập lại mã."),
    ]),
    ("BR-B: Quy tắc sản phẩm và tồn kho (Product & Inventory Rules)", "Nhóm quy tắc này chi phối việc hiển thị sản phẩm, màu, size và số lượng còn lại.", [
        ("BR-B01", "Sản phẩm bị quản trị viên ẩn hoặc xoá không hiển thị ở cửa hàng; xoá là xoá mềm (đánh dấu deleted), khôi phục được."),
        ("BR-B02", "Màu đã ngừng bán vẫn hiển thị nhưng không chọn được; sản phẩm tồn kho bằng 0 hiện nhãn “Sold out”."),
        ("BR-B03", "Size bán gồm XXS - XXL (hoặc One size với phụ kiện); khách chỉ chọn được size sản phẩm có bán."),
        ("BR-B04", "Sản phẩm có tồn kho từ 10 trở xuống được đưa vào danh sách “sắp hết hàng” ở trang quản trị."),
        ("BR-B05", "Giá niêm yết bằng USD, lớn hơn 0; giá hiển thị bằng tiền khác được quy đổi theo tỷ giá, làm tròn theo từng loại tiền."),
        ("BR-B06", "Sản phẩm do quản trị viên thêm phải có tên không trùng, giá > 0, tồn kho là số nguyên ≥ 0, ít nhất một size và một ảnh (JPG/PNG/WebP ≤ 10 MB)."),
    ]),
    ("BR-C: Quy tắc giỏ hàng (Cart Rules)", "Nhóm quy tắc này đảm bảo giỏ hàng luôn hợp lệ so với dữ liệu sản phẩm.", [
        ("BR-C01", "Mỗi dòng giỏ hàng được xác định bởi bộ ba sản phẩm + màu + size; thêm lại cùng bộ ba thì cộng dồn số lượng."),
        ("BR-C02", "Tổng số lượng của một sản phẩm trong giỏ (mọi màu, size) không vượt quá tồn kho; nút “+” bị khoá khi đạt giới hạn."),
        ("BR-C03", "Số lượng mỗi dòng tối thiểu là 1; muốn bỏ món thì bấm Remove."),
        ("BR-C04", "Khi mở giỏ, món đã bị ẩn, xoá, hết màu hoặc vượt tồn kho được tự bỏ hoặc giảm số lượng, kèm thông báo cho khách."),
        ("BR-C05", "Giỏ hàng lưu trong trình duyệt (localStorage), giữ nguyên khi tắt trình duyệt; giỏ chưa giữ chỗ hàng cho tới khi đặt thành công."),
    ]),
    ("BR-D: Quy tắc đặt hàng và thanh toán (Checkout Rules)", "Nhóm quy tắc này chi phối quá trình chuyển từ giỏ hàng thành đơn hàng.", [
        ("BR-D01", "Mọi ô bắt buộc (họ tên ≥ 2 ký tự, email, SĐT 8 - 15 chữ số, địa chỉ ≥ 5 ký tự, thành phố) phải hợp lệ mới được đặt hàng."),
        ("BR-D02", "Thanh toán bằng thẻ: số thẻ 13 - 19 chữ số và đúng thuật toán Luhn; hạn thẻ dạng MM/YY chưa hết hạn; CVC 3 - 4 chữ số. Chọn PayPal, Apple Pay, Google Pay thì không cần nhập thẻ."),
        ("BR-D03", "Mã giảm giá phải là mã athlete đang bật; giảm 10% tiền hàng; mỗi đơn một mã."),
        ("BR-D04", "Ngay lúc bấm đặt, hệ thống kiểm tra lại giỏ; nếu giỏ vừa thay đổi thì dừng lại để khách xem tổng tiền mới."),
        ("BR-D05", "Đơn mới có mã “SD-” + chuỗi thời gian, trạng thái Processing; đơn hàng và tồn kho được ghi cùng lúc, lỗi thì không ghi gì."),
        ("BR-D06", "Khách đang đăng nhập thì đơn gắn với tài khoản; khách chưa đăng nhập vẫn đặt được (đơn khách vãng lai)."),
    ]),
    ("BR-E: Quy tắc vận chuyển và thuế (Shipping & Tax Rules)", "Nhóm quy tắc này quy định cách tính phí vận chuyển và các loại thuế.", [
        ("BR-E01", "Khối lượng đơn = 0,15 kg bao bì + tổng khối lượng ước tính theo loại của từng món × số lượng."),
        ("BR-E02", "Khối lượng tính cước làm tròn lên mỗi 0,5 kg; phí ship = phí gốc của vùng + giá mỗi kg × khối lượng tính cước."),
        ("BR-E03", "Thuế nhập khẩu = % thuế nhập khẩu × tiền hàng sau giảm giá + phí cố định mỗi món (nếu có)."),
        ("BR-E04", "VAT/GST = % thuế của nước × (tiền hàng sau giảm + phí ship + thuế nhập khẩu); nước không có VAT hiện “None”."),
        ("BR-E05", "Các con số phí và thuế là ước tính để minh hoạ, không phải báo giá thật của hãng vận chuyển."),
    ]),
    ("BR-F: Quy tắc tài khoản (Account Rules)", "Nhóm quy tắc này quy định đăng ký, đăng nhập và bảo vệ thông tin tài khoản.", [
        ("BR-F01", "Mỗi email chỉ đăng ký một tài khoản; email được chuẩn hoá (bỏ khoảng trắng, chữ thường)."),
        ("BR-F02", "Mật khẩu tối thiểu 8 ký tự, có cả chữ và số; ô xác nhận phải trùng mật khẩu."),
        ("BR-F03", "Mật khẩu lưu dạng băm SHA-256 kèm salt 16 byte ngẫu nhiên riêng từng tài khoản, không lưu chữ thô."),
        ("BR-F04", "Đăng nhập sai email hay sai mật khẩu đều báo chung “Incorrect email or password.”."),
        ("BR-F05", "Đổi mật khẩu phải nhập đúng mật khẩu hiện tại; đăng ký xong thì đăng nhập luôn."),
    ]),
    ("BR-G: Quy tắc đánh giá và liên hệ (Review & Contact Rules)", "Nhóm quy tắc này chi phối việc hiển thị đánh giá và tiếp nhận tin nhắn.", [
        ("BR-G01", "Đánh giá được nhóm theo người viết; điểm 4,7 được tính vào nhóm 4 sao khi lọc (làm tròn xuống)."),
        ("BR-G02", "Popup sản phẩm hiện đánh giá đúng sản phẩm; nếu chưa có thì hiện đánh giá mẫu của cùng loại sản phẩm."),
        ("BR-G03", "Form liên hệ bắt buộc tên, email hợp lệ, nội dung; nội dung tối đa 1.000 ký tự."),
        ("BR-G04", "Tin nhắn mới ở trạng thái chưa đọc; số tin chưa đọc hiện trên menu quản trị."),
    ]),
    ("BR-H: Quy tắc quản trị và vận hành (Admin & Operation Rules)", "Nhóm quy tắc này chi phối các thao tác của quản trị viên.", [
        ("BR-H01", "Đơn hàng có 4 trạng thái: Processing, Shipped, Delivered, Cancelled; doanh thu không tính đơn Cancelled."),
        ("BR-H02", "Chuyển đơn sang Cancelled thì cộng lại tồn kho; mở lại đơn đã huỷ thì trừ kho lần nữa."),
        ("BR-H03", "Ảnh sản phẩm tải lên được thu nhỏ còn tối đa 800 px rồi lưu dạng WebP để vừa dung lượng lưu trữ trình duyệt."),
        ("BR-H04", "Ngày ra mắt đặt theo giờ Việt Nam (UTC+7); mặc định 01/12/2026 00:00; có thể khôi phục về mặc định."),
        ("BR-H05", "File khôi phục phải đúng cấu trúc của file sao lưu; bản ghi sai cấu trúc bị từ chối, không ghi đè dữ liệu đang có."),
        ("BR-H06", "Xoá mã athlete không làm thay đổi các đơn hàng cũ đã dùng mã đó."),
    ]),
]

FR = [
    ("FR-01: Nhóm chức năng Truy cập và Phân quyền", [
        ("FR-01.1", "Hiển thị trang cổng", "Hiện đồng hồ đếm ngược, ngày ra mắt, tên bộ sưu tập, lookbook", "Khách"),
        ("FR-01.2", "Nhập mã truy cập", "Kiểm tra mã quản trị và mã athlete, chuyển đến trang tương ứng hoặc báo lỗi", "Khách, Quản trị viên"),
        ("FR-01.3", "Chặn truy cập trái phép", "Chuyển về cổng nếu chưa qua cổng; chặn khách vào trang quản trị", "Hệ thống"),
    ]),
    ("FR-02: Nhóm chức năng Sản phẩm", [
        ("FR-02.1", "Xem danh sách sản phẩm", "Hiện 3 khu nam, nữ, phụ kiện, chia nhóm theo loại; thẻ có ảnh, tên, giá, màu", "Khách"),
        ("FR-02.2", "Lọc và sắp xếp", "Lọc theo size, màu; sắp xếp giá tăng/giảm; xoá bộ lọc", "Khách"),
        ("FR-02.3", "Đổi tiền tệ", "Chọn vùng (15 loại tiền), giá quy đổi theo tỷ giá thật", "Khách"),
        ("FR-02.4", "Xem chi tiết sản phẩm", "Ảnh theo màu, chọn màu, size, số lượng, tồn kho, thông số, đánh giá liên quan", "Khách"),
        ("FR-02.5", "Bảng size và gợi ý size", "Bảng size cm/kg hoặc in/lb; gợi ý size từ chiều cao, cân nặng", "Khách"),
        ("FR-02.6", "Xem và lọc đánh giá", "Popup đánh giá, lọc theo sao, dòng, loại; xem ảnh phóng to", "Khách"),
    ]),
    ("FR-03: Nhóm chức năng Giỏ hàng và Đặt hàng", [
        ("FR-03.1", "Thêm vào giỏ", "Thêm sản phẩm theo màu, size, số lượng; cập nhật số trên biểu tượng giỏ", "Khách"),
        ("FR-03.2", "Quản lý giỏ hàng", "Đổi số lượng, xoá món, xem tạm tính, gợi ý sản phẩm khác", "Khách"),
        ("FR-03.3", "Áp mã giảm giá", "Nhập mã athlete để giảm 10%", "Khách"),
        ("FR-03.4", "Tính phí vận chuyển, thuế", "Tính theo nước nhận và khối lượng đơn", "Hệ thống"),
        ("FR-03.5", "Thanh toán", "Điền thông tin giao hàng, chọn phương thức, kiểm tra dữ liệu, đặt hàng, hiện mã đơn", "Khách"),
    ]),
    ("FR-04: Nhóm chức năng Tài khoản", [
        ("FR-04.1", "Đăng ký", "Tạo tài khoản bằng tên, email, mật khẩu", "Khách"),
        ("FR-04.2", "Đăng nhập, đăng xuất", "Đăng nhập bằng email, mật khẩu; đăng xuất", "Thành viên"),
        ("FR-04.3", "Quản lý hồ sơ", "Sửa tên, SĐT, địa chỉ, thành phố, nước; tự điền khi thanh toán", "Thành viên"),
        ("FR-04.4", "Đổi mật khẩu", "Nhập mật khẩu hiện tại và mật khẩu mới", "Thành viên"),
        ("FR-04.5", "Xem lịch sử đơn hàng", "Danh sách đơn, món hàng, tổng tiền, trạng thái", "Thành viên"),
    ]),
    ("FR-05: Nhóm chức năng Thông tin và Hỗ trợ", [
        ("FR-05.1", "Gửi liên hệ", "Form liên hệ có kiểm tra, đếm ký tự, báo đã gửi", "Khách"),
        ("FR-05.2", "Xem chính sách", "Các tab Shipping/Returns, điều khoản, quyền riêng tư, khả năng truy cập", "Khách"),
        ("FR-05.3", "Xem bản đồ, giới thiệu", "Bản đồ nhúng iframe; trang About", "Khách"),
    ]),
    ("FR-06: Nhóm chức năng Quản trị (Admin Panel)", [
        ("FR-06.1", "Tổng quan", "Doanh thu, số đơn, giá trị đơn trung bình, khách, tin chưa đọc, đơn gần đây, hàng sắp hết, bán chạy", "Quản trị viên"),
        ("FR-06.2", "Quản lý đơn hàng", "Tìm, lọc theo trạng thái, xem chi tiết, đổi trạng thái", "Quản trị viên"),
        ("FR-06.3", "Quản lý sản phẩm", "Thêm có ảnh, sửa giá, tồn kho, nổi bật, ẩn/hiện, xoá mềm, khôi phục, đặt lại", "Quản trị viên"),
        ("FR-06.4", "Xem khách hàng", "Danh sách tài khoản, số đơn, tổng chi tiêu, tìm kiếm", "Quản trị viên"),
        ("FR-06.5", "Quản lý tin nhắn", "Đọc, đánh dấu đã đọc, trả lời qua email, xoá", "Quản trị viên"),
        ("FR-06.6", "Quản lý mã athlete", "Thêm (có gợi ý mã), bật/tắt, sao chép, xoá, đặt lại theo file gốc", "Quản trị viên"),
        ("FR-06.7", "Đặt ngày ra mắt", "Đổi mốc đếm ngược của trang cổng", "Quản trị viên"),
        ("FR-06.8", "Sao lưu, khôi phục", "Tải file sao lưu JSON, khôi phục có kiểm tra, xoá dữ liệu, tạo dữ liệu mẫu", "Quản trị viên"),
    ]),
]

NFR = [
    ("NFR-01: Hiệu năng (Performance)", [
        ("NFR-01.1", "Trang hiển thị nội dung chính nhanh trên máy tính", "LCP ≤ 2,5 s (ngưỡng “tốt” của Core Web Vitals)"),
        ("NFR-01.2", "Bố cục không bị xô lệch khi tải ảnh", "CLS ≤ 0,1"),
        ("NFR-01.3", "Ảnh và video được tối ưu", "Ảnh WebP, video H.264 nén; ảnh ngoài màn hình tải lười (lazy)"),
        ("NFR-01.4", "Dữ liệu chung chỉ tải một lần", "Bảng size, tỷ giá được nhớ tạm (tỷ giá lưu 1 giờ)"),
    ]),
    ("NFR-02: Khả năng sử dụng và truy cập (Usability & Accessibility)", [
        ("NFR-02.1", "Dùng tốt trên mọi kích thước màn hình", "Không cuộn ngang ở 390, 820, 1440 px"),
        ("NFR-02.2", "Người dùng bàn phím, trình đọc màn hình dùng được", "Lighthouse Accessibility ≥ 90; mọi ô nhập có nhãn; Esc đóng popup"),
        ("NFR-02.3", "Thông báo lỗi rõ ràng", "Lỗi hiện ngay dưới ô nhập, bằng câu dễ hiểu"),
        ("NFR-02.4", "Tôn trọng tuỳ chọn giảm chuyển động", "prefers-reduced-motion: dừng video, tắt hiệu ứng"),
    ]),
    ("NFR-03: Bảo mật (Security)", [
        ("NFR-03.1", "Không lưu mật khẩu dạng chữ thô", "SHA-256 + salt riêng từng tài khoản"),
        ("NFR-03.2", "Không lộ mã quản trị trong mã nguồn", "Chỉ lưu giá trị băm của mã"),
        ("NFR-03.3", "Chống chèn mã (XSS)", "Dữ liệu người dùng ghi bằng textContent"),
        ("NFR-03.4", "Truyền dữ liệu an toàn", "Toàn bộ website chạy HTTPS (Vercel)"),
    ]),
    ("NFR-04: Tính ổn định và chịu lỗi (Reliability)", [
        ("NFR-04.1", "Dữ liệu hỏng không làm sập trang", "Kiểm tra cấu trúc khi đọc localStorage, bỏ qua bản ghi sai"),
        ("NFR-04.2", "Không có đơn “nửa vời”", "Ghi đơn và tồn kho cùng lúc, lỗi thì hoàn tác"),
        ("NFR-04.3", "Mất mạng vẫn xem được giá", "Tỷ giá dự phòng khi API không phản hồi"),
        ("NFR-04.4", "Tải dữ liệu lỗi có lối thoát", "Hiện thông báo và nút “Try again” thay vì trang trống"),
    ]),
    ("NFR-05: Khả năng bảo trì và kiểm thử (Maintainability & Testability)", [
        ("NFR-05.1", "Mã nguồn dễ đọc, dễ giải thích", "Chia mô-đun theo nhiệm vụ; chú thích tiếng Việt ở đoạn quan trọng"),
        ("NFR-05.2", "Mã HTML đúng chuẩn", "0 lỗi theo W3C Nu Html Checker"),
        ("NFR-05.3", "Kiểm thử lặp lại được", "Bộ kiểm thử tự động chạy được trên máy và trên bản triển khai"),
        ("NFR-05.4", "Dữ liệu và sơ đồ sinh lại được", "Script Python tạo dữ liệu, sơ đồ; LESS biên dịch bằng npm"),
    ]),
]


def build(R, ctx):
    R.chapter(2, "INSIGHT KHÁCH HÀNG VÀ QUY TRÌNH NGHIỆP VỤ")
    R.h3("2.1. Hành trình cơ bản của khách hàng")
    R.ps(
        "Để thiết kế chức năng sát với nhu cầu, nhóm phác hoạ chân dung và hành trình mua hàng của ba nhóm khách hàng tiêu biểu "
        "của SANCTUARY: sinh viên tập gym, nữ nhân viên văn phòng yêu thích tập luyện và khách hàng quốc tế theo dõi athlete.",
        "Do đây là dự án giả định, chưa có khách hàng thật, các chân dung dưới đây được nhóm **phác hoạ giả định** dựa trên "
        "khách hàng mục tiêu ở Phần A và các nghiên cứu đã trích dẫn, không phải kết quả khảo sát. Mỗi chân dung gồm bảng mô tả "
        "và bản đồ hành trình khách hàng qua bốn giai đoạn: nhận biết, cân nhắc, mua hàng và sau mua.")
    for i, ps in enumerate(PERSONAS, 1):
        R.h4("2.1.%d. %s" % (i, ps["title"]))
        R.table(["Thông tin", "Mục tiêu và mong muốn", "Thách thức và vấn đề"], [(ps["info"], ps["goals"], ps["pains"])],
                widths=[3.8, 6.6, 6.6], caption="Chân dung khách hàng " + ps["info"].split("\n")[0], size=12,
                col_fills=[BLUE, GREEN, RED], center_cols=(0,))
        R.table(["Giai đoạn", "Nhận biết", "Cân nhắc", "Mua hàng", "Sau mua"], [(r[0],) + r[1:] for r in ps["journey"]],
                widths=[2.8, 3.55, 3.55, 3.55, 3.55], caption="Bản đồ hành trình khách hàng " + ps["info"].split("\n")[0],
                size=11, bold_first=True, center_cols=(0,))
        R.p("Từ hành trình trên, nhóm rút ra nhu cầu then chốt của nhóm khách hàng này: " + {
            1: "biết chắc size và tổng tiền trước khi trả tiền, mua nhanh mà không bắt buộc tạo tài khoản. Đây là lý do SANCTUARY "
               "đặt công cụ gợi ý size ngay trong popup sản phẩm và tính phí ship, thuế ngay trong giỏ hàng.",
            2: "tin tưởng vào chất lượng thông qua hình ảnh, đánh giá thật và thông số rõ ràng, đồng thời yên tâm về dữ liệu cá nhân. "
               "Website đáp ứng bằng đánh giá có ảnh lọc theo dòng sản phẩm, bảng size theo số đo thật và mật khẩu được băm.",
            3: "minh bạch chi phí quốc tế và đơn vị đo quen thuộc. Website hỗ trợ đổi 15 loại tiền tệ, đơn vị ft-in/lbs, phí "
               "vận chuyển và thuế nhập khẩu ước tính theo từng nước trước khi đặt hàng.",
        }[i])

    R.h4("2.1.4. Tổng hợp insight khách hàng")
    R.table(["Insight", "Nhóm khách", "Tính năng SANCTUARY đáp ứng"], [
        ("Sợ chọn sai size khi không thử đồ", "Cả ba nhóm", "Bảng size theo số đo thật (cm/kg, in/lb); gợi ý size từ chiều cao, cân nặng"),
        ("Muốn biết tổng chi phí trước khi trả tiền", "Sinh viên, khách quốc tế", "Phí ship theo khối lượng, thuế nhập khẩu, VAT/GST hiện ngay trong giỏ"),
        ("Muốn món đồ ít người có", "Sinh viên, nhân viên văn phòng", "Drop giới hạn, đếm ngược, vào cửa hàng bằng mã athlete"),
        ("Tin vào đánh giá có ảnh thật", "Nhân viên văn phòng", "157 đánh giá có ảnh, lọc theo sao, dòng, loại sản phẩm"),
        ("Không muốn bắt buộc tạo tài khoản", "Sinh viên", "Đặt hàng khách vãng lai; tài khoản là tuỳ chọn"),
        ("Lo về dữ liệu cá nhân", "Nhân viên văn phòng", "Mật khẩu băm kèm salt; chính sách quyền riêng tư rõ ràng"),
        ("Cần giá và đơn vị đo quen thuộc", "Khách quốc tế", "15 loại tiền tệ theo tỷ giá thật; đơn vị ft-in/lbs"),
        ("Cần được hỗ trợ khi có thắc mắc", "Khách quốc tế", "Form liên hệ, câu hỏi nhanh, chính sách giao hàng theo vùng"),
    ], widths=[5.0, 3.8, 8.2], caption="Tổng hợp insight khách hàng và tính năng đáp ứng", size=12)

    R.h3("2.2. Software Requirements Specification (SRS)")
    R.h4("2.2.1. Giới thiệu")
    R.ps(
        "**Mục đích.** Tài liệu đặc tả yêu cầu phần mềm (SRS) mô tả đầy đủ quy tắc nghiệp vụ, yêu cầu chức năng và phi chức "
        "năng của website SANCTUARY, làm căn cứ cho thiết kế, lập trình và kiểm thử.",
        "**Phạm vi.** SANCTUARY là website thương mại điện tử front-end, chạy hoàn toàn trên trình duyệt, gồm phía khách hàng và "
        "phía quản trị; dữ liệu gốc ở file JSON/XML, dữ liệu phát sinh lưu bằng Web Storage.",
        "**Thuật ngữ.** *Drop*: đợt mở bán bộ sưu tập giới hạn. *Athlete*: vận động viên, người có ảnh hưởng hợp tác với thương "
        "hiệu. *Mã athlete*: mã truy cập kiêm mã giảm giá. *Khách vãng lai*: khách đặt hàng không đăng nhập.")
    R.h4("2.2.2. Mô tả tổng quan")
    R.table(["Tác nhân", "Mô tả", "Quyền hạn chính"], [
        ("Khách", "Người đã nhập đúng mã athlete ở trang cổng", "Xem sản phẩm, đánh giá; giỏ hàng; đặt hàng; liên hệ; đăng ký"),
        ("Thành viên", "Khách có tài khoản, kế thừa mọi quyền của khách", "Thêm: đăng nhập, hồ sơ, đổi mật khẩu, lịch sử đơn"),
        ("Quản trị viên", "Người nhập đúng mã quản trị", "Toàn bộ chức năng của trang quản trị"),
        ("Dịch vụ tỷ giá", "Hệ thống bên ngoài open.er-api.com", "Cung cấp tỷ giá cho việc quy đổi tiền tệ"),
    ], widths=[3.2, 6.6, 7.2], caption="Các tác nhân của hệ thống", size=12, bold_first=True)
    R.p("**Môi trường hoạt động:** trình duyệt hiện đại (Chrome, Edge, Firefox, Safari) có bật JavaScript và cho phép lưu "
        "trữ cục bộ; website chạy qua HTTP(S) (Live Server khi phát triển, Vercel khi triển khai). **Ràng buộc:** không có máy "
        "chủ ứng dụng và cơ sở dữ liệu; không dùng framework JavaScript; thư viện ngoài (nếu có) phải tải về trong dự án.")
    R.h4("2.2.3. Quy tắc nghiệp vụ (Business Rules)")
    for title, intro, rows in BR:
        R.p("❖ **" + title + "**", indent=False, keep_next=True)
        R.p(intro)
        R.table(["Mã số", "Mô tả"], rows, widths=[2.4, 14.6], caption=title.split(": ")[1].split(" (")[0], size=12,
                center_cols=(0,))
    R.h4("2.2.4. Yêu cầu chức năng (Functional Requirements)")
    for title, rows in FR:
        R.table(["Mã", "Chức năng", "Mô tả", "Tác nhân"], rows, widths=[2.1, 4.0, 7.9, 3.0], caption=title, size=12,
                center_cols=(0,))
    R.h4("2.2.5. Yêu cầu phi chức năng (Non-functional Requirements)")
    R.p("Mỗi yêu cầu phi chức năng có tiêu chí đo được; kết quả đo thực tế được trình bày ở Phần C, mục 1.5.")
    for title, rows in NFR:
        R.table(["Mã", "Yêu cầu", "Tiêu chí đánh giá"], rows, widths=[2.4, 7.3, 7.3], caption=title, size=12, center_cols=(0,))
    R.h4("2.2.6. Ma trận truy vết yêu cầu")
    R.p("Ma trận truy vết nối mỗi yêu cầu chức năng với use case (Chương 5), quy trình BPMN (Chương 3) và ca kiểm thử (Phần C, "
        "mục 1.5.1), bảo đảm không có yêu cầu nào bị bỏ sót khi thiết kế và kiểm thử.")
    R.table(["Yêu cầu", "Use case", "Quy trình BPMN", "Ca kiểm thử"], [
        ("FR-01.1, FR-01.2", "UC01, UC16", "3.1 Vào website qua cổng", "TC01 - TC03, TC37"),
        ("FR-01.3", "UC16", "3.1 Vào website qua cổng", "TC04, TC05"),
        ("FR-02.1", "UC02", "-", "TC06"),
        ("FR-02.2", "UC02", "-", "TC07, TC08"),
        ("FR-02.3", "UC09", "-", "TC09"),
        ("FR-02.4", "UC03", "3.4 Thêm vào giỏ", "TC10, TC11"),
        ("FR-02.5", "UC04", "Lưu đồ 3.9.2", "TC14, TC15"),
        ("FR-02.6", "UC05", "-", "TC16"),
        ("FR-03.1, FR-03.2", "UC06", "3.4 Thêm vào giỏ", "TC12, TC13, TC17, TC18"),
        ("FR-03.3", "UC08", "3.5 Đặt hàng", "TC20, TC21"),
        ("FR-03.4", "UC07", "3.5 Đặt hàng; lưu đồ 3.9.3", "TC19"),
        ("FR-03.5", "UC07", "3.5 Đặt hàng; lưu đồ 3.9.4, 3.9.5", "TC22 - TC25"),
        ("FR-04.1", "UC11", "3.2 Đăng ký", "TC29, TC30"),
        ("FR-04.2", "UC12", "3.3 Đăng nhập", "TC31, TC32"),
        ("FR-04.5", "UC15", "-", "TC32"),
        ("FR-04.3, FR-04.4", "UC13, UC14", "-", "Chưa có ca tự động (kiểm thử thủ công)"),
        ("FR-05.1", "UC10", "3.7 Liên hệ", "TC26, TC27"),
        ("FR-05.3", "UC10", "-", "TC28"),
        ("FR-06.1, FR-06.8", "UC17, UC24", "-", "TC33, TC38"),
        ("FR-06.2", "UC18", "3.6 Quản trị viên xử lý đơn", "TC34"),
        ("FR-06.3", "UC19", "3.8 Quản trị viên thêm sản phẩm", "TC35, TC36"),
        ("FR-06.6", "UC22", "-", "TC37"),
        ("NFR-02.1", "-", "-", "TC39 - TC41"),
    ], widths=[3.8, 3.2, 6.0, 4.0], caption="Ma trận truy vết yêu cầu - use case - quy trình - kiểm thử", size=11, center_cols=(1, 3))
