"""
Exporta metricas de CI/CD en formato Prometheus.
"""

from argparse import ArgumentParser
from pathlib import Path
from xml.etree import ElementTree


def parse_coverage_percent(path):
    root = ElementTree.parse(path).getroot()
    line_rate = float(root.attrib.get("line-rate", 0))
    return round(line_rate * 100, 2)


def metric_line(name, value, labels=None):
    labels = labels or {}
    label_text = ",".join(
        f'{key}="{label_value}"' for key, label_value in labels.items() if label_value
    )
    if label_text:
        return f"{name}{{{label_text}}} {value}"
    return f"{name} {value}"


def main():
    parser = ArgumentParser()
    parser.add_argument("--coverage", type=Path)
    parser.add_argument("--deploy-duration", type=float)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--branch", default="")
    parser.add_argument("--commit", default="")
    args = parser.parse_args()

    labels = {
        "branch": args.branch.replace("/", "_"),
        "commit": args.commit[:12],
    }

    lines = []

    if args.coverage:
        coverage = parse_coverage_percent(args.coverage)
        lines.extend([
            "# TYPE devops_ev1_ci_test_coverage_percent gauge",
            metric_line("devops_ev1_ci_test_coverage_percent", coverage, labels),
        ])

    if args.deploy_duration is not None:
        lines.extend([
            "# TYPE devops_ev1_ci_deploy_duration_seconds gauge",
            metric_line("devops_ev1_ci_deploy_duration_seconds", args.deploy_duration, labels),
        ])

    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
