# Quản lý Chi tiêu Cá nhân

Ứng dụng quản lý thu/chi cá nhân, có **giao diện cửa sổ (GUI)** dễ dùng
cho người không rành công nghệ — chỉ cần bấm nút, chọn trong danh sách.
Ngoài ra vẫn giữ bản dòng lệnh (CLI) cho ai thích gõ nhanh.

## Yêu cầu

- Python 3.8 trở lên (chỉ dùng thư viện chuẩn: `sqlite3`, `tkinter` — không cần cài thêm gì)

## Cách chạy

```bash
python3 gui.py      # Bản giao diện cửa sổ (khuyên dùng)
python3 main.py     # Bản dòng lệnh (CLI)
```

Dữ liệu được lưu trong file `expenses.db` (SQLite) cùng thư mục,
sẽ tự động được tạo ở lần chạy đầu tiên. Cả hai bản GUI và CLI
dùng chung một database, có thể chạy xen kẽ thoải mái.

## Chức năng (bản GUI - gui.py)

**Tab "Giao dịch":**
- Form bên trái: chọn loại (Thu/Chi), nhập số tiền, chọn danh mục
  (Ăn uống, Học tập, Giải trí, Đi lại, Hóa đơn, hoặc gõ danh mục riêng),
  ghi chú, ngày → bấm "Thêm giao dịch".
- Bảng bên phải: danh sách toàn bộ giao dịch, có thể chọn dòng rồi
  bấm "Xóa giao dịch đã chọn".

**Tab "Tổng kết theo tháng":**
- Chọn tháng từ danh sách thả xuống.
- Hiển thị tổng thu, tổng chi, số dư.
- Hai bảng: chi tiêu và thu nhập theo từng danh mục, kèm phần trăm.

## Cấu trúc dự án

```
expense_tracker/
├── gui.py           # Giao diện cửa sổ (tkinter) — bản chính, khuyên dùng
├── main.py          # Giao diện dòng lệnh (CLI) — bản thay thế
├── database.py      # Thao tác với SQLite (thêm, lấy, xóa giao dịch)
├── utils.py         # Danh mục mặc định, định dạng tiền tệ/ngày tháng
├── build.bat         # Đóng gói bản GUI thành .exe
├── build_cli.bat     # Đóng gói bản CLI thành .exe (tùy chọn)
├── expenses.db       # Cơ sở dữ liệu (tự tạo khi chạy lần đầu)
└── README.md
```

## Ví dụ nhập số tiền và ngày

- Số tiền: `50000` hoặc `50.000` đều được (không cần dấu chấm phân cách)
- Ngày: `25/12/2026` (định dạng dd/mm/yyyy), để trống = ngày hôm nay

## Đóng gói thành file .exe (chạy trên Windows, không cần cài Python)

Vì file `.exe` phải được build ngay trên hệ điều hành Windows, hãy làm theo các bước sau **trên máy Windows** của bạn:

1. Cài Python (nếu chưa có): tải tại https://www.python.org/downloads/ — nhớ tick vào ô "Add Python to PATH" lúc cài.
2. Copy toàn bộ thư mục `expense_tracker` (gồm `main.py`, `database.py`, `utils.py`, `requirements.txt`, `build.bat`) sang máy Windows.
3. Mở thư mục đó, double-click vào file **`build.bat`** (hoặc mở CMD tại thư mục này rồi gõ `build.bat`).
4. Đợi quá trình cài đặt và đóng gói hoàn tất (khoảng 1–2 phút).
5. File `.exe` sẽ nằm ở: `dist\QuanLyChiTieu.exe` — copy file này ra dùng thoải mái, không cần cài Python nữa.

Lưu ý: `expenses.db` sẽ được tạo ngay cạnh file `.exe`, nên hãy giữ file `.exe` trong một thư mục cố định để không bị mất dữ liệu khi di chuyển.

### Build thủ công (không dùng build.bat)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name QuanLyChiTieu gui.py
```

## Mở rộng trong tương lai (gợi ý)

- Xuất báo cáo ra file CSV/Excel
- Vẽ biểu đồ bằng matplotlib
- Đặt hạn mức chi tiêu (budget) theo danh mục và cảnh báo khi vượt
- Giao diện đồ họa (Tkinter) hoặc web (Flask)
