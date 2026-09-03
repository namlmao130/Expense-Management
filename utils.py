"""
utils.py
Các hàm tiện ích: danh mục mặc định, định dạng số tiền,
xác thực dữ liệu người dùng nhập vào.
"""

from datetime import datetime

# Danh mục mặc định cho từng loại giao dịch
EXPENSE_CATEGORIES = ["Ăn uống", "Học tập", "Giải trí", "Đi lại", "Hóa đơn", "Khác"]
INCOME_CATEGORIES = ["Lương", "Thưởng", "Trợ cấp", "Đầu tư", "Khác"]


def format_currency(amount):
    """Định dạng số tiền theo kiểu Việt Nam, ví dụ: 1.500.000 đ"""
    return f"{amount:,.0f}".replace(",", ".") + " đ"


def parse_amount(text):
    """Chuyển chuỗi nhập vào thành số tiền (float). Ném ValueError nếu không hợp lệ."""
    cleaned = text.strip().replace(".", "").replace(",", "").replace("đ", "").replace("d", "")
    value = float(cleaned)
    if value <= 0:
        raise ValueError("Số tiền phải lớn hơn 0")
    return value


def parse_date(text):
    """
    Chuyển chuỗi ngày dd/mm/yyyy thành yyyy-mm-dd để lưu vào DB.
    Nếu để trống, trả về ngày hôm nay.
    """
    text = text.strip()
    if not text:
        return datetime.now().strftime("%Y-%m-%d")
    dt = datetime.strptime(text, "%d/%m/%Y")
    return dt.strftime("%Y-%m-%d")


def display_date(iso_date):
    """Chuyển ngày yyyy-mm-dd (lưu trong DB) sang dd/mm/yyyy để hiển thị."""
    dt = datetime.strptime(iso_date, "%Y-%m-%d")
    return dt.strftime("%d/%m/%Y")


def choose_category(type_):
    """
    Hiển thị danh sách danh mục tương ứng với loại giao dịch (thu/chi)
    và cho phép người dùng chọn hoặc nhập danh mục mới.
    """
    categories = INCOME_CATEGORIES if type_ == "thu" else EXPENSE_CATEGORIES
    print("\nChọn danh mục:")
    for i, cat in enumerate(categories, start=1):
        print(f"  {i}. {cat}")
    print(f"  {len(categories) + 1}. Nhập danh mục khác")

    while True:
        choice = input("Lựa chọn của bạn: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(categories):
                return categories[idx - 1]
            if idx == len(categories) + 1:
                custom = input("Nhập tên danh mục mới: ").strip()
                if custom:
                    return custom
        print("Lựa chọn không hợp lệ, vui lòng thử lại.")
