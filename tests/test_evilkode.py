import random
import pytest

from src.evilnkode import EvilNKode
from src.keypad.keypad import (
    RandomShuffleKeypad,
)
from src.utils import observations


@pytest.fixture
def passcode(number_of_keys, properties_per_key, passcode_len):
    return [random.randint(0, number_of_keys * properties_per_key - 1) for _ in range(passcode_len)]


@pytest.mark.parametrize(
    "number_of_keys, properties_per_key, passcode_len",
    [
        (5, 4, 4),  # Test case 1
        (10, 5, 6),  # Test case 2
        (8, 4, 5),  # Test case 3
    ]
)
def test_evilkode(number_of_keys, properties_per_key, passcode_len, passcode):
    keypad = RandomShuffleKeypad.new_keypad(number_of_keys, properties_per_key)
    obs = observations(passcode, keypad)
    evilkode = EvilNKode(
        observations=obs,
        number_of_keys=number_of_keys,
        properties_per_key=properties_per_key,
        passcode_len=passcode_len,
    )
    evilout = evilkode.run()
    assert evilout.iterations_to_break > 1
