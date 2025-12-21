## 👥 Thông tin Nhóm
- **Nhóm: 2 ** 
- **Thành viên:** 
  - Nguyễn Nam Cường
  - Nguyễn Văn Đạt
  - Trần Việt Vinh
- **Dataset:** Online Retail (UCI)
# Q2: Thực Nghiệm Apriori vs FP-Growth - So Sánh Độ Nhạy Tham Số

## 📌 Tóm Tắt Thực Nghiệm

Notebook này chạy Apriori và FP-Growth trên cùng một `basket_bool` với các giá trị **min_support từ 0.05 xuống 0.02**, so sánh và phân tích:
- Số lượng frequent itemsets & association rules
- Thời gian chạy (Apriori vs FP-Growth)
- Chất lượng luật (support, confidence, lift)
- Độ dài trung bình của itemset

### 📊 Dữ Liệu Thực Tế Từ Notebook

```
Số hoá đơn: 18,021
Số sản phẩm: 4,007
Sparsity: 0.66%
Data size: 68.87 MB
```

---

## 🚀 Cách Chạy Notebook

### Cách 1: Jupyter (Khuyến Nghị)
```bash
cd d:\KHMT_16-01\Data Mining\shopping_cart_advanced_analysis
jupyter notebook notebooks/parameter_sensitivity_analysis.ipynb
```

### Cách 2: VS Code
1. Mở file: `notebooks/parameter_sensitivity_analysis.ipynb`
2. Chọn Python kernel
3. Chạy từng cell (Shift+Enter) hoặc Run All (Ctrl+Shift+Enter)

### Cách 3: Terminal
```bash
python -m jupyter notebook notebooks/parameter_sensitivity_analysis.ipynb
```

### Cách 4: Google Colab
Upload project lên Google Drive → Mở .ipynb với Colab → Run

---

## 📊 Cấu Trúc Notebook

### Section 1: Setup & Chuẩn Bị Dữ Liệu
- Import libraries (pandas, matplotlib, seaborn, mlxtend)
- Tải hoặc tạo `basket_bool.parquet`
- Kiểm tra thông tin dữ liệu (shape, sparsity, size)

### Section 2: Thử Nghiệm Min_Support
- **Giá trị test**: [0.05, 0.04, 0.03, 0.02]
- Chạy Apriori & FP-Growth cho từng min_support
- Đo: Thời gian, số itemsets, số rules
- Output: Bảng chi tiết + 4 biểu đồ

### Section 3: So Sánh Thời Gian Chạy
- Line plot: Time vs Min_Support (log scale)
- Bar chart: Speedup factor (FP-Growth/Apriori)
- Bảng: Timing comparison chi tiết

### Section 4: Thử Nghiệm Min_Confidence
- **Giá trị test**: [0.1, 0.3, 0.5, 0.7, 0.9]
- Với min_support = [0.05, 0.02]
- Output: 2 biểu đồ so sánh

### Section 5: Phân Tích Chất Lượng Luật
- Average Support, Confidence, Lift
- 4 line plots: Metrics vs Min_Support
- Bảng so sánh chi tiết

### Section 6: Phân Tích Phân Phối
- Histograms: Support, Confidence, Lift
- Chọn min_support = 0.02 làm tiêu biểu
- So sánh Apriori vs FP-Growth

### Section 7: Kết Luận
- Tóm tắt findings
- Phân tích độ nhạy tham số
- Khuyến nghị sử dụng

---

## 📈 Kết Quả Chính (DỮ LIỆU THỰC TẾ)

### Min_Support - RẤT NHẠY ✅
```
Giảm từ 0.05 → 0.02:

| Min Support | Itemsets | Rules | Time Apriori | Time FP-Growth |
|-------------|----------|-------|--------------|----------------|
| 0.05        | 34       | 0     | 0.089s       | 2.623s         |
| 0.04        | 66       | 2     | 0.156s       | 2.826s         |
| 0.03        | 145      | 22    | 0.383s       | 3.362s         |
| 0.02        | 400      | 218   | 1.764s       | 7.431s         |

Nhận xét:
• Itemsets: 0.05 → 0.02 tăng ~12x (34 → 400)
• Rules: 0 → 218 (rất lớn)
• Apriori nhanh hơn FP-Growth trong case này
```

### APRIORI NHANH HƠN (Không Phải FP-Growth!) ⚠️
```
Kết quả thực tế từ dataset:
• Min_support 0.05: Apriori nhanh hơn ~30x
• Min_support 0.04: Apriori nhanh hơn ~18x
• Min_support 0.03: Apriori nhanh hơn ~9x
• Min_support 0.02: Apriori nhanh hơn ~4x

Speedup = Apriori Time / FP-Growth Time:
• 0.05: 0.034x (Apriori 30x NHANH hơn)
• 0.04: 0.055x (Apriori 18x NHANH hơn)
• 0.03: 0.114x (Apriori 9x NHANH hơn)
• 0.02: 0.237x (Apriori 4x NHANH hơn)

→ Apriori tỏ ưu thế hơn FP-Growth trong dataset này
```

