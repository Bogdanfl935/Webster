import random

def make_status_get(authenticated_user: str) -> dict:
    # Return dummy data until microservices are integrated
    letters = "abcdefghijklmonpqrstuvwxyz"
    data = dict(active=False, memoryUsage=random.randint(1, 500), domain=str(random.choice(letters)*random.randint(1, 10)),
                url=str(random.choice(letters)*random.randint(1, 10)))
    return data

def make_crawler_start_post(authenticated_user: str) -> dict:
    pass

def make_crawler_stop_post(authenticated_user: str) -> dict:
    pass