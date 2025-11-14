import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, date

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.tasks = []

        self.root.title("To-Do List")
        self.root.geometry("750x500")
        self.root.configure(bg="#F8F9FA")
        self.root.resizable(False, False)

        self.setup_styles()
        self.create_widgets()
        self.load_tasks()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        self.accent = "#A3C9A8"
        self.hover = "#86B49B"
        self.text_dark = "#37474F"
        self.bg_light = "#F8F9FA"

        style.configure(
            "Accent.TButton",
            font=("Segoe UI", 11, "bold"),
            background=self.accent,
            foreground=self.text_dark,
            borderwidth=0,
            padding=8
        )
        style.map("Accent.TButton",
                  background=[("active", self.hover)],
                  foreground=[("active", "#1B1B1B")])

        style.configure("TLabel", background=self.bg_light, foreground=self.text_dark, font=("Segoe UI", 12))
        style.configure("Header.TLabel", background=self.bg_light, foreground="#2F4858", font=("Segoe UI", 22, "bold"))
        style.configure("TEntry", padding=6, font=("Segoe UI", 12))

    def create_widgets(self):
        header = ttk.Label(self.root, text="My To-Do List", style="Header.TLabel")
        header.pack(pady=(20, 10))

        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10, padx=20, fill="x")

        self.task_field = ttk.Entry(input_frame, font=("Segoe UI", 12))
        self.task_field.pack(side="left", expand=True, fill="x", padx=(0, 10))

        self.date_field = ttk.Entry(input_frame, width=12, font=("Segoe UI", 12))
        self.date_field.insert(0, date.today().strftime('%Y-%m-%d'))
        self.date_field.pack(side="left", padx=(0, 10))

        add_btn = ttk.Button(input_frame, text="Add Task", style="Accent.TButton", command=self.add_task)
        add_btn.pack(side="left")

        list_frame = ttk.Frame(self.root)
        list_frame.pack(pady=10, padx=25, fill="both", expand=True)

        self.task_list = tk.Listbox(
            list_frame,
            font=("Segoe UI", 12),
            bg="white",
            fg=self.text_dark,
            selectbackground=self.accent,
            selectforeground="black",
            activestyle="none",
            relief="flat",
            highlightthickness=1,
            highlightcolor=self.accent
        )
        self.task_list.pack(side="left", fill="both", expand=True, padx=(0, 5))

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.task_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.task_list.config(yscrollcommand=scrollbar.set)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Remove Task", style="Accent.TButton", command=self.delete_task).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Delete All", style="Accent.TButton", command=self.delete_all_tasks).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="Search Task", style="Accent.TButton", command=self.search_task).grid(row=0, column=2, padx=10)
        ttk.Button(btn_frame, text="Exit", style="Accent.TButton", command=self.close).grid(row=0, column=3, padx=10)

        self.task_list.bind("<Double-1>", lambda e: self.delete_task())

    def add_task(self):
        task = self.task_field.get().strip()
        due_date = self.date_field.get().strip()
        if not task:
            messagebox.showwarning("Input Error", "Please enter a task.")
            return

        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Input Error", "Date must be in YYYY-MM-DD format.")
            return

        self.tasks.append({"title": task, "due": due_date})
        self.task_field.delete(0, "end")
        self.load_tasks()

    def delete_task(self):
        try:
            index = self.task_list.curselection()[0]
            self.tasks.pop(index)
            self.load_tasks()
        except IndexError:
            messagebox.showinfo("Error", "No task selected.")

    def delete_all_tasks(self):
        if messagebox.askyesno("Confirm Delete", "Delete all tasks?"):
            self.tasks.clear()
            self.load_tasks()

    def load_tasks(self):
        self.task_list.delete(0, "end")
        for task in self.tasks:
            self.task_list.insert("end", f"• {task['title']}  |  Due: {task['due']}")

        if self.tasks:
            earliest_index = self.get_earliest_due_index()
            self.task_list.selection_clear(0, tk.END)
            self.task_list.selection_set(earliest_index)
            self.task_list.see(earliest_index)

    def binary_search(self, sorted_tasks, target):
        low, high = 0, len(sorted_tasks) - 1
        while low <= high:
            mid = (low + high) // 2
            mid_val = sorted_tasks[mid]['title'].lower()
            if mid_val == target.lower():
                return mid
            elif mid_val < target.lower():
                low = mid + 1
            else:
                high = mid - 1
        return -1

    def search_task(self):
        if not self.tasks:
            messagebox.showinfo("Info", "No tasks to search.")
            return

        task_name = simpledialog.askstring("Search Task", "Enter task title:")
        if not task_name:
            return

        sorted_tasks = sorted(self.tasks, key=lambda x: x['title'].lower())
        index = self.binary_search(sorted_tasks, task_name)

        if index != -1:
            task_found = sorted_tasks[index]
            messagebox.showinfo("Task Found", f"Task: {task_found['title']}\nDue: {task_found['due']}")
        else:
            messagebox.showinfo("Not Found", "Task not found.")

    def get_earliest_due_index(self):
        if not self.tasks:
            return None
        earliest_index = 0
        earliest_date = self.tasks[0]['due']
        for i, task in enumerate(self.tasks):
            if task['due'] < earliest_date:
                earliest_date = task['due']
                earliest_index = i
        return earliest_index

    def close(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
