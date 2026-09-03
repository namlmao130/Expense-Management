"""
gui.py
Giao diện cửa sổ (GUI) cho ứng dụng Quản lý Chi tiêu Cá nhân,
dùng tkinter (có sẵn trong Python, không cần cài thêm thư viện).
Dành cho người dùng không rành công nghệ: chỉ cần bấm nút, chọn
trong danh sách, không cần gõ lệnh hay số thứ tự menu.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict
from datetime import datetime

import database
import utils

MONTH_NAMES_VI = [
    "", "Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6",
    "Tháng 7", "Tháng 8", "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12",
]


class ExpenseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quản Lý Chi Tiêu Cá Nhân")
        self.geometry("900x600")
        self.minsize(780, 520)

        style = ttk.Style(self)
        try:
            style.theme_use("vista")
        except tk.TclError:
            pass
        style.configure("Treeview", rowheight=26, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 13, "bold"))
        style.configure("Big.TLabel", font=("Segoe UI", 16, "bold"))

        database.init_db()

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.transactions_tab = ttk.Frame(notebook)
        self.summary_tab = ttk.Frame(notebook)
        notebook.add(self.transactions_tab, text="  Giao dịch  ")
        notebook.add(self.summary_tab, text="  Tổng kết theo tháng  ")

        self._build_transactions_tab()
        self._build_summary_tab()

        self.refresh_transactions()
        self.refresh_months()

    # ---------------------------------------------------------------
    # TAB 1: GIAO DỊCH (thêm / xem / xóa)
    # ---------------------------------------------------------------
    def _build_transactions_tab(self):
        container = self.transactions_tab
        container.columnconfigure(0, weight=0)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)

        # ---- Cột trái: form thêm giao dịch ----
        form = ttk.LabelFrame(container, text="Thêm giao dịch mới", padding=15)
        form.grid(row=0, column=0, sticky="ns", padx=(0, 10))

        ttk.Label(form, text="Loại giao dịch:").grid(row=0, column=0, sticky="w", pady=(0, 4))
        self.type_var = tk.StringVar(value="chi")
        type_frame = ttk.Frame(form)
        type_frame.grid(row=1, column=0, sticky="w", pady=(0, 12))
        ttk.Radiobutton(
            type_frame, text="Khoản chi", variable=self.type_var, value="chi",
            command=self._on_type_change,
        ).pack(side="left", padx=(0, 10))
        ttk.Radiobutton(
            type_frame, text="Khoản thu", variable=self.type_var, value="thu",
            command=self._on_type_change,
        ).pack(side="left")

        ttk.Label(form, text="Số tiền (VNĐ):").grid(row=2, column=0, sticky="w")
        self.amount_entry = ttk.Entry(form, width=28)
        self.amount_entry.grid(row=3, column=0, sticky="we", pady=(0, 12))

        ttk.Label(form, text="Danh mục:").grid(row=4, column=0, sticky="w")
        self.category_combo = ttk.Combobox(form, width=26, state="normal")
        self.category_combo.grid(row=5, column=0, sticky="we", pady=(0, 12))

        ttk.Label(form, text="Ghi chú (không bắt buộc):").grid(row=6, column=0, sticky="w")
        self.desc_entry = ttk.Entry(form, width=28)
        self.desc_entry.grid(row=7, column=0, sticky="we", pady=(0, 12))

        ttk.Label(form, text="Ngày (dd/mm/yyyy):").grid(row=8, column=0, sticky="w")
        self.date_entry = ttk.Entry(form, width=28)
        self.date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.date_entry.grid(row=9, column=0, sticky="we", pady=(0, 16))

        add_btn = ttk.Button(form, text="➕  Thêm giao dịch", command=self._add_transaction)
        add_btn.grid(row=10, column=0, sticky="we")

        self._on_type_change()

        # ---- Cột phải: danh sách giao dịch ----
        list_frame = ttk.LabelFrame(container, text="Danh sách giao dịch", padding=10)
        list_frame.grid(row=0, column=1, sticky="nsew")
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        columns = ("id", "type", "amount", "category", "date", "desc")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        headings = {
            "id": ("ID", 40), "type": ("Loại", 60), "amount": ("Số tiền", 120),
            "category": ("Danh mục", 110), "date": ("Ngày", 90), "desc": ("Ghi chú", 160),
        }
        for col, (text, width) in headings.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor="w")
        self.tree.column("amount", anchor="e")

        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        self.tree.tag_configure("thu", foreground="#0a7d2c")
        self.tree.tag_configure("chi", foreground="#c0392b")

        btn_frame = ttk.Frame(list_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, sticky="we", pady=(10, 0))
        ttk.Button(btn_frame, text="🗑  Xóa giao dịch đã chọn", command=self._delete_selected).pack(side="left")
        ttk.Button(btn_frame, text="🔄  Làm mới", command=self.refresh_transactions).pack(side="left", padx=8)

    def _on_type_change(self):
        cats = utils.INCOME_CATEGORIES if self.type_var.get() == "thu" else utils.EXPENSE_CATEGORIES
        self.category_combo["values"] = cats
        self.category_combo.set(cats[0])

    def _add_transaction(self):
        type_ = self.type_var.get()
        try:
            amount = utils.parse_amount(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Lỗi", "Số tiền không hợp lệ. Vui lòng nhập số lớn hơn 0.")
            return

        category = self.category_combo.get().strip()
        if not category:
            messagebox.showerror("Lỗi", "Vui lòng chọn hoặc nhập danh mục.")
            return

        description = self.desc_entry.get().strip()

        try:
            date_iso = utils.parse_date(self.date_entry.get())
        except ValueError:
            messagebox.showerror("Lỗi", "Ngày không hợp lệ. Định dạng đúng: dd/mm/yyyy (VD: 25/12/2026).")
            return

        database.add_transaction(type_, amount, category, description, date_iso)

        self.amount_entry.delete(0, "end")
        self.desc_entry.delete(0, "end")
        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))

        self.refresh_transactions()
        self.refresh_months()
        messagebox.showinfo("Thành công", "Đã thêm giao dịch mới.")

    def refresh_transactions(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for t in database.get_all_transactions():
            loai = "Thu" if t["type"] == "thu" else "Chi"
            self.tree.insert(
                "", "end",
                values=(
                    t["id"], loai, utils.format_currency(t["amount"]),
                    t["category"], utils.display_date(t["date"]), t["description"] or "",
                ),
                tags=(t["type"],),
            )

    def _delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một giao dịch trong danh sách trước.")
            return
        item = self.tree.item(selected[0])
        transaction_id = item["values"][0]
        if messagebox.askyesno("Xác nhận", f"Xóa giao dịch ID {transaction_id}?"):
            database.delete_transaction(transaction_id)
            self.refresh_transactions()
            self.refresh_months()

    # ---------------------------------------------------------------
    # TAB 2: TỔNG KẾT THEO THÁNG
    # ---------------------------------------------------------------
    def _build_summary_tab(self):
        container = self.summary_tab
        container.columnconfigure(0, weight=1)
        container.rowconfigure(2, weight=1)

        top = ttk.Frame(container, padding=(0, 10))
        top.grid(row=0, column=0, sticky="we")
        ttk.Label(top, text="Chọn tháng:").pack(side="left", padx=(0, 8))
        self.month_combo = ttk.Combobox(top, width=15, state="readonly")
        self.month_combo.pack(side="left")
        self.month_combo.bind("<<ComboboxSelected>>", lambda e: self._show_summary())

        totals = ttk.Frame(container, padding=(0, 5))
        totals.grid(row=1, column=0, sticky="we")
        self.income_label = ttk.Label(totals, text="Tổng thu: —", style="Big.TLabel", foreground="#0a7d2c")
        self.income_label.grid(row=0, column=0, sticky="w", padx=(0, 30))
        self.expense_label = ttk.Label(totals, text="Tổng chi: —", style="Big.TLabel", foreground="#c0392b")
        self.expense_label.grid(row=0, column=1, sticky="w", padx=(0, 30))
        self.balance_label = ttk.Label(totals, text="Số dư: —", style="Big.TLabel")
        self.balance_label.grid(row=0, column=2, sticky="w")

        tables = ttk.Frame(container)
        tables.grid(row=2, column=0, sticky="nsew", pady=(10, 0))
        tables.columnconfigure(0, weight=1)
        tables.columnconfigure(1, weight=1)
        tables.rowconfigure(0, weight=1)

        expense_box = ttk.LabelFrame(tables, text="💸 Chi tiêu theo danh mục", padding=10)
        expense_box.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        expense_box.columnconfigure(0, weight=1)
        expense_box.rowconfigure(0, weight=1)
        self.expense_tree = ttk.Treeview(
            expense_box, columns=("cat", "amount", "pct"), show="headings", height=8
        )
        for col, text, width in [("cat", "Danh mục", 110), ("amount", "Số tiền", 120), ("pct", "%", 60)]:
            self.expense_tree.heading(col, text=text)
            self.expense_tree.column(col, width=width, anchor="w")
        self.expense_tree.column("amount", anchor="e")
        self.expense_tree.column("pct", anchor="e")
        self.expense_tree.grid(row=0, column=0, sticky="nsew")

        income_box = ttk.LabelFrame(tables, text="💰 Thu nhập theo danh mục", padding=10)
        income_box.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        income_box.columnconfigure(0, weight=1)
        income_box.rowconfigure(0, weight=1)
        self.income_tree = ttk.Treeview(
            income_box, columns=("cat", "amount", "pct"), show="headings", height=8
        )
        for col, text, width in [("cat", "Danh mục", 110), ("amount", "Số tiền", 120), ("pct", "%", 60)]:
            self.income_tree.heading(col, text=text)
            self.income_tree.column(col, width=width, anchor="w")
        self.income_tree.column("amount", anchor="e")
        self.income_tree.column("pct", anchor="e")
        self.income_tree.grid(row=0, column=0, sticky="nsew")

        self.no_data_label = ttk.Label(container, text="", foreground="#888")
        self.no_data_label.grid(row=3, column=0, sticky="w", pady=(10, 0))

    def refresh_months(self):
        months = database.get_available_months()
        labels = []
        self._month_map = {}
        for ym in months:
            year, month = ym.split("-")
            label = f"{MONTH_NAMES_VI[int(month)]} {year}"
            labels.append(label)
            self._month_map[label] = ym

        current_selection = self.month_combo.get()
        self.month_combo["values"] = labels
        if labels:
            if current_selection in labels:
                self.month_combo.set(current_selection)
            else:
                self.month_combo.set(labels[0])
            self._show_summary()
        else:
            self.month_combo.set("")
            self._clear_summary()

    def _clear_summary(self):
        self.income_label.config(text="Tổng thu: —")
        self.expense_label.config(text="Tổng chi: —")
        self.balance_label.config(text="Số dư: —")
        for row in self.expense_tree.get_children():
            self.expense_tree.delete(row)
        for row in self.income_tree.get_children():
            self.income_tree.delete(row)
        self.no_data_label.config(text="Chưa có dữ liệu giao dịch nào. Hãy thêm giao dịch ở tab bên cạnh.")

    def _show_summary(self):
        label = self.month_combo.get()
        ym = self._month_map.get(label)
        if not ym:
            self._clear_summary()
            return

        year, month = map(int, ym.split("-"))
        transactions = database.get_transactions_by_month(year, month)

        for row in self.expense_tree.get_children():
            self.expense_tree.delete(row)
        for row in self.income_tree.get_children():
            self.income_tree.delete(row)

        if not transactions:
            self.no_data_label.config(text="Không có giao dịch nào trong tháng này.")
            return
        self.no_data_label.config(text="")

        total_income = sum(t["amount"] for t in transactions if t["type"] == "thu")
        total_expense = sum(t["amount"] for t in transactions if t["type"] == "chi")
        balance = total_income - total_expense

        self.income_label.config(text=f"Tổng thu: {utils.format_currency(total_income)}")
        self.expense_label.config(text=f"Tổng chi: {utils.format_currency(total_expense)}")
        balance_text = "Dư" if balance >= 0 else "Thâm hụt"
        self.balance_label.config(
            text=f"{balance_text}: {utils.format_currency(abs(balance))}",
            foreground="#0a7d2c" if balance >= 0 else "#c0392b",
        )

        expense_by_category = defaultdict(float)
        income_by_category = defaultdict(float)
        for t in transactions:
            if t["type"] == "chi":
                expense_by_category[t["category"]] += t["amount"]
            else:
                income_by_category[t["category"]] += t["amount"]

        for cat, amt in sorted(expense_by_category.items(), key=lambda x: -x[1]):
            pct = (amt / total_expense * 100) if total_expense else 0
            self.expense_tree.insert("", "end", values=(cat, utils.format_currency(amt), f"{pct:.1f}%"))

        for cat, amt in sorted(income_by_category.items(), key=lambda x: -x[1]):
            pct = (amt / total_income * 100) if total_income else 0
            self.income_tree.insert("", "end", values=(cat, utils.format_currency(amt), f"{pct:.1f}%"))


def main():
    app = ExpenseApp()
    app.mainloop()


if __name__ == "__main__":
    main()
