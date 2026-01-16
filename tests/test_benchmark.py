from src.utils import passcode_generator
from src.keypad.keypad import (
    RandomShuffleKeypad,
    RandomSplitShuffleKeypad,
    SlidingTowerShuffleKeypad,
    SlidingSplitShuffleKeypad
)
from src.benchmark import benchmark
import pytest


@pytest.mark.parametrize(
    "k, p, n, c, d, runs",
    [
        (6, 9, 4, 4, 4, 100)
    ]
)
def test_passcode_generator(k, p, n, c, d, runs):
    for _ in range(runs):
        passcode = passcode_generator(k=k, p=p, n=n, c=c, d=d)
        passcode_sets = [el // p for el in passcode]
        assert c <= len(set(passcode))
        assert d <= len(set(passcode_sets))


@pytest.mark.parametrize(
    "number_of_keys,properties_per_key,passcode_len,max_tries_before_lockout,complexity,disparity,run_count,keypad",
    [
        (6, 8, 4, 5, 4, 4, 100, RandomShuffleKeypad),
        (6, 8, 4, 5, 4, 4, 100, RandomSplitShuffleKeypad),
        (6, 8, 4, 5, 4, 4, 100, SlidingSplitShuffleKeypad),
        (6, 8, 4, 5, 4, 4, 100, SlidingTowerShuffleKeypad),
    ]
)
def test_benchmark(number_of_keys, properties_per_key, passcode_len, max_tries_before_lockout, complexity, disparity,
                   run_count, keypad):
    benchmark(
        number_of_keys=number_of_keys,
        properties_per_key=properties_per_key,
        passcode_len=passcode_len,
        max_tries_before_lockout=max_tries_before_lockout,
        run_count=run_count,
        complexity=complexity,
        disparity=disparity,
        keypad=keypad.new_keypad(number_of_keys, properties_per_key)
    )
