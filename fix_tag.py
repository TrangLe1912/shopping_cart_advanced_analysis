import nbformat

# Đường dẫn đến file notebook cần sửa
notebook_path = "notebooks/fp_growth_modelling.ipynb"

# Đọc file notebook
with open(notebook_path, "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

found = False
# Duyệt qua từng ô để tìm ô chứa PARAMETERS
for cell in nb.cells:
    if cell.cell_type == "code" and "BASKET_BOOL_PATH =" in cell.source:
        # Tìm thấy ô cấu hình!
        print("Đã tìm thấy ô PARAMETERS.")
        
        # Xem tag hiện tại là gì
        current_tags = cell.metadata.get("tags", [])
        print(f"Tag hiện tại: {current_tags}")
        
        # Sửa lại cho đúng (Xóa hết cũ, đặt lại là 'parameters')
        cell.metadata["tags"] = ["parameters"]
        found = True
        print("--> Đã sửa tag thành: ['parameters']")
        break

if found:
    # Lưu lại file notebook đã sửa
    with open(notebook_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print("\nSUCESS: Đã lưu file notebook thành công! Bạn có thể chạy lại run_papermill.py ngay.")
else:
    print("\nERROR: Không tìm thấy ô chứa 'BASKET_BOOL_PATH'. Hãy kiểm tra lại file notebook.")