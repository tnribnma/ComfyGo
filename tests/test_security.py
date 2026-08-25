import pytest
from datetime import datetime, timedelta, timezone

from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)

class TestPasswordHashing:
    def test_hash_is_not_plaintext(self):
        hashed = get_password_hash("MySecret1")
        assert hashed != "MySecret1"
        assert len(hashed) > 20 

    def test_verify_correct_password(self):
        plain = "StrongPass1"
        hashed = get_password_hash(plain)
        assert verify_password(plain, hashed) is True

    def test_verify_wrong_password(self):
        hashed = get_password_hash("Correct1")
        assert verify_password("WrongPass1", hashed) is False

    def test_different_hashes_for_same_input(self):
        """bcrypt salts produce unique hashes."""
        h1 = get_password_hash("SamePassword1")
        h2 = get_password_hash("SamePassword1")
        assert h1 != h2
        assert verify_password("SamePassword1", h1)
        assert verify_password("SamePassword1", h2)

    def test_password_truncated_to_72_chars(self):
        long_pw = "A" * 100 + "1"
        hashed = get_password_hash(long_pw)
        assert verify_password(long_pw, hashed)

    def test_empty_password_hash(self):
        hashed = get_password_hash("")
        assert isinstance(hashed, str)
        assert verify_password("", hashed)


class TestAccessToken:
    def test_create_and_decode(self):
        token = create_access_token(subject="42", role="admin")
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "42"
        assert payload["role"] == "admin"
        assert payload["type"] == "access"
        assert "exp" in payload
        assert "iat" in payload

    def test_custom_expiry(self):
        token = create_access_token(
            subject="1", role="customer", expires_minutes=5
        )
        payload = decode_token(token)
        assert payload is not None
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        iat = datetime.fromtimestamp(payload["iat"], tz=timezone.utc)
        diff = exp - iat
        assert 4 * 60 <= diff.total_seconds() <= 6 * 60

    def test_extra_claims(self):
        token = create_access_token(
            subject="7", role="employee", extra={"hotel_id": 3}
        )
        payload = decode_token(token)
        assert payload["hotel_id"] == 3

    def test_invalid_token_returns_none(self):
        assert decode_token("not.a.real.jwt") is None

    def test_tampered_token_returns_none(self):
        token = create_access_token(subject="1", role="admin")
        tampered = token[:-5] + "XXXXX"
        assert decode_token(tampered) is None


class TestRefreshToken:
    def test_create_and_decode(self):
        token = create_refresh_token(subject="10", role="customer")
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "10"
        assert payload["role"] == "customer"
        assert payload["type"] == "refresh"

    def test_refresh_longer_than_access(self):
        access = create_access_token(subject="1", role="admin")
        refresh = create_refresh_token(subject="1", role="admin")
        a_payload = decode_token(access)
        r_payload = decode_token(refresh)
        assert r_payload["exp"] > a_payload["exp"]

    def test_invalid_refresh_token(self):
        assert decode_token("garbage") is None
