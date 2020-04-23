from .constants import COMMAND_PREFIX, SERVICE_ID_PREFIX, Command


def command_key(command: Command, prefix: str = COMMAND_PREFIX) -> str:
    return f"{prefix}{command}"


def bool2str(arg: bool) -> str:
    return "true" if arg is True else "false"
