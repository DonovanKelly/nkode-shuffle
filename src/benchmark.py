from tqdm import tqdm
from src.evilnkode import EvilNKode
from dataclasses import dataclass
from src.utils import observations, passcode_generator
from src.keypad.keypad import BaseKeypad
from pathlib import Path
import pickle


@dataclass
class Benchmark:
    iterations_to_break: list[int]
    iterations_to_replay: list[int]


def benchmark(
        number_of_keys: int,
        properties_per_key: int,
        passcode_len: int,
        max_tries_before_lockout: int,
        run_count: int,
        complexity: int,
        disparity: int,
        keypad: BaseKeypad,
        file_path: Path = '../output',
        overwrite: bool = False
) -> Benchmark:
    shuffle_type = str(type(keypad)).lower().split('.')[-1].replace("'>", "")
    file_name = f"{shuffle_type}-{number_of_keys}-{properties_per_key}-{passcode_len}-{max_tries_before_lockout}-{complexity}-{disparity}-{run_count}.pkl"
    full_path = Path(file_path) / "benchmark" / file_name
    if not overwrite and full_path.exists():
        print(f"File exists: {full_path}")
        with open(full_path, "rb") as fp:
            return pickle.load(fp)

    iterations_to_break = []
    iterations_to_replay = []
    for _ in tqdm(range(run_count)):
        passcode = passcode_generator(number_of_keys, properties_per_key, passcode_len, complexity, disparity)
        evilnkode = EvilNKode(
            observations=observations(
                target_passcode=passcode,
                keypad=keypad,
            ),
            number_of_keys=number_of_keys,
            properties_per_key=properties_per_key,
            passcode_len=passcode_len,
            max_tries_before_lockout=max_tries_before_lockout,
        )
        evilout = evilnkode.run()
        iterations_to_break.append(evilout.iterations_to_break)
        iterations_to_replay.append(evilout.iterations_to_replay)

    benchmark_result = Benchmark(
        iterations_to_break=iterations_to_break,
        iterations_to_replay=iterations_to_replay
    )

    if file_path:
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, "wb") as fp:
            pickle.dump(benchmark_result, fp)

    return benchmark_result
