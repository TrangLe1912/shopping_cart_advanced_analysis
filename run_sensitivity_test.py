import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import fpgrowth, apriori

# CẤU HÌNH THÍ NGHIỆM
# Thử nghiệm từ dễ (5%) đến khó (0.5%)
SUPPORT_LEVELS = [0.05, 0.03, 0.02, 0.01, 0.005] 

def run_experiments():
    print("🚀 BẮT ĐẦU THỰC NGHIỆM ĐỘ NHẠY THAM SỐ (MỤC 5.2 - Q2)")
    print("-" * 60)
    
    # 1. Đọc dữ liệu đã chuẩn bị
    print("📦 Đang đọc dữ liệu basket_bool.parquet...")
    try:
        basket = pd.read_parquet("data/processed/basket_bool.parquet")
        print(f"   -> Kích thước dữ liệu: {basket.shape}")
    except Exception as e:
        print("❌ Lỗi: Không tìm thấy file data/processed/basket_bool.parquet")
        print("   Hãy chạy 'python run_papermill.py' trước để tạo dữ liệu!")
        return

    results = []

    # 2. Chạy vòng lặp thí nghiệm
    print(f"\n⚡ Đang chạy test với các mức Support: {SUPPORT_LEVELS}")
    print(f"{'Min Support':<12} | {'Algorithm':<10} | {'Itemsets':<10} | {'Time (s)':<10}")
    print("-" * 60)

    for min_sup in SUPPORT_LEVELS:
        # --- Test FP-Growth ---
        start_time = time.time()
        # FP-Growth luôn chạy được, kể cả support thấp
        fp_itemsets = fpgrowth(basket, min_support=min_sup, use_colnames=True)
        fp_time = time.time() - start_time
        
        results.append({
            'min_support': min_sup,
            'algorithm': 'FP-Growth',
            'num_itemsets': len(fp_itemsets),
            'execution_time': fp_time
        })
        print(f"{min_sup:<12} | {'FP-Growth':<10} | {len(fp_itemsets):<10} | {fp_time:.4f}")

        # --- Test Apriori ---
        # CẢNH BÁO: Apriori rất chậm ở support thấp. 
        # Để tránh treo máy, ta chỉ chạy Apriori nếu min_sup >= 0.01
        if min_sup >= 0.01:
            start_time = time.time()
            ap_itemsets = apriori(basket, min_support=min_sup, use_colnames=True)
            ap_time = time.time() - start_time
            
            results.append({
                'min_support': min_sup,
                'algorithm': 'Apriori',
                'num_itemsets': len(ap_itemsets),
                'execution_time': ap_time
            })
            print(f"{min_sup:<12} | {'Apriori':<10} | {len(ap_itemsets):<10} | {ap_time:.4f}")
        else:
            print(f"{min_sup:<12} | {'Apriori':<10} | {'SKIPPED':<10} | {'(Quá lâu)'}")

    # 3. Vẽ biểu đồ kết quả
    print("\n📊 Đang vẽ biểu đồ so sánh...")
    df_res = pd.DataFrame(results)
    
    plt.figure(figsize=(12, 6))
    
    # Biểu đồ 1: Thời gian chạy
    plt.subplot(1, 2, 1)
    sns.lineplot(data=df_res, x='min_support', y='execution_time', hue='algorithm', marker='o')
    plt.title('Độ nhạy thời gian thực thi (Time Sensitivity)')
    plt.xlabel('Min Support (Càng nhỏ càng khó)')
    plt.ylabel('Thời gian (giây)')
    plt.gca().invert_xaxis() # Đảo trục X để support giảm dần từ trái qua phải
    plt.grid(True, linestyle='--')

    # Biểu đồ 2: Số lượng Itemsets sinh ra
    plt.subplot(1, 2, 2)
    # Lấy dữ liệu FP-Growth đại diện (vì số lượng itemset 2 thuật toán ra giống nhau)
    fp_data = df_res[df_res['algorithm'] == 'FP-Growth']
    plt.plot(fp_data['min_support'], fp_data['num_itemsets'], marker='s', color='green')
    plt.title('Số lượng tập phổ biến sinh ra')
    plt.xlabel('Min Support')
    plt.ylabel('Số lượng Itemsets')
    plt.gca().invert_xaxis()
    plt.grid(True, linestyle='--')

    plt.tight_layout()
    plt.savefig('notebooks/runs/sensitivity_comparison.png')
    print("✅ Đã lưu biểu đồ tại: notebooks/runs/sensitivity_comparison.png")
    plt.show()

if __name__ == "__main__":
    run_experiments()