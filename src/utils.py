import random
from math import factorial, comb

from src.evilnkode import Observation
from src.keypad.keypad import BaseKeypad
from typing import Iterator


def total_valid_nkode_states(k: int, p: int) -> int:
    return factorial(k) ** (p - 1)


def total_shuffle_states(k: int, p: int) -> int:
    return comb((p - 1), (p - 1) // 2) * factorial(k)


def observations(target_passcode: list[int], keypad: BaseKeypad, number_of_observations: int = 100) -> Iterator[
    Observation]:
    def obs():
        for _ in range(number_of_observations):
            yield Observation(
                keypad=keypad.keypad_mat(),
                key_selection=keypad.key_entry(target_passcode=target_passcode)
            )
            keypad.shuffle()

    return obs()


def passcode_generator(k: int, p: int, n: int, c: int, d: int) -> list[int]:
    assert n >= c
    assert p * k >= c

    assert n >= d
    assert p >= d
    passcode_prop = []
    passcode_set = []
    valid_choices = {i for i in range(k * p)}
    repeat_set = n - d
    repeat_prop = n - c
    prop_added = set()
    set_added = set()

    for _ in range(n):
        prop = random.choice(list(valid_choices))
        prop_set = prop // p
        passcode_prop.append(prop)
        passcode_set.append(prop_set)

        if prop in prop_added:
            repeat_prop -= 1
        if prop_set in set_added:
            repeat_set -= 1

        prop_added.add(prop)
        set_added.add(prop_set)

        if repeat_prop <= 0:
            valid_choices -= prop_added

        if repeat_set <= 0:
            for el in valid_choices.copy():
                if el // p in set_added:
                    valid_choices.remove(el)

    return passcode_prop
