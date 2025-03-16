from hashlib import sha256

import pytest


@pytest.fixture(autouse=True)
def override_password(monkeypatch):
    monkeypatch.setenv("PASSWORD_HASH", sha256("test".encode()))
