import httpx


class UserClient:
    def __init__(self):
        self.base_url = "http://18.228.48.67/users"

    def get_user(self, user_id: str):
        response = httpx.get(f"{self.base_url}/{user_id}")

        if response.status_code == 404:
            return None

        return response.json()