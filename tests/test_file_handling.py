from utils.file_handler import load_file, save_file
from models.Task import Task
from models.ToDoList import ToDoList

json_data = [
    {
        "id": 1,
        "title": "Simple test task",
        "desc": "This is a test task",
        "due_to": "2022-01-03",
        "is_done": False,
        "categories": ["test"],
        "created_at": "2025-02-02T20:20:00.000000",
    },
    {
        "id": 2,
        "title": "A test task ",
        "desc": "This is a test task 2",
        "due_to": "2022-01-02",
        "is_done": False,
        "categories": ["test"],
        "created_at": "2025-02-02T20:20:00.000000",
    },
    {
        "id": 3,
        "title": "Test task 3",
        "desc": "This is a test task 3",
        "due_to": "2022-01-01",
        "is_done": False,
        "categories": ["test"],
        "created_at": "2025-02-02T20:20:00.000000",
    },
]
new_item = {
    "id": 4,
    "title": "Test task 4",
    "desc": "This is a test task 4",
    "due_to": "2022-01-04",
    "categories": ["test"],
    "is_done": False,
}


def test_load_file():
    loaded_data = load_file("tests/test_data.json")
    assert isinstance(loaded_data, list)
    assert [isinstance(item, Task) for item in loaded_data]
    assert len(loaded_data) == 3


def test_save_file():
    loaded_data = load_file("tests/test_data.json")
    test_todo_list = ToDoList(loaded_data)
    test_todo_list.add_item(new_item)
    save_file(test_todo_list, "tests/test_data.json")
    new_loaded_data = load_file("tests/test_data.json")
    assert loaded_data != new_loaded_data
    assert isinstance(new_loaded_data, list)
    assert [isinstance(item, Task) for item in new_loaded_data]
    assert len(new_loaded_data) == 4
    test_todo_list.todo_list.pop()
    assert len(test_todo_list.todo_list) == 3
    save_file(test_todo_list, "tests/test_data.json")
