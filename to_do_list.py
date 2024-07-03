import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class Task:
    def __init__(self, description, priority='low', due_date=None, completed=False):
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = completed

    def __str__(self):
        status = "Done" if self.completed else "Not Done"
        due_date = self.due_date if self.due_date else "No due date"
        return f"[{status}] {self.description} (Priority: {self.priority}, Due: {due_date})"

    def to_dict(self):
        return {
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date,
            'completed': self.completed
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            description=data['description'],
            priority=data.get('priority', 'low'),
            due_date=data.get('due_date'),
            completed=data.get('completed', False)
        )

class TaskManager:
    def __init__(self, filename='tasks.json'):
        self.tasks = []
        self.filename = filename
        self.load_tasks()

    def add_task(self, description, priority='low', due_date=None):
        task = Task(description, priority, due_date)
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save_tasks()
        else:
            print("Invalid task number")

    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True
            self.save_tasks()
        else:
            print("Invalid task number")

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                tasks_data = json.load(file)
                self.tasks = [Task.from_dict(data) for data in tasks_data]

class TaskManagerGUI(tk.Tk):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.title("Task Manager")
        self.geometry("500x400")

        self.create_widgets()
        self.update_task_list()

    def create_widgets(self):
        self.task_listbox = tk.Listbox(self, height=15, width=50)
        self.task_listbox.pack(pady=20)

        self.add_button = tk.Button(self, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        self.remove_button = tk.Button(self, text="Remove Task", command=self.remove_task)
        self.remove_button.pack(pady=5)

        self.complete_button = tk.Button(self, text="Complete Task", command=self.complete_task)
        self.complete_button.pack(pady=5)

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.manager.tasks:
            self.task_listbox.insert(tk.END, str(task))

    def add_task(self):
        description = simpledialog.askstring("Task Description", "Enter task description:")
        if description:
            priority = simpledialog.askstring("Task Priority", "Enter task priority (high, medium, low):")
            due_date = simpledialog.askstring("Due Date", "Enter due date (YYYY-MM-DD), leave blank if none:")
            due_date = due_date if due_date else None
            self.manager.add_task(description, priority, due_date)
            self.update_task_list()

    def remove_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            self.manager.remove_task(index)
            self.update_task_list()
        except IndexError:
            messagebox.showwarning("Remove Task", "Please select a task to remove.")

    def complete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            self.manager.complete_task(index)
            self.update_task_list()
        except IndexError:
            messagebox.showwarning("Complete Task", "Please select a task to mark as completed.")

if __name__ == "__main__":
    manager = TaskManager()
    app = TaskManagerGUI(manager)
    app.mainloop()
