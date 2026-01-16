from dataclasses import dataclass
from pathlib import Path
from statistics import mean

import matplotlib.pyplot as plt

from src.benchmark import benchmark
from src.keypad.keypad import SlidingTowerShuffleKeypad

HIST_DIR = Path("hist")


@dataclass(frozen=True)
class Scenario:
    name: str
    number_of_keys: int
    properties_per_key: int
    passcode_len: int
    max_tries_before_lockout: int
    complexity: int
    disparity: int
    run_count: int


SCENARIOS = [
    Scenario(
        name="baseline_k6_p8",
        number_of_keys=6,
        properties_per_key=8,
        passcode_len=4,
        max_tries_before_lockout=5,
        complexity=4,
        disparity=4,
        run_count=5000,
    ),
    Scenario(
        name="short_passcode_k6_p8",
        number_of_keys=6,
        properties_per_key=8,
        passcode_len=3,
        max_tries_before_lockout=5,
        complexity=3,
        disparity=3,
        run_count=5000,
    ),
    Scenario(
        name="dense_keypad_k8_p10",
        number_of_keys=8,
        properties_per_key=10,
        passcode_len=4,
        max_tries_before_lockout=5,
        complexity=4,
        disparity=4,
        run_count=5000,
    ),
    Scenario(
        name="longer_passcode_k6_p8",
        number_of_keys=6,
        properties_per_key=8,
        passcode_len=5,
        max_tries_before_lockout=5,
        complexity=5,
        disparity=4,
        run_count=5000,
    ),
]


def render_histogram(data: list[int], title: str, scenario: Scenario, output_dir: Path) -> Path:
    min_val = min(data)
    max_val = max(data)
    bins = range(min_val, max_val + 2)

    plt.figure(figsize=(8, 5))
    plt.hist(data, bins=bins, edgecolor="black")
    plt.title(title)
    plt.xlabel("# of Login Observations")
    plt.ylabel("Simulations")
    text = (
        f"number_of_keys={scenario.number_of_keys}\n"
        f"properties_per_key={scenario.properties_per_key}\n"
        f"passcode_len={scenario.passcode_len}\n"
        f"max_tries_before_lockout={scenario.max_tries_before_lockout}\n"
        f"complexity={scenario.complexity}\n"
        f"disparity={scenario.disparity}\n"
        f"run_count={scenario.run_count}"
    )
    plt.text(
        0.98,
        0.98,
        text,
        transform=plt.gca().transAxes,
        fontsize=9,
        verticalalignment="top",
        horizontalalignment="right",
        bbox=dict(facecolor="white", alpha=0.6),
    )

    filename = f"{scenario.name}_break.png"
    output_path = output_dir / filename
    plt.savefig(output_path, bbox_inches="tight", dpi=250)
    plt.close()
    return output_path


def run_scenario(scenario: Scenario, output_dir: Path) -> Path:
    keypad = SlidingTowerShuffleKeypad.new_keypad(
        scenario.number_of_keys,
        scenario.properties_per_key,
    )
    results = benchmark(
        number_of_keys=scenario.number_of_keys,
        properties_per_key=scenario.properties_per_key,
        passcode_len=scenario.passcode_len,
        max_tries_before_lockout=scenario.max_tries_before_lockout,
        run_count=scenario.run_count,
        complexity=scenario.complexity,
        disparity=scenario.disparity,
        keypad=keypad,
        file_path=None,
    )
    avg_break = mean(results.iterations_to_break)
    print(f"{scenario.name}: mean break observations = {avg_break:.2f}")
    return render_histogram(
        results.iterations_to_break,
        "Sliding Tower Shuffle - Observations to Break",
        scenario,
        output_dir,
    )


def main() -> None:
    HIST_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating SlidingTowerShuffle histograms...")
    for scenario in SCENARIOS:
        output_path = run_scenario(scenario, HIST_DIR)
        print(f"Saved histogram: {output_path}")


if __name__ == "__main__":
    main()
