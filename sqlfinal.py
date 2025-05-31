import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# Database setup
conn = sqlite3.connect('user.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    code_melli TEXT NOT NULL UNIQUE
)
''')
conn.commit()

def add_user():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    code_melli = entry_code_melli.get()
    if not (first_name and last_name and code_melli):
        messagebox.showwarning("خطا", "همه فیلدها را پر کنید!")
        return
    try:
        cursor.execute('INSERT INTO users (first_name, last_name, code_melli) VALUES (?, ?, ?)',
                       (first_name, last_name, code_melli))
        conn.commit()
        messagebox.showinfo("موفق", "کاربر با موفقیت اضافه شد.")
        show_all_users()
    except sqlite3.IntegrityError:
        messagebox.showerror("خطا", "کد ملی تکراری است!")

def find_user():
    code_melli = simpledialog.askstring("جستجو", "کد ملی را وارد کنید:")
    if code_melli:
        cursor.execute('SELECT * FROM users WHERE code_melli = ?', (code_melli,))
        user = cursor.fetchone()
        if user:
            messagebox.showinfo("یافت شد", f"کاربر: {user}")
        else:
            messagebox.showwarning("یافت نشد", "کاربری با این کد ملی یافت نشد.")

def show_all_users():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    for user in users:
        tree.insert('', tk.END, values=user)

# GUI setup
root = tk.Tk()
root.title("مدیریت کاربران")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="نام:").grid(row=0, column=0)
entry_first_name = tk.Entry(frame)
entry_first_name.grid(row=0, column=1)

tk.Label(frame, text="نام خانوادگی:").grid(row=1, column=0)
entry_last_name = tk.Entry(frame)
entry_last_name.grid(row=1, column=1)

tk.Label(frame, text="کد ملی:").grid(row=2, column=0)
entry_code_melli = tk.Entry(frame)
entry_code_melli.grid(row=2, column=1)

tk.Button(frame, text="افزودن کاربر", command=add_user).grid(row=3, column=0, pady=5)
tk.Button(frame, text="جستجو با کد ملی", command=find_user).grid(row=3, column=1, pady=5)

tree = ttk.Treeview(root, columns=("id", "first_name", "last_name", "code_melli"), show="headings")
tree.heading("id", text="ID")
tree.heading("first_name", text="نام")
tree.heading("last_name", text="نام خانوادگی")
tree.heading("code_melli", text="کد ملی")
tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

show_all_users()

root.mainloop()
conn.close()