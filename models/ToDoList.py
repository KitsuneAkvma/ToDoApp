from models.Task import Task


class ToDoList:
    def __init__(self, list_data=[]):
        self.todo_list = list_data
        self.default_sort_options = {
            "sort_by": "",
            "Show": "",
            "filter_value": [],
        }
        self.current_sort_options = self.default_sort_options
        self.sorted_list = self.get_sorted_list()

    def get_list(self):
        return [task.to_dict() for task in self.todo_list]

    def get_sorted_list(self):
        sorted_list = self.todo_list[:]

        if self.current_sort_options["sort_by"] == "ID":
            sorted_list.sort(key=lambda task: task.id)
        elif self.current_sort_options["sort_by"] == "Title":
            sorted_list.sort(key=lambda task: task.title)
        elif self.current_sort_options["sort_by"] == "Due to":
            sorted_list.sort(key=lambda task: task.due_to)

        if type(self.current_sort_options["Show"]) is type(True):
            state = self.current_sort_options["Show"]
            sorted_list = [task for task in sorted_list if task.is_done == state]

        if len(self.current_sort_options["filter_value"]) > 0:
            filter_data = self.current_sort_options["filter_value"]
            sorted_list = [
                task
                for task in sorted_list
                if any(category in task.categories for category in filter_data)
            ]
        self.sorted_list = sorted_list
        return sorted_list

    def get_list_len(self):
        return len(self.todo_list)

    def get_task(self, task_nr):
        tasks_list = self.get_list()
        for task in tasks_list:
            if task["id"] == task_nr:
                return task
        return {}

    def add_item(self, item_data):
        todo_item = Task(item_data)
        self.todo_list.append(todo_item)

    def del_item(self, sel_item):
        self.todo_list.remove(sel_item)

    def sort_by_id(self):
        self.current_sort_options["sort_by"] = "ID"

    def sort_by_title(self):
        self.current_sort_options["sort_by"] = "Title"

    def sort_by_date(self):
        self.current_sort_options["sort_by"] = "Due to"

    def filter_categories(self, filter_data):
        self.current_sort_options["filter_value"] = filter_data

    def filter_state(self, state):
        self.current_sort_options["Show"] = state

    def revert_saved_sorting(self):
        return self.current_sort_options

    def reset_sorting_filtering(self):
        self.current_sort_options = self.default_sort_options

    def __iter__(self):
        return iter(self.todo_list)

    def __repr__(self):
        return self.get_list()
