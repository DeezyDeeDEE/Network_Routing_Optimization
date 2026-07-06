"""Small dependency-free SVG chart generation for checkpoint results."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean


def make_charts(input_csv: Path, output_dir: Path) -> list[Path]:
    rows = _read_rows(input_csv)
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = [
        _bar_chart(
            _mean_by_algorithm(rows, "runtime_ms"),
            "Mean Runtime by Algorithm",
            "Runtime (ms)",
            output_dir / "runtime_by_algorithm.svg",
        ),
        _bar_chart(
            _mean_by_algorithm(rows, "path_cost"),
            "Mean Path Cost by Algorithm",
            "Path cost",
            output_dir / "path_cost_by_algorithm.svg",
        ),
    ]
    hs_error = _hs_error_by_graph(rows)
    if hs_error:
        outputs.append(_bar_chart(hs_error, "Harmony Search Error vs Dijkstra", "Cost difference", output_dir / "hs_error.svg"))
    return outputs


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _mean_by_algorithm(rows: list[dict[str, str]], field: str) -> dict[str, float]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        if row.get(field):
            grouped[row["algorithm"]].append(float(row[field]))
    return {algorithm: mean(values) for algorithm, values in grouped.items() if values}


def _hs_error_by_graph(rows: list[dict[str, str]]) -> dict[str, float]:
    dijkstra_cost: dict[str, float] = {}
    hs_costs: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        if not row.get("path_cost"):
            continue
        if row["algorithm"] == "dijkstra":
            dijkstra_cost.setdefault(row["graph_id"], float(row["path_cost"]))
        elif row["algorithm"] == "harmony_search":
            hs_costs[row["graph_id"]].append(float(row["path_cost"]))

    errors = []
    for graph_id, costs in hs_costs.items():
        if graph_id in dijkstra_cost:
            errors.append(mean(costs) - dijkstra_cost[graph_id])
    return {"HS mean error": mean(errors)} if errors else {}


def _bar_chart(values: dict[str, float], title: str, y_label: str, output_path: Path) -> Path:
    width, height = 760, 440
    margin_left, margin_bottom, margin_top, margin_right = 90, 80, 60, 40
    chart_width = width - margin_left - margin_right
    chart_height = height - margin_top - margin_bottom
    max_value = max(values.values(), default=1.0) or 1.0
    bar_gap = 24
    bar_width = max(28, (chart_width - bar_gap * (len(values) + 1)) / max(1, len(values)))
    palette = ["#2f6f8f", "#5b8f52", "#c57b32", "#7b5ea7", "#b84a62"]

    pieces = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="{width / 2}" y="32" text-anchor="middle" font-family="Arial" font-size="22" font-weight="700">{_escape(title)}</text>',
        f'<text x="24" y="{height / 2}" transform="rotate(-90 24 {height / 2})" text-anchor="middle" font-family="Arial" font-size="13">{_escape(y_label)}</text>',
        f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{height - margin_bottom}" stroke="#444"/>',
        f'<line x1="{margin_left}" y1="{height - margin_bottom}" x2="{width - margin_right}" y2="{height - margin_bottom}" stroke="#444"/>',
    ]

    for index, (label, value) in enumerate(values.items()):
        bar_height = (value / max_value) * chart_height
        x = margin_left + bar_gap + index * (bar_width + bar_gap)
        y = height - margin_bottom - bar_height
        color = palette[index % len(palette)]
        pieces.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" height="{bar_height:.1f}" fill="{color}"/>')
        pieces.append(f'<text x="{x + bar_width / 2:.1f}" y="{y - 8:.1f}" text-anchor="middle" font-family="Arial" font-size="12">{value:.2f}</text>')
        pieces.append(f'<text x="{x + bar_width / 2:.1f}" y="{height - margin_bottom + 22}" text-anchor="middle" font-family="Arial" font-size="12">{_escape(label)}</text>')

    pieces.append("</svg>")
    output_path.write_text("\n".join(pieces), encoding="utf-8")
    return output_path


def _escape(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
