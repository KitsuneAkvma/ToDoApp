import traceback

from models import ToDoList
from rich.console import Console


console = Console()
todo_list = ToDoList.ToDoList()

if __name__ == "__main__":
    try:
        from ui.Menu import main_menu, reset_view

        while True:
            reset_view()

            sel_option = main_menu()
            if sel_option == "ext":
                console.print("[pink]Bye bye!!")
                break
    except Exception as e:
        console.print(f"[red]An [{type(e)}] occurred! {e}")
        console.print(f"[deep_pink3] {traceback.format_exc()}")
