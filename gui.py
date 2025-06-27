import customtkinter as ctk
from tkinter import messagebox, filedialog
from operations import validate_date, Tasks_Manager
import datetime
from tkcalendar import DateEntry

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Custom colors
COLORS = {
    'window_bg': '#2E2E2E',      # Dark gray
    'frame_bg': '#3F3F74',       # Indigo
    'button_fg': '#FFFFFF',      # White text
    'text_fg': '#FFFFFF'         # White text
}

class TaskInputDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add New Task")
        
        # Calculate 40% of parent window size
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        dialog_width = int(parent_width * 0.2)
        dialog_height = int(parent_height * 0.2)
        
        # Set size and position
        self.geometry(f"{dialog_width}x{dialog_height}+{parent.winfo_rootx() + 50}+{parent.winfo_rooty() + 50}")
        self.resizable(False, False)
        self.transient(parent)
        
        self.create_widgets()
        self.grab_set()
        self.result = None

    def create_widgets(self):
        # Main container frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        ctk.CTkLabel(main_frame, text="Title:").pack(anchor="w", padx=5, pady=2)
        self.title_var = ctk.StringVar()
        ctk.CTkEntry(main_frame, textvariable=self.title_var, width=300).pack(fill="x", padx=5, pady=2)

        # Category
        ctk.CTkLabel(main_frame, text="Category:").pack(anchor="w", padx=5, pady=2)
        self.category_var = ctk.StringVar()
        ctk.CTkEntry(main_frame, textvariable=self.category_var, width=300).pack(fill="x", padx=5, pady=2)

        # Due Date
        ctk.CTkLabel(main_frame, text="Due Date:").pack(anchor="w", padx=5, pady=2)
        date_frame = ctk.CTkFrame(main_frame)
        date_frame.pack(fill="x", padx=5, pady=2)
        self.date_var = ctk.StringVar()
        cal = DateEntry(date_frame, width=30,
                       date_pattern='yyyy-mm-dd',
                       textvariable=self.date_var)
        cal.pack(side="left", padx=5)

        # Buttons
        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.pack(fill="x", pady=10)
        ctk.CTkButton(btn_frame, text="Add Task", command=self.on_add).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Cancel", command=self.on_cancel).pack(side="right", padx=5)

    def on_add(self):
        title = self.title_var.get().strip()
        category = self.category_var.get().strip()
        due_date = self.date_var.get().strip()

        if not all([title, category, due_date]):
            messagebox.showerror("Error", "All fields are required!", parent=self)
            return

        if not validate_date(due_date):
            messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD", parent=self)
            return

        self.result = {
            "title": title,
            "category": category,
            "due_date": due_date
        }
        self.destroy()

    def on_cancel(self):
        self.destroy()

class TaskManagerGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Task Manager")
        self.root.minsize(600, 400)
        
        self.manager = Tasks_Manager()
        self.manager.load_tasks()
        
        # Initialize filter variables
        self.filter_var = ctk.StringVar(value="all")
        self.category_var = ctk.StringVar()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Button frame
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=10)
        
        # Buttons
        buttons = [
            ("Add Task", self.add_task),
            ("Mark Complete", self.mark_completed),
            ("Delete", self.delete_task),
            ("Export CSV", self.export_csv)
        ]
        
        for text, command in buttons:
            ctk.CTkButton(button_frame, text=text, command=command).pack(side="left", padx=5)

        # Filter frame
        filter_frame = ctk.CTkFrame(main_frame)
        filter_frame.pack(fill="x", pady=5)
        
        # Filter options
        filters = [("All", "all"), ("By Category", "category"), ("By Due Date", "due_date")]
        for text, value in filters:
            ctk.CTkRadioButton(filter_frame, text=text, variable=self.filter_var,
                             value=value, command=self.update_task_list).pack(side="left", padx=10)

        # Task list frame with scrollbar
        self.task_frame = ctk.CTkScrollableFrame(main_frame, height=400)
        self.task_frame.pack(fill="both", expand=True, pady=10, padx=5)
        
        # Dictionary to store task buttons
        self.task_buttons = {}
        
        self.update_task_list()
        
        # Save on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_task_list(self):
        # Clear existing task buttons
        for button in self.task_buttons.values():
            button.destroy()
        self.task_buttons.clear()
        
        tasks = self.manager.tasks
        
        if self.filter_var.get() == "category":
            category = self.category_var.get().strip()
            if category:
                tasks = [t for t in tasks if t["category"].lower() == category.lower()]
        elif self.filter_var.get() == "due_date":
            tasks = sorted(tasks, key=lambda x: x["due_date"], reverse=True)
            
        for i, task in enumerate(tasks, 1):
            status = "✅" if task["completed"] else "❌"
            task_text = f"{i}. {task['title']} | {task['category']} | Due: {task['due_date']} | {status}"
            
            # Create button for each task
            btn = ctk.CTkButton(
                self.task_frame, 
                text=task_text,
                height=40,
                anchor="w",
                fg_color=COLORS['frame_bg'],
                hover_color="#4B4B8C",  # Slightly lighter than frame_bg
                command=lambda idx=i-1: self.select_task(idx)
            )
            btn.pack(fill="x", pady=2)
            self.task_buttons[i-1] = btn
        
        if not tasks:
            ctk.CTkLabel(self.task_frame, 
                        text="No tasks available",
                        text_color=COLORS['text_fg']).pack(pady=20)

    def select_task(self, idx):
        # Highlight selected task
        for i, btn in self.task_buttons.items():
            if i == idx:
                btn.configure(fg_color="#4B4B8C")
            else:
                btn.configure(fg_color=COLORS['frame_bg'])
        self.selected_task_idx = idx

    def add_task(self):
        dialog = TaskInputDialog(self.root)
        self.root.wait_window(dialog)
        
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
        if not hasattr(self, 'selected_task_idx'):
            messagebox.showwarning("Warning", "Please select a task to mark as completed!")
            return
            
        self.manager.tasks[self.selected_task_idx]["completed"] = True
        self.update_task_list()

    def delete_task(self):
        if not hasattr(self, 'selected_task_idx'):
            messagebox.showwarning("Warning", "Please select a task to delete!")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
            del self.manager.tasks[self.selected_task_idx]
            delattr(self, 'selected_task_idx')
            self.update_task_list()

    def export_csv(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="tasks.csv",
            title="Export Tasks to CSV"
        )
        if filename:
            self.manager.export_to_csv(filename)
            messagebox.showinfo("Success", f"Tasks exported to {filename}")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to save before quitting?"):
            self.manager.save_tasks()
        self.root.destroy()

def main():
    # Make Windows DPI aware
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except (ImportError, AttributeError):
        pass

    app = TaskManagerGUI()
    app.root.mainloop()

if __name__ == "__main__":
    main()