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
csv_filename = "data.csv"
markdown_filename = "./sample_data/data.txt"

# Read CSV to file
with open(csv_filename, "r", newline='') as f:
    f.seek(0)  # Reset file pointer to the beginning
    csv_content = f.read()

markdown_output = csv_to_markdown(csv_content)

# Write Markdown to file
with open(markdown_filename, "w") as f:
    f.write(markdown_output)

print("Converted CSV to Markdown:")
print(markdown_output)

"""
Converted CSV to Markdown:
| **Attributes**         | **Goals**                                                   | **Signals**                                               | **Metrics**                                   |  |
| ---------------------- | ----------------------------------------------------------- | --------------------------------------------------------- | --------------------------------------------- |  |
| **Excitement**         | Generate positive energy and engagement                     | Activity and energy . High user enthusiasm, viral sharing | Frequency and intensity of activities         |  |
| **Adoption**           | Smooth onboarding<br>Low cognitive load                     | Re-use and re-adaptation<br>Low friction usage            | Number of sessions<br>Feature re-use          |  |
| **Retention**          | Users return regularly and stick over time                  | Continued engagement over days/weeks/months               | Retention rate (7-day, 30-day, etc.)          |  |
| **Task Effectiveness** | Users complete tasks with minimal effort and error          | Low error rate<br>Smooth flow                             | Duration<br>Completion rate                   |  |
| **Clarity**            | Users understand what to do and why it matters              | Low need for support<br>Correct self-navigation           | Fewer support tickets<br>Fewer drop-offs      |  |
| **Trust**              | Users feel safe, respected, and informed                    | Transparent communication<br>Positive sentiment           | Trust score (survey)<br>Fewer opt-outs        |  |
| **Delight**            | Users experience moments of joy or surprise                 | Positive emotional responses<br>Spontaneous praise        | NPS (Net Promoter Score)<br>User quotes       |  |
| **Efficiency**         | Users accomplish goals faster and easier over time          | Task automation<br>Learning curve flattening              | Average time to complete<br>Error reduction   |  |
| **Accessibility**      | Inclusive use by people with diverse abilities and contexts | Compatibility with screen readers, input methods, etc.    | WCAG compliance<br>Accessibility audit scores |  |
| **Scalability**        | System grows with usage without degrading experience        | Consistent performance under load                         | Uptime<br>Latency under high load             |  |
| **Consistency**        | Interface and interaction behave the same across flows      | Predictable outcomes<br>No surprises                      | Usability test scores<br>User confidence      |  |

"""