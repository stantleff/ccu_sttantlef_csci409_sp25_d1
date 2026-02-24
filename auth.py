"""
Basic Auth helper used across all microservices.

Credentials are read from environment variables:
  BASIC_AUTH_USERNAME
  BASIC_AUTH_PASSWORD

defaults are:
  admin / password
"""

import os
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

basic_security = HTTPBasic()

def verify_basic_auth(
    credentials: HTTPBasicCredentials = Depends(basic_security),
) -> str:
    expected_username = os.getenv("BASIC_AUTH_USERNAME", "admin")
    expected_password = os.getenv("BASIC_AUTH_PASSWORD", "password")

    username_ok = secrets.compare_digest(credentials.username, expected_username)
    password_ok = secrets.compare_digest(credentials.password, expected_password)

    if not (username_ok and password_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username