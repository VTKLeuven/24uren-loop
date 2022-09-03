from locust import HttpUser, task, between


class GeneralUser(HttpUser):
    weight = 1
    wait_time = between(1, 2)

    @task(10)
    def index_page(self):
        self.client.get('/api/queue-ticket/')
        self.client.get('/api/runner/top_runners/')
        self.client.get('/api/group/top_groups/')
        self.client.get('/api/runner/most_active')
        self.client.get('/api/lap/', params={'duration__isnull': True})
        self.client.get('/api/lap/', params={
            'ordering': '-start_time',
            'limit': 3,
            'duration__isnull': False,
        })

    @task(1)
    def queue_page(self):
        self.client.get('/api/queue-ticket')

    @task(3)
    def fullscreen_page(self):
        self.client.get('/api/lap/', params={'duration__isnull': True})
        self.client.get('/api/lap/', params={
            'ordering': '-start_time',
            'limit': 1,
            'duration__isnull': False,
        })
        self.client.get('/api/queue-ticket/')


class StreamUser(HttpUser):
    weight = 1

    @task
    def open_stream(self):
        with self.client.get('/events/', stream=True) as r:
            for _ in r.iter_lines():
                pass


