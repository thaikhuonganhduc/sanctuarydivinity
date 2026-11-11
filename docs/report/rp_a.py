# -*- coding: utf-8 -*-
"""PHẦN A. HÌNH THÀNH Ý TƯỞNG KINH DOANH"""
import xml.dom.minidom as minidom

from docx_helpers import L

LINE_NAME = {"him": "Sanctuary (nam)", "her": "Sanctuary Selene (nữ)", "unisex": "Accessories (phụ kiện)"}
CAT_NAME = {"compression": "Áo compression", "oversize": "Áo thun oversized", "tops": "Áo stringer, áo tank, baby tee",
            "hoodies": "Hoodie, áo khoác, crewneck", "bottoms": "Quần (cargo, jeans, sweatpants, legging, short)",
            "bodysuits": "Bodysuit", "accessories": "Mũ, phụ kiện"}
ZONE_NAME = {"domestic": "Nội địa Việt Nam", "asia": "Châu Á", "oceania": "Châu Đại Dương", "europe": "Châu Âu",
             "northAmerica": "Bắc Mỹ", "southAmerica": "Nam Mỹ"}


def money(x):
    return ("%.0f" % x) if x == int(x) else ("%.2f" % x).replace(".", ",")


def build(R, ctx):
    W = ctx["web"]
    R.part_heading("A", "HÌNH THÀNH Ý TƯỞNG KINH DOANH")

    # ======================= CHƯƠNG 1 =======================
    R.chapter(1, "TỔNG QUAN ĐỀ TÀI")
    R.h3("1.1. Bối cảnh thực tế")
    R.ps(
        "Thương mại điện tử Việt Nam đang ở giai đoạn tăng trưởng mạnh. Theo báo cáo e-Conomy SEA 2024 của Google, Temasek và "
        "Bain & Company, tổng giá trị hàng hoá giao dịch (GMV) của thương mại điện tử Việt Nam năm 2024 ước đạt khoảng 22 tỷ "
        "USD, tăng 18% so với năm trước và chiếm hơn 60% quy mô nền kinh tế số (Google và cộng sự, 2024). Mua sắm trực tuyến "
        "không còn là lựa chọn phụ mà đã trở thành thói quen của người tiêu dùng trẻ ở các đô thị lớn.",
        "Song song, phong trào tập luyện thể hình phát triển rõ rệt. Khảo sát của Cốc Cốc năm 2024 trên 1.206 người dùng từ "
        "18 tuổi cho thấy fitness và gym là nhóm hoạt động thể thao được quan tâm nhiều thứ hai, chỉ sau bóng đá (Cốc Cốc, "
        "2024). Đi kèm là nhu cầu về trang phục tập luyện vừa có công năng vừa thể hiện cá tính: thị trường athleisure (trang "
        "phục thể thao mặc được cả khi tập lẫn đi chơi) tại Việt Nam được IMARC ước tính đạt khoảng 1,61 tỷ USD năm 2024 và "
        "dự báo tăng trưởng bình quân 7,2% mỗi năm đến 2033 (IMARC Group, n.d.).",
        "Trên thế giới, nhiều thương hiệu đồ tập bán trực tiếp qua website đã thành công nhờ cộng đồng người tập. Gymshark, "
        "một thương hiệu khởi đầu từ cửa hàng trực tuyến, đạt doanh thu 607,3 triệu bảng Anh trong năm tài chính 2024, năm "
        "thứ 12 liên tiếp tăng trưởng (FashionUnited, 2025). Bên cạnh các thương hiệu đại trà, một nhánh nhỏ hơn nhưng có tính "
        "nhận diện rất cao là **luxury gymwear**: thương hiệu nhỏ, thiết kế cầu kỳ, may cắt theo lô và chỉ mở bán theo từng "
        "đợt giới hạn, tiêu biểu như Breathe Divinity (Breathe Divinity, n.d.).",
        "Tuy nhiên, các thương hiệu đồ tập nhỏ thường gặp ba khó khăn khi bán hàng trực tuyến. Một là khách không được thử đồ "
        "nên dễ chọn sai size; trả hàng do sai size là vấn đề lớn nhất của thời trang trực tuyến (Stöcker và cộng sự, 2021). "
        "Hai là website phổ thông không thể hiện được cá tính thương hiệu và cảm giác độc quyền của các đợt drop. Ba là chi phí "
        "xây dựng và vận hành một hệ thống bán hàng đầy đủ khá cao so với quy mô của một thương hiệu mới.")
    R.h3("1.2. Lý do chọn đề tài")
    R.ps(
        "Nhóm chọn đề tài website bán quần áo gym vì đây là lĩnh vực vừa gần gũi với sinh viên vừa có bài toán kinh doanh "
        "rõ ràng. Một thương hiệu luxury gymwear cần nhiều hơn một danh sách sản phẩm: cần trang cổng tạo cảm giác chờ đợi "
        "trước ngày ra mắt, cần phân biệt khách hàng đến từ cộng đồng của athlete nào, cần công cụ giúp khách chọn đúng size, "
        "và cần một trang quản trị đủ để một nhóm nhỏ tự vận hành.",
        "Về mặt học thuật, đề tài đòi hỏi vận dụng gần như toàn bộ nội dung học phần Phát triển Web kinh doanh: thẻ HTML5 có "
        "ngữ nghĩa, biểu mẫu, bảng, khung nhúng; CSS box model, thiết kế đáp ứng, bộ tiền xử lý LESS; JavaScript, mô hình "
        "DOM và xử lý sự kiện; XML và AJAX; hệ thống thương mại điện tử mã nguồn mở và quản trị website. Đồ án cũng là cơ "
        "hội để nhóm đi trọn quy trình từ ý tưởng kinh doanh, phân tích nghiệp vụ, mô hình hoá hệ thống đến lập trình, kiểm "
        "thử và triển khai thực tế.")
    R.h3("1.3. Mục tiêu của đồ án")
    R.h4("1.3.1. Mục tiêu chung")
    R.p("Hiện thực hoá ý tưởng kinh doanh thương hiệu quần áo gym **“SANCTUARY”** bằng một website thương mại điện tử hoàn "
        "chỉnh ở phía người dùng, chạy trực tuyến, có trang quản trị, mô phỏng trọn vẹn mô hình bán hàng theo đợt drop, và "
        "đánh giá được chất lượng bằng số liệu đo đạc khách quan.")
    R.h4("1.3.2. Mục tiêu cụ thể")
    R.p("Website hướng tới khách hàng trẻ yêu thích tập luyện, chủ yếu từ 18 đến 35 tuổi, với các mục tiêu cụ thể sau:")
    R.bullets([
        ("Trải nghiệm người dùng và giao diện:", [
            "Thiết kế giao diện tối, mạnh, cao cấp, thống nhất với nhận diện thương hiệu; ảnh sản phẩm lớn, chữ dễ đọc trên nền đen.",
            "Đảm bảo website đáp ứng (responsive) trên điện thoại, máy tính bảng và máy tính, ưu tiên điện thoại (mobile-first).",
            "Đạt điểm Accessibility của Google Lighthouse từ 90 trở lên dù dùng giao diện nền tối."]),
        ("Chức năng bán hàng:", [
            "Mô phỏng mô hình drop: trang cổng có đồng hồ đếm ngược, vào cửa hàng bằng mã athlete, mã kiêm mã giảm giá 10%.",
            "Xem, lọc, sắp xếp sản phẩm; xem chi tiết theo màu, size, tồn kho; bảng size và gợi ý size từ chiều cao, cân nặng.",
            "Giỏ hàng lưu trên trình duyệt, không cho mua vượt tồn kho; thanh toán có kiểm tra dữ liệu; phí vận chuyển, thuế tính theo nước nhận.",
            "Tài khoản khách hàng: đăng ký, đăng nhập, cập nhật hồ sơ, đổi mật khẩu, xem lịch sử và trạng thái đơn hàng."]),
        ("Quản trị và vận hành:", [
            "Trang quản trị gồm tổng quan doanh thu, đơn hàng, sản phẩm, khách hàng, tin nhắn, mã athlete, ngày ra mắt, sao lưu.",
            "Cài đặt và quản trị thử nền tảng mã nguồn mở WooCommerce để so sánh với cách tự lập trình."]),
        ("Kỹ thuật và học thuật:", [
            "Áp dụng đủ các kỹ thuật trong đề cương: HTML5, CSS3, LESS, JavaScript, DOM, sự kiện, XML, AJAX, iframe.",
            "Mã nguồn chia mô-đun, có chú thích tiếng Việt; mã HTML hợp lệ theo W3C; triển khai trực tuyến trên Vercel."]),
    ])
    R.h3("1.4. Phạm vi và giới hạn của đồ án")
    R.ps(
        "**Phạm vi.** Website gồm 7 trang HTML: trang cổng, trang chủ kiêm cửa hàng, giỏ hàng kèm thanh toán, trang thông tin "
        "(liên hệ và chính sách), giới thiệu thương hiệu, tài khoản và quản trị. Người dùng có ba vai trò: khách (đã nhập mã "
        "athlete), thành viên (khách có tài khoản) và quản trị viên. Dữ liệu mẫu gồm " + str(ctx["n_products"]) + " sản phẩm "
        "với " + str(ctx["n_colors"]) + " biến thể màu, " + str(ctx["n_reviews"]) + " đánh giá có ảnh và 15 nước giao hàng.",
        "**Giới hạn.** Đây là đồ án học tập, không kinh doanh thật. Website không có máy chủ ứng dụng và cơ sở dữ liệu: đơn "
        "hàng, tài khoản và thay đổi của quản trị viên lưu trong bộ nhớ của từng trình duyệt; bảo mật chỉ ở mức mô phỏng phía "
        "máy khách; thanh toán chỉ kiểm tra định dạng số thẻ, không kết nối cổng thanh toán; phí vận chuyển và thuế là số ước "
        "tính. Sản phẩm, hình ảnh và đánh giá mẫu lấy từ breathedivinity.com để làm dữ liệu học tập; nhóm không dùng tên và "
        "logo của thương hiệu này. Chân trang mọi trang đều ghi “Student project, not a real store”.")

    # ======================= CHƯƠNG 2 =======================
    R.chapter(2, "CONCEPT ART – HÀNH TRÌNH CỦA SANCTUARY")
    R.h3("2.1. Câu chuyện hình thành ý tưởng")
    R.p("*Câu chuyện dưới đây là câu chuyện thương hiệu do nhóm sáng tác để định hướng thiết kế (concept), nhân vật và tình "
        "huống là giả định. Hình minh hoạ là ảnh lookbook dùng trên trang cổng của website.*", indent=False)
    R.figure(ctx["root"] / "assets" / "images" / "home-01.webp", "Ảnh lookbook mở đầu câu chuyện SANCTUARY", height=11)
    R.ps(
        "Năm giờ sáng, phòng tập ở một con hẻm quận Thủ Đức vẫn còn tối. Khang, sinh viên năm ba, là người đầu tiên đẩy cửa "
        "bước vào. Anh không tập để chụp ảnh hay để chạy theo trào lưu. Với Khang, mỗi buổi sáng ở đây là một nghi thức: "
        "tiếng tạ chạm sàn, hơi thở đều đặn, và khoảng lặng sau hiệp tập cuối cùng. Nơi này là chốn trú ẩn của anh, nơi anh "
        "được là chính mình mà không cần xin phép ai.",
        "Nhưng mỗi lần chọn đồ tập, Khang lại thấy lạc lõng. Quần áo thể thao trên thị trường hoặc quá ồn ào với khẩu hiệu và "
        "logo to, hoặc quá nhạt nhẽo. Không bộ đồ nào nói lên được cảm giác của những giờ tập không ai nhìn thấy. Thỉnh thoảng "
        "anh đặt một chiếc áo từ thương hiệu nước ngoài, chờ ba tuần, rồi nhận về một chiếc áo chật vì không biết chọn size nào.")
    R.figure(ctx["root"] / "assets" / "images" / "home-03.webp", "Hình ảnh “giờ tập không ai nhìn thấy” trong lookbook", height=11)
    R.ps(
        "Từ những buổi sáng như vậy, ý tưởng về **SANCTUARY** ra đời: một thương hiệu dành cho “những giờ không ai nhìn thấy”. "
        "Không khẩu hiệu ồn ào. Đen trên nền đen, đường cắt sát cơ thể, hoạ tiết lấy cảm hứng từ những ô cửa nhà thờ cổ và "
        "kim loại. Nhìn từ xa thì trầm lặng, nhìn gần thì không thể quên.",
        "SANCTUARY không có danh mục bán quanh năm. Mỗi bộ sưu tập ra mắt một lần, số lượng giới hạn, bán hết là khép lại mãi "
        "mãi. Ai mặc nó là người đã đến sớm. Và để không ai phải chờ ba tuần rồi nhận một chiếc áo sai size, website SANCTUARY "
        "có công cụ gợi ý size học từ số đo cơ thể của hàng nghìn người thật. Câu chuyện của Khang cũng là câu chuyện của "
        "những khách hàng mà SANCTUARY hướng tới: người trẻ coi phòng tập là chốn trú ẩn, và muốn bộ đồ của mình kể được điều đó.")
    R.figure(ctx["root"] / "assets" / "images" / "home-07.webp", "Bộ sưu tập Collection X: “nhìn xa trầm lặng, nhìn gần không thể quên”", height=11)

    R.h3("2.2. Giới thiệu về mô hình kinh doanh SANCTUARY")
    R.h4("2.2.1. Tên thương hiệu và ý nghĩa")
    R.p("**Sanctuary** nghĩa là chốn trú ẩn, nơi linh thiêng. Thương hiệu nhìn phòng tập không phải như một nghĩa vụ hay một "
        "trào lưu, mà như một nghi thức mỗi người tự giữ cho riêng mình. Dòng sản phẩm nữ mang tên **Sanctuary Selene** (Selene "
        "là nữ thần mặt trăng trong thần thoại Hy Lạp), gợi vẻ đẹp mạnh mẽ nhưng huyền bí. Tuyên ngôn thương hiệu, dùng ở trang "
        "About: *“A sanctuary is where you go to be unbroken.”* (Chốn trú ẩn là nơi bạn đến để không gục ngã).")
    R.h4("2.2.2. Logo thương hiệu")
    R.p("Logo SANCTUARY dùng chữ gothic có gai, như được khắc lên cánh cửa nhà thờ cổ, thể hiện cảm giác bước vào một căn "
        "phòng đầy tạ và quyết định rằng mình thuộc về nơi đó. Logo có ba phiên bản màu: trắng trên nền đen (dùng chính trên "
        "website), đen trên nền sáng và đỏ cho điểm nhấn (" + R.next_fig() + ").")
    R.figure(ctx["root"] / "assets" / "logo" / "logo.png", "Logo thương hiệu SANCTUARY", width=9)
    R.h4("2.2.3. Bảng màu và phông chữ")
    R.p("Bảng màu tối giản, lấy đen làm chủ đạo để ảnh sản phẩm nổi bật, chỉ dùng một màu nhấn là đỏ thương hiệu. Các màu "
        "được khai báo thành biến CSS trong `css/base.css` để dùng thống nhất trên mọi trang (" + R.next_fig() + "). Tiêu đề "
        "dùng phông Angel Wish (dáng chữ gothic), nội dung dùng Times New Roman in hoa, giãn chữ rộng, tạo cảm giác sang trọng.")
    R.figure(ctx["comp"] / "palette.png", "Bảng màu chính của thương hiệu SANCTUARY", width=15)
    R.h4("2.2.4. Mô hình kinh doanh")
    R.p("SANCTUARY kinh doanh theo mô hình **bán trực tiếp cho người tiêu dùng (D2C)** qua website, kết hợp **bán theo đợt "
        "giới hạn (drop)** và **tiếp thị qua người có ảnh hưởng (athlete)**. " + R.next_tab() + " tóm tắt mô hình theo khung "
        "Business Model Canvas.")
    R.table(["Thành phần", "Nội dung"], [
        ("Phân khúc khách hàng", "Nam, nữ 18 - 35 tuổi tập gym thường xuyên, ở đô thị, thích phong cách tối, cá tính; khách quốc tế từ cộng đồng của athlete"),
        ("Giá trị cung cấp", "Đồ tập cao cấp thiết kế độc quyền, số lượng giới hạn; gợi ý size dựa trên dữ liệu; trải nghiệm thương hiệu nhất quán"),
        ("Kênh phân phối", "Website SANCTUARY (duy nhất); mạng xã hội của athlete dẫn về website"),
        ("Quan hệ khách hàng", "Cộng đồng theo từng athlete; tài khoản thành viên lưu lịch sử đơn; hỗ trợ qua form liên hệ, email"),
        ("Dòng doanh thu", "Bán sản phẩm theo từng drop (giá niêm yết USD, 40 - 150 USD/món); phí vận chuyển thu theo đơn"),
        ("Nguồn lực chính", "Thiết kế, hoạ tiết độc quyền; cộng đồng athlete; website và dữ liệu sản phẩm"),
        ("Hoạt động chính", "Thiết kế bộ sưu tập, sản xuất theo lô, tổ chức drop, vận hành đơn hàng, chăm sóc khách"),
        ("Đối tác chính", "Xưởng may cut-and-sew, đơn vị vận chuyển quốc tế, cổng thanh toán, các athlete"),
        ("Cơ cấu chi phí", "Sản xuất theo lô, hoa hồng cho athlete (qua mã giảm giá), vận chuyển, hosting website (gói miễn phí của Vercel)"),
    ], widths=[4.2, 12.8], caption="Mô hình kinh doanh SANCTUARY theo Business Model Canvas", bold_first=True, size=12)
    R.h4("2.2.5. Mô hình drop và cộng đồng athlete")
    R.ps(
        "Mỗi bộ sưu tập (hiện tại là **Collection X**) có một ngày ra mắt. Trước ngày đó, trang cổng của website hiện đồng hồ "
        "đếm ngược và ảnh lookbook để khơi gợi sự chờ đợi. Cửa hàng không mở công khai: khách vào bằng **mã truy cập** do từng "
        "athlete chia sẻ cho cộng đồng của mình. Cùng mã đó dùng làm **mã giảm giá 10%** khi thanh toán, nhờ vậy thương hiệu "
        "biết đơn hàng đến từ cộng đồng của ai để tính hiệu quả hợp tác.",
        "Khi một bộ sưu tập bán hết, nó được khép lại vĩnh viễn: không tái sản xuất, không giảm giá. Chính sách này tạo tính "
        "khan hiếm, vốn được chứng minh là làm tăng giá trị cảm nhận và ý định mua của người tiêu dùng trẻ Việt Nam đối với "
        "sản phẩm phiên bản giới hạn (Ha, 2021).")
    R.figure(W / "01-gate.png", "Trang cổng với đồng hồ đếm ngược tới ngày ra mắt Collection X", width=15)
    R.h4("2.2.6. Lộ trình một đợt drop")
    R.p("Mỗi bộ sưu tập đi qua bốn giai đoạn; website hỗ trợ từng giai đoạn bằng các chức năng cụ thể (kế hoạch giả định cho "
        "Collection X):")
    R.table(["Giai đoạn", "Thời gian", "Hoạt động kinh doanh", "Website hỗ trợ"], [
        ("Chuẩn bị", "4 - 6 tuần trước", "Hoàn thiện thiết kế, sản xuất lô đầu, chụp lookbook, chọn athlete", "Quản trị viên thêm sản phẩm, ảnh, tồn kho; tạo mã athlete"),
        ("Khởi động", "2 tuần trước", "Athlete đăng ảnh, chia sẻ mã truy cập; công bố ngày ra mắt", "Trang cổng đếm ngược, lookbook; đặt ngày ra mắt"),
        ("Mở bán", "Ngày ra mắt", "Khách vào cửa hàng bằng mã, đặt hàng trong số lượng giới hạn", "Cửa hàng, gợi ý size, giỏ hàng, thanh toán, mã giảm giá"),
        ("Sau mở bán", "1 - 4 tuần sau", "Xử lý đơn, giao hàng, hỗ trợ khách, đánh giá hiệu quả từng athlete", "Quản lý đơn, tin nhắn, tổng quan doanh thu, đơn theo mã giảm giá"),
        ("Khép lại", "Khi bán hết", "Bộ sưu tập ngừng bán vĩnh viễn, chuẩn bị drop sau", "Ẩn sản phẩm, tắt mã, sao lưu dữ liệu"),
    ], widths=[2.6, 2.8, 6.0, 5.6], caption="Lộ trình một đợt drop và chức năng website hỗ trợ", size=12, bold_first=True)

    # ======================= CHƯƠNG 3 =======================
    R.chapter(3, "XÁC ĐỊNH MỤC TIÊU CHIẾN LƯỢC")
    R.h3("3.1. Tuyên bố định hướng thị trường")
    R.bullets([
        "**Tầm nhìn:** trở thành thương hiệu luxury gymwear được nhận diện rõ nhất trong cộng đồng tập luyện trẻ tại Việt Nam và Đông Nam Á.",
        "**Sứ mệnh:** may những bộ đồ dành cho “những giờ không ai nhìn thấy”, giúp người tập tự tin thể hiện mình, và giúp họ mua đúng size ngay lần đầu.",
        ("**Giá trị cốt lõi:**", [
            "*Độc quyền:* mỗi thiết kế chỉ ra mắt một lần, số lượng giới hạn.",
            "*Tay nghề:* cắt may theo lô, đường may phẳng ở vùng vận động, vải dày dặn.",
            "*Minh bạch:* giá niêm yết rõ, phí vận chuyển và thuế hiển thị trước khi đặt, gợi ý size dựa trên dữ liệu thật.",
            "*Cộng đồng:* lớn lên cùng các athlete và những người theo dõi họ."]),
        "**Định vị:** đồ tập cao cấp, phong cách tối và gai góc, giá trung - cao (40 - 150 USD/món), bán trực tuyến theo đợt giới hạn.",
    ])
    R.h3("3.2. Phân tích thị trường")
    R.h4("3.2.1. Tổng quan thị trường")
    R.ps(
        "**Thương mại điện tử.** Việt Nam đứng thứ ba Đông Nam Á về quy mô thương mại điện tử với GMV khoảng 22 tỷ USD năm "
        "2024, tăng 18%; thương mại điện tử chiếm hơn 60% nền kinh tế số (Google và cộng sự, 2024). Người tiêu dùng trẻ đã "
        "quen mua quần áo trực tuyến, là điều kiện thuận lợi cho một thương hiệu chỉ bán qua website.",
        "**Trang phục thể thao.** Thị trường athleisure Việt Nam ước đạt khoảng 1,61 tỷ USD năm 2024, dự báo tăng trưởng "
        "7,2%/năm giai đoạn 2025 - 2033 (IMARC Group, n.d.). Trên thế giới, các mô hình bán trực tiếp qua website như Gymshark "
        "cho thấy tiềm năng của đồ tập gắn với cộng đồng: doanh thu năm tài chính 2024 đạt 607,3 triệu bảng (FashionUnited, 2025).",
        "**Thói quen tập luyện.** Fitness và gym là nhóm hoạt động được người Việt quan tâm nhiều thứ hai sau bóng đá; rào "
        "cản chính khi tập là thời gian (32,7%), không gian (27,4%) và chi phí (26,2%) (Cốc Cốc, 2024). Người đã vượt qua "
        "các rào cản này và tập đều đặn là nhóm sẵn sàng đầu tư cho trang phục, đúng với khách hàng mục tiêu của SANCTUARY.")
    R.h4("3.2.2. Khách hàng mục tiêu")
    R.table(["Tiêu chí", "Mô tả"], [
        ("Nhân khẩu học", "Nam và nữ 18 - 35 tuổi; sinh viên năm cuối, người mới đi làm, người làm nghề tự do; thu nhập trung bình khá trở lên"),
        ("Địa lý", "Đô thị lớn tại Việt Nam (TP. Hồ Chí Minh, Hà Nội, Đà Nẵng); khách quốc tế theo dõi các athlete (Mỹ, châu Âu, châu Á)"),
        ("Tâm lý", "Coi tập luyện là một phần bản sắc; thích phong cách tối, gothic, streetwear; muốn sở hữu món đồ ít người có"),
        ("Hành vi", "Tập 3 - 6 buổi/tuần; theo dõi athlete trên mạng xã hội; mua đồ theo đợt ra mắt; quen thanh toán trực tuyến"),
        ("Nỗi lo khi mua", "Sợ chọn sai size; lo phí vận chuyển, thuế phát sinh; lo hàng giả, hàng kém chất lượng"),
    ], widths=[3.6, 13.4], caption="Chân dung khách hàng mục tiêu của SANCTUARY", bold_first=True, size=12)
    R.h4("3.2.3. Đối thủ cạnh tranh")
    R.table(["Nhóm đối thủ", "Đặc điểm", "Điểm SANCTUARY khác biệt"], [
        ("Thương hiệu thể thao lớn toàn cầu", "Danh mục rộng, giá đa dạng, bán quanh năm qua nhiều kênh", "Thiết kế độc quyền, số lượng giới hạn, phong cách riêng"),
        ("Thương hiệu gymwear D2C (ví dụ Gymshark)", "Bán trực tuyến, cộng đồng athlete mạnh, phong cách tối giản", "Phong cách gothic cao cấp; vào cửa hàng bằng mã athlete"),
        ("Luxury gymwear quốc tế (ví dụ Breathe Divinity)", "Hoạ tiết cầu kỳ, drop giới hạn, giá cao, giao quốc tế lâu", "Gợi ý size theo dữ liệu; hiện phí ship và thuế theo nước trước khi đặt"),
        ("Đồ tập nội địa, hàng phổ thông", "Giá rẻ, mua nhanh trên sàn thương mại điện tử", "Chất lượng, trải nghiệm thương hiệu và tính độc quyền"),
    ], widths=[4.4, 6.3, 6.3], caption="Phân tích nhóm đối thủ cạnh tranh", size=12)
    R.h4("3.2.4. Phân tích SWOT")
    R.table(["ĐIỂM MẠNH (STRENGTHS)", "ĐIỂM YẾU (WEAKNESSES)"], [(
        "- ***Nhận diện khác biệt:*** phong cách gothic, đen trên đen, hoạ tiết cầu kỳ, khó nhầm lẫn.\n"
        "- ***Tính độc quyền:*** mỗi thiết kế chỉ ra mắt một lần, tạo động lực mua sớm.\n"
        "- ***Gợi ý size dựa trên dữ liệu:*** học từ số đo của hơn 6.000 người, giảm rủi ro chọn sai size.\n"
        "- ***Minh bạch chi phí:*** phí vận chuyển, thuế hiển thị theo nước trước khi đặt hàng.\n"
        "- ***Chi phí vận hành thấp:*** website tĩnh, hosting miễn phí, triển khai tự động.",
        "- ***Thương hiệu mới:*** chưa có độ tin cậy và lượng khách quen.\n"
        "- ***Phụ thuộc athlete:*** doanh số phụ thuộc vào độ phủ của người giới thiệu.\n"
        "- ***Giá cao:*** khó tiếp cận sinh viên thu nhập thấp.\n"
        "- ***Hạ tầng còn đơn giản:*** chưa có máy chủ, cơ sở dữ liệu và cổng thanh toán thật.\n"
        "- ***Quy mô sản xuất nhỏ:*** chi phí mỗi sản phẩm cao, khó đáp ứng khi nhu cầu tăng đột biến.")],
        widths=[8.5, 8.5], caption="Phân tích SWOT (phần 1)", size=12, col_fills=["BDD7EE", "F8CBAD"])
    R.table(["CƠ HỘI (OPPORTUNITIES)", "THÁCH THỨC (THREATS)"], [(
        "- ***Thương mại điện tử tăng trưởng:*** GMV Việt Nam khoảng 22 tỷ USD năm 2024, tăng 18%.\n"
        "- ***Phong trào tập luyện:*** fitness là mối quan tâm thể thao lớn thứ hai của người Việt.\n"
        "- ***Athleisure:*** thị trường khoảng 1,61 tỷ USD, tăng khoảng 7%/năm.\n"
        "- ***Văn hoá drop và streetwear:*** người trẻ quen săn hàng giới hạn.\n"
        "- ***Mạng xã hội:*** athlete giúp tiếp cận khách quốc tế với chi phí thấp.",
        "- ***Cạnh tranh mạnh:*** từ thương hiệu lớn và hàng giá rẻ trên sàn.\n"
        "- ***Hàng nhái:*** thiết kế nổi bật dễ bị sao chép.\n"
        "- ***Chi phí vận chuyển, thuế quốc tế:*** làm tăng giá cuối của khách nước ngoài.\n"
        "- ***Thị hiếu thay đổi nhanh:*** phong cách có thể lỗi thời.\n"
        "- ***Rủi ro an ninh mạng:*** khi chuyển sang thanh toán thật cần đầu tư bảo mật.")],
        widths=[8.5, 8.5], caption="Phân tích SWOT (phần 2)", size=12, col_fills=["C6E0B4", "FFE699"])
    R.h4("3.2.5. Định hướng chiến lược từ SWOT")
    R.table(["Chiến lược", "Nội dung"], [
        ("S-O (phát huy điểm mạnh, nắm cơ hội)", "Dùng mô hình drop + mã athlete để khai thác văn hoá săn hàng giới hạn và mạng xã hội; quảng bá công cụ gợi ý size như một lợi thế khi mua trực tuyến"),
        ("W-O (khắc phục điểm yếu nhờ cơ hội)", "Hợp tác nhiều athlete ở nhiều nước để giảm phụ thuộc một người; khi doanh số tăng thì đầu tư máy chủ, cổng thanh toán hoặc chuyển lên WooCommerce"),
        ("S-T (dùng điểm mạnh chống thách thức)", "Bảo hộ thiết kế, nhấn mạnh tính độc quyền và tay nghề để chống hàng nhái; hiển thị minh bạch phí ship, thuế để giảm bỏ giỏ"),
        ("W-T (giảm điểm yếu, tránh thách thức)", "Sản xuất theo lô nhỏ, bán hết mới làm lô mới để hạn chế tồn kho; tăng cường bảo mật trước khi nhận thanh toán thật"),
    ], widths=[5.0, 12.0], caption="Định hướng chiến lược rút ra từ phân tích SWOT", bold_first=True, size=12)

    R.h3("3.3. Mục tiêu chiến lược")
    R.p("Từ định hướng thị trường và phân tích SWOT, nhóm đặt các mục tiêu chiến lược theo tiêu chí SMART (cụ thể, đo được, "
        "khả thi, liên quan, có thời hạn) cho giai đoạn ra mắt Collection X. Đây là mục tiêu **giả định** cho kịch bản kinh "
        "doanh của đồ án; mục tiêu về website được đo thật ở Phần C.")
    R.table(["Nhóm mục tiêu", "Mục tiêu SMART", "Cách đo"], [
        ("Doanh số", "Bán hết 70% tồn kho Collection X trong 30 ngày đầu sau ngày ra mắt 01/12/2026", "Tồn kho còn lại, doanh thu ở trang tổng quan quản trị"),
        ("Cộng đồng athlete", "Hợp tác ít nhất 5 athlete ở 3 nước, mỗi mã mang về ít nhất 30 đơn trong drop đầu", "Số đơn theo mã giảm giá trong dữ liệu đơn hàng"),
        ("Trải nghiệm mua", "Tỷ lệ yêu cầu đổi hàng do sai size dưới 5% số đơn", "Tin nhắn chủ đề “Returns and exchanges” trên tổng số đơn"),
        ("Chất lượng website", "Lighthouse Accessibility ≥ 90, LCP desktop ≤ 2,5 s ở mọi trang trước ngày ra mắt", "Báo cáo Lighthouse sau mỗi lần triển khai"),
        ("Khách hàng thân thiết", "30% khách của drop đầu tạo tài khoản thành viên", "Số tài khoản trên số khách đặt hàng"),
    ], widths=[3.4, 8.0, 5.6], caption="Mục tiêu chiến lược theo tiêu chí SMART", size=12, bold_first=True)
    R.h3("3.4. Chiến lược marketing hỗn hợp (4P)")
    R.table(["Thành phần", "Chiến lược của SANCTUARY"], [
        ("Product (Sản phẩm)", "- Đồ tập cao cấp cắt may theo lô: compression, áo oversized, stringer, hoodie, quần, bodysuit, phụ kiện.\n"
                               "- Hoạ tiết gothic độc quyền, bảng màu tối; mỗi thiết kế chỉ ra mắt một lần.\n"
                               "- Thông tin đầy đủ: chất liệu, định lượng vải, kiểu dáng, cách giặt, bảng size theo số đo thật."),
        ("Price (Giá)", "- Định giá cao cấp 40 - 150 USD/món, thể hiện tính độc quyền.\n"
                        "- Không giảm giá theo mùa; ưu đãi duy nhất là 10% qua mã athlete để thưởng cho cộng đồng.\n"
                        "- Giá hiển thị theo 15 loại tiền tệ; phí ship, thuế hiển thị trước khi đặt."),
        ("Place (Phân phối)", "- Bán trực tiếp qua website, không qua sàn hay đại lý để giữ trải nghiệm thương hiệu.\n"
                              "- Giao hàng từ TP. Hồ Chí Minh tới 15 nước, phân theo 6 vùng."),
        ("Promotion (Xúc tiến)", "- Trang cổng đếm ngược và lookbook tạo sự chờ đợi trước ngày ra mắt.\n"
                                 "- Athlete chia sẻ mã truy cập cho cộng đồng; mã kiêm giảm giá giúp đo hiệu quả từng người.\n"
                                 "- Đánh giá có ảnh thật của khách làm bằng chứng xã hội."),
    ], widths=[3.8, 13.2], caption="Chiến lược marketing hỗn hợp 4P", size=12, bold_first=True)
    R.h3("3.5. Phân tích mô hình năm áp lực cạnh tranh")
    R.table(["Áp lực", "Mức độ", "Phân tích"], [
        ("Cạnh tranh giữa các đối thủ hiện tại", ("Cao", "F8CBAD"), "Nhiều thương hiệu thể thao lớn và thương hiệu gymwear trực tuyến; SANCTUARY cạnh tranh bằng phong cách riêng và tính độc quyền thay vì giá."),
        ("Nguy cơ đối thủ mới gia nhập", ("Cao", "F8CBAD"), "Rào cản thấp với thương hiệu bán trực tuyến; lợi thế phòng thủ là cộng đồng athlete và nhận diện thương hiệu đã xây dựng."),
        ("Sản phẩm thay thế", ("Trung bình", "FFF2CC"), "Đồ thể thao phổ thông giá rẻ có thể thay thế về công năng nhưng không thay thế được giá trị thể hiện cá tính."),
        ("Quyền thương lượng của người mua", ("Trung bình", "FFF2CC"), "Khách có nhiều lựa chọn, nhưng sản phẩm giới hạn làm giảm độ nhạy về giá với khách hàng mục tiêu."),
        ("Quyền thương lượng của nhà cung cấp", ("Trung bình", "FFF2CC"), "Xưởng cut-and-sew sản xuất lô nhỏ thường đòi giá cao; cần xây quan hệ lâu dài với một vài xưởng uy tín."),
    ], widths=[4.6, 2.4, 10.0], caption="Phân tích năm áp lực cạnh tranh của Porter", size=12, center_cols=(1,))

    # ======================= CHƯƠNG 4 =======================
    R.chapter(4, "DỊCH VỤ VÀ QUY TẮC KINH DOANH")
    R.h3("4.1. Dịch vụ")
    R.h4("4.1.1. Dòng sản phẩm")
    R.p("Bộ sưu tập Collection X gồm " + str(ctx["n_products"]) + " mẫu sản phẩm thuộc ba dòng. Giá niêm yết bằng USD; khách "
        "xem được giá quy đổi sang 15 loại tiền tệ theo tỷ giá thật. Các bảng dưới lấy trực tiếp từ dữ liệu `data/products.json` "
        "của website.")
    products = ctx["products"]
    for gender in ("him", "her", "unisex"):
        rows = []
        for p in [x for x in products if x["gender"] == gender]:
            rows.append((p["id"].upper(), p["name"], CAT_NAME.get(p["category"], p["category"]).split(",")[0].split("(")[0].strip(),
                         str(len(p["colors"])), ", ".join(p["sizes"]) if len(p["sizes"]) < 3 else p["sizes"][0] + " - " + p["sizes"][-1],
                         money(p["price"])))
        R.table(["Mã", "Tên sản phẩm", "Loại", "Số màu", "Size", "Giá (USD)"], rows,
                widths=[1.4, 6.4, 3.3, 1.5, 2.2, 2.2], caption="Bảng giá dòng " + LINE_NAME[gender], size=11,
                center_cols=(0, 3, 4, 5), align_cells=L)
    R.h4("4.1.2. Dịch vụ đi kèm")
    R.bullets([
        "**Gợi ý size:** khách nhập chiều cao, cân nặng (cm/kg hoặc ft-in/lbs), website gợi ý size phù hợp kèm lưu ý theo kiểu dáng.",
        "**Bảng size chi tiết:** vòng ngực, vòng eo, chiều cao, cân nặng theo từng size, đổi được giữa cm/kg và in/lb.",
        "**Hiển thị giá theo vùng:** chọn vùng ở chân trang để xem giá bằng tiền địa phương.",
        "**Giao hàng quốc tế:** 15 nước, phí vận chuyển và thuế ước tính hiển thị ngay trong giỏ hàng.",
        "**Tài khoản thành viên:** lưu thông tin giao hàng, tự điền khi thanh toán, theo dõi trạng thái đơn.",
        "**Hỗ trợ khách hàng:** form liên hệ, câu hỏi thường gặp, chính sách rõ ràng; phản hồi trong 48 giờ.",
    ])
    R.h3("4.2. Quy tắc kinh doanh")
    R.h4("4.2.1. Quy tắc truy cập và mã athlete")
    R.bullets([
        "Cửa hàng chỉ mở cho người nhập đúng mã truy cập đang hoạt động; mã không phân biệt chữ hoa, chữ thường.",
        "Mỗi athlete có một mã riêng (4 - 30 ký tự gồm chữ in hoa, số, dấu gạch ngang); quản trị viên có thể tạm tắt hoặc xoá mã.",
        "Mã athlete kiêm mã giảm giá 10% trên tiền hàng; mỗi đơn chỉ dùng một mã, không cộng dồn, không quy đổi tiền mặt.",
        "Thương hiệu có quyền vô hiệu hoá mã bị lạm dụng hoặc chia sẻ ngoài cộng đồng được cấp.",
    ])
    R.h4("4.2.2. Quy tắc giá, tồn kho và drop")
    R.bullets([
        "Giá niêm yết bằng USD; giá quy đổi sang tiền khác chỉ để tham khảo, số tiền cuối cùng là số trong giỏ hàng.",
        "Mỗi sản phẩm có số lượng tồn kho; khách không thể thêm vào giỏ vượt quá số còn lại (tính cả các màu, size khác của cùng sản phẩm đã có trong giỏ).",
        "Sản phẩm trong giỏ chưa được giữ chỗ cho tới khi đặt hàng thành công; tồn kho được trừ ngay khi đơn được ghi nhận.",
        "Màu đã ngừng bán vẫn hiển thị để khách biết nhưng không chọn được; sản phẩm hết hàng hiện nhãn “Sold out”.",
        "Bộ sưu tập bán hết là khép lại, không tái sản xuất, không giảm giá.",
    ])
    R.h4("4.2.3. Quy tắc vận chuyển và thuế")
    R.p("Phí vận chuyển tính theo vùng của nước nhận và khối lượng đơn hàng. Khối lượng đơn = 0,15 kg bao bì + khối lượng ước "
        "tính theo loại của từng món; khối lượng tính cước làm tròn lên mỗi 0,5 kg. Phí = phí gốc của vùng + giá mỗi kg × khối "
        "lượng tính cước. Thuế nhập khẩu và VAT/GST tính theo quy định ước tính của từng nước. Số liệu lấy từ `data/shipping.xml`:")
    doc = minidom.parse(str(ctx["root"] / "data" / "shipping.xml"))
    zones = {z.getAttribute("id"): (z.getAttribute("base"), z.getAttribute("perKg")) for z in doc.getElementsByTagName("zone")}
    countries = {}
    for c in doc.getElementsByTagName("country"):
        countries.setdefault(c.getAttribute("zone"), []).append(c.getAttribute("name"))
    R.table(["Vùng", "Phí gốc (USD)", "Giá mỗi kg (USD)", "Các nước"],
            [(ZONE_NAME[z], b, k.replace(".", ","), ", ".join(countries.get(z, []))) for z, (b, k) in zones.items()],
            widths=[3.6, 2.6, 2.8, 8.0], caption="Bảng phí vận chuyển theo vùng", size=12, center_cols=(1, 2))
    rows = []
    for c in doc.getElementsByTagName("country"):
        tax = c.getElementsByTagName("tax")[0]
        duty = c.getElementsByTagName("duty")[0]
        d = []
        if duty.getAttribute("pct") != "0":
            d.append(duty.getAttribute("pct") + "% giá hàng")
        if duty.getAttribute("perItemUsd") != "0":
            d.append(duty.getAttribute("perItemUsd").replace(".", ",") + " USD/món")
        rows.append((c.getAttribute("name"), tax.getAttribute("label"), tax.firstChild.data.replace(".", ",") + "%", " + ".join(d) or "Không"))
    R.table(["Nước", "Loại thuế", "Thuế suất", "Thuế nhập khẩu"], rows, widths=[4.6, 4.0, 2.8, 5.6],
            caption="Thuế ước tính theo nước nhận hàng", size=12, center_cols=(2,))
    R.h4("4.2.4. Quy tắc đổi trả và huỷ đơn")
    R.bullets([
        "Mọi giao dịch là cuối cùng: không đổi trả vì đổi ý, màu sắc hay kích cỡ; khách được khuyến khích dùng công cụ gợi ý size trước khi mua.",
        "Ngoại lệ là sản phẩm bị lỗi, hư hỏng hoặc giao sai: khách gửi email trong vòng 48 giờ kể từ khi nhận hàng, kèm mã đơn và ảnh sản phẩm, nhãn vận chuyển.",
        "Yêu cầu hợp lệ được đổi sản phẩm cùng loại nếu còn hàng; nếu hết hàng thì hoàn bằng tín dụng mua sắm.",
        "Đơn đã xử lý không thể huỷ; khi quản trị viên huỷ đơn, số lượng được cộng lại vào tồn kho.",
        "Thời gian xử lý 1 - 3 ngày làm việc; thời gian giao dự kiến từ 2 - 4 ngày (Việt Nam) đến 10 - 20 ngày (Nam Mỹ).",
    ])
    R.h4("4.2.5. Quy tắc tài khoản và dữ liệu khách hàng")
    R.bullets([
        "Khách mua được mà không cần tài khoản (đơn khách vãng lai); có tài khoản thì đơn được gắn vào lịch sử của tài khoản.",
        "Mật khẩu tối thiểu 8 ký tự, có cả chữ và số; mỗi email chỉ đăng ký một tài khoản.",
        "Website không lưu mật khẩu dạng chữ thô và không lưu đầy đủ thông tin thẻ thanh toán.",
        "Khách có quyền xem, sửa thông tin cá nhân; mọi dữ liệu mẫu chỉ dùng cho mục đích học tập.",
    ])
    R.h3("4.3. Tính năng dự kiến")
    R.p("Để đáp ứng mô hình kinh doanh trên, website **“SANCTUARY”** được thiết kế với các nhóm tính năng sau:")
    feats = [
        ("Trang cổng và truy cập bằng mã", "Trang đầu tiên khách nhìn thấy, gồm đồng hồ đếm ngược tới ngày ra mắt, tên bộ sưu tập và ảnh lookbook. Khách nhập mã athlete để vào cửa hàng; quản trị viên nhập mã quản trị để vào trang quản trị. Người chưa qua cổng mở thẳng trang bên trong sẽ bị đưa về cổng."),
        ("Duyệt sản phẩm", "Trang chủ có video giới thiệu, sau đó là cửa hàng chia ba khu nam, nữ, phụ kiện, mỗi khu chia nhóm theo loại sản phẩm. Menu Armory ở mép trái cho phép lọc theo size, màu và sắp xếp theo giá; khách đổi được tiền tệ hiển thị theo vùng."),
        ("Chi tiết sản phẩm và gợi ý size", "Bấm vào sản phẩm mở cửa sổ chi tiết: ảnh trượt theo màu, chọn màu, size, số lượng theo tồn kho, thông số chất liệu, bảng size và công cụ gợi ý size, cùng các đánh giá liên quan."),
        ("Đánh giá khách hàng", "Cửa sổ đánh giá hiện điểm trung bình, bộ lọc theo số sao, dòng nam/nữ, loại sản phẩm; mỗi đánh giá có ảnh thật của khách, xem phóng to được."),
        ("Giỏ hàng và thanh toán", "Sửa số lượng, xoá món, áp mã giảm giá, chọn nước nhận để tính phí vận chuyển và thuế, điền thông tin giao hàng và thanh toán có kiểm tra dữ liệu, nhận mã đơn sau khi đặt."),
        ("Tài khoản thành viên", "Đăng ký, đăng nhập qua cửa sổ nổi; trang tài khoản cho sửa hồ sơ, đổi mật khẩu, xem lịch sử và trạng thái đơn; thanh toán tự điền thông tin."),
        ("Thông tin và hỗ trợ", "Trang Info gồm liên hệ (form, bản đồ, câu hỏi nhanh) và các chính sách: giao hàng/đổi trả, điều khoản, điều khoản dịch vụ, quyền riêng tư, khả năng truy cập. Trang About kể câu chuyện thương hiệu."),
        ("Quản trị cửa hàng", "Tổng quan doanh thu và chỉ số, quản lý đơn hàng, sản phẩm (thêm, sửa, ẩn, xoá), khách hàng, tin nhắn, mã athlete, ngày ra mắt, sao lưu và khôi phục dữ liệu."),
    ]
    for i, (t, d) in enumerate(feats, 1):
        R.h5("4.3.%d. %s" % (i, t))
        R.p(d)
