import datetime
from inquirer import errors
from app import todo_list


def is_int(_, current):

    if current.isdigit() is False:
        raise errors.ValidationError(
            "",
            reason="""
        You need to enter an number""",
        )
    return True


def is_date_format(_, x):
    try:
        datetime.datetime.strptime(x, "%d-%m-%Y")
        return True
    except ValueError:
        raise errors.ValidationError(
            "", reason="Please write the date in format DD-MM-YYYY !"
        )


def is_value(_, x):
    if x == "":
        raise errors.ValidationError("", reason="This cannot be empty")
    return True


def does_task_exist(_, x):
    tasks = todo_list.get_list()
    print(tasks)
    for task in tasks:
        print(task.id)
    input("Press Enter to continue...")

    if not any(task.id == x for task in tasks):
        raise errors.ValidationError("", reason="This task does not exist")
    else:
        return True
