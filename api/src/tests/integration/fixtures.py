from app.auth.functions import generate_token


def auth_headers():
    return {"Authorization": f"Bearer {generate_token()}"}
