import tempfile
import unittest
from pathlib import Path

from routing_project.experiments import (
    CSV_FIELDS,
    ExperimentConfig,
    format_result_summary,
    run_experiment,
    run_parameter_sweep,
)


class ExperimentTests(unittest.TestCase):
    def test_tiny_experiment_writes_csv(self):
        config = ExperimentConfig(
            node_counts=(8,),
            densities=("sparse",),
            graph_seeds=(5,),
            deterministic_repeats=1,
            harmony_trials=1,
            harmony_iterations=5,
            hms=4,
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "results.csv"
            rows = run_experiment(config, output)

            self.assertTrue(output.exists())
            self.assertEqual(len(rows), 4)
            header = output.read_text(encoding="utf-8").splitlines()[0].split(",")
            self.assertEqual(header, CSV_FIELDS)

    def test_parameter_sweep_can_run_at_small_scale(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "sweep.csv"
            rows = run_parameter_sweep(output, node_count=12, trials=1, iterations=2)

            self.assertTrue(output.exists())
            self.assertEqual(len(rows), 27)

    def test_result_summary_mentions_fastest_and_benchmark(self):
        rows = [
            {"algorithm": "dijkstra", "graph_id": "g1", "runtime_ms": 2.0, "path_cost": 10, "success": True},
            {"algorithm": "harmony_search", "graph_id": "g1", "runtime_ms": 5.0, "path_cost": 12, "success": True},
        ]

        summary = format_result_summary(rows)

        self.assertIn("Fastest average runtime: dijkstra", summary)
        self.assertIn("Dijkstra is the exact benchmark", summary)


if __name__ == "__main__":
    unittest.main()
