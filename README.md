

## bash
python3 gui.py      # Bản giao diện cửa sổ (khuyên dùng)
python3 main.py     # Bản dòng lệnh (CLI)


Dữ liệu được lưu trong file `expenses.db` (SQLite) cùng thư mục,
sẽ tự động được tạo ở lần chạy đầu tiên. Cả hai bản GUI và CLI
dùng chung một database, có thể chạy xen kẽ thoải mái.
Lưu ý: `expenses.db` sẽ được tạo ngay cạnh file `.exe`, nên hãy giữ file `.exe` trong một thư mục cố định để không bị mất dữ liệu khi di chuyển.

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

## Mở rộng trong tương lai

- Xuất báo cáo ra file CSV/Excel
- Vẽ biểu đồ bằng matplotlib
- Đặt hạn mức chi tiêu (budget) theo danh mục và cảnh báo khi vượt
- Giao diện đồ họa (Tkinter) hoặc web (Flask)
