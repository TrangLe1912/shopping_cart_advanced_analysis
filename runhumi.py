import pandas as pd
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.preprocessing import TransactionEncoder
import tqdm  # Thư viện hiển thị thanh tiến trình (pip install tqdm nếu chưa có)

# --- CẤU HÌNH ---
INPUT_FILE = 'data/processed/cleaned_uk_data.csv'
MIN_SUPPORT_THRESHOLD = 0.005  # 0.5% - Để thấp để bắt được các món đắt tiền nhưng ít mua
OUTPUT_FILE = 'high_utility_results_manual.csv'

def main():
    print(f"📂 Đang đọc dữ liệu từ {INPUT_FILE}...")
    try:
        df = pd.read_csv(INPUT_FILE, encoding='ISO-8859-1')
    except:
        df = pd.read_csv(INPUT_FILE)

    # 1. TIỀN XỬ LÝ & TÍNH DOANH THU
    print("🧹 Đang làm sạch và tính toán doanh thu từng dòng...")
    # Xóa đơn hủy và số lượng âm
    df = df[~df['InvoiceNo'].astype(str).str.contains('C')]
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
    
    # Tính cột Thành Tiền (Utility) cho từng dòng
    df['LineTotal'] = df['Quantity'] * df['UnitPrice']
    
    # Chỉ giữ lại các cột cần thiết để tiết kiệm RAM
    df_slim = df[['InvoiceNo', 'Description', 'LineTotal']].copy()
    df_slim['Description'] = df_slim['Description'].str.strip() # Xóa khoảng trắng thừa

    # 2. CHUẨN BỊ DỮ LIỆU CHO FP-GROWTH (BASKET MATRIX)
    print("🔄 Đang chuyển đổi dữ liệu sang dạng Transaction list...")
    # Gom nhóm sản phẩm theo hóa đơn
    transactions = df_slim.groupby('InvoiceNo')['Description'].apply(list).values.tolist()
    
    print("⚙️ Đang mã hóa One-Hot (bước này có thể mất chút thời gian)...")
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df_trans = pd.DataFrame(te_ary, columns=te.columns_)
    
    # 3. CHẠY FP-GROWTH ĐỂ TÌM TẬP ỨNG VIÊN
    print(f"🚀 Đang chạy FP-Growth (min_support={MIN_SUPPORT_THRESHOLD})...")
    # Chúng ta dùng FP-Growth để tìm ra các nhóm sản phẩm hay đi cùng nhau trước
    frequent_itemsets = fpgrowth(df_trans, min_support=MIN_SUPPORT_THRESHOLD, use_colnames=True)
    
    print(f"✅ Tìm thấy {len(frequent_itemsets)} tập phổ biến. Giờ sẽ tính tiền cho chúng!")

    # 4. TÍNH UTILITY (DOANH THU) CHO TỪNG TẬP
    # Đây là hàm cốt lõi thay thế cho PAMI
    
    # Để tính nhanh, ta gom dữ liệu gốc về dạng: Invoice -> {Item: Money, Item: Money}
    print("🧮 Đang xây dựng chỉ mục tra cứu nhanh...")
    invoice_map = {}
    for inv, group in df_slim.groupby('InvoiceNo'):
        # Tạo dict: {'ItemA': 10.5, 'ItemB': 20.0} cho mỗi hóa đơn
        item_dict = dict(zip(group['Description'], group['LineTotal']))
        invoice_map[inv] = item_dict

    def calculate_exact_utility(itemset):
        """
        Tính tổng tiền thực tế mà itemset này mang lại.
        Logic: Duyệt qua tất cả hóa đơn, nếu hóa đơn chứa ĐỦ itemset,
        thì cộng tổng tiền của các item đó lại.
        """
        total_utility = 0
        items = set(itemset)
        
        for inv_items in invoice_map.values():
            # Kiểm tra xem hóa đơn này có chứa đủ set không (subset check)
            # Dùng set keys view để check nhanh hơn
            if items.issubset(inv_items.keys()):
                # Nếu đủ, cộng tiền của CÁC MÓN ĐÓ trong hóa đơn này
                for item in items:
                    total_utility += inv_items[item]
        return total_utility

    # Áp dụng tính toán (Có thanh progress bar)
    tqdm.tqdm.pandas(desc="Tính Utility")
    # Chạy tính toán trên cột itemsets
    frequent_itemsets['utility_value'] = frequent_itemsets['itemsets'].progress_apply(calculate_exact_utility)

    # 5. XUẤT KẾT QUẢ
    # Sắp xếp theo Utility giảm dần
    top_utility = frequent_itemsets.sort_values(by='utility_value', ascending=False).head(20)
    
    print("\n" + "="*60)
    print("🏆 TOP 20 BỘ SẢN PHẨM MANG LẠI DOANH THU CAO NHẤT (HIGH-UTILITY)")
    print("="*60)
    
    # Format hiển thị đẹp
    results = []
    for index, row in top_utility.iterrows():
        items_str = ", ".join(list(row['itemsets']))
        print(f"💰 ${row['utility_value']:<10.2f} | Support: {row['support']:.4f} | {items_str}")
        results.append({'Itemsets': items_str, 'Utility': row['utility_value'], 'Support': row['support']})

    # Lưu file
    pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)
    print(f"\n✅ Đã lưu kết quả vào: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()