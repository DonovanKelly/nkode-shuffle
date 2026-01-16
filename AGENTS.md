# AGENTS.md

## Scope
- Applies to the entire repository unless a nested `AGENTS.md` overrides it.
- Read this file before making code or config changes.
- Keep updates minimal and focused on the requested task.

## Repo Summary
- Python project focused on keypad shuffle simulations and benchmarking.
- Primary packages live in `src/` with CLI utilities in `cli/`.
- Tests are in `tests/` and use `pytest`.
- Outputs and artifacts are written to `output/` during runs.

## Environment Setup
- Dependencies are defined in `environment.yaml` (Conda).
- The file currently declares `name: base`; confirm or change the env name if needed.
- Create the environment with `conda env create -f environment.yaml`.
- Activate with `conda activate <env-name>` (see `environment.yaml`).
- `requirements.txt` exists but only pins `numpy`.
- Python version in the env is 3.12.
- Prefer Conda for full dependency coverage.

## Build / Run Commands
- Run benchmark CLI: `python -m cli.benchmark_histogram`.
- Show CLI help: `python -m cli.benchmark_histogram -help`.
- Output is written under `output/` by default.
- README mentions `cli.visualnkode`, but the module is not present.
- Use module execution (`python -m ...`) instead of running scripts directly.

## Test Commands
- Run all tests: `python -m pytest`.
- Run a single file: `python -m pytest tests/test_keypad.py`.
- Run a single test: `python -m pytest tests/test_keypad.py::test_key_entry`.
- Run tests by keyword: `python -m pytest -k keypad`.
- Use `-q` to reduce output noise if needed.
- Keep tests deterministic and quick.

## Lint / Format / Type Check
- Format: `black src tests cli`.
- Sort imports: `isort src tests cli`.
- Lint: `flake8 src tests cli`.
- Type check: `mypy src` (no repo config; add flags if needed).
- Run formatters before linting when touching many files.
- Ensure formatting passes before committing changes.

## Project Layout
- `src/` contains core logic and domain models.
- `src/keypad/` contains shuffle implementations.
- `src/evilnkode.py` and `src/benchmark.py` are core logic entry points.
- `cli/` scripts orchestrate runs and write to `output/`.
- `tests/` mirrors core functionality with pytest tests.
- `output/` holds generated artifacts; avoid editing by hand.

## CLI Conventions
- Prefer `argparse` for CLI arguments (current pattern).
- Use `Path` for filesystem paths.
- Keep default values explicit and documented in help text.
- Avoid heavy logic inside CLI modules; delegate to `src/`.
- When adding new CLI args, update README if needed.

## Imports
- Group imports: standard library, third-party, then local.
- Keep a blank line between import groups.
- Prefer absolute imports from `src` (e.g., `from src.keypad.keypad import BaseKeypad`).
- Keep imports alphabetized within a group when easy.
- Avoid unused imports; keep modules lean.
- Use `typing` imports for public annotations.

## Formatting
- Use 4-space indentation.
- Keep line lengths reasonable (aim for ~88–100 chars).
- Break long argument lists across lines with trailing commas.
- Use consistent quote style within a file (existing code mixes single/double).
- Keep simple helpers small and focused.
- Prefer explicit parentheses for line wrapping.
- Avoid inline comments unless clarifying tricky logic.

## Types and Data Structures
- Use type hints for public functions and dataclass fields.
- `dataclass` is preferred for simple data containers.
- Use `list[int]` / `list[list[int]]` (Python 3.12 style) consistently.
- Use `np.ndarray` for array-backed data in keypad classes.
- Return plain Python lists for JSON-friendly outputs.
- Use `Self` for fluent class constructors where appropriate.

## Naming Conventions
- `snake_case` for functions and variables.
- `PascalCase` for classes and dataclasses.
- Constants in `UPPER_SNAKE_CASE` when needed.
- Domain-specific short names (`k`, `p`) are accepted for keypad dimensions.
- Avoid one-letter names outside established domain usage.
- Use descriptive names for data frames, arrays, and iterators.

## Error Handling
- Validate inputs early and raise `ValueError` with clear messages.
- Use `assert` for internal invariants when appropriate.
- Avoid broad `except` blocks; catch specific exceptions.
- Prefer returning structured results over printing in library code.
- Bubble up exceptions from CLI only if they convey actionable context.
- Use `Exception` only when no narrower type fits.

## Randomness and Determinism
- Use `numpy.random.default_rng()` for new RNG usage.
- Avoid seeding in library code unless the API requests it.
- Keep randomness in `shuffle` operations encapsulated.
- Tests should avoid relying on random outcomes.
- If deterministic behavior is needed, inject a seed or RNG.

## Testing Patterns
- Use `pytest` fixtures or `@pytest.mark.parametrize` where helpful.
- Keep tests deterministic; avoid random seeds unless required.
- Print debugging output only when needed during development.
- Prefer checking shapes, invariants, and value ranges.
- Use small inputs for unit tests to keep runtime low.
- Avoid depending on `output/` artifacts in tests.

## Output and Artifacts
- Benchmarks write pickles and images under `output/`.
- Ensure directories are created with `mkdir(parents=True, exist_ok=True)`.
- Avoid committing generated artifacts or `__pycache__`.
- Use descriptive run names in output paths.
- Prefer `Path` joins over string concatenation.

## Performance and Safety
- Prefer numpy vectorized ops over Python loops when easy.
- Avoid unnecessary copies of `np.ndarray` unless mutating.
- Keep memory use predictable for large benchmarks.
- Avoid writing to disk in library code except when requested.
- Guard expensive operations behind CLI flags or explicit calls.

## Git Hygiene
- Do not commit artifacts under `output/`.
- Avoid adding `__pycache__` or local IDE settings.
- Keep diffs minimal and scoped to the request.
- Avoid reformatting unrelated files.
- Do not modify `environment.yaml` unless required.
- Document new scripts or commands only if requested.
- Use `git status` to double-check staged files.

## Documentation Notes
- README content is partially stale (mentions missing CLI module).
- Update README only if the user requests documentation edits.
- Keep docstrings concise and focused on behavior.
- Avoid adding new docs unless requested.

## Cursor / Copilot Rules
- No `.cursor/rules/`, `.cursorrules`, or `.github/copilot-instructions.md` found.
- If new rules are added, mirror them here.
