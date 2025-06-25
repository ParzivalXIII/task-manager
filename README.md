# 📝 Task Manager

A versatile Python-based Task Management application that supports both CLI and GUI interfaces. Manage your tasks with categories and due dates, track completion status, and export data in multiple formats.

## ✨ Features

### Multiple Interfaces
- 🖥️ Interactive Command Line Interface (CLI)
- 🪟 Graphical User Interface (GUI) using Tkinter
- ⌨️ Command-line arguments for quick actions

### Task Management
- ➕ Add tasks with title, category, and due date
- 👀 View tasks with filtering options (category/due date)
- ✅ Mark tasks as complete
- 🗑️ Delete tasks
- 🔍 Filter tasks by category or due date

### Data Management
- 💾 Save/load tasks to JSON
- 📊 Export tasks to CSV
- 🔄 Automatic data persistence

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/parzivalXIII/task-manager.git

# Navigate to project directory
cd task-manager

# No additional dependencies required! (Python 3.10+ recommended)
```

## 🎮 Usage

### GUI Mode
```bash
python main.py --gui
```

### Interactive CLI Mode
```bash
python main.py --interactive
```

### Command Line Arguments
```bash
# Add a new task
python main.py -a "New Task"

# View all tasks
python main.py -v

# Filter tasks by category
python main.py -v -f category

# Mark task as complete
python main.py -c <task_id>

# Delete task
python main.py -d <task_id>

# Export to CSV
python main.py -e tasks.csv

# Show help
python main.py --help
```

## 📁 File Structure
```
task-manager/
├── main.py         # Entry point and CLI interface
├── operations.py   # Core task management logic
├── gui.py         # GUI implementation
└── tasks.json     # Data storage (auto-generated)
```

## 💻 System Requirements
- Python 3.10 or higher
- tkinter (included with standard Python installation)
- Windows/Linux/macOS supported

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## 📜 License
[MIT](https://choosealicense.com/licenses/mit/)