### Chất Lượng Luật - GIỐNG NHAU ✅
```
Apriori vs FP-Growth (Min Support = 0.02):

| Metric | Apriori | FP-Growth | Chênh Lệch |
|--------|---------|-----------|-----------|
| Số rules | 218 | 218 | 0% |
| Avg Support | 0.0246 | 0.0246 | 0% |
| Avg Confidence | 0.4529 | 0.4529 | 0% |
| Avg Lift | 8.2923 | 8.2923 | 0% |
| Max Lift | 27.2003 | 27.2003 | 0% |

→ KẾT LUẬN: Hoàn toàn giống nhau!
```

### Min_Confidence - KIỂM SOÁT SỐ LƯỢNG ✅
```
Thử nghiệm với min_confidence = [0.1, 0.3, 0.5, 0.7, 0.9]:
• Tăng confidence → Giảm số rules
• Trend: Gần tuyến tính (không exponential)
→ Dùng để lọc rules có độ tin cậy cao
```

---

## 🎯 Độ Nhạy Tham Số (Parameter Sensitivity)

### Min_Support ❌❌❌ (Rất Nhạy)
```
Dữ liệu thực tế:

Min_Support = 0.05  →  34 itemsets
Min_Support = 0.04  → 66 itemsets (2x)
Min_Support = 0.03  → 145 itemsets (4.3x)
Min_Support = 0.02  → 400 itemsets (11.8x)

→ Tăng theo HÀNG HÀM MŨ khi giảm min_support
```

**Hậu quả**: 
- Số rules tăng dramatically
- Apriori vẫn nhanh hơn FP-Growth
- Itemsets trở dài hơn (từ 1.0 → 1.26 items)

### Min_Confidence ⏹️⏹️ (Trung Bảo)
```
Thử nghiệm với 2 mức min_support:

Min_support = 0.05:
  Min_Confidence = 0.1 → Nhiều rules
  Min_Confidence = 0.9 → Ít rules (0.1x)
  Trend: Tuyến tính

Min_support = 0.02:
  Min_Confidence = 0.1 → 218 rules
  Min_Confidence = 0.9 → 20 rules (0.09x)
  Trend: Tuyến tính
```

**Hậu quả**:
- Rules giảm linearly
- Thời gian chạy không đổi
- Rules còn lại có tin cậy cao

### Min_Lift ⏹️ (Đều Đặn)
```
Min_Lift = 1.0:  Tất cả rules (neutral + positive)
Min_Lift = 1.2:  Giảm ~20% (strong positive only)

Avg Lift từ data: 8.29 (rất cao → strong associations)
Max Lift: 27.2 (relationship rất mạnh)
```

**Hậu quả**:
- Lọc rules có sức mạnh liên kết tốt
- Giảm false positives

---

## 💡 So Sánh Apriori vs FP-Growth

### Apriori (Generate-and-Test)
```
Ưu điểm (trong dataset này):
✓ NHANH hơn FP-Growth (4-30x)
✓ Dễ hiểu, dễ cài đặt
✓ Lý thuyết cơ bản

Nhược điểm:
✗ Lý thuyết: Chậm với min_support thấp
  (nhưng thực tế không phải vậy với dataset này)
✗ Tiêu thụ NHIỀU BỘ NHỚ (candidates)

Phù hợp: Dataset này (sparse data, low support)
```

### FP-Growth (Pattern Growth)
```
Ưu điểm (theo lý thuyết):
✓ Nên nhanh hơn
✓ Tiết kiệm bộ nhớ (no candidates)
✓ Tốt với long itemsets

Nhược điểm (thực tế):
✗ CHẬM hơn Apriori trên dataset này (4-30x)
✗ Xây dựng FP-tree tốn overhead
✗ Phức tạp hơn

Phù hợp: Dense datasets với items rất phổ biến
```

### Lý Giải Kết Quả Bất Ngờ
```
Tại sao Apriori nhanh hơn FP-Growth?

1. Dataset SPARSE (0.66%)
   → Ít frequent itemsets
   → Ít candidates cần kiểm tra
   → Apriori không phải lặp nhiều

2. FP-Tree overhead
   → Xây dựng FP-tree tốn thời gian
   → Pattern mining từ tree cũng tốn
   → Không bù được lợi thế trong sparse data

3. Mlxtend implementation
   → Apriori implementation hiệu quả
   → FP-Growth có thể chưa tối ưu
```

### Decision Matrix (Dựa Vào Dữ Liệu Thực)
```
┌──────────────────────┬────────────┬───────────────┐
│ Tình Huống           │ Apriori    │ FP-Growth     │
├──────────────────────┼────────────┼───────────────┤
│ Sparse data (< 1%)   │ ✓✓ BEST    │ ✗ BAD         │
│ Dense data (> 10%)   │ ✗ BAD      │ ✓✓ BEST       │
│ Min_support cao      │ ✓ FAST     │ ✗ SLOW        │
│ Min_support thấp     │ ✓ OK       │ ✗ SLOWER      │
│ Bộ nhớ limited       │ ✗ HIGH     │ ✓ LOW         │
│ Dễ hiểu              │ ✓✓ EASY    │ ✗ HARD        │
└──────────────────────┴────────────┴───────────────┘

→ KHUYẾN NGHỊ cho dataset này: APRIORI
```

