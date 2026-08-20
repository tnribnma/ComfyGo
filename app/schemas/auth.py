from typing import Optional
from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    role: str
    user_id: int


class RefreshTokenRequest(BaseModel):
    refresh_token: str