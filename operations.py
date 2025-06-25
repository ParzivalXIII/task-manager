import datetime
import json
import csv
from operator import itemgetter

def validate_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


class Tasks_Manager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title=None):
        if title is None:  # Interactive mode
            while True:
                title = input("Enter task title: ").strip()
                if title:
                    break
            print("❌ Title cannot be empty. Please enter a valid title.")

        # Category Validation
        while True:
            category = input("Category: ").strip()
            if category:
                break
            print("❌ Category cannot be empty. Please enter a valid category.")

        # Due Date Validation
        while True:
            due_date = input("Due date (YYYY-MM-DD): ").strip()
            if validate_date(due_date):
                break
            print("❌ Invalid date format. Please use YYYY-MM-DD.")
        
        self.tasks.append({
            "title": title,
            "category": category,
            "due_date": due_date,
            "completed": False
        })
        print(f"✅ {title} added to tasks.\n")

    def view_tasks(self, filter_by=None):
        if not self.tasks:
            print("No tasks available.\n")
            return
        try:
            filtered = []
            if filter_by == "category":
                while True:
                    cate = input("Enter category to filter: ").strip()
                    if cate:
                        break
                    print("❌ Category cannot be empty. Please enter a valid category.")

                for t in self.tasks:
                    if t["category"].lower() == cate.lower():
                        filtered.append(t)
                    if not filtered:
                        print(f"❌ No tasks found in category '{cate}'.\n")
                        return
            elif filter_by == "due_date":
                filtered = sorted(self.tasks, key=itemgetter("due_date"), reverse=True)
            else:
                filtered = self.tasks
        except KeyError:
            print("Invalid filter option.\n")
            return
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.\n")

        for idx, task in enumerate(filtered, start=1):
            status = "✅" if task["completed"] else "❌"
            print(f"{idx}. {task['title']} | {task['category']} | Due: {task['due_date']} | {status}")
            print()

    def mark_completed(self, task_id=None):
        if not self.tasks:
            print("No tasks available to mark as completed.\n")
            return
        
        print("=====Tasks=====")
        print("Here are your tasks:")
        self.view_tasks()
        try:
            task_id = int(input("Enter task number to mark as completed: "))
        except ValueError:
            print("❌ Invalid input. Please enter a number.\n")
            return

        try:
            idx = task_id - 1
            if 0 <= idx < len(self.tasks):
                self.tasks[idx]["completed"] = True
                print(f"✅ Task '{self.tasks[idx]['title']}' marked as completed.\n")
            else:
                raise IndexError("❌Invalid task number.")
        except ValueError as e:
            print(f"❌ {e}\n")

    def delete_task(self, task_id=None):
        if not self.tasks:
            print("No tasks available to delete.\n")
            return

        if task_id is None:  # Interactive mode
            self.view_tasks()
        try:
            task_id = int(input("Enter task number to delete: "))
        except ValueError:
            print("❌ Invalid input. Please enter a number.\n")
            return

        try:
            idx = task_id - 1
            if 0 <= idx < len(self.tasks):
                deleted_task = self.tasks.pop(idx)
                print(f"✅ Task '{deleted_task['title']}' deleted.\n")
            else:
                raise IndexError("❌Invalid task number.")
        except ValueError as e:
            print(f"❌ {e}\n")

    def save_tasks(self, filename="tasks.json"):
        with open(filename, 'w') as f:
            json.dump(self.tasks, f, indent=4)
        print(f"✅ Tasks saved to {filename}.\n")

    def load_tasks(self, filename="tasks.json"):
        global tasks
        try:
            with open(filename, 'r') as f:
                self.tasks = json.load(f)
            print(f"Tasks loaded from {filename}.\n")
        except FileNotFoundError:
            print(f"❌ {filename} not found. Starting with an empty task list.\n")
            self.tasks = []

    def export_to_csv(self, filename="tasks.csv"):
        """Export tasks to a CSV file"""
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["title", "category", "due_date", "completed"])
                writer.writeheader()
                writer.writerows(self.tasks)
            print(f"✅ Tasks exported to {filename}.\n")
        except IOError as e:
            print(f"❌ Error exporting tasks: {e}\n")
