from dataclasses import dataclass
import numpy as np


@dataclass
class Tower:
    floors: list[np.ndarray]

    def split_tower(self) -> tuple[np.ndarray, np.ndarray]:
        discard = np.array([], dtype=int)
        keep = np.array([], dtype=int)
        balance = self.balance()
        for idx, floor in enumerate(self.floors):
            div = len(floor) // 2 + balance[idx]
            floor_shuffle = np.random.permutation(len(floor))
            keep = np.concatenate((keep, floor[floor_shuffle[:div]]))
            discard = np.concatenate((discard, floor[floor_shuffle[div:]]))
        diff = len(discard) - len(keep)
        assert 0 <= diff <= 1
        return keep, discard

    def balance(self) -> list[int]:
        odd_floors = np.array([idx for idx, el in enumerate(self.floors) if len(el) & 1])
        balance = np.zeros(len(self.floors), dtype=int)
        if len(odd_floors) == 0:
            return balance.tolist()
        shuffle = np.random.permutation(len(odd_floors))[:len(odd_floors) // 2]
        odd_floors = odd_floors[shuffle]
        balance[odd_floors] = 1
        return balance.tolist()

    def update_tower(self, keep: np.ndarray, other_discard: np.ndarray):
        new_floors = []
        for floor in self.floors:
            new_floor = np.intersect1d(floor, keep)
            if len(new_floor):
                new_floors.append(new_floor)
        self.floors = new_floors
        self.floors.insert(0, other_discard)

    def __str__(self):
        str_val = ""
        floor_numb = [i for i in reversed(range(len(self.floors)))]
        for idx, val in enumerate(reversed(self.floors)):
            str_val += f"Floor {floor_numb[idx]}: {val.tolist()}\n"
        return str_val

    def tolist(self) -> list[int]:
        tower = []
        for floor in self.floors:
            tower.extend(floor.tolist())
        return tower


@dataclass
class TowerShuffle:
    # TODO: I don't think total_positions is used anywhere
    total_positions: int
    left_tower: Tower
    right_tower: Tower

    @classmethod
    def new(cls, total_pos: int):
        assert total_pos >= 3
        rand_pos = np.random.permutation(total_pos)
        return TowerShuffle(
            total_positions=total_pos,
            left_tower=Tower(floors=[rand_pos[:total_pos // 2]]),
            right_tower=Tower(floors=[rand_pos[total_pos // 2:]]),
        )

    def shuffle(self):
        left_keep, left_discard = self.left_tower.split_tower()
        right_keep, right_discard = self.right_tower.split_tower()
        self.left_tower.update_tower(left_keep, right_discard)
        self.right_tower.update_tower(right_keep, left_discard)

    def __str__(self):
        return f"""Left Tower:
{self.left_tower}
Right Tower:
{self.right_tower}"""
