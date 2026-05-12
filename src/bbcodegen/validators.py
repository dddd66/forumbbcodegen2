# unused, refactor later...


def validate_input(required_fields: list[str]) -> bool:
    for value in required_fields:
        if value.strip() == "":
            return False
    return True
