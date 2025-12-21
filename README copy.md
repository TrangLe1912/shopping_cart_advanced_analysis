# 🛒 Market Basket Analysis: Khi Tốc độ gặp Lợi nhuận
# Frequent vs. High-Utility: Cuộc chiến giữa "Số Lượng" và "Chất Lượng"
> **"Dữ liệu không nói dối, nhưng cách chúng ta đặt câu hỏi (Tần suất hay Lợi nhuận) sẽ quyết định câu trả lời đáng giá bao nhiêu tiền."**


![Data Mining](https://img.shields.io/badge/Domain-Data%20Mining-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![Algorithm](https://img.shields.io/badge/Algorithm-FP--Growth%20%26%20Apriori-orange)
 ![Header](https://capsule-render.vercel.app/api?type=waving&height=300&color=gradient&text=WL-Win%20for%20Life&textBg=false&rotate=1&desc=Blog%202%20%20%20Cuộc%20chiến%20giữa%20"số%20lượng"%20và%20"chất%20lượng"&descAlign=50&descSize=20)
--
Dự án này thực hiện phân tích giỏ hàng (Market Basket Analysis) trên bộ dữ liệu bán lẻ thực tế (**UK Online Retail**). Điểm nhấn của dự án là sự chuyển dịch tư duy từ **Khai phá tập phổ biến (Frequent Itemset Mining)** truyền thống sang **Khai phá tập giá trị cao (High-Utility Itemset Mining - HUIM)** để tối ưu hóa doanh thu thực tế.
> **Case Study:** Online Retail Dataset (UCI)  
> **Chủ đề:** So sánh Apriori vs. FP-Growth & Đột phá tư duy với High-Utility Mining  
> **Thực hiện bởi:** Nhóm 3 - WL (Win for Life)

## 👥 Thông tin Nhóm
| Vai trò | Thành viên | 
| :--- | :--- | 
| **Leader** | [Nguyễn Văn Vinh] | 
| **Member** | [Bạch Ngọc Lương] |
| **Member** | [Đỗ Văn Vinh] | 
| **Member** | [Lại Thành Đoàn] | 
---

## 📑 Mục lục
1. [Giới thiệu Pipeline](#giới-thiệu-pipeline)
2. [Thực nghiệm & So sánh Hiệu năng](#thực-nghiệm--so-sánh-hiệu-năng)
3. [Đánh giá Luật theo Giá trị Kinh doanh](#đánh-giá-luật-theo-giá-trị-kinh-doanh)
4. [Trực quan hóa Nâng cao](#trực-quan-hóa-nâng-cao)
5. [Hướng dẫn Cài đặt](#hướng dẫn-cài-đặt)

---

## 🛠 Pipeline Xử lý

Chúng tôi áp dụng quy trình **Hybrid Approach**:
1.  **Tiền xử lý:** Làm sạch đơn hủy, lọc dữ liệu rác từ `online_retail.csv`.
2.  **Lọc ứng viên:** Dùng FP-Growth với `min_support` thấp (0.5%) để tìm tất cả các tập hợp tiềm năng.
3.  **Tính toán Utility:** Áp dụng hàm trọng số: 
            $Utility = \sum (Quantity \times UnitPrice)$.
4.  **Xếp hạng:** So sánh Top Frequent vs. Top Utility.
---

## ⚖️ Thực nghiệm & So sánh Hiệu năng (Q2)
Qua thực nghiệm thực tế trên tập dữ liệu 18,021 hóa đơn, chúng tôi rút ra các nhận định quan trọng về độ nhạy tham số:

| Ngưỡng Support | Apriori Time | FP-Growth Time | Trạng thái |
| :--- | :--- | :--- | :--- |
| **0.02 (2%)** | ~1.65 giây | ~6.93 giây | Apriori nhanh hơn ở ngưỡng cao. |
| **0.01 (1%)** | **68.44 giây** | **52.45 giây** | FP-Growth bắt đầu vượt trội. |
| **0.008 (0.8%)** | 251.11 giây | 134.97 giây | Sự chênh lệch hiệu năng rõ rệt. |
| **0.006 (0.6%)** | **FAILED** | **210 giây** | Apriori lỗi `MemoryError` (Yêu cầu >15GB RAM). |

[cite_start]**Kết luận**: FP-Growth là giải pháp tối ưu cho "mẫu đuôi dài" (long-tail patterns) - những luật có support thấp nhưng mang lại giá trị insight sâu sắc[cite: 77, 95].



---
## ⚔️ Thực nghiệm 1: Apriori vs FP-Growth

Chúng tôi đã kiểm tra độ nhạy tham số của hai thuật toán bằng cách giảm dần ngưỡng `min_support`.
![Comparison Chart](images/output3.png)
### Kết quả hiệu năng:
| Ngưỡng Support | Apriori Time | FP-Growth Time | Luật sinh ra | Kết luận |
| :--- | :--- | :--- | :--- | :--- |
| **0.02** | ~2.24s | ~7.20s | 218 | Apriori nhanh hơn ở tập dữ liệu thưa. |
| **0.015** | 5.38s | 13.69s | 738 | FP-Growth bắt đầu vượt trội. |
| **0.01** | 79.33s | **78.57s** | 4376 | FP-Growth bắt đầu vượt trội. |
| **0.008** | 269.13s | **201.89s** | 12876 | FP-Growth vượt trội hơn rõ rệt. |

**Nhận xét:** Apriori không có khả năng mở rộng (non-scalable) khi cần đào sâu vào dữ liệu (support thấp) do bùng nổ tổ hợp ứng viên. FP-Growth với cấu trúc cây nén là lựa chọn bắt buộc cho Big Data.

---

## 💎 Thực nghiệm 2: High-Utility Mining (Advanced)

> *Đây là phần mở rộng nâng cao nhằm tối ưu hóa theo Lợi nhuận (Utility) thay vì Tần suất (Support).*

### Vấn đề của phương pháp truyền thống
Các thuật toán như FP-Growth thường bỏ qua các sản phẩm giá trị cao nhưng ít người mua (Support thấp).

### Kết quả đối chứng (Mindset Shift)
Chúng tôi đã tìm ra sự khác biệt lớn giữa Top sản phẩm bán chạy (Frequent) và Top sản phẩm lợi nhuận (High-Utility):

![Comparison Chart](images/output2.png)
*(Biểu đồ Scatter Plot cho thấy vùng "Hidden Gems" - nơi Support thấp nhưng Utility cực cao)*

| Xếp hạng | Top Tần Suất (Support) | Top Giá Trị (Utility) | Ý nghĩa |
| :--- | :--- | :--- | :--- |
| **#1** | *White Hanging Heart T-Light* | **DOTCOM POSTAGE** | Doanh thu Online (Phí ship) là nguồn thu khổng lồ. |
| **#2** | *Regency Cakestand 3 Tier* | **Jumbo Bag + Postage** | Combo túi cỡ lớn + Ship đi tỉnh. |
| **#3** | *Jumbo Bag Red Retrospot* | **Regency Cakestand 3 Tier** | Sản phẩm "Ngôi sao" toàn diện. |
| **#4** | *Party Bunting* | **Jam Making Set (Support 1.6%)** | **Mỏ vàng bị bỏ quên!** |

### Phát hiện đắt giá: "Jam Making Set"
* **Support:** `0.016` (1.6%) -> *Sẽ bị Apriori loại bỏ vì < 2%.*
* **Utility:** `~$141,646` -> *Top 5 Doanh thu toàn công ty.*
👉 **Kết luận:** High-Utility Mining giúp doanh nghiệp không bỏ lỡ các dòng tiền ẩn từ nhóm khách hàng ngách (Niche Market).

---

## 💡 Insight Kinh doanh & Chiến lược

Dựa trên kết quả khai phá dữ liệu, Nhóm 3 đề xuất:

1.  **Chiến lược "Phí ship thông minh":**
    * Dữ liệu cho thấy `DOTCOM POSTAGE` đi kèm với các đơn hàng giá trị cực lớn.
    * **Hành động:** Miễn phí vận chuyển cho các đơn hàng chứa *Jumbo Bag* hoặc *Jam Making Set* để kích cầu nhóm khách hàng sỉ này.

2.  **Khai thác "Ngôi sao" Regency Cakestand:**
    * Đây là sản phẩm duy nhất vừa bán chạy vừa lãi cao.
    * **Hành động:** Sử dụng nó làm sản phẩm trung tâm (Hub) để bán chéo (Cross-sell) các loại trà cao cấp (*Teacup*).

3.  **Tái cấu trúc danh mục:**
    * Tạo danh mục *"Hidden Treasures"* trên website dành riêng cho các sản phẩm có Support thấp nhưng Utility cao (như bộ làm mứt) để tăng khả năng hiển thị.
    
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
