import csv
from io import StringIO

# Convert CSV string to Markdown table
def csv_to_markdown(csv_text):
    reader = csv.reader(StringIO(csv_text))
    rows = list(reader)
    col_widths = [max(len(cell) for cell in col) for col in zip(*rows)]

    def format_row(row):
        return "| " + " | ".join(cell.ljust(w) for cell, w in zip(row, col_widths)) + " |"

    header = format_row(rows[0])
    divider = "| " + " | ".join('-' * w for w in col_widths) + " |"
    body = "\n".join(format_row(row) for row in rows[1:])

    return f"{header}\n{divider}\n{body}"

# Convert Markdown table to CSV string
def markdown_to_csv(md_table):
    lines = [line.strip() for line in md_table.strip().split("\n") if line.startswith("|")]
    cleaned = [line.strip('|').split('|') for line in lines if '-' not in line]
    return "\n".join(",".join(cell.strip() for cell in row) for row in cleaned)

# Convert merged-cell table (with [^^^] and [>>>]) to Markdown
def merge_token_table_to_markdown(grid):
    markdown = []
    num_cols = max(len(row) for row in grid)

    def is_merge(cell): return cell in ["[^^^]", "[>>>]"]

    col_widths = [0] * num_cols
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if not is_merge(grid[r][c]):
                col_widths[c] = max(col_widths[c], len(grid[r][c]))

    def format_row(row):
        return "| " + " | ".join(
            ("" if is_merge(cell) else cell).ljust(col_widths[i])
            for i, cell in enumerate(row)
        ) + " |"

    markdown.append(format_row(grid[0]))
    markdown.append("| " + " | ".join("-" * w for w in col_widths) + " |")
    for row in grid[1:]:
        markdown.append(format_row(row))

    return "\n".join(markdown)


# File paths
csv_filename = "table.csv"
markdown_filename = "table.md"

# Example 1: CSV to Markdown and save
csv_content = """Name,Role,Team
Alice,Engineer,AI
John,Designer,UI
Bob,Security,Infra"""

# Save original CSV to file
with open(csv_filename, "w", newline='') as f:
    f.write(csv_content)

# Convert and save Markdown version
markdown_output = csv_to_markdown(csv_content)
with open(markdown_filename, "w") as f:
    f.write(markdown_output)

print("Converted CSV to Markdown:")
print(markdown_output)

# Example 2: Merge-cell table
merge_table = [
    ["Name", "Role", "Team"],
    ["Alice", "Engineer", "AI"],
    ["[^^^]", "Designer", "UI"],
    ["Bob", "[>>>]", "Security"]
]

merged_markdown = merge_token_table_to_markdown(merge_table)
print("\nMerge-Token Table in Markdown:")
print(merged_markdown)

csv_content = markdown_to_csv(merged_markdown)
print("\nCSV from Markdown ...")

# Save original CSV to file
with open(csv_filename, "w", newline='') as f:
    f.write(csv_content)

"""
Converted CSV to Markdown:
| Name  | Role     | Team  |
| ----- | -------- | ----- |
| Alice | Engineer | AI    |
| John  | Designer | UI    |
| Bob   | Security | Infra |

Merge-Token Table in Markdown:
| Name  | Role     | Team     |
| ----- | -------- | -------- |
| Alice | Engineer | AI       |
|       | Designer | UI       |
| Bob   |          | Security |

CSV from Markdown ...
"""