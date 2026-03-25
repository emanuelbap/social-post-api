import httpx


class UserServiceError(RuntimeError):
    pass


class UserClient:
    def __init__(self, base_url: str, timeout: float = 5.0, token: str | None = None):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.token = token

    def user_exists(self, user_id: str) -> bool:
        url = f"{self.base_url}/{user_id}"
        headers = {}

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url, headers=headers)
        except httpx.RequestError as exc:
            raise UserServiceError(f"Falha ao consultar API de usuários: {exc}") from exc

        if response.status_code == 404:
            return False

        if 200 <= response.status_code < 300:
            return True

        raise UserServiceError(f"Status inesperado da API de usuários: {response.status_code}")