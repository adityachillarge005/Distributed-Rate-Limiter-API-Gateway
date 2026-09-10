from locust import HttpUser, task, between


class GatewayUser(HttpUser):

    wait_time = between(1, 2)

    @task
    def gateway_request(self):
        self.client.get(
            "/api/gateway/",
            headers={
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg5MDY0NDQ5LCJpYXQiOjE3ODkwNjQxNDksImp0aSI6ImQ5NzI1MzI1NzI0ZTQ3ODc4MWM1MjcwYTRlZTU4MWRhIiwidXNlcl9pZCI6IjEifQ.FSuSsSknHHym_F2v2a8Csrgtzho4hwDn6eVzH4fgcAs"
            }
        )