"""Command-line entry points for experiments and chart generation."""

from __future__ import annotations

import argparse
from pathlib import Path

from routing_project.charts import make_charts
from routing_project.experiments import (
    CHECKPOINT_CONFIG,
    SMALL_CONFIG,
    format_result_summary,
    run_experiment,
    run_parameter_sweep,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "results" / "raw"
CHART_DIR = PROJECT_ROOT / "results" / "charts"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CSC 2400 routing project tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    small = subparsers.add_parser("run-small", help="Run a quick checkpoint-sized experiment.")
    small.add_argument("--output", type=Path, default=RAW_DIR / "small_experiment.csv")

    checkpoint = subparsers.add_parser("run-checkpoint", help="Run the larger checkpoint grid.")
    checkpoint.add_argument("--output", type=Path, default=RAW_DIR / "checkpoint_experiment.csv")

    sweep = subparsers.add_parser("run-sweep", help="Run the Harmony Search parameter sweep.")
    sweep.add_argument("--output", type=Path, default=RAW_DIR / "harmony_parameter_sweep.csv")
    sweep.add_argument("--nodes", type=int, default=500, help="Number of graph nodes for the sweep.")
    sweep.add_argument("--trials", type=int, default=3, help="Trials per parameter combination.")
    sweep.add_argument("--iterations", type=int, default=100, help="Harmony Search iterations per trial.")

    charts = subparsers.add_parser("make-charts", help="Create SVG charts from a CSV result file.")
    charts.add_argument("--input", type=Path, default=RAW_DIR / "small_experiment.csv")
    charts.add_argument("--output-dir", type=Path, default=CHART_DIR)

    args = parser.parse_args(argv)

    if args.command == "run-small":
        rows = run_experiment(SMALL_CONFIG, args.output)
        print(f"Wrote {len(rows)} rows to {args.output}")
        print(format_result_summary(rows))
    elif args.command == "run-checkpoint":
        rows = run_experiment(CHECKPOINT_CONFIG, args.output)
        print(f"Wrote {len(rows)} rows to {args.output}")
        print(format_result_summary(rows))
    elif args.command == "run-sweep":
        rows = run_parameter_sweep(
            args.output,
            node_count=args.nodes,
            trials=args.trials,
            iterations=args.iterations,
            progress=True,
        )
        print(f"Wrote {len(rows)} rows to {args.output}")
        print(format_result_summary(rows))
    elif args.command == "make-charts":
        outputs = make_charts(args.input, args.output_dir)
        for output in outputs:
            print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
