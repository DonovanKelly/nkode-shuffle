from src.keypad.tower_shuffle import TowerShuffle


def test_tower_shuffle():
    tower = TowerShuffle.new(13)
    print(tower)
    for _ in range(100):
        tower.shuffle()
        print(tower)
