import tempfile
import unittest
from pathlib import Path

from routing_project.experiments import CSV_FIELDS, ExperimentConfig, run_experiment


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


if __name__ == "__main__":
    unittest.main()
