from dataclasses import dataclass
import numpy as np
from src.keypad.tower_shuffle import TowerShuffle
from abc import ABC, abstractmethod
from typing import Self


class BaseKeypad(ABC):
    keypad: np.ndarray
    k: int  # number of keys
    p: int  # properties per key

    @classmethod
    def _build_keypad(cls, k: int, p: int) -> np.ndarray:
        rng = np.random.default_rng()
        total = k * p
        array = np.arange(total)
        keypad = array.reshape(k, p)
        set_view = keypad.T.copy()
        for set_idx in set_view:
            rng.shuffle(set_idx)
        return set_view.T

    @classmethod
    @abstractmethod
    def new_keypad(cls, k: int, p: int) -> Self:
        raise NotImplementedError

    def key_entry(self, target_passcode: list[int]) -> list[int]:
        vals = np.array(target_passcode)
        if np.any((vals < 0) | (vals >= self.k * self.p)):
            raise ValueError("One or more values are out of the valid range.")
        flat = self.keypad.flatten()
        inv_index = np.empty(self.k * self.p, dtype=int)
        for i, v in enumerate(flat):
            inv_index[v] = i // self.p
        return inv_index[vals].tolist()

    @abstractmethod
    def shuffle(self):
        pass

    def keypad_mat(self) -> list[list[int]]:
        return [el.tolist() for el in self.keypad]


@dataclass
class SlidingTowerShuffleKeypad(BaseKeypad):
    keypad: np.ndarray
    k: int  # number of keys
    p: int  # properties per key
    tower_shuffle: TowerShuffle

    @classmethod
    def new_keypad(cls, k: int, p: int) -> Self:
        kp = cls._build_keypad(k, p)
        return cls(keypad=kp, k=k, p=p, tower_shuffle=TowerShuffle.new(p))

    def shuffle(self):
        selected_positions = self.tower_shuffle.left_tower.tolist()
        shift = np.random.randint(1, self.k)  # random int in [1, k-1]
        new_key_idxs = np.roll(np.arange(self.k), shift)
        shuffled_sets = self.keypad.copy()
        shuffled_sets[:, selected_positions] = shuffled_sets[new_key_idxs, :][:, selected_positions]
        self.keypad = shuffled_sets
        self.tower_shuffle.shuffle()


@dataclass
class RandomShuffleKeypad(BaseKeypad):
    keypad: np.ndarray
    k: int  # number of keys
    p: int  # properties per key

    @classmethod
    def new_keypad(cls, k: int, p: int) -> Self:
        kp = cls._build_keypad(k, p)
        return cls(keypad=kp, k=k, p=p)

    def shuffle(self):
        shuffled_matrix = np.array([np.random.permutation(row) for row in self.keypad.T])
        self.keypad = shuffled_matrix.T


@dataclass
class RandomSplitShuffleKeypad(BaseKeypad):
    keypad: np.ndarray
    k: int  # number of keys
    p: int  # properties per key

    @classmethod
    def new_keypad(cls, k: int, p: int) -> Self:
        kp = cls._build_keypad(k, p)
        return cls(keypad=kp, k=k, p=p)

    def shuffle(self):
        column_permutation = np.random.permutation(self.p)
        column_subset = column_permutation[:self.p // 2]
        new_key_idxs = np.random.permutation(self.k)
        shuffled_sets = self.keypad.copy()
        shuffled_sets[:, column_subset] = shuffled_sets[new_key_idxs, :][:, column_subset]
        self.keypad = shuffled_sets


@dataclass
class SlidingSplitShuffleKeypad(BaseKeypad):
    keypad: np.ndarray
    k: int  # number of keys
    p: int  # properties per key

    @classmethod
    def new_keypad(cls, k: int, p: int) -> Self:
        kp = cls._build_keypad(k, p)
        return cls(keypad=kp, k=k, p=p)

    def shuffle(self):
        selected_positions = np.random.permutation(self.p)
        column_subset = selected_positions[:self.p // 2]
        shift = np.random.randint(1, self.k)
        new_key_idxs = np.roll(np.arange(self.k), shift)
        shuffled_sets = self.keypad.copy()
        shuffled_sets[:, column_subset] = shuffled_sets[new_key_idxs, :][:, column_subset]
        self.keypad = shuffled_sets
