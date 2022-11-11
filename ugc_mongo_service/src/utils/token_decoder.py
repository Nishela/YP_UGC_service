import os

import jwt


def get_token_payload(token: str) -> dict:
    unverified_headers = jwt.get_unverified_header(token)
    return jwt.decode(token, key=os.getenv('JWT_SECRET'), algorithms=unverified_headers["alg"])
