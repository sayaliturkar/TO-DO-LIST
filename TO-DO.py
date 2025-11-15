import bisect

# Priority map
priority_map = {
    "high": 1,
    "medium": 2,
    "low": 3
}


class DSATodo:
    def init(self):
        self.tasks = []              # Task list (array)
        self.undo_stack = []         # Stack
        self.queue = []              # Queue

    # add task
    def add_task(self, task, priority):
        p_value = priority_map.get(priority.lower(), 3)
        item = (task, p_value)

        self.tasks.append(item)
        self.undo_stack.append(item)
        self.queue.append(item)

        print(f"✔ Task '{task}' added with priority '{priority}'!")

    # show task
    def show_tasks(self):
        if not self.tasks:
            print("No tasks yet.")
            return

        print("\n📌 Your Tasks:")
        for i, (task, p) in enumerate(self.tasks):
            pr = self.priority_text(p)
            print(f"{i+1}. {task}  ({pr})")

    def priority_text(self, p):
        return "High" if p == 1 else "Medium" if p == 2 else "Low"

    # linear serach
    def search_task(self, key):
        print("\n🔎 Searching...")
        for i, (task, p) in enumerate(self.tasks):
            if task.lower() == key.lower():
                print(f"✔ Found at position {i+1}: {task} ({self.priority_text(p)})")
                return
        print("❌ Task not found.")

    # bubble sort
    def bubble_sort(self):
        arr = self.tasks[:]
        n = len(arr)

        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j][1] > arr[j+1][1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]

        self.print_sorted(arr, "Bubble Sort")

    # selection sort
    def selection_sort(self):
        arr = self.tasks[:]
        n = len(arr)

        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                if arr[j][1] < arr[min_idx][1]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]

        self.print_sorted(arr, "Selection Sort")

    # insertion sort
    def insertion_sort(self):
        arr = self.tasks[:]

        for i in range(1, len(arr)):
            key_item = arr[i]
            j = i - 1

            while j >= 0 and arr[j][1] > key_item[1]:
                arr[j+1] = arr[j]
                j -= 1

            arr[j+1] = key_item

        self.print_sorted(arr, "Insertion Sort")

    def print_sorted(self, arr, method):
        print(f"\n📑 {method} Result (High → Medium → Low):")
        for task, p in arr:
            print(f"- {task} ({self.priority_text(p)})")

    # undo task 
    def undo(self):
        if not self.undo_stack:
            print("❌ Nothing to undo.")
            return

        last = self.undo_stack.pop()
        self.tasks.remove(last)
        print(f"↩ Undo successful! Removed: {last[0]}")

    # next task
    def next_task(self):
        if not self.queue:
            print("❌ No upcoming tasks.")
            return

        task, p = self.queue[0]
        print(f"⏭ Next task: {task} ({self.priority_text(p)})")

    # delete task
    def delete_task(self, num):
        if 0 <= num - 1 < len(self.tasks):
            removed = self.tasks.pop(num - 1)
            print(f"🗑 Deleted: {removed[0]}")
        else:
            print("❌ Invalid task number.")


# main code

todo = DSATodo()

while True:

    print(" DSA TO-DO LIST")
    
    print("1. Add Task with Priority")
    print("2. Show Tasks")
    print("3. Search Task")
    print("4. Sort Tasks (Bubble Sort)")
    print("5. Sort Tasks (Selection Sort)")
    print("6. Sort Tasks (Insertion Sort)")
    print("7. Undo Last Task")
    print("8. View Next Task (Queue)")
    print("9. Delete Task")
    print("10. Exit")
    

    choice = input("Enter your choice: ")

    if choice == "1":
        task = input("Enter task name: ")
        priority = input("Enter priority (High / Medium / Low): ")
        todo.add_task(task, priority)

    elif choice == "2":
        todo.show_tasks()

    elif choice == "3":
        key = input("Enter task name to search: ")
        todo.search_task(key)

    elif choice == "4":
        todo.bubble_sort()

    elif choice == "5":
        todo.selection_sort()

    elif choice == "6":
        todo.insertion_sort()

    elif choice == "7":
        todo.undo()

    elif choice == "8":
        todo.next_task()

    elif choice == "9":
        num = int(input("Enter task number to delete: "))
        todo.delete_task(num)

    elif choice == "10":
        print("Goodbye!")
        break

    else:
        print("Invalid choice! Try again.")