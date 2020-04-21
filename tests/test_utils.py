from ps2_census.constants import Command
from ps2_census.utils import bool2str, command_key, service_id_key


def test_service_id_key():
    res = service_id_key(service_id="someid", prefix="s:")
    assert res == "s:someid"


def test_command_key():
    res = command_key(Command.HAS, prefix="c:")
    assert res == "c:has"


def test_bool2str():
    tr = bool2str(True)
    fa = bool2str(False)

    assert tr == "true"
    assert fa == "false"
