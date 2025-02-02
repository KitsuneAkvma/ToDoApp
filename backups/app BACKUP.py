import os
import traceback
import datetime
import json
from rich.console import Console
from rich.table import Table
import inquirer
from inquirer import errors


console = Console()


class DataValids:

    def is_int(self, _, current):

        if current.isdigit() is False:
            raise errors.ValidationError("", reason="You need to enter an number")
        return True

    def is_date_format(self, _, x):
        try:
            datetime.datetime.strptime(x, "%d-%m-%Y")
            return True
        except ValueError:
            raise errors.ValidationError(
                "", reason="Please write the date in format DD-MM-YYYY !"
            )

    def is_value(self, _, x):
        if x == "":
            raise errors.ValidationError("", reason="This cannot be empty")
        return True


def get_time(*date):
    if date:
        time_now = datetime.datetime.now()
        formatted_time_now = time_now.strftime("%c")
        return formatted_time_now
    else:
        formatted_time = datetime.datetime(date).strftime("%c")
        return formatted_time


def main_menu():
    questions = [
        inquirer.List(
            "main menu",
            message="What do you want toDo",
            choices=(
                ["Add", "Select", "Exit"]
                if (todo_list.get_list_len() > 0)
                else ["Add", "Exit"]
            ),
        )
    ]
    sel_option = inquirer.prompt(questions)
    if sel_option["main menu"] == "Add":
        add_menu()
    elif sel_option["main menu"] == "Select":
        select_menu()
    elif sel_option["main menu"] == "Exit":
        print("EXIT!")
        return "ext"


def add_menu():
    def create_new_id():
        return max([task.id for task in todo_list.todo_list], default=0) + 1

    new_item_id = create_new_id()
    new_item = {"id": new_item_id}
    questions = [
        inquirer.Text("title", message="Select a title", validate=validations.is_value),
        inquirer.Text("desc", message="Write an description"),
        inquirer.Text(
            "due_to",
            message="Enter a due date (format: DD-MM-YYYY)",
            validate=validations.is_date_format,
        ),
        inquirer.Text(
            "categories",
            message="Enter categories (separate by commas, e.g., work, personal, )",
        ),
        inquirer.Confirm("is_done", message="Is this task done?"),
    ]

    console.print("[bold dark_cyan]ADDING NEW ITEM!")
    new_item.update(**inquirer.prompt(questions))
    new_item["categories"] = [cat.strip() for cat in new_item["categories"].split(",")]
    console.print(f"[green]{new_item}")
    todo_list.add_item(new_item)


def select_menu():

    selected_task = {}

    def edit_menu():
        selected_task_data = selected_task.get_object()
        console.print("\n")
        select_options = [
            inquirer.List(
                "select option",
                message="What do you want to do with this task ?",
                choices=["Edit", "Change status", "Delete Task", "Go back"],
            )
        ]
        selected_option = inquirer.prompt(select_options)
        if selected_option["select option"] == "Edit":
            edit_menu_input = [
                inquirer.Text(
                    "title",
                    message="Select a title",
                    default=selected_task_data["title"],
                ),
                inquirer.Text(
                    "desc",
                    message="Write the description",
                    default=selected_task_data["desc"],
                ),
                inquirer.Text(
                    "due_to",
                    message="Select new date (DD-MM-YYYY)",
                    default=selected_task_data["due_to"],
                ),
                inquirer.Text(
                    "categories",
                    message="Select categories",
                    default=", ".join(selected_task_data["categories"]),
                ),
            ]
            edited_values = inquirer.prompt(edit_menu_input)

            edited_task = selected_task_data
            edited_task["title"] = edited_values["title"]
            edited_task["desc"] = edited_values["desc"]
            edited_task["due_to"] = edited_values["due_to"]
            edited_task["categories"] = [
                cat.strip() for cat in edited_values["categories"].split(",")
            ]
            selected_task.edit_task(edited_task)
            todo_list.save_file()
        elif selected_option["select option"] == "Change status":
            selected_task.update_status()
            todo_list.save_file()
        elif selected_option["select option"] == "Delete Task":
            a_y_s = [
                inquirer.Confirm(
                    "are you sure?", message="This cannot be reverted!! Are you sure?"
                )
            ]
            a_y_s_answer = inquirer.prompt(a_y_s)

            if a_y_s_answer["are you sure?"] is True:
                todo_list.del_item(selected_task)
                todo_list.save_file()
            else:
                pass

        else:
            todo_list.reset_view()

    task_nr_input = inquirer.Text(
        "task_nr", message="Select task ID", validate=validations.is_int
    )
    if todo_list.get_list_len() == 1:
        selected_task = todo_list.get_list()[0]
        todo_list.task_view(selected_task)
        edit_menu()

    else:
        task_nr = int(inquirer.prompt([task_nr_input])["task_nr"])
        selected_task = todo_list.get_task(task_nr)
        todo_list.task_view(selected_task)
        edit_menu()


