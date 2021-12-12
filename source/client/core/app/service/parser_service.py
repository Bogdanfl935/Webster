import random

def make_status_get(authenticated_user: str) -> dict:
    # Return dummy data until microservices are integrated
    letters = "abcdefghijklmonpqrstuvwxyz"
    data = dict(domain=str(random.choice(letters)*random.randint(1, 10)),
                url=str(random.choice(letters)*random.randint(1, 10)),
                content=[
                    dict(tag=str(random.choice(letters)*random.randint(1, 10)), size=random.randint(1, 10)),
                    dict(tag=str(random.choice(letters)*random.randint(1, 10)), size=random.randint(1, 10)),
                    dict(tag=str(random.choice(letters)*random.randint(1, 10)), size=random.randint(1, 10))
                    ])
    return data
    """
    return dict(
        active=True,
        url="https://stackoverflow.com/questions/2281087/center-a-div-in-css",
        domain="stackoverflow",
        content=[
            dict(tag="div", size=4153),
            dict(tag="input", size=109),
            dict(tag="img", size=7953),
            dict(tag="style", size=27311),
            dict(tag="form", size=1291),
            dict(tag="title", size=20)
        ]
    )"""
