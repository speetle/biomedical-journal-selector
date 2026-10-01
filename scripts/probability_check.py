#!/usr/bin/env python3
"""Check coherence of three-stage journal acceptance probability ranges."""

import argparse
import sys


def probability_range(values: list[float], label: str) -> tuple[float, float]:
    low, high = values
    if not (0 <= low <= high <= 100):
        raise ValueError(f"{label} must satisfy 0 <= LOW <= HIGH <= 100")
    return low, high


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--screen", nargs=2, type=float, required=True, metavar=("LOW", "HIGH"))
    parser.add_argument("--review", nargs=2, type=float, required=True, metavar=("LOW", "HIGH"))
    parser.add_argument("--overall", nargs=2, type=float, required=True, metavar=("LOW", "HIGH"))
    parser.add_argument("--tolerance", type=float, default=3.0, help="Allowed percentage-point deviation")
    args = parser.parse_args()

    try:
        screen = probability_range(args.screen, "screen")
        review = probability_range(args.review, "review")
        overall = probability_range(args.overall, "overall")
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    expected = (screen[0] * review[0] / 100, screen[1] * review[1] / 100)
    coherent = (
        abs(overall[0] - expected[0]) <= args.tolerance
        and abs(overall[1] - expected[1]) <= args.tolerance
        and overall[1] <= screen[1] + args.tolerance
    )
    print(f"Expected overall range: {expected[0]:.1f}%–{expected[1]:.1f}%")
    print(f"Reported overall range: {overall[0]:.1f}%–{overall[1]:.1f}%")
    print("Result: coherent" if coherent else "Result: review required")
    return 0 if coherent else 1


if __name__ == "__main__":
    raise SystemExit(main())

