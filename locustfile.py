import os
from locust import HttpUser, task, between


class GatewayUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def gateway_request(self):
        token = os.getenv("LOCUST_ACCESS_TOKEN")

        if not token:
            raise RuntimeError("Set LOCUST_ACCESS_TOKEN before running Locust")

        self.client.get(
            "/api/gateway/",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )