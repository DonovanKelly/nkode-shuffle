import argparse
from src.benchmark import benchmark
import matplotlib.pyplot as plt
from pathlib import Path
from statistics import mean
from src.keypad.keypad import (
    RandomSplitShuffleKeypad,
    RandomShuffleKeypad,
    SlidingSplitShuffleKeypad,
    SlidingTowerShuffleKeypad,
)


def bench_histogram(data, title, number_of_keys, properties_per_key, passcode_len, max_tries_before_lockout, complexity,
                    disparity, run_count, save_path: Path = None):
    min_val = min(data)
    max_val = max(data)
    bins = range(min_val, max_val + 2)
    plt.hist(data, bins=bins, edgecolor='black')
    plt.title(title)
    plt.xlabel('# of Login Observations')
    plt.ylabel('Simulations')
    text = (f"number_of_keys={number_of_keys}\n"
            f"properties_per_key={properties_per_key}\n"
            f"passcode_len={passcode_len}\n"
            f"max_tries_before_lockout={max_tries_before_lockout}\n"
            f"complexity={complexity}\n"
            f"disparity={disparity}\n"
            f"run_count={run_count}")
    plt.text(0.95, 0.95, text, transform=plt.gca().transAxes, fontsize=10,
             verticalalignment='top', horizontalalignment='right', bbox=dict(facecolor='white', alpha=0.5))
    if save_path:
        save_path = save_path / "histogram"
        save_path.mkdir(parents=True, exist_ok=True)
        filename = (f"{title.replace(' ', '_')}_keys{number_of_keys}_"
                    f"props{properties_per_key}_pass{passcode_len}_tries{max_tries_before_lockout}_"
                    f"comp{complexity}_disp{disparity}_runs{run_count}.png")
        plt.savefig(save_path / filename, bbox_inches='tight', dpi=300)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description='Benchmark Keypad Shuffle')
    parser.add_argument('--shuffle_type', type=str,
                        choices=['RandomSplitShuffle', 'RandomShuffle', 'SlidingSplitShuffle', 'SlidingTowerShuffle'],
                        default='SlidingTowerShuffle', help='Type of keypad shuffle')
    parser.add_argument('--number_of_keys', type=int, default=6, help='Number of keys')
    parser.add_argument('--properties_per_key', type=int, default=8, help='Properties per key')
    parser.add_argument('--passcode_len', type=int, default=4, help='Passcode length')
    parser.add_argument('--max_tries_before_lockout', type=int, default=5, help='Max tries before lockout')
    parser.add_argument('--complexity', type=int, default=4, help='Complexity')
    parser.add_argument('--disparity', type=int, default=4, help='Disparity')
    parser.add_argument('--run_count', type=int, default=10000, help='Number of runs')
    parser.add_argument('--output_dir', type=str, default='./output',
                        help='Output directory for histograms')

    args = parser.parse_args()

    shuffle_classes = {
        'RandomSplitShuffle': RandomSplitShuffleKeypad,
        'RandomShuffle': RandomShuffleKeypad,
        'SlidingSplitShuffle': SlidingSplitShuffleKeypad,
        'SlidingTowerShuffle': SlidingTowerShuffleKeypad
    }

    keypad_class = shuffle_classes[args.shuffle_type]
    keypad = keypad_class.new_keypad(args.number_of_keys, args.properties_per_key)

    shuffle_type = str(type(keypad)).lower().split('.')[-1].replace("'>", "")
    run_name = f"{shuffle_type}-{args.number_of_keys}-{args.properties_per_key}-{args.passcode_len}-{args.max_tries_before_lockout}-{args.complexity}-{args.disparity}-{args.run_count}"
    save_path = Path(args.output_dir) / run_name
    bench_result = benchmark(
        number_of_keys=args.number_of_keys,
        properties_per_key=args.properties_per_key,
        passcode_len=args.passcode_len,
        max_tries_before_lockout=args.max_tries_before_lockout,
        run_count=args.run_count,
        complexity=args.complexity,
        disparity=args.disparity,
        keypad=keypad,
        file_path=save_path,
    )

    print(f"Bench {args.shuffle_type} Break {mean(bench_result.iterations_to_break)}")
    print(f"Bench {args.shuffle_type} Replay {mean(bench_result.iterations_to_replay)}")

    bench_histogram(
        bench_result.iterations_to_break,
        f"{args.shuffle_type} Break",
        args.number_of_keys,
        args.properties_per_key,
        args.passcode_len,
        args.max_tries_before_lockout,
        args.complexity,
        args.disparity,
        args.run_count,
        save_path
    )

    bench_histogram(
        bench_result.iterations_to_replay,
        f"{args.shuffle_type} Replay",
        args.number_of_keys,
        args.properties_per_key,
        args.passcode_len,
        args.max_tries_before_lockout,
        args.complexity,
        args.disparity,
        args.run_count,
        save_path,
    )


if __name__ == "__main__":
    main()
