from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):

    @task(2)
    def index(self):
        self.client.get("/")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=100
    max_wait=500
