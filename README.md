# Shopping Cart Analysis

Khám phá hành vi mua sắm của khách hàng trong cửa hàng bán lẻ: sản phẩm nào thường được mua cùng nhau, và làm thế nào để từ dữ liệu đó rút ra chiến lược kinh doanh hữu ích.  
Chúng tôi sử dụng **Apriori** và **FP-Growth** – hai thuật toán phổ biến trong **Association Rule Mining** – để tìm các luật kết hợp sản phẩm.

---

## 👥 Thông tin Nhóm

- **Nhóm:** Nhóm 9
- **Thành viên:**
  - Trần Trường Giang
  - Nguyễn Đức Dương
- **Chủ đề:** **5.3.2.4 – Phân tích độ nhạy tham số với và không có trọng số (Parameter Sensitivity)**
  - Thực nghiệm nhiều giá trị **min_support, min_confidence, min_lift** cho:
    - Luật thường
    - Luật có trọng số (ví dụ: min_weighted_support, min_weighted_lift)
  - Quan sát sự thay đổi về:
    1. Số lượng luật
    2. Cấu trúc / cụm sản phẩm chính
    3. Sự xuất hiện hoặc biến mất của các luật có giá trị kinh doanh cao
  - Rút ra “ngưỡng hợp lý” cho cả hai trường hợp:
    - Khi mục tiêu là khai thác hành vi mua phổ biến
    - Khi mục tiêu là tối đa hóa giá trị/doanh thu
- **Dataset:** Online Retail (UCI Machine Learning Repository)


---

## Mục tiêu:

- Hiểu hành vi mua hàng của khách.
- Khai thác **các cặp/mẫu sản phẩm thường đi cùng nhau**.
- Hỗ trợ quyết định: **cross-selling**, combo sản phẩm, trưng bày tại cửa hàng.

Dữ liệu được lưu trong:

- `data/raw/online_retail.csv` — file gốc không chỉnh sửa.
- `data/processed/` — chứa dữ liệu làm sạch, basket matrix và luật kết hợp.

---

## Pipeline: từ dữ liệu đến insight

Quy trình được thiết kế theo **pipeline tự động** với Papermill:

1. **Tiền xử lý & EDA**
   - Làm sạch dữ liệu: loại bỏ hóa đơn hủy, giá trị không hợp lệ.  
   - Khám phá đặc điểm mua sắm: số lượng sản phẩm mỗi hóa đơn, tần suất mua theo quốc gia.

2. **Chuẩn bị basket matrix**
   - Mỗi hóa đơn là một dòng, mỗi sản phẩm là một cột.  
   - Dữ liệu Boolean: 1 nếu khách mua sản phẩm, 0 nếu không.

3. **Khai phá luật bằng Apriori & FP-Growth**
   - Sinh tập mục phổ biến (frequent itemsets).  
   - Tạo luật kết hợp với **support, confidence, lift**.  
   - Lọc các luật mạnh theo ngưỡng để tập trung vào các mối liên kết quan trọng.

4. **So sánh thuật toán**
   - Hai thuật toán tạo cùng số lượng tập mục phổ biến và luật.  
   - Điểm khác biệt chính là **hiệu năng**:
     - MIN_SUPPORT cao → Apriori nhanh hơn.  
     - MIN_SUPPORT thấp → FP-Growth mở rộng tốt hơn với dữ liệu lớn.

5. **Trực quan hóa & insight**
   - **Bar chart:** top luật theo Lift.
  <img width="1000" height="600" alt="image" src="https://github.com/user-attachments/assets/6e555b6b-7ddd-4707-82c2-e3b2a47c6478" />
   - **Scatter plot:** Support vs Confidence.
<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/db505e78-716a-4e02-8c14-3e2706cc7e77" />
   - **Box plot:** phân bố Lift.  
 <img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/a9414f7f-e61f-4ea6-8b64-38909b5523a6" />

---

## Kết quả chính & insight kinh doanh

