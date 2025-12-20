import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns
import os
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules

# --- 1. Cấu hình đường dẫn và tham số ---
# Sử dụng đường dẫn từ pipeline của Lab
BASKET_PATH = "data/processed/basket_bool.parquet"
OUTPUT_IMG_DIR = "reports/figures/"
os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)

# Dải tham số min_support để kiểm tra độ nhạy (giảm dần)
# Theo kỳ vọng của Lab: Apriori sẽ chậm đi đáng kể khi support giảm
SUPPORT_LEVELS = [0.02, 0.015, 0.01, 0.008, 0.006] 
MIN_CONFIDENCE = 0.3

# --- 2. Nạp dữ liệu ---
if not os.path.exists(BASKET_PATH):
    print(f"Lỗi: Không tìm thấy {BASKET_PATH}. Hãy chạy notebook basket_preparation trước.")
    exit()

basket_bool = pd.read_parquet(BASKET_PATH)
print(f"Đã nạp dữ liệu: {basket_bool.shape[0]} giao dịch, {basket_bool.shape[1]} sản phẩm.")

# --- 3. Thực hiện thí nghiệm ---
results = []

for sup in SUPPORT_LEVELS:
    print(f"\nĐang thử nghiệm với min_support = {sup}...")
    
    # Đo hiệu năng Apriori
    start_ap = time.time()
    freq_ap = apriori(basket_bool, min_support=sup, use_colnames=True)
    end_ap = time.time() - start_ap
    
    # Đo hiệu năng FP-Growth
    start_fp = time.time()
    freq_fp = fpgrowth(basket_bool, min_support=sup, use_colnames=True)
    end_fp = time.time() - start_fp
    
    # Sinh luật kết hợp để đếm số lượng
    rules = association_rules(freq_fp, metric="confidence", min_threshold=MIN_CONFIDENCE)
    
    # Tính độ dài trung bình của itemset
    avg_len = freq_fp['itemsets'].apply(len).mean() if not freq_fp.empty else 0
    
    results.append({
        'min_support': sup,
        'apriori_time': end_ap,
        'fpgrowth_time': end_fp,
        'num_itemsets': len(freq_fp),
        'num_rules': len(rules),
        'avg_itemset_len': avg_len
    })
    print(f" - Apriori: {end_ap:.2f}s | FP-Growth: {end_fp:.2f}s | Luật: {len(rules)}")

# Chuyển kết quả sang DataFrame
df_res = pd.DataFrame(results)

# --- 4. Trực quan hóa kết quả (Yêu cầu 5.2.3) ---

sns.set_theme(style="whitegrid")
fig, ax1 = plt.subplots(figsize=(12, 6))

# Biểu đồ 1: Thời gian thực thi (So sánh độ nhạy hiệu năng)
ax1.set_xlabel('Min Support (Giảm dần)')
ax1.set_ylabel('Thời gian chạy (giây)', color='tab:red')
ax1.plot(df_res['min_support'], df_res['apriori_time'], 'o-', color='tab:red', label='Thời gian Apriori', linewidth=2)
ax1.plot(df_res['min_support'], df_res['fpgrowth_time'], 's--', color='tab:orange', label='Thời gian FP-Growth', linewidth=2)
ax1.tick_params(axis='y', labelcolor='tab:red')
ax1.invert_xaxis() # Đảo ngược trục X để thấy xu hướng khi support giảm

# Biểu đồ 2: Số lượng luật sinh ra (Trục phụ)
ax2 = ax1.twinx()
ax2.set_ylabel('Số lượng luật / Tập phổ biến', color='tab:blue')
ax2.bar(df_res['min_support'], df_res['num_rules'], alpha=0.3, color='tab:blue', width=0.001, label='Số lượng luật')
ax2.step(df_res['min_support'], df_res['num_itemsets'], where='mid', color='tab:cyan', label='Số tập phổ biến')
ax2.tick_params(axis='y', labelcolor='tab:blue')

fig.tight_layout()
plt.title('So sánh hiệu năng và Quy mô dữ liệu: Apriori vs FP-Growth', fontsize=15)
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.savefig(os.path.join(OUTPUT_IMG_DIR, 'sensitivity_analysis.png'))
print(f"\nThí nghiệm hoàn tất. Biểu đồ đã lưu tại: {OUTPUT_IMG_DIR}sensitivity_analysis.png")