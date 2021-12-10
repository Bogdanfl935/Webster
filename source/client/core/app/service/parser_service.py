

def make_status_get(authenticated_user: str) -> dict:
    # Return dummy data until microservices are integrated
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
    )
