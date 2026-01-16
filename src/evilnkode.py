import math
from dataclasses import dataclass
from typing import Iterator


@dataclass
class Observation:
    keypad: list[list[int]]
    key_selection: list[int]

    @property
    def property_list(self) -> list[set[int]]:
        return [set(self.keypad[idx]) for idx in self.key_selection]

    @property
    def flat_keypad(self) -> list[int]:
        return [num for row in self.keypad for num in row]


@dataclass
class EvilOutput:
    iterations_to_break: int
    iterations_to_replay: int


@dataclass
class EvilNKode:
    observations: Iterator[Observation]
    passcode_len: int
    number_of_keys: int
    properties_per_key: int
    max_tries_before_lockout: int = 5
    possible_nkode = None

    def initialize(self):
        possible_values = set(range(self.number_of_keys * self.properties_per_key))
        self.possible_nkode = [possible_values.copy() for _ in range(self.passcode_len)]

    def run(self) -> EvilOutput:
        self.initialize()
        iterations_to_replay = None
        for idx, obs in enumerate(self.observations):
            if iterations_to_replay is None:
                replay_possibilities = self.replay_attack(obs)
                if replay_possibilities <= self.max_tries_before_lockout:
                    iterations_to_replay = idx + 1
            if math.prod([len(el) for el in self.possible_nkode]) <= self.max_tries_before_lockout:
                assert iterations_to_replay <= idx + 1
                return EvilOutput(
                    # possible_nkodes=[list(el) for el in self.possible_nkode],
                    iterations_to_break=idx + 1,
                    iterations_to_replay=iterations_to_replay
                )
            for jdx, props in enumerate(obs.property_list):
                self.possible_nkode[jdx] = props.intersection(self.possible_nkode[jdx])
        raise Exception("error in Evilkode, observations stopped yielding")

    def replay_attack(self, obs: Observation) -> int:
        possible_combos = 1
        for el in self.possible_nkode:
            possible_combos *= len({obs.flat_keypad.index(el2) // self.properties_per_key for el2 in el})
        return possible_combos
