import json
import click

from report.test_report import TestReport
from report.html import generate_report_html


@click.command()
@click.option('-p', '--project_path', help='The project path of tests',
              required=True)
@click.option('-f', '--format', default="html", help='The format of output')
def report_tag(**kwargs):
    """Execute the report for files."""

    test_obj = TestReport(kwargs["project_path"])
    test_tags = test_obj.get_report()

    if kwargs["format"] == "json":
        with open("report.json", "w") as report:
            report.write(json.dumps(test_tags))
    else:
        generate_report_html(**test_tags)

    click.echo("Generate report with success")

if __name__ == '__main__':
    report_tag()
