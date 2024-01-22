import os
import json
import argparse

class Task:
    def __init__(self, description, priority=1):
        self.description = description
        self.priority = priority

    def to_dict(self):
        return {"description": self.description, "priority": self.priority}

    @classmethod
    def from_dict(cls, task_dict):
        return cls(description=task_dict["description"], priority=task_dict["priority"])

class TaskManager:
    def __init__(self, global_tasks=None, local_tasks=None):
        self.global_tasks = global_tasks or []
        self.local_tasks = local_tasks or []
        self.loadFromFile("local")
        self.loadFromFile("global")

    def addTask(self, description, priority=1, task_type="local"):
        if task_type not in ("local", "global"):
            raise ValueError("Invalid task type. Accepted values are 'local' or 'global'.")

        task_list = self.local_tasks if task_type == "local" else self.global_tasks
        task_list.append(Task(description, priority=priority))

        self.saveToFile(task_type)
        directory = os.getcwd() if task_type == "local" else os.path.expanduser("~")
        print(f"{task_type.capitalize()} task created in the folder: {directory}")

    def removeTask(self, identifier, task_type):
        try:
            index = int(identifier) - 1
            task_list = self.local_tasks if task_type == "local" else self.global_tasks

            if 0 <= index < len(task_list):
                removed_task = task_list.pop(index)
                print(f"{task_type.capitalize()} task '{removed_task.description}' removed.")
                self.saveToFile("local")
                self.saveToFile("global")
            else:
                print(f"Invalid task number for {task_type} tasks.")
        except ValueError:
            print(f"Invalid task identifier. Please provide a valid task number.")

    def showTasks(self, tasks, header, display_header=True):
        if display_header:
            print(f"\033[92m{header}:\033[0m")

        for idx, task in enumerate(tasks, 1):
            color = getPriorityColor(task.priority)
            print(f"{idx}. {color}{task.description} (Priority: {task.priority}\033[0m)")

    def searchTasks(self, search_type, keyword):
        matching_tasks = []

        tasks_to_search = (
            self.global_tasks + self.local_tasks
            if search_type == "all"
            else self.global_tasks if search_type == "global"
            else self.local_tasks
        )

        green = "\033[92m"
        red = "\033[91m"
        reset = "\033[0m"

        for task in tasks_to_search:
            if keyword.lower() in task.description.lower():
                matching_tasks.append(task)

        if matching_tasks:
            print(f"{green}Found tasks matching '{red}{keyword}{reset}{green}':{reset}")
            for idx, task in enumerate(matching_tasks, 1):
                color = getPriorityColor(task.priority)
                print(f"{idx}. {color}{task.description} (Priority: {task.priority}){reset}")
        else:
            print(f"{green}No tasks found matching {red}'{keyword}'.{reset}")

    def saveToFile(self, task_type="local"):
        try:
            if task_type == "local":
                filename = "tasks.json"
            elif task_type == "global":
                filename = os.path.join(os.path.expanduser("~"), "tasks_global.json")
            else:
                raise ValueError("Invalid task type. Accepted values are 'local' or 'global'.")

            with open(filename, "w", encoding="utf-8") as file:
                tasks_data = {"local_tasks": [task.to_dict() for task in self.local_tasks]} if task_type == "local" else \
                             {"global_tasks": [task.to_dict() for task in self.global_tasks]}

                json.dump(tasks_data, file, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"Error while saving data: {e}")

    def loadFromFile(self, task_type="local"):
        try:
            if task_type == "local":
                filename = "tasks.json"
            elif task_type == "global":
                filename = os.path.join(os.path.expanduser("~"), "tasks_global.json")
            else:
                raise ValueError("Invalid task type. Accepted values are 'local' or 'global'.")

            with open(filename, "r", encoding="utf-8") as file:
                tasks_data = json.load(file)
                task_list = self.local_tasks if task_type == "local" else self.global_tasks

                task_list.clear()
                task_list.extend([Task.from_dict(task_dict) for task_dict in tasks_data.get(f"{task_type}_tasks", [])])

                if not tasks_data.get(f"{task_type}_tasks"):
                    print(f"{task_type.capitalize()} tasks file is empty.")

        except FileNotFoundError:
            print(f"File '{filename}' does not exist. Creating a new {task_type} file.")
            self.saveToFile(task_type)
        except Exception as e:
            print(f"Error while loading data: {e}")

    def createFileIfNotExist(self, filename, is_global=False):
        directory = os.path.expanduser("~") if is_global else os.getcwd()
        file_path = os.path.join(directory, filename)

        if not os.path.isfile(file_path):
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump({filename.split('.')[0]: []}, file)

def getPriorityColor(priority):
    color_codes = {
        1: "\033[37m",
        2: "\033[97m",
        3: "\033[93m",
        4: "\033[91m",
        5: "\033[31m",
        0: "\033[0m"
    }
    return color_codes.get(priority, color_codes[0])

def parseArgs():
    parser = argparse.ArgumentParser(description="Simple task manager in Python.")
    parser.add_argument("-ag", metavar="TASK", help="Add global task.")
    parser.add_argument("-al", metavar="TASK", help="Add local task.")
    parser.add_argument("-p", type=int, default=1, help="Task priority.")
    parser.add_argument("-rg", metavar="ID", help="Remove global task.")
    parser.add_argument("-rl", metavar="ID", help="Remove local task.")
    parser.add_argument("-s", metavar="TASK", help="Search for a task (in global and local).")
    parser.add_argument("-sg", metavar="TASK", help="Search for a task in global tasks.")
    parser.add_argument("-sl", metavar="TASK", help="Search for a task in local tasks.")
    parser.add_argument("-l", action="store_true", help="View all tasks.")
    parser.add_argument("-ll", action="store_true", help="List local tasks.")

    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    taskManager = TaskManager()

    try:
        if args.ag:
            taskManager.addTask(args.ag, priority=args.p, task_type="global")
        elif args.al:
            taskManager.addTask(args.al, priority=args.p, task_type="local")
        elif args.rg:
            taskManager.removeTask(args.rg, task_type="global")
        elif args.rl:
            taskManager.removeTask(args.rl, task_type="local")
        elif args.s:
            taskManager.searchTasks("all", args.s)
        elif args.sg:
            taskManager.searchTasks("global", args.sg)
        elif args.sl:
            taskManager.searchTasks("local", args.sl)
        elif args.l or not any(vars(args)):
            taskManager.showTasks(taskManager.global_tasks, header="Global tasks", display_header=bool(taskManager.global_tasks))
            taskManager.showTasks(taskManager.local_tasks, header="Local tasks", display_header=bool(taskManager.local_tasks))
        elif args.ll:
            taskManager.showTasks(taskManager.local_tasks, header="Local tasks", display_header=bool(taskManager.local_tasks))
        else:
            taskManager.showTasks(taskManager.global_tasks, header="Global tasks", display_header=bool(taskManager.global_tasks))
            taskManager.showTasks(taskManager.local_tasks, header="Local tasks", display_header=bool(taskManager.local_tasks))
    except Exception as e:
        print(f"An error occurred: {e}")
