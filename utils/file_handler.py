import os
import json
from models import Task
from rich.console import Console

console = Console()


def load_file():

    def fix_json(data):
        fixed_data = []
        for item in data:
            fixed_data.append(
                {
                    "id": item["id"],
                    "title": (
                        item["title"]["title"]
                        if isinstance(item["title"], dict)
                        else item["title"]
                    ),
                    "desc": (
                        item["desc"]["desc"]
                        if isinstance(item["desc"], dict)
                        else item["desc"]
                    ),
                    "due_to": item["due_to"],
                    "categories": item["categories"],
                    "is_done": (
                        item["is_done"]["is_done"]
                        if isinstance(item["is_done"], dict)
                        else item["is_done"]
                    ),
                }
            )
        return fixed_data

    if os.path.exists("toDoData.json"):
        with open("toDoData.json", "r", encoding="utf-8") as data_file:
            content = data_file.read()
            if not content.strip():
                return []
            try:
                data = json.loads(content)
                data = fix_json(data)
                return [Task.Task.from_dict(item) for item in data]
            except json.JSONDecodeError as e:
                console.print(f"[red]JSON loading error: {e}")
                return []

    else:
        with open("toDoData.json", "w") as data_file:
            pass
            return []


def save_file(todo_list):
    try:
        with open("toDoData.json", "w", encoding="utf-8") as data_file:
            json.dump([item.to_dict() for item in todo_list], data_file, indent=4)
    except TypeError as e:
        console.print(f"[red]An Error occurred! {e}")
