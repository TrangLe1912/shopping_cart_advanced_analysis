"""
Script tự động chạy toàn bộ pipeline phân tích giỏ hàng sử dụng Papermill.

Pipeline bao gồm 5 bước:
1. Tiền xử lý và khám phá dữ liệu (EDA)
2. Chuẩn bị ma trận giỏ hàng
3. Khai thác luật kết hợp bằng Apriori
4. Khai thác luật kết hợp bằng FP-Growth
5. So sánh kết quả giữa Apriori và FP-Growth
"""

import papermill as pm
import os

# Tạo thư mục để lưu kết quả
os.makedirs("notebooks/runs", exist_ok=True)

# =========================================================
# BƯỚC 1: TIỀN XỬ LÝ VÀ KHÁM PHÁ DỮ LIỆU
# =========================================================
pm.execute_notebook(
    "notebooks/preprocessing_and_eda.ipynb",
    "notebooks/runs/preprocessing_and_eda_run.ipynb",
    parameters=dict(
        DATA_PATH="data/raw/online_retail.csv",          # Đường dẫn file dữ liệu gốc
        COUNTRY="United Kingdom",                         # Chỉ lấy khách hàng UK
        OUTPUT_DIR="data/processed",                      # Thư mục lưu dữ liệu đã xử lý
        PLOT_REVENUE=True,                                 # Vẽ biểu đồ doanh thu
        PLOT_TIME_PATTERNS=True,                           # Vẽ biểu đồ theo thời gian
        PLOT_PRODUCTS=True,                                # Vẽ biểu đồ sản phẩm
        PLOT_CUSTOMERS=True,                               # Vẽ biểu đồ khách hàng
        PLOT_RFM=True,                                     # Vẽ phân tích RFM
    ),
    kernel_name="python3",
)

# =========================================================
# BƯỚC 2: CHUẨN BỊ MA TRẬN GIỎ HÀNG
# =========================================================
pm.execute_notebook(
    "notebooks/basket_preparation.ipynb",
    "notebooks/runs/basket_preparation_run.ipynb",
    parameters=dict(
        CLEANED_DATA_PATH="data/processed/cleaned_uk_data.csv",  # Dữ liệu đã làm sạch
        BASKET_BOOL_PATH="data/processed/basket_bool.parquet",   # File output ma trận giỏ hàng
        INVOICE_COL="InvoiceNo",                                  # Cột số hóa đơn
        ITEM_COL="Description",                                   # Cột mô tả sản phẩm
        QUANTITY_COL="Quantity",                                  # Cột số lượng
        THRESHOLD=1,                                              # Ngưỡng: >= 1 coi như có trong giỏ
    ),
    kernel_name="python3",
)

# =========================================================
# BƯỚC 3: KHAI THÁC LUẬT KẾT HỢP - THUẬT TOÁN APRIORI
# =========================================================
pm.execute_notebook(
    "notebooks/apriori_modelling.ipynb",
    "notebooks/runs/apriori_modelling_run.ipynb",
    parameters=dict(
        BASKET_BOOL_PATH="data/processed/basket_bool.parquet",
        RULES_OUTPUT_PATH="data/processed/rules_apriori_filtered.csv",

        # Tham số thuật toán Apriori
        MIN_SUPPORT=0.02,              # Support tối thiểu: 2% giao dịch
        MAX_LEN=3,                     # Độ dài itemset tối đa: 3 sản phẩm

        # Tham số sinh luật
        METRIC="lift",                 # Chỉ số đánh giá: lift
        MIN_THRESHOLD=1.0,             # Ngưỡng tối thiểu cho lift

        # Lọc luật theo điều kiện
        FILTER_MIN_SUPPORT=0.02,       # Lọc: support >= 2%
        FILTER_MIN_CONF=0.3,           # Lọc: confidence >= 30%
        FILTER_MIN_LIFT=2.0,           # Lọc: lift >= 2.0
        FILTER_MAX_ANTECEDENTS=2,      # Lọc: tối đa 2 sản phẩm bên trái
        FILTER_MAX_CONSEQUENTS=1,      # Lọc: tối đa 1 sản phẩm bên phải

        # Số luật để vẽ biểu đồ
        TOP_N_RULES=20,                # Hiển thị top 20 luật

        # Tùy chọn vẽ biểu đồ
        PLOT_TOP_LIFT=True,            # Vẽ top luật theo lift
        PLOT_TOP_CONF=True,            # Vẽ top luật theo confidence
        PLOT_SCATTER=True,             # Vẽ scatter plot
        PLOT_NETWORK=True,             # Vẽ network graph
        PLOT_PLOTLY_NETWORK=True,      # Vẽ network graph tương tác
        PLOT_PLOTLY_SCATTER=True,      # Vẽ scatter plot tương tác
    ),
    kernel_name="python3",
)=========================================================
# BƯỚC 4: KHAI THÁC LUẬT KẾT HỢP - THUẬT TOÁN FP-GROWTH
# =========================================================

# Chạy Notebook FP_Growth Modelling
pm.execute_notebook(
    "notebooks/fp_growth_modelling.ipynb",
    "notebooks/runs/fp_growth_modelling_run.ipynb",
    parameters=dict(
        BASKET_BOOL_PATH="data/processed/basket_bool.parquet",
        RULES_OUTPUT_PATH="data/processed/rules_fpgrowth_filtered.csv",

        MIN_SUPPORT=0.02,
        MAX_LEN=3,

        METRIC="lift",
        MIN_THRESHOLD=1.0,

        FILTER_MIN_SUPPORT=0.02,
        FILTER_MIN_CONF=0.3,
        FILTER_MIN_LIFT=2.0,
        FILTER_MAX_ANTECEDENTS=2,
        FILTER_MAX_CONSEQUENTS=1,

        TOP_N_RULES=20,

        PLOT_TOP_LIFT=True,
        PLOT_TOP_CONF=True,
        PLOT_SCATTER=True,
        PLOT_NETWORK=True,
        PLOT_PLOTLY_SCATTER=True,
    ),
    kernel_name="python3",
)

# =========================================================
# BƯỚC 5: SO SÁNH APRIORI VS FP-GROWTH
# =========================================================
pm.execute_notebook(
    "notebooks/compare_apriori_fpgrowth.ipynb",
    "notebooks/runs/compare_apriori_fpgrowth_run.ipynb",
    parameters=dict(
        BASKET_BOOL_PATH="data/processed/basket_bool.parquet",

        # Tham số giống nhau cho cả 2 thuật toán
        MIN_SUPPORT=0.02,              # Support tối thiểu: 2%
        MAX_LEN=3,                     # Độ dài itemset tối đa: 3

        METRIC="lift",                 # Chỉ số: lift
        MIN_THRESHOLD=1.0,             # Ngưỡng lift tối thiểu: 1.0
    ),
    kernel_name="python3",
)

print("✓ Hoàn thành! Tất cả các notebook đã được thực thi thành công.")
print("Kết quả được lưu trong thư mục: notebooks/runs/")
