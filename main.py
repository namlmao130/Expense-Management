"""
main.py
Ứng dụng dòng lệnh Quản lý Chi tiêu Cá nhân.
Cho phép nhập khoản thu/chi, phân loại theo danh mục,
và xem tổng kết theo tháng.
"""

from collections import defaultdict
from datetime import datetime

import database
import utils

MONTH_NAMES_VI = [
    "", "Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6",
    "Tháng 7", "Tháng 8", "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12",
]


def print_header(title):
    print("\n" + "=" * 50)
    print(title.center(50))
    print("=" * 50)


def add_transaction_flow(type_):
    """Luồng nhập một khoản thu hoặc chi từ người dùng."""
    label = "KHOẢN THU" if type_ == "thu" else "KHOẢN CHI"
    print_header(f"THÊM {label}")

    while True:
        try:
            amount_text = input("Số tiền (VD: 50000 hoặc 50.000): ")
            amount = utils.parse_amount(amount_text)
            break
        except ValueError:
            print("⚠ Số tiền không hợp lệ. Vui lòng nhập lại.")

    category = utils.choose_category(type_)
    description = input("Ghi chú (có thể để trống): ").strip()

    while True:
        try:
            date_text = input("Ngày (dd/mm/yyyy, Enter = hôm nay): ")
            date_iso = utils.parse_date(date_text)
            break
        except ValueError:
            print("⚠ Định dạng ngày không hợp lệ (VD: 25/12/2025). Vui lòng nhập lại.")

    database.add_transaction(type_, amount, category, description, date_iso)
    print(f"\n✅ Đã thêm {label.lower()}: {utils.format_currency(amount)} "
          f"- {category} - {utils.display_date(date_iso)}")


def list_transactions_flow():
    """Hiển thị toàn bộ giao dịch đã lưu."""
    print_header("DANH SÁCH GIAO DỊCH")
    transactions = database.get_all_transactions()

    if not transactions:
        print("Chưa có giao dịch nào.")
        return

    print(f"{'ID':<5}{'Loại':<8}{'Số tiền':<15}{'Danh mục':<14}{'Ngày':<12}{'Ghi chú'}")
    print("-" * 75)
    for t in transactions:
        loai = "Thu" if t["type"] == "thu" else "Chi"
        print(
            f"{t['id']:<5}{loai:<8}{utils.format_currency(t['amount']):<15}"
            f"{t['category']:<14}{utils.display_date(t['date']):<12}{t['description'] or ''}"
        )


def monthly_summary_flow():
    """Hiển thị tổng kết thu/chi theo tháng do người dùng chọn."""
    print_header("TỔNG KẾT THEO THÁNG")

    available_months = database.get_available_months()
    if not available_months:
        print("Chưa có dữ liệu để tổng kết.")
        return

    print("Các tháng có dữ liệu:")
    for ym in available_months:
        year, month = ym.split("-")
        print(f"  - {MONTH_NAMES_VI[int(month)]} năm {year} ({ym})")

    default_ym = available_months[0]
    text = input(f"\nNhập tháng cần xem (yyyy-mm, Enter = {default_ym}): ").strip()
    ym = text if text else default_ym

    try:
        year, month = map(int, ym.split("-"))
    except ValueError:
        print("⚠ Định dạng tháng không hợp lệ.")
        return

    transactions = database.get_transactions_by_month(year, month)
    if not transactions:
        print(f"Không có giao dịch nào trong {MONTH_NAMES_VI[month]} năm {year}.")
        return

    total_income = sum(t["amount"] for t in transactions if t["type"] == "thu")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "chi")
    balance = total_income - total_expense

    # Tổng chi theo từng danh mục
    expense_by_category = defaultdict(float)
    income_by_category = defaultdict(float)
    for t in transactions:
        if t["type"] == "chi":
            expense_by_category[t["category"]] += t["amount"]
        else:
            income_by_category[t["category"]] += t["amount"]

    print(f"\n📅 {MONTH_NAMES_VI[month]} năm {year}")
    print("-" * 50)
    print(f"Tổng thu:  {utils.format_currency(total_income)}")
    print(f"Tổng chi:  {utils.format_currency(total_expense)}")
    balance_label = "Dư" if balance >= 0 else "Thâm hụt"
    print(f"{balance_label}:    {utils.format_currency(abs(balance))}")

    if expense_by_category:
        print("\n💸 Chi tiêu theo danh mục:")
        for cat, amt in sorted(expense_by_category.items(), key=lambda x: -x[1]):
            percent = (amt / total_expense * 100) if total_expense else 0
            bar = "█" * int(percent / 5)
            print(f"  {cat:<12} {utils.format_currency(amt):<15} {percent:5.1f}% {bar}")

    if income_by_category:
        print("\n💰 Thu nhập theo danh mục:")
        for cat, amt in sorted(income_by_category.items(), key=lambda x: -x[1]):
            percent = (amt / total_income * 100) if total_income else 0
            print(f"  {cat:<12} {utils.format_currency(amt):<15} {percent:5.1f}%")


def delete_transaction_flow():
    """Xóa một giao dịch theo ID."""
    print_header("XÓA GIAO DỊCH")
    list_transactions_flow()
    text = input("\nNhập ID giao dịch cần xóa (Enter để hủy): ").strip()
    if not text:
        return
    if not text.isdigit():
        print("⚠ ID không hợp lệ.")
        return
    if database.delete_transaction(int(text)):
        print("✅ Đã xóa giao dịch.")
    else:
        print("⚠ Không tìm thấy giao dịch với ID này.")


def show_menu():
    print_header("QUẢN LÝ CHI TIÊU CÁ NHÂN")
    print("1. Thêm khoản thu")
    print("2. Thêm khoản chi")
    print("3. Xem danh sách giao dịch")
    print("4. Xem tổng kết theo tháng")
    print("5. Xóa giao dịch")
    print("0. Thoát")


def main():
    database.init_db()
    while True:
        show_menu()
        choice = input("\nChọn chức năng: ").strip()

        if choice == "1":
            add_transaction_flow("thu")
        elif choice == "2":
            add_transaction_flow("chi")
        elif choice == "3":
            list_transactions_flow()
        elif choice == "4":
            monthly_summary_flow()
        elif choice == "5":
            delete_transaction_flow()
        elif choice == "0":
            print("\nCảm ơn bạn đã sử dụng ứng dụng. Hẹn gặp lại!")
            break
        else:
            print("⚠ Lựa chọn không hợp lệ, vui lòng thử lại.")

        input("\n(Nhấn Enter để tiếp tục...)")


if __name__ == "__main__":
    main()
