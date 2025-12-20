import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules

# 1. Nạp dữ liệu từ pipeline (Sửa lỗi NameError)
BASKET_PATH = "data/processed/basket_bool.parquet"

if os.path.exists(BASKET_PATH):
    basket_bool = pd.read_parquet(BASKET_PATH)
    print(f"Đã nạp dữ liệu thành công: {basket_bool.shape}")
else:
    print(f"Lỗi: Không tìm thấy file {BASKET_PATH}. Hãy chạy notebook basket_preparation trước.")
    exit()

def run_sensitivity_test(df, support_range):
    results = []
    for sup in support_range:
        # Đo Apriori
        t0 = time.time()
        freq_ap = apriori(df, min_support=sup, use_colnames=True)
        t_ap = time.time() - t0
        
        # Đo FP-Growth
        t1 = time.time()
        freq_fp = fpgrowth(df, min_support=sup, use_colnames=True)
        t_fp = time.time() - t1
        
        # Sinh luật để xem số lượng luật thay đổi thế nào
        rules = association_rules(freq_fp, metric="lift", min_threshold=1.0)
        
        results.append({
            'min_support': sup,
            'apriori_time': t_ap,
            'fpgrowth_time': t_fp,
            'n_rules': len(rules)
        })
        print(f"Sup: {sup:.3f} | Apriori: {t_ap:.2f}s | FP-Growth: {t_fp:.2f}s | Rules: {len(rules)}")
    return pd.DataFrame(results)

# Chạy thử nghiệm với các ngưỡng support giảm dần
support_levels = [0.02, 0.015, 0.01, 0.008]
sensitivity_results = run_sensitivity_test(basket_bool, support_levels)

# Vẽ biểu đồ hiệu năng
plt.figure(figsize=(10, 6))
plt.plot(sensitivity_results['min_support'], sensitivity_results['apriori_time'], 'o-', label='Apriori')
plt.plot(sensitivity_results['min_support'], sensitivity_results['fpgrowth_time'], 's-', label='FP-Growth')
plt.gca().invert_xaxis()
plt.title('Độ nhạy thời gian chạy theo Min Support')
plt.xlabel('Min Support')
plt.ylabel('Thời gian (giây)')
plt.legend()
plt.grid(True)
plt.savefig('performance_comparison.png')
plt.show()