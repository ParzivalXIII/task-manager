from operations import Tasks_Manager
import argparse


def interactive_mode():
    manager = Tasks_Manager()
    manager.load_tasks()

    while True:
        print("=====Welcome to the Task Manager!=====")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Export to CSV")
        print("6. Exit")

        choice = input("Choose an option (1-6): ")

        match choice:
            case '1':
                manager.add_task(None)
            case '2': 
                filter_option = input("Filter by (category/due_date) or press Enter to view all tasks: ").strip().lower()
                if filter_option in ["category", "due_date"]:
                    manager.view_tasks(filter_by=filter_option)
                else:
                    manager.view_tasks()
            case '3': manager.mark_completed()
            case '4': manager.delete_task()
            case '5':
                filename = input("Enter CSV filename (or press Enter for default 'tasks.csv'): ").strip()
                if not filename:
                    filename = "tasks.csv"
                manager.export_to_csv(filename)
            case '6':
                print("Exiting Task Manager. Goodbye!")
                break
            case _:
                print("❌ Invalid choice. Please choose a valid option (1-6).")

def main():
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    parser.add_argument("--gui", action="store_true", help="Launch GUI version")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument('-a', '--add', type=str, metavar='TITLE', help='Add a new task')
    parser.add_argument('-v', '--view', action='store_true', help='View all tasks')
    parser.add_argument('-f', '--filter', type=str, choices=['category', 'due_date'], help='Filter tasks by category or due date')
    parser.add_argument('-c', '--complete', type=bool, metavar='TASK_ID', help='Mark a task as completed by ID')
    parser.add_argument('-d', '--delete', type=int, metavar='TASK_ID', help='Delete a task by ID')
    parser.add_argument('-s', '--save', action='store_true', help='Save tasks to file')
    parser.add_argument('-l', '--load', action='store_true', help='Load tasks from file')
    parser.add_argument('-e', '--export', type=str, metavar='FILENAME', help='Export tasks to CSV file (default: tasks.csv)')

    args = parser.parse_args()
    manager = Tasks_Manager()
    manager.load_tasks()

    if args.gui:
        from gui import main as gui_main
        gui_main()
    elif args.interactive or not any([args.add, args.view, args.filter, args.complete, args.delete, args.save, args.load, args.export]):
        interactive_mode()
    else:
        if args.add:
            manager.add_task(args.add)
        if args.view:
            if args.filter:
                manager.view_tasks(filter_by=args.filter)
            else:
                manager.view_tasks()
        if args.complete is not None:
            manager.mark_completed()
        if args.delete is not None:
            manager.delete_task()
        if args.save:
            manager.save_tasks()
        if args.load:
            manager.load_tasks()
        if args.export:
            manager.export_to_csv(args.export)

if __name__ == "__main__":
    main()