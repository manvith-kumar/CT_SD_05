# CT_SD_05 - Persistent Task Manager
import json
import os

TASK_FILE = "tasks.json"

class PersistentTaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        try:
            if os.path.exists(TASK_FILE):
                with open(TASK_FILE, 'r') as file:
                    self.tasks = json.load(file)
            print(f"Loaded {len(self.tasks)} tasks from storage.")
        except Exception as e:
            print(f"⚠ Error loading tasks: {e}")
            self.tasks = []

    def save_tasks(self):
        try:
            with open(TASK_FILE, 'w') as file:
                json.dump(self.tasks, file, indent=2)
        except Exception as e:
            print(f"⚠ Error saving tasks: {e}")

    def add_task(self):
        print("\n--- Add New Task ---")
        task = {
            "id": len(self.tasks) + 1,
            "title": input("Title: ").strip(),
            "description": input("Description: ").strip(),
            "due_date": input("Due Date (DD-MM-YYYY): ").strip(),
            "completed": False
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"✅ Task '{task['title']}' added!")

    def view_tasks(self, show_all=True):
        print("\n--- Your Tasks ---")
        if not self.tasks:
            print("No tasks found.")
            return

        for task in self.tasks:
            if show_all or not task["completed"]:
                status = "✓" if task["completed"] else "✗"
                print(f"{task['id']}. [{status}] {task['title']} (Due: {task['due_date']})")
                print(f"   Description: {task['description']}\n")

    def update_task(self):
        self.view_tasks()
        try:
            task_id = int(input("\nEnter task ID to update: ")) - 1
            if 0 <= task_id < len(self.tasks):
                task = self.tasks[task_id]
                print(f"\nEditing Task {task_id + 1}: '{task['title']}'")
                
                task["title"] = input(f"New Title [{task['title']}]: ").strip() or task["title"]
                task["description"] = input(f"New Description [{task['description']}]: ").strip() or task["description"]
                task["due_date"] = input(f"New Due Date [{task['due_date']}]: ").strip() or task["due_date"]
                
                complete_input = input(f"Completed? (y/n) [{'y' if task['completed'] else 'n'}]: ").lower()
                if complete_input in ('y', 'n'):
                    task["completed"] = complete_input == 'y'
                
                self.save_tasks()
                print("✅ Task updated successfully!")
            else:
                print("❌ Invalid task ID!")
        except ValueError:
            print("❌ Please enter a valid number!")

    def delete_task(self):
        self.view_tasks()
        try:
            task_id = int(input("\nEnter task ID to delete: ")) - 1
            if 0 <= task_id < len(self.tasks):
                deleted_task = self.tasks.pop(task_id)
                # Reassign IDs
                for idx, task in enumerate(self.tasks, 1):
                    task["id"] = idx
                self.save_tasks()
                print(f"✅ Task '{deleted_task['title']}' deleted!")
            else:
                print("❌ Invalid task ID!")
        except ValueError:
            print("❌ Please enter a valid number!")

def main():
    manager = PersistentTaskManager()
    
    while True:
        print("\n=== Task Manager ===")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. View Pending Tasks")
        print("4. Update Task")
        print("5. Delete Task")
        print("6. Exit")
        
        choice = input("\nSelect operation (1-6): ")
        
        if choice == "1":
            manager.add_task()
        elif choice == "2":
            manager.view_tasks(show_all=True)
        elif choice == "3":
            manager.view_tasks(show_all=False)
        elif choice == "4":
            manager.update_task()
        elif choice == "5":
            manager.delete_task()
        elif choice == "6":
            print("Goodbye! Your tasks are saved.")
            break
        else:
            print("Invalid choice! Please select 1-6")

if __name__ == "__main__":
    main()