---

## 📐 Công Thức Toán Học

### Support
$$\text{Support}(X) = \frac{\text{# transactions with } X}{\text{Total # transactions}}$$

**Ý nghĩa**: Tần suất xuất hiện của itemset

### Confidence
$$\text{Confidence}(A \to B) = \frac{\text{Support}(A \cup B)}{\text{Support}(A)}$$

**Ý nghĩa**: P(B|A) = Xác suất B xảy ra khi A đã xảy ra

### Lift
$$\text{Lift}(A \to B) = \frac{\text{Confidence}(A \to B)}{\text{Support}(B)}$$

**Ý nghĩa**: 
- Lift = 1: A và B độc lập
- Lift > 1: Liên kết dương (A → B)
- Lift < 1: Liên kết âm (A → ¬B)

---

## ⚙️ Tham Số Mặc Định

```python
# Min_Support - Tham số chính
min_supports = [0.05, 0.04, 0.03, 0.02]

# Min_Confidence - Kiểm soát số rules
min_confidences = [0.1, 0.3, 0.5, 0.7, 0.9]

# Min_Lift - Lọc sức mạnh liên kết
min_lift = 1.0
```

**Có thể thay đổi** trong code cells.

---

## 📋 Data Requirements

```
Input:
├─ basket_bool.parquet (Dataset thực tế)
│  └─ Matrix: 18,021 invoices × 4,007 products
│  └─ Sparsity: 0.66% (Rất SPARSE)
│
Output:
├─ Visualizations (6 biểu đồ)
├─ Tables (5+ bảng dữ liệu)
├─ Statistics (support, confidence, lift)
└─ Conclusions (kết luận & khuyến nghị)

Time: ~15 giây chạy
Memory: ~200-300MB
```

---

## 🐛 Troubleshooting

### Problem 1: "basket_bool.parquet not found"
```bash
# Solution: Chạy basket_preparation.ipynb trước
# Hoặc để code tự động tạo từ cleaned_uk_data.csv
```

### Problem 2: "ImportError: mlxtend"
```bash
pip install mlxtend
```

### Problem 3: Kernel không respond
```
Kernel > Restart
Cell > Clear All Outputs
Chạy lại từ đầu
```

### Problem 4: Memory Error
```
→ Giảm min_support (quá thấp gây explosion)
→ Hoặc dùng FP-Growth thay Apriori
```

---

## 📚 Tài Liệu Tham Khảo

1. **Apriori Algorithm**
   - Agrawal & Srikant (1994)
   - https://en.wikipedia.org/wiki/Apriori_algorithm

2. **FP-Growth Algorithm**
   - Han, Pei, Yin (2000)
   - https://en.wikipedia.org/wiki/FP-growth

3. **mlxtend Library**
   - Raschka, S. M. (2018)
   - http://rasbt.github.io/mlxtend/

4. **Association Rule Mining**
   - Tan, Steinbach, Kumar (2005)

---

## ✅ Checklist

Trước khi chạy:
- [x] Python 3.7+ cài đặt
- [x] Libraries: pandas, numpy, matplotlib, seaborn, mlxtend
- [x] Data: cleaned_uk_data.csv hoặc basket_bool.parquet

Sau khi chạy:
- [x] Xem 70+ visualizations
- [x] Đọc kết luận ở cuối notebook
- [x] Verify speedup numbers
- [x] Check rule quality metrics

---

## 🎯 Quick Reference

| Tham Số | Min | Max | Ảnh Hưởng | Khuyến Nghị |
|---------|-----|-----|----------|------------|
| min_support | 0.001 | 1.0 | **Exponential** | Chọn hợp lý |
| min_confidence | 0.0 | 1.0 | **Linear** | Dùng để lọc |
| min_lift | 1.0 | ∞ | **Moderate** | ≥ 1.2 để filter |

---

## 📞 Support

**Câu hỏi**: Cách chạy notebook?  
**Trả lời**: Xem section "Cách Chạy Notebook" trên

**Câu hỏi**: Tại sao FP-Growth nhanh hơn?  
**Trả lời**: Quét database 2 lần vs n lần + không tạo candidates

**Câu hỏi**: Khi nào dùng Apriori vs FP-Growth?  
**Trả lời**: Xem "Decision Matrix" trên

**Câu hỏi**: Làm sao hiểu kết quả?  
**Trả lời**: Xem "Kết Quả Chính" + Notebook visualizations

---


👉 **BẮT ĐẦU**: Chạy `notebooks/parameter_sensitivity_analysis.ipynb`
