"""
database.py
Xử lý toàn bộ thao tác với cơ sở dữ liệu SQLite cho ứng dụng
Quản lý Chi tiêu Cá nhân.
"""

import sqlite3
import sys
from pathlib import Path


def _get_app_dir():
    """
    Trả về thư mục chứa ứng dụng.
    Khi chạy dạng .py bình thường: thư mục chứa file database.py.
    Khi đã đóng gói bằng PyInstaller (.exe): thư mục chứa file .exe,
    để database không bị lưu vào thư mục tạm rồi mất khi đóng app.
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).parent


DB_PATH = _get_app_dir() / "expenses.db"


def get_connection():
    """Tạo và trả về kết nối tới database SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Khởi tạo bảng transactions nếu chưa tồn tại."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL CHECK(type IN ('thu', 'chi')),
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def add_transaction(type_, amount, category, description, date):
    """Thêm một giao dịch (thu hoặc chi) vào database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO transactions (type, amount, category, description, date)
        VALUES (?, ?, ?, ?, ?)
        """,
        (type_, amount, category, description, date),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_all_transactions(order_by="date DESC"):
    """Lấy toàn bộ giao dịch, sắp xếp theo tiêu chí order_by."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM transactions ORDER BY {order_by}")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_transactions_by_month(year, month):
    """Lấy các giao dịch trong một tháng cụ thể (year-month)."""
    conn = get_connection()
    cursor = conn.cursor()
    month_str = f"{year:04d}-{month:02d}"
    cursor.execute(
        "SELECT * FROM transactions WHERE date LIKE ? ORDER BY date",
        (f"{month_str}%",),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def delete_transaction(transaction_id):
    """Xóa một giao dịch theo id. Trả về True nếu xóa thành công."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


def get_available_months():
    """Trả về danh sách các tháng (YYYY-MM) đã có giao dịch, mới nhất trước."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT substr(date, 1, 7) AS ym FROM transactions ORDER BY ym DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    return [row["ym"] for row in rows]
