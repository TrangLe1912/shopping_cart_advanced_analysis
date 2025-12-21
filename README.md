# Shopping Cart Analysis

Phân tích dữ liệu bán lẻ nhằm khám phá mối quan hệ giữa các sản phẩm thường được mua cùng nhau bằng các kỹ thuật **Association Rule Mining** như **Apriori** và **FP-Growth**.  
Project triển khai pipeline đầy đủ từ xử lý dữ liệu → khai thác luật → so sánh thuật toán → trực quan hóa kết quả.

---

## Features

- Làm sạch dữ liệu & xử lý giao dịch lỗi
- Xây dựng basket matrix (transaction × product)
- Khai thác tập mục phổ biến (Frequent Itemsets)
- Sinh luật kết hợp (Association Rules)
- Hỗ trợ 2 thuật toán:
  - Apriori
  - FP-Growth
- So sánh Apriori vs FP-Growth
- Các chỉ số đánh giá:
  - Support
  - Confidence
  - Lift
- Trực quan hóa với:
  - Bar chart
  - Scatter plot
  - Network graph
  - Biểu đồ tương tác Plotly
- Tự động hóa pipeline bằng **Papermill**
- Dashboard tương tác bằng **Streamlit**

---

## Project Structure

```text
shopping_cart_advanced_analysis/
├── data/
│   ├── raw/
│   │   └── online_retail.csv
│   └── processed/
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
│       └── compare_apriori_fpgrowth_run.ipynb
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


## Installation
git clone <your_repo_url>
cd shopping_cart_advanced_analysis
conda create -n shopping_env python=3.11
conda activate shopping_env
pip install -r requirements.txt

## Data Preparation

#Đặt file dữ liệu gốc tại:
data/raw/online_retail.csv

#File output sẽ được sinh tự động tại:
data/processed/

##Pipeline Overview
1. Data Preprocessing & EDA

📓 Notebook: preprocessing_and_eda.ipynb

Làm sạch dữ liệu (huỷ đơn, quantity âm, price = 0)

Chuẩn hoá thông tin sản phẩm & khách hàng

Phân tích thống kê mô tả dữ liệu
#Biểu đồ phân bố số giao dịch theo thời gian
https://github.com/TrangLe1912/shopping_cart_advanced_analysis/blob/main/pic/Screenshot%202025-12-21%20222435.png
#Top sản phẩm bán chạy
https://github.com/TrangLe1912/shopping_cart_advanced_analysis/blob/main/pic/Screenshot%202025-12-21%20222510.png

##2. Basket Preparation

📓 Notebook: basket_preparation.ipynb

Group dữ liệu theo InvoiceNo và Description

Xây dựng Basket Matrix

Chuyển dữ liệu về dạng nhị phân (0/1)
#Trích xuất một phần Basket Matrix
https://github.com/TrangLe1912/shopping_cart_advanced_analysis/blob/main/pic/Screenshot%202025-12-21%20222938.png

Output:
data/processed/basket_bool.parquet

## 3. Apriori Modelling

📓 Notebook: apriori_modelling.ipynb

Khai thác Frequent Itemsets bằng Apriori

Sinh luật kết hợp dựa trên Support, Confidence, Lift

Lọc và sắp xếp các luật có ý nghĩa
#Bar chart: Top luật theo Lift
https://github.com/TrangLe1912/shopping_cart_advanced_analysis/blob/main/pic/Screenshot%202025-12-21%20223047.png

#Scatter plot: Support – Confidence – Lift
https://github.com/TrangLe1912/shopping_cart_advanced_analysis/blob/main/pic/Screenshot%202025-12-21%20223233.png

#Network graph luật kết hợp (Apriori)
https://github.com/TrangLe1912/shopping_cart_advanced_analysis/blob/main/pic/Screenshot%202025-12-21%20224201.png
Output:
data/processed/rules_apriori_filtered.csv

## 4. FP-Growth Modelling

📓 Notebook: fp_growth_modelling.ipynb

Khai thác Frequent Itemsets bằng FP-Growth

Sinh luật kết hợp

So sánh kết quả với Apriori
Bar chart: Top luật theo Lift (FP-Growth)
https://github.com/TrangLe1912/shopping_cart_advanced_analysis/blob/main/pic/Screenshot%202025-12-21%20224056.png

Network graph luật kết hợp (FP-Growth)
https://github.com/TrangLe1912/shopping_cart_advanced_analysis/blob/main/pic/Screenshot%202025-12-21%20223956.png
Output:

data/processed/rules_fpgrowth_filtered.csv
##5. So sánh Apriori vs FP-Growth

📓 Notebook: compare_apriori_fpgrowth.ipynb

So sánh thời gian chạy

So sánh số Frequent Itemsets

So sánh số Association Rules
Bảng/biểu đồ so sánh Apriori vs FP-Growth:
# Chạy benchmark
https://github.com/TrangLe1912/shopping_cart_advanced_analysis/blob/main/pic/Screenshot%202025-12-21%20224720.png
#Biểu đồ so sánh thời gian
https://github.com/TrangLe1912/shopping_cart_advanced_analysis/blob/main/pic/Screenshot%202025-12-21%20224736.png
# Biểu đồ số lượng itemsets & rules
https://github.com/TrangLe1912/shopping_cart_advanced_analysis/blob/main/pic/Screenshot%202025-12-21%20224751.png
# Độ dài trung bình iemset
https://github.com/TrangLe1912/shopping_cart_advanced_analysis/blob/main/pic/Screenshot%202025-12-21%20224800.png
# Một vài luật tiêu biểu từ mỗi thuật toán
https://github.com/TrangLe1912/shopping_cart_advanced_analysis/blob/main/pic/Screenshot%202025-12-21%20224812.png


##Run Pipeline

Chạy toàn bộ pipeline tự động bằng Papermill:
python run_papermill.py

Kết quả sinh ra:
data/processed/
├── cleaned_uk_data.csv
├── basket_bool.parquet
├── rules_apriori_filtered.csv
└── rules_fpgrowth_filtered.csv

notebooks/runs/
├── preprocessing_and_eda_run.ipynb
├── basket_preparation_run.ipynb
├── apriori_modelling_run.ipynb
├── fp_growth_modelling_run.ipynb
└── compare_apriori_fpgrowth_run.ipynb

##Changing Parameters

Có thể điều chỉnh tham số trong run_papermill.py hoặc cell PARAMETERS:
MIN_SUPPORT = 0.01
MAX_LEN = 3
FILTER_MIN_CONF = 0.3
FILTER_MIN_LIFT = 1.2

##Visualization & Results

Các notebook modelling hiển thị:

Top luật theo Lift

Top luật theo Confidence

Scatter plot Support – Confidence – Lift

Network graph giữa các sản phẩm

Biểu đồ Plotly tương tác

Export notebook sang HTML:

jupyter nbconvert notebooks/runs/apriori_modelling_run.ipynb --to html

##Ứng dụng thực tế

Product recommendation

Cross-selling strategy

Gợi ý combo sản phẩm

Phân tích hành vi mua hàng

Sắp xếp sản phẩm trong siêu thị

##Tech Stack
| Công nghệ            | Mục đích                      |
| -------------------- | ----------------------------- |
| Python               | Ngôn ngữ chính                |
| Pandas               | Xử lý dữ liệu transaction     |
| MLxtend              | Apriori / FP-Growth           |
| Papermill            | Tự động hóa pipeline          |
| Matplotlib & Seaborn | Biểu đồ tĩnh                  |
| Plotly               | Biểu đồ & dashboard tương tác |
| Jupyter Notebook     | Môi trường phân tích          |

##Roadmap

Streamlit dashboard

Weighted association rules

Correlation-aware rule ranking

##Author

Project được thực hiện bởi:
Trang Le