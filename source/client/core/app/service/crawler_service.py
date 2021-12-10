
def make_status_get(authenticated_user: str) -> dict:
    # Return dummy data until microservices are integrated
    return dict(active=True, memoryUsage=999999, domain="stackoverflow",
                url="https://stackoverflow.com/questions/2281087/center-a-div-in-css")