class ToDoItem:

    def __init__(self, item_data):
        self.id = item_data["id"]
        self.title = item_data["title"]
        self.desc = item_data["desc"]
        self.due_to = item_data["due_to"]
        self.categories = item_data["categories"]
        self.is_done = item_data["is_done"]
        self.created_at = datetime.datetime.now()

    def to_dict(self):

        return {
            "id": self.id,
            "title": self.title,
            "desc": self.desc,
            "due_to": self.due_to,
            "categories": self.categories,
            "is_done": self.is_done,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            {
                "id": data["id"],
                "title": data["title"],
                "desc": data["desc"],
                "due_to": data["due_to"],
                "categories": data["categories"],
                "is_done": data["is_done"],
            }
        )

    def get_object(self):
        return {
            "id": self.id,
            "title": self.title,
            "desc": self.desc,
            "due_to": self.due_to,
            "categories": self.categories,
            "is_done": self.is_done,
            "created_at": self.created_at,
        }

    def get_values(self):
        return [
            self.id,
            self.title,
            self.desc,
            self.due_to,
            self.categories,
            self.is_done,
        ]

    def edit_task(self, task_data):
        new_title = task_data["title"]
        new_desc = task_data["desc"]
        new_due_to = task_data["due_to"]
        new_categories = task_data["categories"]
        self.title = new_title
        self.desc = new_desc
        self.due_to = new_due_to
        self.categories = new_categories

        todo_list.save_file()

    def update_status(self):
        self.is_done = not self.is_done
        todo_list.save_file()


class ToDoList:
    def __init__(self):
        self.todo_list = self.load_file()
        self.todo_list_len = len(self.todo_list)

    def get_list(self):
        return self.todo_list

    def get_list_len(self):
        return self.todo_list_len

    def get_task(self, task_nr):
        tasks_list = self.get_list()
        for task in tasks_list:
            if task.id == task_nr:
                return task

    def load_file(self):

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
            with open("toDoData.json", "r") as data_file:
                content = data_file.read()
                if not content.strip():
                    return []
                try:
                    data = json.loads(content)
                    data = fix_json(data)
                    return [ToDoItem.from_dict(item) for item in data]
                except json.JSONDecodeError as e:
                    console.print(f"[red]JSON loading error: {e}")
                    return []

        else:
            console.print("[red]The file does not exist. I am creating a new file!")
            with open("toDoData.json", "w") as data_file:
                pass
                return []

    def save_file(self):
        try:
            with open("toDoData.json", "w") as data_file:
                json.dump(
                    [item.to_dict() for item in self.todo_list], data_file, indent=4
                )
        except TypeError as e:
            console.print(f"[red]An Error occurred! {e}")

    def main_view(self):

        def print_table():
            table = Table(title="Your list")
            if len(self.todo_list) <= 0:
                console.print(
                    "\n[light gray]Your list is empty T_T Let's add something toDo :)\n"
                )
            else:
                table.add_column("ID")
                table.add_column("Title")
                table.add_column("Due to")
                table.add_column("Categories")
                table.add_column("Is Done?")
                for x in self.todo_list:
                    values = x.get_values()
                    day, month, year = values[3].split("-")
                    table.add_row(
                        str(values[0]),
                        values[1],
                        f"{day}-{month}-{year}",
                        " | ".join(values[4]),
                        ("✔️" if (values[5] is True) else "❌"),
                    )
            console.print(table)

        self.todo_list = self.load_file()
        console.print("[bold lime]TODO APP", justify="center")
        console.print("[dark gray]===========================", justify="center")
        console.print(f"Right now is: [cyan]{get_time("")}")
        print_table()

    def task_view(self, item_data):
        os.system("cls")
        console.rule(f"{item_data.title} #{item_data.id}")
        console.print(
            f"[italic grey50] Due to: {item_data.due_to} {'✔️' if item_data.is_done else '❌'}"
        )
        console.print("\n[bold]Description:", justify="center")
        console.print(f"\n[grey89]{item_data.desc}", justify="center")
        console.print(
            f"\n[white on green][ {' ][ '.join(item_data.categories)} ]",
            justify="center",
        )

    def reset_view(self):
        os.system("cls")
        self.main_view()

    def add_item(self, item_data):
        todo_item = ToDoItem(item_data)
        self.todo_list.append(todo_item)
        self.save_file()

    def del_item(self, sel_item):
        self.todo_list.remove(sel_item)
        self.save_file()
        pass

    def update_item_status(self, id):
        pass


if __name__ == "__main__":
    try:
        todo_list = ToDoList()
        validations = DataValids()

        while True:
            todo_list.todo_list = todo_list.load_file()
            todo_list.reset_view()

            sel_option = main_menu()
            if sel_option == "ext":
                console.print("[pink]Bye bye!!")
                break
    except Exception as e:
        console.print(f"[red]An [{type(e)}] occurred! {e}")
        console.print(f"[deep_pink3] {traceback.format_exc()}")
