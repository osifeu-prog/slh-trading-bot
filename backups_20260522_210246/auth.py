import os
import jwt
from jwt.exceptions import InvalidTokenError

# קריאת SECRET_KEY ממשתנה סביבה, או שימוש בברירת מחדל
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-in-production-!@#")
ALGORITHM = "HS256"

def decode_access_token(token: str) -> dict:
    """פענוח טוקן JWT. מחזיר payload."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        raise ValueError("Invalid token")
