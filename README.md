# Phân Tích Giỏ Hàng Nâng Cao: Hiểu Hành Vi Mua Sắm Qua Khoa Học Dữ Liệu

## Báo Cáo Tổng Hợp - Phong Cách Feynman

---

## Mục Lục

1. [Vấn Đề Chúng Ta Đang Giải Quyết](#vấn-đề-chúng-ta-đang-giải-quyết)
2. [Dữ Liệu Của Chúng Ta](#dữ-liệu-của-chúng-ta)
3. [Cách Thức Hoạt Động](#cách-thức-hoạt-động)
4. [So Sánh Hai Thuật Toán: Apriori và FP-Growth](#so-sánh-hai-thuật-toán-apriori-và-fp-growth)
5. [Những Phát Hiện Quan Trọng](#những-phát-hiện-quan-trọng)
6. [Phân Tích Có Trọng Số](#phân-tích-có-trọng-số)
7. [Hành Động Cụ Thể](#hành-động-cụ-thể)
8. [Kết Luận](#kết-luận)

---

## Vấn Đề Chúng Ta Đang Giải Quyết

Hãy tưởng tượng bạn sở hữu một cửa hàng bán lẻ trực tuyến. Mỗi ngày có hàng trăm khách hàng vào mua sắm, mỗi người chọn những món hàng khác nhau bỏ vào giỏ. Câu hỏi đặt ra là: Liệu có những sản phẩm nào thường được mua cùng nhau không? Nếu một khách hàng mua sản phẩm A, họ có xu hướng mua sản phẩm B không?

Đây chính xác là vấn đề mà phân tích giỏ hàng (Market Basket Analysis) giải quyết. Nó giống như việc bạn đứng quan sát hàng nghìn người mua sắm và ghi chú lại những mẫu hình lặp lại: "À, người mua bánh mì thường mua bơ", "Người mua tách trà màu hồng thường mua cả tách màu xanh".

Trong dự án này, chúng ta phân tích dữ liệu từ một cửa hàng bán lẻ ở Anh với gần 400,000 giao dịch để tìm ra những mẫu hình này. Chúng ta không chỉ muốn biết sản phẩm nào bán chạy, mà còn muốn hiểu sản phẩm nào "kéo theo" sản phẩm nào khác.

### Tại Sao Điều Này Quan Trọng?

Khi bạn hiểu được khách hàng thường mua gì cùng nhau, bạn có thể:

- Đặt sản phẩm gần nhau trên kệ hoặc trên website
- Gợi ý sản phẩm phù hợp khi khách đang xem một món
- Tạo combo khuyến mãi hấp dẫn
- Lên kế hoạch nhập hàng thông minh hơn
- Tăng doanh thu mà không cần tăng lượng khách

---

## Dữ Liệu Của Chúng Ta

Chúng ta làm việc với bộ dữ liệu "UK Online Retail" - dữ liệu thực tế từ một cửa hàng bán đồ trang trí và quà tặng ở Anh trong khoảng thời gian từ tháng 12/2010 đến tháng 12/2011.

### Những Con Số Ban Đầu

- Tổng số giao dịch gốc: 485,125 giao dịch
- Sau khi làm sạch: 397,924 giao dịch (giữ lại 82%)
- Số sản phẩm khác nhau: 4,372 sản phẩm
- Tổng doanh thu: Hơn 9.7 triệu bảng Anh

### Làm Sạch Dữ Liệu - Bước Quan Trọng Đầu Tiên

Dữ liệu thô luôn có vấn đề. Trong trường hợp này, chúng ta phát hiện:

- Giao dịch bị hủy (InvoiceNo bắt đầu bằng chữ C)
- Số lượng âm (trả hàng)
- Giá bằng 0 hoặc âm (lỗi nhập liệu)
- Mã khách hàng bị thiếu
- Mô tả sản phẩm trống

Tất cả những giao dịch này đều bị loại bỏ vì chúng không phản ánh hành vi mua sắm thật sự. Chúng ta chỉ giữ lại những giao dịch "sạch" - tức là khách hàng thật sự mua và thanh toán cho sản phẩm.

### Chuyển Đổi Dữ Liệu

Dữ liệu ban đầu có dạng như thế này:

```
InvoiceNo | StockCode | Description        | Quantity | Price
536365    | 85123A    | WHITE HANGING...   | 6        | 2.55
536365    | 71053     | WHITE METAL...     | 6        | 3.39
536366    | 22633     | HAND WARMER...     | 6        | 1.85
```

Nhưng để phân tích, chúng ta cần chuyển nó thành dạng "ma trận giỏ hàng":

```
InvoiceNo | WHITE HANGING... | WHITE METAL... | HAND WARMER...
536365    | 1                | 1              | 0
536366    | 0                | 0              | 1
```

Mỗi hàng là một giao dịch, mỗi cột là một sản phẩm. Giá trị 1 nghĩa là "có trong giỏ", 0 nghĩa là "không có". Đây là định dạng mà thuật toán khai thác luật kết hợp yêu cầu.

---

## Cách Thức Hoạt Động

Để tìm ra những sản phẩm thường được mua cùng nhau, chúng ta sử dụng kỹ thuật gọi là "Association Rule Mining" (Khai Thác Luật Kết Hợp). Hãy nghĩ về nó như việc tìm kiếm các mẫu hình "NẾU... THÌ..." trong dữ liệu.

### Khái Niệm Cơ Bản

Một "luật kết hợp" có dạng: NẾU khách hàng mua {Sản phẩm A} THÌ họ cũng mua {Sản phẩm B}

Ví dụ: NẾU mua {WOODEN HEART} THÌ mua {WOODEN STAR}

### Ba Chỉ Số Quan Trọng

Để đánh giá một luật có "tốt" hay không, chúng ta xem xét ba chỉ số:

**1. Support (Độ Hỗ Trợ)**

Đây là tỷ lệ phần trăm giao dịch chứa cả hai sản phẩm. Nó trả lời câu hỏi: "Mẫu hình này xuất hiện thường xuyên như thế nào?"

Công thức: Support(A → B) = Số giao dịch có cả A và B / Tổng số giao dịch

Ví dụ: Nếu có 2.04% giao dịch chứa cả WOODEN HEART và WOODEN STAR, thì support = 0.0204 (hay 2.04%)

**2. Confidence (Độ Tin Cậy)**

Đây là xác suất có điều kiện. Trong số những người mua A, có bao nhiêu phần trăm cũng mua B?

Công thức: Confidence(A → B) = Số giao dịch có cả A và B / Số giao dịch có A

Ví dụ: Nếu có 1000 người mua WOODEN HEART, trong đó 723 người cũng mua WOODEN STAR, thì confidence = 72.3%

**3. Lift (Độ Nâng)**

Đây là chỉ số quan trọng nhất. Lift so sánh xác suất mua B khi đã mua A với xác suất mua B một cách ngẫu nhiên. Nó trả lời: "Việc mua A có thực sự ảnh hưởng đến việc mua B không?"

Công thức: Lift(A → B) = Confidence(A → B) / Support(B)

- Lift > 1: A và B có xu hướng được mua cùng nhau (tích cực)
- Lift = 1: A và B độc lập, không ảnh hưởng lẫn nhau
- Lift < 1: A và B có xu hướng không được mua cùng nhau (tiêu cực)

Ví dụ: Luật WOODEN HEART → WOODEN STAR có Lift = 27.2, nghĩa là khách hàng mua WOODEN HEART có khả năng mua WOODEN STAR cao gấp 27.2 lần so với một khách hàng ngẫu nhiên.

---

## So Sánh Hai Thuật Toán: Apriori và FP-Growth

Để tìm ra những luật kết hợp, chúng ta có thể dùng nhiều thuật toán khác nhau. Trong dự án này, chúng ta so sánh hai thuật toán phổ biến nhất: Apriori và FP-Growth.

### Thuật Toán Apriori - Cách Tiếp Cận Trực Quan

Hãy tưởng tượng bạn muốn tìm nhóm bạn nào thường đi chơi cùng nhau.

**Cách Apriori làm:**

Bước 1: Đếm xem mỗi người đi chơi bao nhiêu lần. Loại bỏ những người ít đi chơi (dưới ngưỡng min_support).

Bước 2: Thử tất cả các cặp đôi từ những người còn lại. Đếm xem mỗi cặp đi chơi cùng nhau bao nhiêu lần. Loại bỏ những cặp ít gặp nhau.

Bước 3: Thử tất cả các nhóm ba người từ những cặp đôi còn lại. Đếm xem mỗi nhóm ba đi chơi cùng nhau bao nhiêu lần.

Cứ thế tiếp tục cho đến khi không còn nhóm nào đủ lớn.

**Ưu điểm:**
- Dễ hiểu, logic rõ ràng
- Cài đặt đơn giản
- Phù hợp với dữ liệu nhỏ

**Nhược điểm:**
- Phải quét dữ liệu nhiều lần (số lần quét = độ dài itemset lớn nhất)
- Sinh ra rất nhiều tập ứng viên phải kiểm tra
- Chậm với dữ liệu lớn

### Thuật Toán FP-Growth - Cách Tiếp Cận Thông Minh

FP-Growth sử dụng một cấu trúc dữ liệu đặc biệt gọi là "FP-Tree" (Frequent Pattern Tree) - giống như cây gia phả, nhưng để lưu trữ giao dịch.

**Cách FP-Growth làm:**

Bước 1: Quét dữ liệu một lần để đếm tần suất mỗi sản phẩm. Sắp xếp theo thứ tự giảm dần.

Bước 2: Quét dữ liệu lần thứ hai để xây dựng FP-Tree. Mỗi nhánh của cây là một chuỗi sản phẩm xuất hiện cùng nhau, với những phần chung được gộp lại.

Bước 3: Khai thác trực tiếp từ cây mà không cần sinh ứng viên.

**Ví dụ minh họa:**

Giả sử có 3 giao dịch:
```
T1: {Sữa, Bánh mì, Bơ}
T2: {Sữa, Bánh mì}
T3: {Sữa, Bơ}
```

FP-Tree sẽ trông như thế này:
```
        Root
          |
        Sữa (3)
        /    \
  Bánh mì (2)  Bơ (1)
      |
    Bơ (1)
```

Cây này lưu trữ tất cả thông tin nhưng rất gọn. Sữa xuất hiện 3 lần, và từ Sữa có thể đi đến Bánh mì (2 lần) hoặc trực tiếp đến Bơ (1 lần).

**Ưu điểm:**
- Chỉ quét dữ liệu 2 lần
- Không sinh ứng viên
- Nhanh hơn Apriori rất nhiều (thường 5-10 lần)
- Hiệu quả với dữ liệu lớn

**Nhược điểm:**
- Phức tạp hơn để hiểu và cài đặt
- Tốn bộ nhớ để lưu FP-Tree
- Khó debug khi có vấn đề

### Kết Quả So Sánh Trên Dữ Liệu Thực Tế

Chúng ta đã chạy cả hai thuật toán trên cùng dữ liệu với cùng tham số:
- min_support = 0.01 (1%)
- max_length = 3
- metric = lift
- min_threshold = 1.0

**Kết quả:**

| Tiêu chí | Apriori | FP-Growth |
|----------|---------|-----------|
| Số itemsets tìm được | 2,814 | 2,814 |
| Số luật tìm được | 176 | 176 |
| Thời gian thực thi | Chậm hơn | Nhanh hơn 5-10 lần |
| Bộ nhớ sử dụng | Thấp | Cao hơn |
| Luật giống nhau | 100% | 100% |

**Phân tích:**

1. Cả hai thuật toán đều tìm ra chính xác 176 luật giống hệt nhau. Điều này chứng minh tính đúng đắn của cả hai phương pháp.

2. FP-Growth nhanh hơn đáng kể. Với dữ liệu 400,000 giao dịch, FP-Growth hoàn thành trong vài giây, trong khi Apriori mất vài chục giây.

3. Sự khác biệt về tốc độ sẽ càng rõ rệt hơn khi dữ liệu lớn hơn hoặc min_support thấp hơn.

**Kết luận:**

Nếu bạn làm việc với dữ liệu nhỏ (vài nghìn giao dịch) và muốn một giải pháp đơn giản, Apriori là lựa chọn tốt.

Nếu bạn làm việc với dữ liệu lớn (hàng trăm nghìn giao dịch trở lên) hoặc cần kết quả nhanh, FP-Growth là lựa chọn ưu tiên.

Trong môi trường sản xuất thực tế với dữ liệu lớn và yêu cầu xử lý nhanh, FP-Growth được khuyên dùng.

---

## Những Phát Hiện Quan Trọng

Sau khi chạy thuật toán, chúng ta tìm được 176 luật kết hợp có ý nghĩa. Dưới đây là những phát hiện quan trọng nhất và ý nghĩa thực tế của chúng.

### Phát Hiện 1: Bộ Sưu Tập Sản Phẩm

Khách hàng có xu hướng mua các sản phẩm trong cùng một "bộ sưu tập" thiết kế.

**Ví dụ điển hình:**

Luật: WOODEN HEART → WOODEN STAR
- Support: 2.04%
- Confidence: 72.3%
- Lift: 27.2

Điều này có nghĩa: Nếu một khách hàng mua trái tim gỗ trang trí, có 72.3% khả năng họ cũng sẽ mua ngôi sao gỗ. Khả năng này cao gấp 27.2 lần so với việc họ mua ngôi sao một cách ngẫu nhiên.

Tương tự với các bộ sưu tập khác:
- PINK REGENCY → GREEN REGENCY (tách trà)
- RED RETROSPOT → BLUE RETROSPOT (chấm bi)
- ALARM CLOCK BAKELIKE → nhiều sản phẩm Bakelike khác

**Hành động kinh doanh:**
- Tạo landing page "Bộ Sưu Tập" để khách dễ tìm các sản phẩm cùng dòng
- Khi khách thêm một sản phẩm vào giỏ, hiển thị "Sản Phẩm Cùng Bộ Sưu Tập"
- Tạo combo giảm giá: "Mua 3 sản phẩm cùng bộ sưu tập giảm 15%"
- Chụp ảnh sản phẩm theo nhóm, không đơn lẻ

### Phát Hiện 2: Sản Phẩm Đôi

Một số sản phẩm luôn được mua theo cặp.

**Ví dụ:**

Luật: JAM MAKING SET → JAM MAKING SET WITH JARS
- Support: 1.29%
- Confidence: 85.7%
- Lift: 66.2

**Hành động kinh doanh:**
- Tạo gói combo cố định cho những sản phẩm này
- Giảm giá khi mua cả hai
- Trong kho, đặt hai sản phẩm gần nhau để dễ lấy hàng
- Khi hết hàng một món, nhập cả hai cùng lúc

### Phát Hiện 3: Sản Phẩm Hub (Trung Tâm)

Một số sản phẩm xuất hiện trong rất nhiều luật - chúng là "trung tâm" kết nối với nhiều sản phẩm khác.

**Top 5 Sản Phẩm Hub:**

1. PINK REGENCY TEACUP: Xuất hiện trong 28 luật
2. GREEN REGENCY TEACUP: 26 luật
3. ROSES REGENCY TEACUP: 24 luật
4. ALARM CLOCK BAKELIKE: 22 luật
5. JUMBO BAG RED RETROSPOT: 20 luật

**Ý nghĩa:**

Những sản phẩm này là "bánh răng" chính của doanh nghiệp. Chúng không chỉ bán chạy mà còn "kéo theo" nhiều sản phẩm khác.

**Hành động kinh doanh:**
- Không bao giờ để những sản phẩm này hết hàng
- Đặt ở vị trí dễ thấy trên website (trang chủ, banner)
- Đầu tư marketing cho những sản phẩm này vì chúng sẽ kéo theo doanh số của nhiều sản phẩm khác
- Theo dõi sát sao xu hướng và phản hồi khách hàng về những sản phẩm này

### Phát Hiện 4: Mẫu Hình Theo Mùa

Một số luật gợi ý hành vi mua sắm theo mùa hoặc dịp lễ.

**Ví dụ:**

Các sản phẩm trang trí (BUNTING, GARLAND, HANGING) thường được mua cùng nhau, gợi ý nhu cầu trang trí cho sự kiện hoặc lễ hội.

**Hành động kinh doanh:**
- Lên lịch marketing theo mùa
- Tạo combo "Trang Trí Tiệc" hoặc "Trang Trí Giáng Sinh"
- Nhập hàng trước mùa cao điểm 2-3 tháng

### Phát Hiện 5: Hành Vi Mua Quà

Nhiều luật liên quan đến sản phẩm làm quà tặng.

**Mẫu hình:**

Khách hàng mua nhiều sản phẩm nhỏ, giá thấp, thiết kế đồng bộ - đặc điểm của việc mua quà tặng số lượng (cho đồng nghiệp, học sinh, khách mời).

**Hành động kinh doanh:**
- Tạo section "Quà Tặng Số Lượng"
- Giảm giá khi mua từ 10 món trở lên
- Cung cấp dịch vụ gói quà miễn phí cho đơn lớn
- Liên hệ các công ty, trường học về nhu cầu quà tặng

### Phát Hiện 6: Sự Đa Dạng Màu Sắc

Khách hàng thích có nhiều lựa chọn màu cho cùng một sản phẩm.

**Ví dụ:**

Bộ tách trà Regency có nhiều màu (PINK, GREEN, ROSES) và khách hàng thường mua nhiều màu cùng lúc.

**Hành động kinh doanh:**
- Luôn nhập đủ màu cho sản phẩm bán chạy
- Marketing nhấn mạnh "Nhiều Màu Sắc Lựa Chọn"
- Tạo bộ quà "Rainbow Set" gồm nhiều màu

### Phát Hiện 7: Mức Giá Ngọt

Phân tích giá của các sản phẩm trong luật kết hợp cho thấy mức giá "ngọt" (sweet spot) là 1-4 bảng Anh.

**Hành động kinh doanh:**
- Phát triển thêm sản phẩm trong khoảng giá này
- Tạo combo để đưa giá trung bình giỏ hàng về mức này
- Định giá sản phẩm mới xung quanh mức này

### Tóm Tắt Business Impact

Nếu triển khai tất cả những phát hiện trên, chúng ta có thể kỳ vọng:

- Tăng 25-40% giá trị đơn hàng trung bình (Average Order Value)
- Tăng 15-30% tỷ lệ chuyển đổi (Conversion Rate)
- Giảm 20% tình trạng tồn kho của sản phẩm kém hiệu quả
- Tăng 35-50% doanh số từ sản phẩm bổ sung (Cross-sell)

---

## Phân Tích Có Trọng Số

Cho đến giờ, chúng ta chỉ xem xét tần suất: sản phẩm nào được mua cùng nhau thường xuyên. Nhưng không phải tất cả giao dịch đều có giá trị bằng nhau.

### Vấn Đề Với Phân Tích Truyền Thống

Xét hai luật:

**Luật A:** Móc khóa 50 cent → Sticker 30 cent
- Xuất hiện trong 5% giao dịch
- Giá trị: 0.8 bảng

**Luật B:** Bộ đồ ăn cao cấp → Khăn trải bàn
- Xuất hiện trong 2% giao dịch
- Giá trị: 50 bảng

Phân tích truyền thống sẽ ưu tiên Luật A vì tần suất cao hơn. Nhưng từ góc độ doanh thu, Luật B quan trọng hơn gấp nhiều lần.

### Giải Pháp: Weighted Association Rules

Chúng ta tính toán các chỉ số mới có tính đến giá trị giao dịch:

**Weighted Support:**

Thay vì đếm số lần xuất hiện, chúng ta tính tổng giá trị của các giao dịch chứa itemset đó, rồi chia cho tổng doanh thu.

Công thức: Weighted_Support(A,B) = Σ(Invoice_Value của giao dịch có A,B) / Tổng Doanh Thu

**Weighted Lift:**

Tương tự, Weighted_Lift xem xét giá trị chứ không chỉ tần suất.

### Phân Loại Sản Phẩm

Dựa trên hai chiều (Tần suất và Giá trị), chúng ta phân sản phẩm thành 4 loại:

**1. Superstars (Siêu Sao)**
- Tần suất cao (>75th percentile)
- Giá trị cao (>75th percentile)
- Đây là sản phẩm vàng: bán chạy và có giá trị cao

**2. Revenue Stars (Ngôi Sao Doanh Thu)**
- Tần suất thấp (<75th percentile)
- Giá trị cao (>75th percentile)
- Bán ít nhưng mỗi lần bán đem lại doanh thu lớn
- Ví dụ: Đồ nội thất cao cấp, bộ quà tặng xa xỉ

**3. Frequency Hubs (Trung Tâm Tần Suất)**
- Tần suất cao (>75th percentile)
- Giá trị thấp (<75th percentile)
- Bán chạy nhưng giá rẻ
- Ví dụ: Móc khóa, sticker, túi nhỏ

**4. Normal (Bình Thường)**
- Tần suất thấp (<75th percentile)
- Giá trị thấp (<75th percentile)
- Sản phẩm thông thường, không nổi bật

### Kết Quả Phân Tích Weighted Rules

Sau khi phân tích top 100 luật theo weighted metrics, chúng ta phát hiện:

**Luật có Weighted Support cao nhất:**

REGENCY TEACUP sets → Có giá trị giao dịch trung bình 45 bảng, cao hơn 3 lần so với giá trị giao dịch trung bình toàn hệ thống (15 bảng).

**Revenue Stars:**

Các sản phẩm trong nhóm này chỉ chiếm 5% tần suất mua hàng nhưng đóng góp 25% tổng doanh thu. Chúng cần được:
- Chăm sóc đặc biệt
- Bán hàng cá nhân hóa
- Marketing cao cấp
- Đảm bảo chất lượng dịch vụ

**Frequency Hubs:**

Các sản phẩm này là "cửa ngõ" đưa khách hàng vào cửa hàng. Chiến lược:
- Giữ giá cạnh tranh để thu hút khách
- Cross-sell lên sản phẩm có giá trị cao hơn
- Sử dụng làm sản phẩm khuyến mãi, quà tặng

### ROI Dự Kiến

Nếu triển khai chiến lược dựa trên weighted rules:

**Đầu tư:**
- Chi phí phân tích và triển khai hệ thống gợi ý: 40,000 - 60,000 bảng
- Thời gian triển khai: 90 ngày

**Lợi nhuận dự kiến (năm đầu):**
- Tăng 36% giá trị đơn hàng trung bình
- Tăng 83% số lượng sản phẩm trên mỗi giỏ hàng
- Tăng 167% tỷ lệ cross-sell thành công

**ROI:** 900% - 1,400% trong năm đầu tiên

---

## Hành Động Cụ Thể

Dựa trên toàn bộ phân tích, đây là kế hoạch hành động 90 ngày:

### Giai Đoạn 1: Tuần 1-4 - Những Thay Đổi Nhanh

**Tuần 1-2:**
1. Tạo 5 landing page "Bộ Sưu Tập" cho các dòng sản phẩm bán chạy nhất
2. Thêm section "Sản Phẩm Thường Mua Cùng" trên trang chi tiết sản phẩm
3. Cập nhật hệ thống tồn kho cho 15 sản phẩm Hub - không bao giờ để hết hàng

**Tuần 3-4:**
1. Tạo 10 combo sản phẩm dựa trên luật có Lift cao nhất
2. Thiết lập giảm giá tự động: "Mua 3 sản phẩm cùng bộ sưu tập giảm 15%"
3. Gửi email marketing đến 20% khách hàng thân thiết với combo mới

### Giai Đoạn 2: Tuần 5-8 - Tối Ưu Hóa

**Tuần 5-6:**
1. Triển khai hệ thống gợi ý thông minh dựa trên giỏ hàng hiện tại
2. A/B test các vị trí hiển thị sản phẩm liên quan
3. Phân tích dữ liệu tuần đầu, điều chỉnh thuật toán

**Tuần 7-8:**
1. Tối ưu hóa trang thanh toán với upsell sản phẩm bổ sung
2. Tạo chương trình "Mua Quà Số Lượng" cho doanh nghiệp
3. Liên hệ 50 công ty tiềm năng

### Giai Đoạn 3: Tuần 9-12 - Mở Rộng Và Tự Động Hóa

**Tuần 9-10:**
1. Tích hợp hệ thống gợi ý vào email tự động
2. Tạo chương trình khách hàng thân thiết với điểm thưởng cho việc mua combo
3. Phân tích weighted rules theo tháng để phát hiện xu hướng mới

**Tuần 11-12:**
1. Mở rộng phân tích sang phân khúc khách hàng khác nhau
2. Tạo dashboard theo dõi hiệu quả real-time
3. Đào tạo team marketing và sales về cách sử dụng insights

### Theo Dõi Thành Công

Đo lường các chỉ số sau mỗi tuần:

1. Average Order Value (AOV)
2. Items per Transaction
3. Cross-sell Rate
4. Revenue từ combo
5. Tỷ lệ click vào "Sản phẩm liên quan"
6. Tỷ lệ chuyển đổi từ gợi ý

Mục tiêu sau 90 ngày:
- AOV tăng từ 15 lên 20 bảng (+33%)
- Items per Transaction tăng từ 12 lên 22 sản phẩm (+83%)
- Cross-sell rate tăng từ 15% lên 40% (+167%)

---

## Kết Luận

Phân tích giỏ hàng không chỉ là một bài tập kỹ thuật - đó là việc hiểu sâu sắc hành vi khách hàng để đưa ra quyết định kinh doanh thông minh.

### Những Bài Học Chính

**1. Dữ liệu kể câu chuyện**

Đằng sau mỗi luật kết hợp là một câu chuyện về lý do tại sao khách hàng mua những sản phẩm đó. Người mua tách trà hồng cũng mua tách xanh không phải ngẫu nhiên - họ muốn có bộ sưu tập đầy đủ. Hiểu được "tại sao" giúp chúng ta hành động đúng.

**2. Không chỉ về tần suất, mà về giá trị**

Phân tích truyền thống chỉ xem xét tần suất. Nhưng một sản phẩm bán 100 lần với giá 1 bảng không quan trọng bằng sản phẩm bán 20 lần với giá 50 bảng. Weighted analysis giúp chúng ta nhìn thấy điều này.

**3. Hành động quan trọng hơn phân tích**

Phân tích tốt nhất là phân tích dẫn đến hành động. Mỗi insight chúng ta tìm ra đều được chuyển thành kế hoạch hành động cụ thể với timeline và KPI rõ ràng.

**4. Công nghệ là công cụ, không phải mục đích**

Apriori hay FP-Growth, weighted hay non-weighted - đều chỉ là công cụ. Mục đích cuối cùng là hiểu khách hàng tốt hơn và phục vụ họ tốt hơn.

### Áp Dụng Cho Doanh Nghiệp Của Bạn

Nếu bạn đang điều hành một doanh nghiệp bán lẻ, dù online hay offline, bạn có thể áp dụng phương pháp này:

**Bước 1:** Thu thập dữ liệu giao dịch ít nhất 3-6 tháng

**Bước 2:** Làm sạch dữ liệu - loại bỏ giao dịch lỗi, trả hàng

**Bước 3:** Chạy thuật toán Association Rules (bắt đầu với FP-Growth)

**Bước 4:** Phân tích kết quả, tìm patterns có ý nghĩa

**Bước 5:** Chuyển insights thành hành động cụ thể

**Bước 6:** Đo lường kết quả, điều chỉnh

**Bước 7:** Lặp lại mỗi tháng để phát hiện xu hướng mới

### Lời Kết

Dữ liệu là tài sản quý giá nhất của doanh nghiệp trong thời đại này. Nhưng dữ liệu chỉ có giá trị khi chúng ta biết cách khai thác và hành động dựa trên nó.

Phân tích giỏ hàng cho chúng ta một cách nhìn sâu sắc về hành vi khách hàng - những mẫu hình mà mắt thường không thể nhìn thấy trong hàng trăm nghìn giao dịch. Và từ những mẫu hình đó, chúng ta có thể xây dựng chiến lược kinh doanh thông minh, tăng doanh thu và mang lại trải nghiệm tốt hơn cho khách hàng.

Đây không phải là khoa học tên lửa. Đây là khoa học về con người - về cách họ mua sắm, lựa chọn và quyết định. Và đó chính là điều làm cho nó trở nên thú vị và có giá trị.

---

## Phụ Lục: Cấu Trúc Project

### Dữ Liệu
```
data/
├── raw/
│   └── online_retail.csv                 (Dữ liệu gốc 485,125 giao dịch)
└── processed/
    ├── cleaned_uk_data.csv               (Dữ liệu đã làm sạch 397,924 giao dịch)
    ├── basket_bool.parquet               (Ma trận giỏ hàng binary)
    ├── rules_apriori_filtered.csv        (176 luật từ Apriori)
    ├── rules_fpgrowth_filtered.csv       (176 luật từ FP-Growth)
    ├── weighted_rules_analysis.csv       (100 luật có trọng số)
    └── product_segmentation.csv          (Phân loại sản phẩm)
```

### Notebooks
```
notebooks/
├── preprocessing_and_eda.ipynb           (Bước 1: Làm sạch và khám phá dữ liệu)
├── basket_preparation.ipynb              (Bước 2: Tạo ma trận giỏ hàng)
├── apriori_modelling.ipynb               (Bước 3a: Chạy Apriori)
├── fp_growth_modelling.ipynb             (Bước 3b: Chạy FP-Growth)
├── compare_apriori_fpgrowth.ipynb        (Bước 4: So sánh hai thuật toán)
└── advanced_analysis.ipynb               (Bước 5: Phân tích nâng cao + weighted rules)
```

### Công Nghệ Sử Dụng

- Python 3.11
- Pandas (xử lý dữ liệu)
- MLxtend (thuật toán Apriori, FP-Growth)
- Matplotlib, Seaborn (visualization)
- Plotly (biểu đồ tương tác)
- NetworkX (network graph)
- Jupyter Notebook (môi trường phân tích)
- Papermill (tự động hóa pipeline)

### Cách Chạy

**Cài đặt môi trường:**
```bash
conda create -n shopping_env python=3.11
conda activate shopping_env
pip install -r requirements.txt
```

**Chạy toàn bộ pipeline:**
```bash
python run_papermill.py
```

**Hoặc chạy từng notebook riêng lẻ:**
```bash
jupyter notebook notebooks/advanced_analysis.ipynb
```

### Tác Giả

Project được thực hiện bởi: Trang Le

Mục đích: Phân tích Market Basket cho môn Data Mining, học kỳ II năm học 2024-2025

---

Hết.
