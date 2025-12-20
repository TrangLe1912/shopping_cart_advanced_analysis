# Shopping Cart Advanced Analysis: From Frequency to Financial Value

**Báo cáo Dự án Phân tích Dữ liệu Bán lẻ**
Dự án này triển khai quy trình khai phá dữ liệu toàn diện, đi từ các thuật toán cơ bản (Apriori, FP-Growth) để tìm kiếm tần suất, đến việc xây dựng mô hình đánh giá giá trị kinh tế (Weighted Analysis) nhằm đưa ra các chiến lược kinh doanh cụ thể.

---

## MỤC LỤC
1. [Phần 1: Khái niệm, Ý tưởng & Thí nghiệm Hiệu năng](#phần-1-khái-niệm-ý-tưởng--thí-nghiệm-hiệu-năng)
2. [Phần 2: Chủ đề Nâng cao - Trọng số & Giá trị Kinh doanh](#phần-2-chủ-đề-nâng-cao---trọng-số-và-giá-trị-kinh-doanh)
3. [Cấu trúc Dự án & Hướng dẫn Cài đặt](#cấu-trúc-dự-án--hướng-dẫn-cài-đặt)

---

## PHẦN 1: KHÁI NIỆM, Ý TƯỞNG & THÍ NGHIỆM HIỆU NĂNG

### 1. Khái niệm cốt lõi (Core Concepts)
Dự án dựa trên kỹ thuật **Association Rule Mining (Khai phá luật kết hợp)**, hay còn gọi là bài toán phân tích giỏ hàng, sử dụng 3 chỉ số chính:
- **Support (Độ hỗ trợ):** Tần suất xuất hiện của một bộ sản phẩm.
- **Confidence (Độ tin cậy):** Xác suất khách mua sản phẩm B khi đã mua A.
- **Lift (Độ nâng):** Thước đo sức mạnh liên kết thực sự (Lift > 1: Liên kết tích cực; Lift < 1: Liên kết tiêu cực/ngẫu nhiên).

### 2. So sánh Thuật toán & Ý tưởng Thí nghiệm
Chúng tôi so sánh hai thuật toán phổ biến nhất:
- **Apriori:**
    - *Cơ chế:* Duyệt chiều rộng, sinh các tập ứng viên (candidates) và quét lại cơ sở dữ liệu nhiều lần để kiểm tra.
    - *Nhược điểm:* Khi dữ liệu lớn hoặc ngưỡng Support thấp, số lượng ứng viên bùng nổ theo cấp số nhân, gây tốn kém bộ nhớ và thời gian.
- **FP-Growth (Frequent Pattern Growth):**
    - *Cơ chế:* Nén dữ liệu vào cấu trúc cây **FP-Tree**. Không sinh ứng viên, chỉ quét cơ sở dữ liệu 2 lần.
    - *Ưu điểm:* Tốc độ xử lý nhanh vượt trội trên tập dữ liệu lớn.

### 3. Kết quả Thí nghiệm (Tốc độ thay đổi theo Tần suất)
Dựa trên file `compare_apriori_fpgrowth.ipynb`, kết quả cho thấy:
- **Khi Min Support cao (Luật phổ biến):** Cả hai thuật toán có tốc độ tương đương.
- **Khi Min Support thấp (Luật hiếm/Long-tail):**
    - Thời gian chạy của **Apriori tăng vọt (Exponential)** do bùng nổ tổ hợp.
    - Thời gian chạy của **FP-Growth tăng tuyến tính (Linear)** và ổn định.
-> **Kết luận:** FP-Growth là lựa chọn tối ưu cho hệ thống khuyến nghị thực tế.

---

## PHẦN 2: CHỦ ĐỀ NÂNG CAO - TRỌNG SỐ VÀ GIÁ TRỊ KINH DOANH

Đây là trọng tâm của dự án (trong file `nhom3.ipynb`), giải quyết bài toán: *"Làm sao tìm ra luật mang lại nhiều tiền nhất chứ không chỉ là bán chạy nhất?"*

### 1. Mục tiêu & Vấn đề
Các thuật toán truyền thống chỉ đếm số lượng (Frequency). Một luật bán 100 lần gói tăm bông (giá trị thấp) có thể có Support cao hơn luật bán 5 lần Tủ lạnh (giá trị cao). Điều này dẫn đến các quyết định kinh doanh sai lệch nếu chỉ dựa vào Support.

### 2. Giải pháp: Weighted Association Rules
Chúng tôi áp dụng hệ thống trọng số dựa trên doanh thu:
- **Weighted Support:** Mỗi giao dịch được nhân với tổng giá trị đơn hàng (Revenue).
- **Zhang's Metric:** Sử dụng để đo độ kết dính tuyệt đối (-1 đến 1), giúp loại bỏ các luật có Lift cao "ảo" do nghịch lý thống kê.

### 3. Phân nhóm Chiến lược (BCG Matrix Strategy)
Dựa trên tương quan giữa **Support (Tần suất)** và **Weighted Support (Giá trị)**, chúng tôi chia luật thành 3 nhóm chiến lược:

#### Nhóm 1: "Ngôi sao" (Stars)
- **Đặc điểm:** Support Cao & Doanh thu Cao (Lift > 1).
- **Ý nghĩa:** Sản phẩm Best-seller, dòng tiền chính của doanh nghiệp.
- **Chiến lược:**
    - Marketing đại chúng (Mass marketing).
    - Đặt vị trí đẹp nhất (Prime location).
    - Tạo bundle cứng để tối ưu vận hành.

#### Nhóm 2: "Ẩn số giá trị cao" (Hidden Gems)
- **Đặc điểm:** Support Thấp nhưng Weighted Support/Lợi nhuận Cao.
- **Ý nghĩa:** Hàng xa xỉ, hàng chuyên dụng hoặc đơn hàng số lượng lớn (B2B). Ít người mua nhưng mua là "đậm".
- **Chiến lược:**
    - Cá nhân hóa (Personalized Marketing) cho khách VIP.
    - Upsell trực tiếp qua nhân viên tư vấn.
    - Không quảng cáo tràn lan để tiết kiệm chi phí.

#### Nhóm 3: "Phổ thông" (Cash Cows / Dogs)
- **Đặc điểm:** Support Cao nhưng Giá trị thấp, hoặc Lift $\approx$ 1.
- **Ý nghĩa:** Hàng thiết yếu, mua theo thói quen (Ví dụ: Bánh mì, trứng).
- **Chiến lược:**
    - **Tối ưu chi phí:** Không chi tiền quảng cáo.
    - **Mồi nhử (Loss Leader):** Giảm giá nhẹ để kéo traffic, sau đó điều hướng khách sang mua Nhóm 1 hoặc 2.

---

## CẤU TRÚC DỰ ÁN & HƯỚNG DẪN CÀI ĐẶT

### Cấu trúc Thư mục (Project Structure)
```text
shopping_cart_advanced_analysis/
├── data/
│   ├── raw/                  # Dữ liệu gốc (online_retail.csv)
│   └── processed/            # Dữ liệu đã làm sạch & kết quả luật
├── notebooks/
│   ├── preprocessing_and_eda.ipynb   # Làm sạch & Phân tích khám phá
│   ├── basket_preparation.ipynb      # Chuẩn bị dữ liệu giỏ hàng
│   ├── fp_growth_modelling.ipynb     # Mô hình FP-Growth cơ bản
│   ├── nhom3.ipynb                   # PHÂN TÍCH TÀI CHÍNH (CHỦ ĐỀ 3)
│   └── runs/                         # Log kết quả chạy tự động
├── report_images/                    # Chứa biểu đồ xuất ra (Sunburst, Parallel...)
├── src/                              # Thư viện hàm (apriori_library.py)
├── run_papermill.py                  # Script chạy tự động toàn bộ pipeline
└── requirements.txt                  # Các thư viện cần thiết