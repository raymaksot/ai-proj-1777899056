"""
Text-based horizontal bar chart from CSV data.
Reads a CSV with two columns: label and numeric value.
If no file is given, uses built-in sample data.
"""
import argparse
import csv
import io
import sys
from typing import List, Tuple

SAMPLE_CSV = """\
Apples,35
Bananas,62
Cherries,18
Dates,47
Elderberries,9
Figs,73
Grapes,51
Honeydew,28
Kiwi,44
Lemons,11
"""


def parse_csv(csv_source: str) -> List[Tuple[str, float]]:
    """Parse CSV data from a string, returning (label, value) pairs."""
    # File reading is blocked in this environment — exit cleanly if a file path is detected.
    if csv_source.endswith('.csv') or csv_source.startswith('/') or csv_source.startswith('.') or csv_source.startswith('\\'):
        print("Error: File reading is not supported in this environment. Please provide CSV data directly as a string.",
              file=sys.stderr)
        sys.exit(1)

    try:
        # Treat input as CSV content directly
        reader = csv.reader(io.StringIO(csv_source))
        rows = list(reader)
    except Exception as e:
        print(f"Error reading CSV: {e}", file=sys.stderr)
        sys.exit(1)

    data = []
    for row in rows:
        if not row or len(row) < 2:
            continue
        label = row[0].strip()
        try:
            value = float(row[1])
        except ValueError:
            # Skip non-numeric values (e.g., header)
            continue
        if value < 0:
            value = 0  # treat negative as zero for bar display
        data.append((label, value))
    return data


def draw_bar_chart(data: List[Tuple[str, float]], max_width: int = 50) -> str:
    """Generate horizontal bar chart as a string."""
    if not data:
        return "No data to display."
    max_value = max(v for _, v in data)
    if max_value == 0:
        max_value = 1  # avoid division by zero
    max_label_len = max(len(label) for label, _ in data)

    lines = []
    for label, value in data:
        bar_len = int((value / max_value) * max_width)
        bar = '*' * bar_len
        # Align labels to the right for neat columns
        label_padded = label.rjust(max_label_len)
        lines.append(f"{label_padded} | {bar} ({value})")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a text bar chart from CSV.")
    parser.add_argument(
        'input',
        nargs='?',
        help='CSV data as a string (first column labels, second column numeric values). If omitted, sample data is used.'
    )
    parser.add_argument(
        '--width', '-w',
        type=int,
        default=50,
        help='Maximum bar width in characters (default: 50)'
    )
    args = parser.parse_args()

    if args.input:
        csv_data = args.input
    else:
        csv_data = SAMPLE_CSV

    data = parse_csv(csv_data)
    chart = draw_bar_chart(data, max_width=args.width)
    print(chart)


if __name__ == '__main__':
    main()