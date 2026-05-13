
def validate_payload(payload: dict) -> list[str]:
    """
    validate raw payload structure before sending further downstream
    :param payload:
    :return: issues
    """

    issues = []


    if not isinstance(payload, dict):
        issues.append("payload is not a dict")
        return issues


    if "time" not in payload:
        issues.append("time is missing")

    elif not isinstance(payload["time"], int):
        issues.append("time is not an integer")


    if "states" not in payload:
        issues.append("states are missing")

    elif not isinstance(payload["states"], list):
        issues.append("states is not a list")

    return issues