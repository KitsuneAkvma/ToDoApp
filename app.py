import traceback

from models import ToDoList
from rich.console import Console
from utils.file_handler import load_file

console = Console()
todo_list = ToDoList.ToDoList(load_file())

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
