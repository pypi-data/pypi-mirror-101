"""Module for task."""

class Task:
    """Task."""
    def __init__(self, api, **kwargs):
        self.api = api
        self.data = kwargs

    def detail(self):
        """This method may be changed."""
        path = "quantum-tasks/get"
        body = {
            "id": self.data['id'],
        }
        return self.api.post_request(path, body)
