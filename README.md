# Quản lý Chi tiêu Cá nhân

Ứng dụng dòng lệnh (CLI) đơn giản giúp bạn ghi lại các khoản thu/chi,
phân loại theo danh mục và xem tổng kết theo từng tháng.

## Yêu cầu

- Python 3.8 trở lên (không cần cài thêm thư viện ngoài, chỉ dùng thư viện chuẩn)

## Cách chạy

```bash
python3 main.py
```

Dữ liệu được lưu trong file `expenses.db` (SQLite) cùng thư mục,
sẽ tự động được tạo ở lần chạy đầu tiên.

## Chức năng

1. **Thêm khoản thu** – ghi lại tiền lương, thưởng, trợ cấp...
2. **Thêm khoản chi** – ghi lại chi tiêu theo danh mục: Ăn uống, Học tập,
   Giải trí, Đi lại, Hóa đơn, hoặc danh mục tự đặt.
3. **Xem danh sách giao dịch** – liệt kê toàn bộ giao dịch đã nhập.
4. **Xem tổng kết theo tháng** – tổng thu, tổng chi, số dư, và tỷ lệ
   chi tiêu theo từng danh mục (kèm biểu đồ thanh đơn giản).
5. **Xóa giao dịch** – xóa một giao dịch theo ID.

## Cấu trúc dự án

```
expense_tracker/
├── main.py         # Giao diện dòng lệnh, luồng chính của ứng dụng
├── database.py     # Thao tác với SQLite (thêm, lấy, xóa giao dịch)
├── utils.py        # Danh mục mặc định, định dạng tiền tệ/ngày tháng
├── expenses.db      # Cơ sở dữ liệu (tự tạo khi chạy lần đầu)
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
pyinstaller --onefile --console --name QuanLyChiTieu main.py
```

## Mở rộng trong tương lai (gợi ý)

- Xuất báo cáo ra file CSV/Excel
- Vẽ biểu đồ bằng matplotlib
- Đặt hạn mức chi tiêu (budget) theo danh mục và cảnh báo khi vượt
- Giao diện đồ họa (Tkinter) hoặc web (Flask)
