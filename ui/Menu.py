import os
from rich.console import Console
from rich.table import Table
from rich import box
import inquirer

from utils.validators import is_date_format, is_value, is_int
from utils.file_handler import load_file, save_file
from utils.utils import get_time
from app import todo_list


console = Console()
categories_list = [
    "💼 work",
    "🏡 personal",
    "💻 programming",
    "🛒 shopping",
    "🎨 design",
    "📊 raport",
    "✍️ writing",
    "🔍 review",
    "❤️ health",
    "📂 organization",
    "🚀 productivity",
    "📦 logistics",
    "💰 finance",
    "🎓 education",
    "📅 meetings",
    "✈️ travel",
    "🔧 maintenance",
    "🔬 research",
    "📝 planning",
]


def main_view():
    todo_list.todo_list = load_file()
    sorted_list = todo_list.get_sorted_list()

    def print_table():
        if todo_list.get_list_len() <= 0:
            console.print(
                "\n[light gray]Your list is empty T_T Let's add something toDo :)\n"
            )
        else:
            table.add_column("ID")
            table.add_column("Title")
            table.add_column("Due to")
            table.add_column(
                "Categories",
            )
            table.add_column("Is Done?", justify="center")

            for x in sorted_list:
                values = x.get_values()
                categories_list = []
                for x in values[4]:
                    categories_list.append(x[0])

                day, month, year = values[3].split("-")
                table.add_row(
                    str(values[0]),
                    values[1],
                    f"{day}-{month}-{year}",
                    " ".join(categories_list),
                    ("✔️" if (values[5] is True) else "❌"),
                )
        console.print(table)

    table = Table(
        title="Your list",
        row_styles=["none", "dim"],
        header_style="bold magenta",
        box=box.MINIMAL_DOUBLE_HEAD,
    )
    console.print("[bold lime]TODO APP", justify="center")
    console.print("[dark gray]===========================", justify="center")
    console.print(f"Right now is: [cyan]{get_time("")}")
    print_table()


def task_view(item_data):
    os.system("cls")
    console.rule(f"{item_data.title} #{item_data.id}")
    console.print(
        f"[italic grey50] Due to: {item_data.due_to} {'✔️' if item_data.is_done else '❌'}"
    )
    console.print("\n[bold]Description:", justify="center")
    console.print(f"\n[grey89]{item_data.desc}", justify="center")
    for category in item_data.categories:
        console.print(f"[white on dark_green]{category}[/white on dark_green] ", end="")
    console.print("\n", justify="center")


def reset_view():
    os.system("cls")
    main_view()


def main_menu():
    questions = [
        inquirer.List(
            "main menu",
            message="What do you want toDo",
            choices=(
                ["Add", "Select", "Sort", "Filter", "Exit"]
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
    elif sel_option["main menu"] == "Sort":
        sort_menu()
    elif sel_option["main menu"] == "Filter":
        filter_menu()
    elif sel_option["main menu"] == "Exit":
        print("EXIT!")
        return "ext"


def add_menu():
    def create_new_id():
        return max([task.id for task in todo_list.todo_list], default=0) + 1

    new_item_id = create_new_id()
    new_item = {"id": new_item_id}

    questions = [
        inquirer.Text("title", message="Select a title", validate=is_value),
        inquirer.Text("desc", message="Write an description"),
        inquirer.Text(
            "due_to",
            message="Enter a due date (format: DD-MM-YYYY)",
            validate=is_date_format,
        ),
        inquirer.Checkbox(
            "categories",
            message="Select categories press [->]",
            choices=categories_list,
        ),
        inquirer.Confirm("is_done", message="Is this task done?"),
    ]

    console.print("[bold dark_cyan]ADDING NEW ITEM!")
    new_item.update(**inquirer.prompt(questions))
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
            save_file(todo_list)
        elif selected_option["select option"] == "Change status":
            selected_task.update_status()
            save_file(todo_list)
        elif selected_option["select option"] == "Delete Task":
            a_y_s = [
                inquirer.Confirm(
                    "are you sure?", message="This cannot be reverted!! Are you sure?"
                )
            ]
            a_y_s_answer = inquirer.prompt(a_y_s)

            if a_y_s_answer["are you sure?"] is True:
                todo_list.del_item(selected_task)
            else:
                pass

        else:
            reset_view()

    task_nr_input = inquirer.Text("task_nr", message="Select task ID", validate=is_int)
    if todo_list.get_list_len() == 1:
        selected_task = todo_list.get_task(1)
        task_view(selected_task)
        edit_menu(todo_list)
    else:
        task_nr = int(inquirer.prompt([task_nr_input])["task_nr"])
        selected_task = todo_list.get_task(task_nr)
        if selected_task == {}:
            console.print("[red]Task with provided ID does not exist.")
            input("Press Enter to continue...")
            return
    if selected_task:
        task_view(selected_task)
        edit_menu()
    else:
        console.print("[red]Task with provided ID does not exist.")


def sort_menu():

    sort_menu_options = [
        inquirer.List(
            "sort", message="Select sorting option", choices=["ID", "Title", "Due to"]
        )
    ]
    sort_option = inquirer.prompt(sort_menu_options)
    if sort_option["sort"] == "ID":
        todo_list.sort_by_id()
    elif sort_option["sort"] == "Title":
        todo_list.sort_by_title()
    elif sort_option["sort"] == "Due to":
        todo_list.sort_by_date()
    reset_view()


def filter_menu():

    filter_menu_options = [
        inquirer.Checkbox(
            "filter_categories",
            message="Select filtering option",
            choices=categories_list,
            default=todo_list.current_sort_options["filter_value"],
        ),
        inquirer.List(
            "filter_state",
            message="Select filtering option",
            choices=[("All", "ALL"), ("Done", True), ("Not Done", False)],
            default=todo_list.current_sort_options["Show"],
        ),
    ]

    filter_selected_options = inquirer.prompt(filter_menu_options)
    todo_list.filter_categories(filter_selected_options["filter_categories"])

    if filter_selected_options["filter_state"] != "ALL":
        todo_list.filter_state(filter_selected_options["filter_state"])
    reset_view()
