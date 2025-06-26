import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from operations import validate_date, Tasks_Manager
import datetime

class TaskInputDialog:
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New Task")
        self.dialog.geometry("300x200")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50))
        
        # Form fields
        self.create_widgets()
        
        # Make dialog modal
        self.dialog.grab_set()
        self.result = None

    def create_widgets(self):
        # Title
        title_frame = ttk.Frame(self.dialog, padding="5")
        title_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(title_frame, text="Title:").pack(side=tk.LEFT)
        self.title_var = tk.StringVar()
        ttk.Entry(title_frame, textvariable=self.title_var, width=30).pack(side=tk.LEFT, padx=5)

        # Category
        cat_frame = ttk.Frame(self.dialog, padding="5")
        cat_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(cat_frame, text="Category:").pack(side=tk.LEFT)
        self.category_var = tk.StringVar()
        ttk.Entry(cat_frame, textvariable=self.category_var, width=30).pack(side=tk.LEFT, padx=5)

        # Due Date
        date_frame = ttk.Frame(self.dialog, padding="5")
        date_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(date_frame, text="Due Date:").pack(side=tk.LEFT)
        self.date_var = tk.StringVar(value="YYYY-MM-DD")
        ttk.Entry(date_frame, textvariable=self.date_var, width=30).pack(side=tk.LEFT, padx=5)

        # Buttons
        btn_frame = ttk.Frame(self.dialog, padding="10")
        btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(btn_frame, text="Add", command=self.on_add).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.on_cancel).pack(side=tk.RIGHT, padx=5)

    def on_add(self):
        title = self.title_var.get().strip()
        category = self.category_var.get().strip()
        due_date = self.date_var.get().strip()

        if not all([title, category, due_date]):
            messagebox.showerror("Error", "All fields are required!", parent=self.dialog)
            return

        if not validate_date(due_date):
            messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD", parent=self.dialog)
            return

        self.result = {
            "title": title,
            "category": category,
            "due_date": due_date
        }
        self.dialog.destroy()

    def on_cancel(self):
        self.dialog.destroy()

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.manager = Tasks_Manager()
        self.manager.load_tasks()
        self.validate_date = validate_date
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Buttons
        ttk.Button(self.main_frame, text="Add Task", command=self.add_task).grid(row=3, column=0, pady=10)
        ttk.Button(self.main_frame, text="Mark Complete", command=self.mark_completed).grid(row=3, column=1, pady=10)
        ttk.Button(self.main_frame, text="Delete", command=self.delete_task).grid(row=3, column=2, pady=10)
        ttk.Button(self.main_frame, text="Export CSV", command=self.export_csv).grid(row=3, column=3, pady=10)
        
        # Filter options
        self.filter_var = tk.StringVar(value="all")
        self.category_var = tk.StringVar()
        ttk.Radiobutton(self.main_frame, text="All", variable=self.filter_var, 
                       value="all", command=self.update_task_list).grid(row=4, column=0)
        ttk.Radiobutton(self.main_frame, text="By Category", variable=self.filter_var,
                       value="category", command=self.update_task_list).grid(row=4, column=1)
        ttk.Radiobutton(self.main_frame, text="By Due Date", variable=self.filter_var,
                       value="due_date", command=self.update_task_list).grid(row=4, column=2)
        
        # Task list
        self.task_list = ttk.Treeview(self.main_frame, columns=("Title", "Category", "Due Date", "Status"),
                                     show="headings", height=10)
        self.task_list.grid(row=5, column=0, columnspan=3, pady=10)
        
        # Configure columns
        self.task_list.heading("Title", text="Title")
        self.task_list.heading("Category", text="Category")
        self.task_list.heading("Due Date", text="Due Date")
        self.task_list.heading("Status", text="Status")
        
        # Initialize task list
        self.update_task_list()
        
        # Save on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def add_task(self):
        dialog = TaskInputDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            self.manager.tasks.append({
                "title": dialog.result["title"],
                "category": dialog.result["category"],
                "due_date": dialog.result["due_date"],
                "completed": False
            })
            self.update_task_list()
            messagebox.showinfo("Success", f"Task '{dialog.result['title']}' added successfully!")
    
    def mark_completed(self):
        selection = self.task_list.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task to mark as completed!")
            return
            
        idx = self.task_list.index(selection[0])
        self.manager.tasks[idx]["completed"] = True
        self.update_task_list()
    
    def delete_task(self):
        selection = self.task_list.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task to delete!")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
            idx = self.task_list.index(selection[0])
            del self.manager.tasks[idx]
            self.update_task_list()
    
    def update_task_list(self):
        for item in self.task_list.get_children():
            self.task_list.delete(item)
            
        tasks = self.manager.tasks
        if self.filter_var.get() == "category":
            category = self.category_var.get().strip()
            if category:
                tasks = [t for t in tasks if t["category"].lower() == category.lower()]
        elif self.filter_var.get() == "due_date":
            tasks = sorted(tasks, key=lambda x: x["due_date"], reverse=True)
            
        for task in tasks:
            status = "✅" if task["completed"] else "❌"
            self.task_list.insert("", "end", values=(
                task["title"],
                task["category"],
                task["due_date"],
                status
            ))
    
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to save before quitting?"):
            self.manager.save_tasks()
        self.root.destroy()
    
    def export_csv(self):
        """Export tasks to a CSV file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="tasks.csv",
            title="Export Tasks to CSV"
        )
        if filename:
            self.manager.export_to_csv(filename)
            messagebox.showinfo("Success", f"Tasks exported to {filename}")

def main():
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()