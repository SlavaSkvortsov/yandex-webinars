from locust import HttpUser, task


class MyUser(HttpUser):
    @task
    def root(self) -> None:
        self.client.get('/')
