import re
import string

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

PHONE_REGEX = r"^\+?[0-9\s\-\(\)]{7,15}$"

def is_valid_email(email: str) -> bool:
    if not email:
        return False
    return bool(re.match(EMAIL_REGEX, email))


def is_strong_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    special_chars = set(string.punctuation)
    if not any(c in special_chars for c in password):
        return False
    return True


def normalize_phone_number(phone: str) -> str:
    if not phone:
        return ""
    cleaned = re.sub(r"[^\d+]", "", phone)
    if cleaned.startswith("+"):
        return "+" + cleaned[1:].lstrip("+")
    return cleaned


def sanitize_string(text: str, max_length: int = 255) -> str:
    if not text:
        return ""
    return text.strip()[:max_length]