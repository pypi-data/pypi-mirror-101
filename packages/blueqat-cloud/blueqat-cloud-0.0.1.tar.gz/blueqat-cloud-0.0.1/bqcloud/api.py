"""Module for manage API"""
import json
import os
import urllib.request
from typing import Any, List

from .task import Task
from .annealing import AnnealingTask, AnnealingResult

API_ENDPOINT = "https://cloudapi.blueqat.com/"


class Api:
    """Manage API and post request."""
    def __init__(self, api_key: str):
        self.api_key = api_key

    def post_request(self, path: str, body: Any) -> Any:
        """Post request."""
        headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': self.api_key,
        }
        req = urllib.request.Request(API_ENDPOINT + path,
                                     json.dumps(body).encode(), headers)
        with urllib.request.urlopen(req) as res:
            body = res.read()
        return json.loads(body)

    def save_api(self) -> None:
        """Save API to file."""
        d = os.path.join(os.environ["HOME"], ".bqcloud")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "api_key"), "w") as f:
            f.write(self.api_key)

    def credit(self) -> str:
        """Get credit."""
        path = "v1/credit/get"
        return self.post_request(path, {})["amount"]

    def annealing(self, qubo: list[list[float]], chain_strength: int,
                  num_reads: int) -> AnnealingResult:
        """Create annealing task"""
        path = "v1/quantum-tasks/create"
        res = self.post_request(path, {
            "qubo": qubo,
            "chain_strength": chain_strength,
            "num_reads": num_reads
        })
        return AnnealingResult(**res)

    def annealing_tasks(self, index: int = 0) -> List[AnnealingTask]:
        """Get tasks."""
        path = "v1/quantum-tasks/list"
        body = {
            "index": index,
        }
        tasks = self.post_request(path, body)
        assert isinstance(tasks, list)
        return [AnnealingTask(self, **task) for task in tasks]

    def tasks(self, index: int) -> List[Task]:
        """Get tasks."""
        path = "v2/quantum-tasks/list"
        body = {
            "index": index,
        }
        tasks = self.post_request(path, body)
        assert isinstance(tasks, list)
        return [Task(self, **task) for task in tasks]


def load_api() -> Api:
    """Load API from file."""
    with open(os.path.join(os.environ["HOME"], ".bqcloud/api_key")) as f:
        return Api(f.read().strip())


def register_api(api_key: str) -> Api:
    """Save and return API."""
    api = Api(api_key)
    api.save_api()
    return api