1. **Combo sản phẩm Herb Marker**  
   - {Parsley, Rosemary} → Thyme (Confidence ~95%, Lift ~74)  
   - **Ứng dụng:** tạo combo 3 sản phẩm, khuyến mại nhẹ để tăng giá trị đơn hàng.

2. **Mint là sản phẩm kích hoạt**  
   - Khi khách chọn Mint, họ tiếp tục mua các Herb Marker khác.  
   - **Ứng dụng:** đặt Mint ở vị trí dễ thấy, gợi ý sản phẩm liên quan.

3. **Mua theo bộ**  
   - Khách hiếm khi mua lẻ một Herb Marker, thường mua 2–3 sản phẩm cùng lúc.  
   - **Ứng dụng:** trưng bày các Herb Marker liền nhau, thiết kế kệ “Herb Set”.

4. **Cặp bổ trợ mạnh**  
   - Chives → Parsley (Confidence ~92%, Lift ~72).  
   - **Ứng dụng:** gợi ý Parsley khi khách chọn Chives, combo nhỏ 2 sản phẩm.

5. **Quản lý tồn kho theo nhóm sản phẩm**  
   - Nhóm Herb Marker: Mint – Basil – Rosemary – Parsley – Thyme.  
   - Support ~1% nhưng Confidence & Lift cao, nên quản lý nhập – tồn đồng bộ.

---

## So sánh Apriori & FP-Growth

| MIN_SUPPORT | Frequent Itemsets | Số luật | Thời gian chạy |
|------------|-----------------|---------|----------------|
| 0.03       | 145             | 21      | Apriori: 0.37s, FP-Growth: 2.66s |
| 0.02       | 400             | 175     | Apriori: 2.35s, FP-Growth: 6.47s |
| 0.01       | 2,120           | 1,794   | Apriori: 61.06s, FP-Growth: 48.05s |

**Nhận xét:**

- Hai thuật toán tạo cùng luật, chất lượng tương đương.  
- FP-Growth ưu thế khi MIN_SUPPORT thấp và dữ liệu lớn.  
- Apriori nhanh hơn với MIN_SUPPORT cao và dữ liệu nhỏ–trung bình.

---

## Project Structure

```text
shopping_cart_advanced_analysis/
├── data/
│   ├── raw/
│   │   └── online_retail.csv
│   └── processed/
|       ├── charts/  
│       ├── cleaned_uk_data.csv
│       ├── basket_bool.parquet
│       ├── rules_apriori_filtered.csv
│       └── rules_fpgrowth_filtered.csv
│
├── notebooks/
│   ├── preprocessing_and_eda.ipynb
│   ├── basket_preparation.ipynb
│   ├── apriori_modelling.ipynb
│   ├── fp_growth_modelling.ipynb
│   ├── compare_apriori_fpgrowth.ipynb
│   └── runs/
│       ├── preprocessing_and_eda_run.ipynb
│       ├── basket_preparation_run.ipynb
│       ├── apriori_modelling_run.ipynb
│       ├── fp_growth_modelling_run.ipynb
│       ├── parameter_sensitivity_analysis.ipynb
│       └── compare_apriori_fpgrowth_run.ipynb
│       └── visualize_rules.py
│
├── src/
│   └── apriori_library.py
│
├── dashboard/
│   ├── app.py
│   └── requirements.txt
│
├── run_papermill.py
├── requirements.txt
└── README.md
```

## Tech Stack

- Python, Pandas, MLxtend (Apriori/FP-Growth)  
- Matplotlib, Seaborn, Plotly (visualization)  
- Streamlit (dashboard)  
- Papermill (pipeline tự động)  
- Jupyter Notebook

---

## Kết luận

- **Apriori & FP-Growth** đều hiệu quả về mặt lý thuyết.  
- **Chất lượng luật** phản ánh thói quen mua kèm của khách hàng, hữu ích cho **cross-selling và combo sản phẩm**.  
- **FP-Growth** ưu thế hơn với dữ liệu lớn và ngưỡng support thấp.

### Author
Project được thực hiện bởi:
Trang Le

📄 License
MIT — sử dụng tự do cho nghiên cứu, học thuật và ứng dụng nội bộ.
