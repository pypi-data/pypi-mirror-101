import requests


def get_json(url) -> dict:

    request = requests.get(url)

    if request.status_code == 200:
        return request.json()
    else:
        if request.status_code == 404:
            raise Exception("Please double check the slug or ID")

        raise Exception("Network error, please try again later")
