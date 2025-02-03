import datetime


class Task:

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
        return self

    def get_dict(self):
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

    def update_status(self):
        self.is_done = not self.is_done

    def __getitem__(self, key):
        return getattr(self, key)
