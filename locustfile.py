# from locustfile import HttpUser, TaskSet, task,between

# import random
# old version

# class MyTaskClass(TaskSet):
#     @task
#     def like_post(self):
#         post_id = 1
#         self.cleint.get(
#             f"/post_like/{post_id}",
#             data = {},
#             header = { "Content-Type" : "application/json"}
#         )
        
# class WebsiteUser(HttpUser):
#     tasks = [MyTaskClass]
#     wait_time = between(1,2)
    
from locust import HttpUser, task, between

class MyUser(HttpUser):
    host = "http://localhost:8000"
    wait_time = between(1, 5)

    @task
    def like_post(self):
        post_id = 1
        headers = { "Content-Type": "application/json" }
        self.client.get(
            f"/post_like/{post_id}",
            headers=headers
        )

# for post
# @task
# def like_post(self):
#     post_id = 1
#     headers = { "Content-Type": "application/json" }
#     payload = {}

#     self.client.post(
#         f"/post_like/{post_id}",
#         json=payload,
#         headers=headers
#     )


