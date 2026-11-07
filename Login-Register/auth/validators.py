import re


def validate_username(username):
    return (
        isinstance(username, str)
        and 3 <= len(username) <= 20
    )


def validate_email(email):
    if not isinstance(email, str):
        return False

    pola = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pola, email))


def validate_password(password):
    return (
        isinstance(password, str)
        and len(password) >= 6
    )