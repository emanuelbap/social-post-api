from typing import Dict, Optional
import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from functools import lru_cache
import jwt

from app.settings import get_settings

security = HTTPBearer()


class Auth0Handler:
    def __init__(self, domain: str, client_id: str):
        self.domain = domain
        self.client_id = client_id
        self.jwks_url = f"https://{domain}/.well-known/jwks.json"
        self._jwks_cache = None

    @property
    def jwks(self):
        if self._jwks_cache is None:
            response = requests.get(self.jwks_url)
            response.raise_for_status()
            self._jwks_cache = response.json()
        return self._jwks_cache

    def get_signing_key(self, token: str) -> Dict:
        header = jwt.get_unverified_header(token)
        jwks = self.jwks
        
        for key in jwks.get("keys", []):
            if key["kid"] == header["kid"]:
                return key
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    def verify_token(self, token: str) -> Dict:
        try:
            signing_key = self.get_signing_key(token)
            payload = jwt.decode(
                token,
                jwt.algorithms.RSAAlgorithm.from_jwk(signing_key),
                algorithms=["RS256"],
                audience=self.client_id,
                issuer=f"https://{self.domain}/"
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado"
            )
        except jwt.JWTClaimsError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Permissões inválidas no token"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )


@lru_cache
def get_auth_handler() -> Auth0Handler:
    settings = get_settings()
    return Auth0Handler(domain=settings.auth0_domain, client_id=settings.auth0_client_id)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_handler: Auth0Handler = Depends(get_auth_handler)
) -> Dict:
    token = credentials.credentials
    return auth_handler.verify_token(token)


def require_role(required_role: str):
    def role_checker(user: Dict = Depends(get_current_user)) -> Dict:
        roles = user.get("https://courses-api/roles", [])
        
        if required_role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requer papel: {required_role}"
            )
        
        return user
    
    return role_checker
