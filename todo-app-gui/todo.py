"""
To-Do App with Tkinter GUI
Add, delete, and mark tasks as complete
Tasks are saved to a JSON file so they persist between sessions
"""

import json
import os
import tkinter as tk
from tkinter import messagebox


TASKS_FILE = "tasks.json"


def load_tasks():
    """Load tasks from the JSON file, return empty list if file doesn't exist"""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Warning: Could not read tasks file, starting fresh")
        return []


def save_tasks(tasks):
    """Save the current tasks list to JSON file"""
    try:
        with open(TASKS_FILE, "w") as f:
            json.dump(tasks, f, indent=2)
    except IOError:
        messagebox.showerror("Error", "Could not save tasks to file")


def add_task():
    """Add a new task from the entry field"""
    task_text = entry_task.get().strip()
    if not task_text:
        messagebox.showwarning("Warning", "Please enter a task")
        return

    task = {"text": task_text, "completed": False}
    tasks.append(task)
    save_tasks(tasks)
    update_task_list()
    entry_task.delete(0, tk.END)


def delete_task():
    """Delete the selected task from the list"""
    selected = listbox_tasks.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a task to delete")
        return

    index = selected[0]
    task_text = tasks[index]["text"]
    confirm = messagebox.askyesno("Confirm", f"Delete task: '{task_text}'?")
    if confirm:
        tasks.pop(index)
        save_tasks(tasks)
        update_task_list()


def mark_complete():
    """Toggle the completed status of the selected task"""
    selected = listbox_tasks.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a task")
        return

    index = selected[0]
    tasks[index]["completed"] = not tasks[index]["completed"]
    save_tasks(tasks)
    update_task_list()


def update_task_list():
    """Refresh the listbox to show current tasks"""
    listbox_tasks.delete(0, tk.END)
    for task in tasks:
        if task["completed"]:
            display_text = f"[DONE] {task['text']}"
        else:
            display_text = f"[ ] {task['text']}"
        listbox_tasks.insert(tk.END, display_text)

    # Color completed tasks green
    for i, task in enumerate(tasks):
        if task["completed"]:
            listbox_tasks.itemconfig(i, fg="#2e7d32")


def clear_completed():
    """Remove all completed tasks from the list"""
    global tasks
    completed_count = sum(1 for t in tasks if t["completed"])
    if completed_count == 0:
        messagebox.showinfo("Info", "No completed tasks to clear")
        return

    confirm = messagebox.askyesno("Confirm", f"Remove {completed_count} completed tasks?")
    if confirm:
        tasks = [t for t in tasks if not t["completed"]]
        save_tasks(tasks)
        update_task_list()


# Load existing tasks
tasks = load_tasks()

# Create the main window
root = tk.Tk()
root.title("To-Do App")
root.geometry("450x500")
root.resizable(False, False)

# Title label
label_title = tk.Label(root, text="My To-Do List", font=("Arial", 16, "bold"))
label_title.pack(pady=10)

# Entry frame (input + add button)
frame_entry = tk.Frame(root)
frame_entry.pack(pady=5, padx=20, fill=tk.X)

entry_task = tk.Entry(frame_entry, font=("Arial", 12))
entry_task.pack(side=tk.LEFT, fill=tk.X, expand=True)

btn_add = tk.Button(frame_entry, text="Add", command=add_task, width=8)
btn_add.pack(side=tk.RIGHT, padx=(5, 0))

# Bind Enter key to add task
entry_task.bind("<Return>", lambda event: add_task())

# Listbox with scrollbar
frame_list = tk.Frame(root)
frame_list.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame_list)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox_tasks = tk.Listbox(
    frame_list,
    font=("Arial", 11),
    selectmode=tk.SINGLE,
    yscrollcommand=scrollbar.set
)
listbox_tasks.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=listbox_tasks.yview)

# Buttons frame
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_complete = tk.Button(frame_buttons, text="Mark Complete", command=mark_complete, width=14)
btn_complete.pack(side=tk.LEFT, padx=5)

btn_delete = tk.Button(frame_buttons, text="Delete", command=delete_task, width=10)
btn_delete.pack(side=tk.LEFT, padx=5)

btn_clear = tk.Button(frame_buttons, text="Clear Done", command=clear_completed, width=10)
btn_clear.pack(side=tk.LEFT, padx=5)

# Task counter label
label_count = tk.Label(root, text="", font=("Arial", 10))
label_count.pack(pady=5)

# Load tasks into the listbox
update_task_list()

# Start the app
root.mainloop()
