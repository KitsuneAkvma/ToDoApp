from models.ToDoList import ToDoList
from utils.file_handler import load_file

test_todo_list = ToDoList(load_file(file_path="tests/test_data.json"))


def test_create_todo_list():

    assert isinstance(test_todo_list, ToDoList)
    assert len(test_todo_list.todo_list) == 3


def test_get_list_len():
    assert test_todo_list.get_list_len() == 3


def test_get_list():

    assert isinstance(test_todo_list.get_list(), list)
    assert len(test_todo_list.get_list()) == 3


def test_get_task():
    assert isinstance(test_todo_list.get_task(1), dict)
    assert isinstance(test_todo_list.get_task(2), dict)
    assert isinstance(test_todo_list.get_task(3), dict)
    assert test_todo_list.get_task(4) == {}


def test_add_item():
    new_task = {
        "id": 4,
        "title": "New test task",
        "desc": "This is a test task 3",
        "due_to": "2022-01-06",
        "categories": ["test"],
        "is_done": False,
    }
    test_todo_list.add_item(new_task)
    assert test_todo_list.get_list_len() == 4
    assert isinstance(test_todo_list.get_task(4), dict)


def test_del_item():

    task_to_delete = test_todo_list.todo_list[1]
    test_todo_list.del_item(task_to_delete)
    assert test_todo_list.get_list_len() == 2
    assert isinstance(test_todo_list.get_task(1), dict)
    assert test_todo_list.get_task(2) == {}
    assert isinstance(test_todo_list.get_task(3), dict)


def test_sort_by_id():
    test_todo_list.sort_by_id()
    sorted_list = test_todo_list.get_sorted_list()
    assert sorted_list[0]["id"] == 1
    assert sorted_list[1]["id"] == 2
    assert sorted_list[2]["id"] == 3


def test_sort_by_title():
    test_todo_list.sort_by_title()
    sorted_list = test_todo_list.get_sorted_list()
    assert sorted_list[0]["title"] == "A test task"
    assert sorted_list[1]["title"] == "Simple test task"
    assert sorted_list[2]["title"] == "Test task 3"


def test_sort_by_date():
    test_todo_list.sort_by_date()
    sorted_list = test_todo_list.get_sorted_list()
    assert sorted_list[0]["due_to"] == "2022-01-01"
    assert sorted_list[1]["due_to"] == "2022-01-02"
    assert sorted_list[2]["due_to"] == "2022-01-03"


def test_filter_by_category():
    test_todo_list.filter_categories(["cat"])
    filtered_list = test_todo_list.get_sorted_list()
    assert len(filtered_list) == 2
    assert filtered_list[0]["id"] == 1
    assert filtered_list[1]["id"] == 3


def test_filter_by_state():
    test_todo_list.filter_state(True)
    filtered_list = test_todo_list.get_sorted_list()
    assert len(filtered_list) == 1
    assert filtered_list[0]["id"] == 2
