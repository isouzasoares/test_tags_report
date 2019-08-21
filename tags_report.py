import json
import click

from report.test_report import TestReport
from report.html import generate_report_html
from report.csv import read_csv_column


@click.command()
@click.option("-p", "--project_path", help="The project path of tests",
              required=True)
@click.option("-f", "--format", default="html", help="The format of output")
@click.option("-js", "--js", default=False, help="The js report", is_flag=True)
@click.option("-c", "--csv", help="The csv with tags to the comparator")
@click.option("-cc", "--csv_column", help="The csv tags column name")
def report_tag(**kwargs):
    """Execute the report for files."""
    csv_tags = []

    if kwargs["csv"] is not None:
        if kwargs["csv_column"] is not None:
            with open(kwargs["csv"], "r") as csv:
                csv_tags = read_csv_column(csv, kwargs["csv_column"],
                                           kwargs["js"])

    test_obj = TestReport(kwargs["project_path"], kwargs["js"], csv_tags)
    test_tags = test_obj.get_report()
    
    if kwargs["format"] == "json":
        with open("report.json", "w") as report:
            report.write(json.dumps(test_tags))
    else:
        generate_report_html(**test_tags)

    click.echo("Generate report with success")

if __name__ == '__main__':
    report_tag()
