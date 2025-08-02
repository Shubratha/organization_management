from datetime import datetime, timedelta

import pytest
from jose import jwt

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password


def test_password_hash() -> None:
    """Test password hashing and verification."""
    password = "testpassword123"
    hashed = get_password_hash(password)

    # Test that hashes are different for same password
    assert hashed != get_password_hash(password)

    # Test verification
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)


def test_create_access_token() -> None:
    """Test JWT token creation and validation."""
    data = {"sub": "test@example.com", "is_super_admin": True}
    token = create_access_token(data)

    # Decode and verify token
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    # Check payload
    assert payload["sub"] == data["sub"]
    assert payload["is_super_admin"] == data["is_super_admin"]
    assert "exp" in payload

    # Check expiration
    exp = datetime.fromtimestamp(payload["exp"])
    now = datetime.utcnow()
    assert exp > now
    assert exp < now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES + 1)


def test_token_expiration() -> None:
    """Test token expiration."""
    data = {"sub": "test@example.com"}
    token = create_access_token(data)

    # Token should be valid now
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == data["sub"]

    # Modify expiration to be in the past
    expired_payload = {**payload, "exp": datetime.utcnow() - timedelta(minutes=1)}
    expired_token = jwt.encode(expired_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    # Decoding should raise an exception
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(expired_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
