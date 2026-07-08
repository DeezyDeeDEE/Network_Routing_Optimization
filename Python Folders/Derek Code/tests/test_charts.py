import csv
import tempfile
import unittest
from pathlib import Path

from routing_project.charts import make_charts


class ChartTests(unittest.TestCase):
    def test_make_charts_writes_summary_markdown(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            csv_path = temp_path / "results.csv"
            with csv_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=["algorithm", "graph_id", "path_cost", "runtime_ms", "success"],
                    extrasaction="ignore",
                )
                writer.writeheader()
                writer.writerow(
                    {"algorithm": "dijkstra", "graph_id": "g1", "path_cost": 10, "runtime_ms": 1, "success": "True"}
                )
                writer.writerow(
                    {
                        "algorithm": "harmony_search",
                        "graph_id": "g1",
                        "path_cost": 12,
                        "runtime_ms": 3,
                        "success": "True",
                    }
                )

            outputs = make_charts(csv_path, temp_path / "charts")
            summary_path = temp_path / "charts" / "results_summary.md"

            self.assertIn(summary_path, outputs)
            self.assertIn("Experiment Results Summary", summary_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
