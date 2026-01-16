import pytest
import numpy as np
from src.keypad.keypad import (
    RandomSplitShuffleKeypad,
    RandomShuffleKeypad,
    SlidingSplitShuffleKeypad,
    SlidingTowerShuffleKeypad,
)


def test_key_entry():
    keypad = RandomShuffleKeypad(
        keypad=np.array([
            [8, 9, 10, 11],
            [0, 5, 2, 3],
            [4, 1, 6, 7]
        ]), k=3, p=4)
    assert keypad.key_entry([8, 5, 6, 11]) == [0, 1, 2, 0]


@pytest.mark.parametrize(
    "keypad_type, number_of_keys, properties_per_key",
    [
        (RandomShuffleKeypad, 3, 4),
        (RandomSplitShuffleKeypad, 3, 4),
        (SlidingTowerShuffleKeypad, 3, 4),
        (SlidingSplitShuffleKeypad, 3, 4),
    ]
)
def test_keypad_shuffle(keypad_type, number_of_keys, properties_per_key):
    keypad = keypad_type.new_keypad(number_of_keys, properties_per_key)
    print(keypad.keypad)
    keypad.shuffle()
    print(keypad.keypad)
