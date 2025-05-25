import csv
import html
import re

def markdown_to_html_link(text):
    # Convert Markdown links to HTML <a> tags
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    return link_pattern.sub(r'<a href="\2">\1</a>', text)

def csv_to_html(csv_filename, html_filename):
    with open(csv_filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #990000;
            color: white;
        }
        p {
            font-size: 16px;
            margin-bottom: 10px;
        }
    </style>
    <title>Draft Timetable</title>
</head>
<body>
    <p>The following is the draft timetable:</p>
    <table>
        <thead>
            <tr>
"""
        
        for column in header:
            html_content += f"                <th>{html.escape(column)}</th>\n"
        html_content += "            </tr>\n        </thead>\n        <tbody>\n"
        
        for row in reader:
            html_content += "            <tr>\n"
            for column in row:
                html_content += f"                <td>{markdown_to_html_link(html.escape(column))}</td>\n"
            html_content += "            </tr>\n"
        
        html_content += """
        </tbody>
    </table>
</body>
</html>
"""
    
    with open(html_filename, 'w') as htmlfile:
        htmlfile.write(html_content)


# [Example usage]
# Save the CSV content to a file
csv_content = """No,Date,Subject,Lab
1,17 Jan 2020,Quantum Mechanics,Lab [Link](https://ursa.com/lab01.pdf) Demo [Link](https://www.youtube.com/watch?v=Lm9SZf2XFCc)
2,24 Jan 2020,Classical Mechanics,Lab [Link](https://ursa.com/lab02.pdf) Demo [Link](https://www.youtube.com/watch?v=83QCm3LkuEg)
3,31 Jan 2020,Thermodynamics,Lab [Link](https://ursa.com/lab03.pdf)
4,7 Feb 2020,Electromagnetism,Lab [Link](https://ursa.com/lab04.pdf)
5,14 Feb 2020,Statistical Mechanics,Lab [Link](https://ursa.com/lab05.pdf)
6,21 Feb 2020,Guest lecture,Mini-project/Coursework [Link](https://ursa.com/mini_project.pdf)
7,28 Feb 2020,Optics,Lab [Link](https://ursa.com/lab06.pdf)
8,6 Mar 2020,Special Relativity,Lab [Link](https://ursa.com/lab07.pdf)
9,13 Mar 2020,Test 1 (Units 1-5),[Link](https://ursa.com/test01.pdf)
10,20 Mar 2020,General Relativity,Lab [Link](https://ursa.com/lab08.pdf)
11,27 Mar 2020,Particle Physics,Lab [Link](https://ursa.com/lab09.pdf)
12,3 April 2020,Nuclear Physics,Lab [Link](https://ursa.com/lab10.pdf)
13,10 April 2020,Condensed Matter Physics,
14,Week beginning 27 April 2020,Easter Break,
15,Week beginning 4 May 2020 (TBC),Coursework Hand-in [Link](https://ursa.com/coursework.pdf),
"""
with open(dir_start + 'timetable.csv', 'w') as f:
    f.write(csv_content)

dir_start = './sample_data/'
csv_to_html(dir_start + 'timetable.csv', dir_start + 'timetable.html')
