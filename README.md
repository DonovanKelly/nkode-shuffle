# Evilnkode Project

This README provides instructions for setting up and running the `evilnkode` project using Conda, activating the environment, and executing the provided CLI scripts. It also covers how to access help for command-line options.

## Prerequisites

- **Conda**: Ensure you have Conda installed (Miniconda or Anaconda). Download from [conda.io](https://conda.io).

## Setting Up the Environment

To set up the project environment using the provided `environment.yaml` file, follow these steps:

1. **Install the environment**:
   - Ensure you are in the project root directory where `environment.yaml` is located.
   - Run the following command to create the `evilnkode` environment:
     ```bash
     conda env create -f environment.yaml
     ```
   - This will install all dependencies specified in `environment.yaml`.

## Activating the Environment

To activate the `evilnkode` environment, run:

```bash
conda activate evilnkode
```

Once activated, your terminal prompt should change to include `(evilnkode)`, indicating the environment is active.

## Running CLI Scripts

The project includes two main CLI scripts: `cli.visualnkode` and `cli.benchmark_histogram`. Below are instructions to run each.

### Running `cli.visualnkode`

To execute the `visualnkode` CLI script:

```bash
python -m cli.visualnkode
```

- This command runs the `visualnkode` module from the `cli` package.
- To view available options and arguments, use the `-help` flag:
  ```bash
  python -m cli.visualnkode -help
  ```

### Running `cli.benchmark_histogram`

To execute the `benchmark_histogram` CLI script:

```bash
python -m cli.benchmark_histogram
```

- This command runs the `benchmark_histogram` module, which may generate output such as benchmark results or histograms. For example, it might produce output like:
  ```
  File exists: output/slidingtowershufflekeypad-6-8-4-5-4-4-10000/benchmark/slidingtowershufflekeypad-6-8-4-5-4-4-10000.pkl
  Bench SlidingTowerShuffle Break 5
  Bench SlidingTowerShuffle Replay 5
  ```
- To view available options and arguments, use the `-help` flag:
  ```bash
  python -m cli.benchmark_histogram -help
  ```

## Using the `-help` Flag

Both CLI scripts (`cli.visualnkode` and `cli.benchmark_histogram`) support a `-help` flag to display available command-line options and their descriptions. Run the following to explore options for each script:

```bash
python -m cli.visualnkode -help
python -m cli.benchmark_histogram -help
```

This will provide detailed information about parameters, flags, and usage for each script.

## Project Structure

Key files and directories in the project:

- `environment.yaml`: Conda environment configuration file.
- `cli/`: Contains CLI scripts (`visualnkode` and `benchmark_histogram`).
- `output/`: Directory where script outputs, such as benchmark results, are stored.
- `src/`: Source code for the project.
- `tests/`: Test scripts for the project.
- `requirements.txt`: Additional dependencies (if needed outside Conda).

For further details, explore the project documentation in the `docs/` directory.
