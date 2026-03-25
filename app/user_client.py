import httpx


class UserServiceError(RuntimeError):
    pass


class UserClient:
    def __init__(self, base_url: str, timeout: float = 5.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get_user(self, user_id: str):
        url = f"{self.base_url}/{user_id}"

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url)
        except httpx.RequestError as exc:
            raise UserServiceError(f"Falha ao consultar API de usuários: {exc}") from exc

        if response.status_code == 404:
            return None

        if 200 <= response.status_code < 300:
            return response.json()

        raise UserServiceError(f"Status inesperado da API de usuários: {response.status_code}")