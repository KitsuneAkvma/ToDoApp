import datetime
from models.Task import Task

now = datetime.datetime.now()


def test_create_task():
    item = Task(
        {
            "id": 1,
            "title": "Test",
            "desc": "Test description",
            "due_to": "01-01-2021",
            "categories": ["Test"],
            "is_done": False,
        }
    )
    # testing attributes
    assert item.id == 1
    assert item.title == "Test"
    assert item.desc == "Test description"
    assert item.due_to == "01-01-2021"
    assert item.categories == ["Test"]
    assert item.is_done is False
    assert type(item.created_at) is type(now)
    # testing the __getitem__ method
    assert item["id"] == 1
    assert item["title"] == "Test"
    assert item["desc"] == "Test description"
    assert item["due_to"] == "01-01-2021"
    assert item["categories"] == ["Test"]
    assert item["is_done"] is False
    assert type(item["created_at"]) is type(now)


def test_get_object():
    item = Task(
        {
            "id": 1,
            "title": "Test",
            "desc": "Test description",
            "due_to": "01-01-2021",
            "categories": ["Test"],
            "is_done": False,
        }
    )
    item_object = item.get_object()
    assert item_object["id"] == 1
    assert item_object["title"] == "Test"
    assert item_object["desc"] == "Test description"
    assert item_object["due_to"] == "01-01-2021"
    assert item_object["categories"] == ["Test"]
    assert item_object["is_done"] is False
    assert type(item_object["created_at"]) is type(now)


def test_get_values():
    item = Task(
        {
            "id": 1,
            "title": "Test",
            "desc": "Test description",
            "due_to": "01-01-2021",
            "categories": ["Test"],
            "is_done": False,
        }
    )
    item_values = item.get_values()
    assert item_values == [
        1,
        "Test",
        "Test description",
        "01-01-2021",
        ["Test"],
        False,
    ]


def test_edit_task():
    item = Task(
        {
            "id": 1,
            "title": "Test",
            "desc": "Test description",
            "due_to": "01-01-2021",
            "categories": ["Test"],
            "is_done": False,
        }
    )
    item.edit_task(
        {
            "title": "Test2",
            "desc": "Test description 2",
            "due_to": "01-02-2021",
            "categories": ["Test", "Work"],
        }
    )
    assert item.id == 1
    assert item.title == "Test2"
    assert item.desc == "Test description 2"
    assert item.due_to == "01-02-2021"
    assert item.categories == ["Test", "Work"]
    assert item.is_done is False


def test_update_status():
    item = Task(
        {
            "id": 1,
            "title": "Test",
            "desc": "Test description",
            "due_to": "01-01-2021",
            "categories": ["Test"],
            "is_done": False,
        }
    )
    item.update_status()
    assert item.is_done is True


def test_to_dict():
    item = Task(
        {
            "id": 1,
            "title": "Test",
            "desc": "Test description",
            "due_to": "01-01-2021",
            "categories": ["Test"],
            "is_done": False,
        }
    )
    item_dict = item.to_dict()
    assert item_dict == {
        "id": 1,
        "title": "Test",
        "desc": "Test description",
        "due_to": "01-01-2021",
        "categories": ["Test"],
        "is_done": False,
        "created_at": item.created_at.isoformat(),
    }


def test_from_dict():
    item = Task.from_dict(
        {
            "id": 1,
            "title": "Test",
            "desc": "Test description",
            "due_to": "01-01-2021",
            "categories": ["Test"],
            "is_done": False,
        }
    )
    assert item.id == 1
    assert item.title == "Test"
    assert item.desc == "Test description"
    assert item.due_to == "01-01-2021"
    assert item.categories == ["Test"]
    assert item.is_done is False
    assert type(item.created_at) is type(now)
