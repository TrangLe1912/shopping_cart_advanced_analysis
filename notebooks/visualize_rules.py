import os
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# 1. CẤU HÌNH ĐƯỜNG DẪN
# =========================
# LƯU Ý: tên file phải khớp với file đã sinh từ notebook
APRIORI_RULES_PATH = "../data/processed/rules_apriori_filtered.csv"
FPGROWTH_RULES_PATH = "../data/processed/rules_fpgrowth_filtered.csv"

CHART_OUTPUT_DIR = "../data/processed/charts"
os.makedirs(CHART_OUTPUT_DIR, exist_ok=True)

# =========================
# 2. LOAD DỮ LIỆU
# =========================
rules_ap = pd.read_csv(APRIORI_RULES_PATH)
rules_fp = pd.read_csv(FPGROWTH_RULES_PATH)

rules_ap["algorithm"] = "Apriori"
rules_fp["algorithm"] = "FP-Growth"

rules_all = pd.concat([rules_ap, rules_fp], ignore_index=True)

print("Đã load dữ liệu:")
print(f"- Apriori: {len(rules_ap)} luật")
print(f"- FP-Growth: {len(rules_fp)} luật")

# =========================
# 3. BIỂU ĐỒ 1: BAR CHART – TOP LUẬT THEO LIFT
# =========================
top_k = 10
top_lift = (
    rules_all.sort_values("lift", ascending=False)
    .head(top_k)
    .copy()
)

plt.figure(figsize=(10, 6))
plt.barh(range(top_k), top_lift["lift"])

plt.yticks(
    range(top_k),
    top_lift["algorithm"]
    + ": "
    + top_lift["antecedents_str"]
    + " → "
    + top_lift["consequents_str"]
)

plt.xlabel("Lift")
plt.title("Top luật có Lift cao nhất (Apriori & FP-Growth)")
plt.gca().invert_yaxis()
plt.tight_layout()

bar_path = os.path.join(CHART_OUTPUT_DIR, "bar_top_lift_rules.png")
plt.savefig(bar_path)
plt.close()

print(f"Đã lưu biểu đồ bar chart: {bar_path}")

# =========================
# 4. BIỂU ĐỒ 2: SCATTER SUPPORT vs CONFIDENCE
# =========================
plt.figure(figsize=(8, 6))

plt.scatter(
    rules_ap["support"],
    rules_ap["confidence"],
    alpha=0.6,
    label="Apriori"
)

plt.scatter(
    rules_fp["support"],
    rules_fp["confidence"],
    alpha=0.6,
    label="FP-Growth"
)

plt.xlabel("Support")
plt.ylabel("Confidence")
plt.title("So sánh Support – Confidence giữa Apriori và FP-Growth")
plt.legend()
plt.grid(True)

scatter_path = os.path.join(CHART_OUTPUT_DIR, "scatter_support_confidence.png")
plt.savefig(scatter_path)
plt.close()

print(f"Đã lưu scatter plot: {scatter_path}")

# =========================
# 5. BIỂU ĐỒ 3 (THAY THẾ): BOX PLOT PHÂN BỐ LIFT
# =========================
plt.figure(figsize=(8, 6))

plt.boxplot(
    [
        rules_ap["lift"],
        rules_fp["lift"]
    ],
    labels=["Apriori", "FP-Growth"],
    showfliers=True
)

plt.ylabel("Lift")
plt.title("Phân bố Lift của luật kết hợp (Apriori vs FP-Growth)")
plt.grid(axis="y")

boxplot_path = os.path.join(CHART_OUTPUT_DIR, "boxplot_lift_comparison.png")
plt.savefig(boxplot_path)
plt.close()

print(f"Đã lưu box plot Lift: {boxplot_path}")

print("\nHoàn tất trực quan hóa kết quả khai phá luật.")