import os
import requests
import time
import json


class Cotton:
    def __init__(self, task_id: str, url: str = "https://api.cotton.mcoca.dev"):
        """
        init of cocaddy
        :param task_id: task id from cocaddy server like '6068688fe1ae6246c3b7fe2d'
        :param url: cocaddy server url
        """

        self.task_id = task_id
        self.url = url

        self.update_status('active')
        self.update_start_time()

    def update_status(self, status: str):
        d = {'status': status}
        u = os.path.join(self.url, 'tasks', self.task_id, 'status')
        _ = requests.patch(u, d)

    def update_start_time(self):
        t = int(time.time() * 1000)
        d = {'time': t}
        u = os.path.join(self.url, 'tasks', self.task_id, 'start')
        _ = requests.patch(u, d)

    def update_epoch(self, current: int, total: int):
        d = json.dumps({"Current": current, "Total": total})
        u = os.path.join(self.url, 'tasks', self.task_id, 'process', 'epoch')
        h = {'Content-Type': 'application/json'}
        _ = requests.patch(u, d, headers=h)

    def update_iteration(self, current: int, total: int):
        d = json.dumps({"Current": current, "Total": total})
        u = os.path.join(self.url, 'tasks', self.task_id, 'process', 'iteration')
        h = {'Content-Type': 'application/json'}
        _ = requests.patch(u, d, headers=h)

    def insert_log(self, level: str, message: str):
        d = json.dumps({'Level': level, 'Message': message})
        u = os.path.join(self.url, 'tasks', self.task_id, 'log')
        h = {'Content-Type': 'application/json'}
        _ = requests.post(u, d, headers=h)

    status = update_status
    epoch = update_epoch
    iter = update_iteration
    log = insert_log
