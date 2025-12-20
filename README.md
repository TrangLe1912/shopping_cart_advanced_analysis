# 🛒 Market Basket Analysis: Advanced Association Rules Mining

![Data Mining](https://img.shields.io/badge/Domain-Data%20Mining-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![Algorithm](https://img.shields.io/badge/Algorithm-FP--Growth%20%26%20Apriori-orange)

Dự án này tập trung vào việc nghiên cứu và áp dụng các kỹ thuật khai phá luật kết hợp (Association Rules Mining) trên dữ liệu bán lẻ thực tế. Chúng tôi đi sâu vào việc so sánh hiệu năng giữa hai thuật toán kinh điển **Apriori** và **FP-Growth**, đồng thời đề xuất các chiến lược kinh doanh dựa trên trọng số giá trị hóa đơn.

---

## 📑 Mục lục
1. [Giới thiệu Pipeline](#giới-thiệu-pipeline)
2. [Thực nghiệm & So sánh Hiệu năng](#thực-nghiệm--so-sánh-hiệu-năng)
3. [Đánh giá Luật theo Giá trị Kinh doanh](#đánh-giá-luật-theo-giá-trị-kinh-doanh)
4. [Trực quan hóa Nâng cao](#trực-quan-hóa-nâng-cao)
5. [Hướng dẫn Cài đặt](#hướng dẫn-cài-đặt)

---

## 🚀 Giới thiệu Pipeline
[cite_start]Dự án được tổ chức theo quy trình chuẩn hóa giúp đảm bảo tính tái sử dụng cao[cite: 20, 21]:

1.  [cite_start]**Data Cleaning**: Xử lý giá trị thiếu, loại bỏ các đơn hàng bị hủy (`C` prefix trong Invoice) để đảm bảo dữ liệu sạch[cite: 45].
2.  [cite_start]**Basket Preparation**: Chuyển đổi dữ liệu giao dịch sang ma trận giỏ hàng Boolean (Basket Matrix) lưu dưới dạng `.parquet` để tối ưu dung lượng[cite: 46, 53].
3.  [cite_start]**Mining Engine**: Triển khai song song `AssociationRulesMiner` (Apriori) và `FPGrowthMiner` (FP-Growth)[cite: 23].
4.  [cite_start]**Validation & Export**: Lọc luật dựa trên các ngưỡng `min_support`, `min_confidence`, và `min_lift` tối ưu, sau đó lưu kết quả ra file `.csv`[cite: 25, 89].

---

## ⚖️ Thực nghiệm & So sánh Hiệu năng (Q2)
Qua thực nghiệm thực tế trên tập dữ liệu 18,021 hóa đơn, chúng tôi rút ra các nhận định quan trọng về độ nhạy tham số:

| Ngưỡng Support | Apriori Time | FP-Growth Time | Trạng thái |
| :--- | :--- | :--- | :--- |
| **0.02 (2%)** | ~1.65 giây | ~6.93 giây | Apriori nhanh hơn ở ngưỡng cao. |
| **0.01 (1%)** | **68.44 giây** | **52.45 giây** | FP-Growth bắt đầu vượt trội. |
| **0.008 (0.8%)** | 251.11 giây | 134.97 giây | Sự chênh lệch hiệu năng rõ rệt. |
| **0.006 (0.6%)** | **FAILED** | **OK** | Apriori lỗi `MemoryError` (Yêu cầu >15GB RAM). |

[cite_start]**Kết luận**: FP-Growth là giải pháp tối ưu cho "mẫu đuôi dài" (long-tail patterns) - những luật có support thấp nhưng mang lại giá trị insight sâu sắc[cite: 77, 95].



---

## 💎 Đánh giá Luật theo Giá trị Kinh doanh
[cite_start]Không chỉ dừng lại ở các chỉ số đếm thông thường, dự án tập trung vào **Chủ đề 3: Đánh giá dựa trên Lift và Trọng số**[cite: 253]:

### 1. Phân loại theo Ma trận BCG (BCG Matrix)
Chúng tôi phân loại các luật kết hợp thành 4 nhóm chiến lược:
* **Stars (Sao)**: Support & Lift đều cao. Đây là các combo chủ lực, cần trưng bày ở khu vực trung tâm cửa hàng.
* **Cash Cows (Bò sữa)**: Support cao nhưng Lift vừa phải. Đây là các sản phẩm thiết yếu, mang lại dòng tiền ổn định.
* **Question Marks (Dấu hỏi)**: Lift cực cao nhưng Support thấp. Đây là các sản phẩm "ngách" đắt tiền, tiềm năng lớn cho Cross-selling.

### 2. Trọng số Doanh thu (Weighted Support)
[cite_start]Thay vì đếm số lần xuất hiện, chúng tôi gán trọng số dựa trên `InvoiceValue`[cite: 183, 194]. 
* [cite_start]**Insight**: Một số luật có tần suất xuất hiện thấp nhưng lại chủ yếu nằm trong các hóa đơn giá trị cao, xứng đáng được ưu tiên trong các chiến dịch Marketing dành cho khách hàng VIP[cite: 188, 263].

---

## 📊 Trực quan hóa Nâng cao
Sử dụng bộ công cụ `DataVisualizer` để tạo ra các báo cáo tương tác:
* **Sunburst Chart**: Phân cấp hành vi mua sắm từ sản phẩm chính đến sản phẩm đi kèm.
* **Parallel Coordinates**: So sánh đa chiều các chỉ số Support, Confidence, Lift và Leverage để tìm ra "điểm ngọt" của luật kết hợp.
* **Network Graph**: Trực quan hóa mối liên hệ giữa các sản phẩm dưới dạng mạng lưới thần kinh, giúp tối ưu hóa sơ đồ mặt bằng cửa hàng.



---

## 🛠 Hướng dẫn Cài đặt

### Yêu cầu hệ thống
* Python 3.9+
* Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
