from fastapi import Request


def extract_token(request: Request) -> str | None:
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None
    if auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    if auth_header.startswith("Token "):
        return auth_header.split(" ")[1]
    return None
