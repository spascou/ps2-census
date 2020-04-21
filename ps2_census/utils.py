from .constants import COMMAND_PREFIX, SERVICE_ID_PREFIX, Command


def service_id_key(service_id: str, prefix: str = SERVICE_ID_PREFIX) -> str:
    return f"{prefix}{service_id}"


def command_key(command: Command, prefix: str = COMMAND_PREFIX) -> str:
    return f"{prefix}{command}"


def bool2str(arg: bool) -> str:
    return "true" if arg is True else "false"
