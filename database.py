"""
database.py
Xử lý toàn bộ thao tác với cơ sở dữ liệu SQLite cho ứng dụng
Quản lý Chi tiêu Cá nhân.

Có 2 chế độ dùng file này:
1. Chế độ "file cố định" (dùng cho bản CLI - main.py): mọi hàm gọi
   không kèm tham số `conn` sẽ tự mở/ghi/đóng trực tiếp vào DB_PATH,
   y hệt như trước đây.
2. Chế độ "phiên làm việc trong bộ nhớ" (dùng cho bản GUI - gui.py):
   toàn bộ dữ liệu được nạp vào một kết nối SQLite trong RAM
   (giống 1 "tài liệu" đang mở), chỉ thực sự ghi ra ổ đĩa khi gọi
   save_session_to_file(). Nhờ vậy GUI mới làm được các thao tác
   kiểu Notepad: Mới / Mở / Lưu / Lưu thành...
"""

import sqlite3
import sys
from pathlib import Path

SCHEMA_SQL = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL CHECK(type IN ('thu', 'chi')),
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL
    )
"""


def _get_app_dir():
    """
    Trả về thư mục chứa ứng dụng.
    Khi chạy dạng .py bình thường: thư mục chứa file database.py.
    Khi đã đóng gói bằng PyInstaller (.exe): thư mục chứa file .exe.
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).parent


# Vị trí file mặc định, dùng cho bản CLI và làm gợi ý "file gần đây
# nhất" khi bản GUI khởi động lần đầu.
DB_PATH = _get_app_dir() / "expenses.db"


# ---------------------------------------------------------------------
# CHẾ ĐỘ FILE CỐ ĐỊNH (dùng cho main.py / CLI - giữ nguyên hành vi cũ)
# ---------------------------------------------------------------------

def get_connection():
    """Tạo và trả về kết nối tới database SQLite mặc định (DB_PATH)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Khởi tạo bảng transactions nếu chưa tồn tại (file mặc định)."""
    conn = get_connection()
    conn.execute(SCHEMA_SQL)
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------
# CHẾ ĐỘ PHIÊN LÀM VIỆC TRONG BỘ NHỚ (dùng cho gui.py)
# ---------------------------------------------------------------------

def create_schema(conn):
    """Tạo bảng transactions trên một kết nối bất kỳ nếu chưa có."""
    conn.execute(SCHEMA_SQL)
    conn.commit()


def new_session_db():
    """Tạo một 'tài liệu' mới, trống, sống trong bộ nhớ (chưa gắn với file nào)."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    create_schema(conn)
    return conn


def load_file_into_session(path):
    """
    Mở một file .db trên ổ đĩa và nạp toàn bộ nội dung của nó vào
    một kết nối bộ nhớ mới. Trả về kết nối bộ nhớ đó.
    """
    file_conn = sqlite3.connect(str(path))
    create_schema(file_conn)
    session_conn = sqlite3.connect(":memory:")
    session_conn.row_factory = sqlite3.Row
    file_conn.backup(session_conn)
    file_conn.close()
    return session_conn


def save_session_to_file(session_conn, path):
    """Ghi toàn bộ nội dung đang có trong session_conn ra file .db tại path (ghi đè)."""
    path = Path(path)
    if path.exists():
        try:
            path.unlink()
        except OSError:
            pass  # sẽ để backup() ghi đè trực tiếp nếu không xóa được
    file_conn = sqlite3.connect(str(path))
    session_conn.backup(file_conn)
    file_conn.close()


# ---------------------------------------------------------------------
# CÁC HÀM THAO TÁC DỮ LIỆU (dùng chung cho cả 2 chế độ)
# Nếu truyền `conn`, thao tác trên kết nối đó (không tự đóng).
# Nếu không truyền, dùng file mặc định DB_PATH (hành vi cũ, cho CLI).
# ---------------------------------------------------------------------

def add_transaction(type_, amount, category, description, date, conn=None):
    """Thêm một giao dịch (thu hoặc chi). Trả về id vừa tạo."""
    owns_conn = conn is None
    c = conn if conn is not None else get_connection()
    cursor = c.execute(
        """
        INSERT INTO transactions (type, amount, category, description, date)
        VALUES (?, ?, ?, ?, ?)
        """,
        (type_, amount, category, description, date),
    )
    c.commit()
    new_id = cursor.lastrowid
    if owns_conn:
        c.close()
    return new_id


def get_all_transactions(order_by="date DESC", conn=None):
    """Lấy toàn bộ giao dịch, sắp xếp theo tiêu chí order_by."""
    owns_conn = conn is None
    c = conn if conn is not None else get_connection()
    cursor = c.execute(f"SELECT * FROM transactions ORDER BY {order_by}")
    rows = cursor.fetchall()
    if owns_conn:
        c.close()
    return [dict(row) for row in rows]


def get_transactions_by_month(year, month, conn=None):
    """Lấy các giao dịch trong một tháng cụ thể (year-month)."""
    owns_conn = conn is None
    c = conn if conn is not None else get_connection()
    month_str = f"{year:04d}-{month:02d}"
    cursor = c.execute(
        "SELECT * FROM transactions WHERE date LIKE ? ORDER BY date",
        (f"{month_str}%",),
    )
    rows = cursor.fetchall()
    if owns_conn:
        c.close()
    return [dict(row) for row in rows]


def delete_transaction(transaction_id, conn=None):
    """Xóa một giao dịch theo id. Trả về True nếu xóa thành công."""
    owns_conn = conn is None
    c = conn if conn is not None else get_connection()
    cursor = c.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    c.commit()
    deleted = cursor.rowcount > 0
    if owns_conn:
        c.close()
    return deleted


def get_available_months(conn=None):
    """Trả về danh sách các tháng (YYYY-MM) đã có giao dịch, mới nhất trước."""
    owns_conn = conn is None
    c = conn if conn is not None else get_connection()
    cursor = c.execute(
        "SELECT DISTINCT substr(date, 1, 7) AS ym FROM transactions ORDER BY ym DESC"
    )
    rows = cursor.fetchall()
    if owns_conn:
        c.close()
    return [row["ym"] for row in rows]
