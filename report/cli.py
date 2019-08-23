import json
import click

from report.tags_report import TagsReport
from report.html import generate_report_html
from report.csv import read_csv_column


@click.command()
@click.option(
    "-p",
    "--project_path",
    help="The project path where containing the tests",
    required=True,
)
@click.option(
    "-f",
    "--format",
    default="html",
    help="The format of output (.json or .html, .html is default)",
)
@click.option(
    "-ts",
    "--ts",
    default=False,
    help="If placed the command will validate the tag in \n \
              files extensions .spec.ts else validate in test_*.py",
    is_flag=True,
)
@click.option(
    "-c",
    "--csv",
    help="The csv with tags column for the comparator")
@click.option(
    "-cc",
    "--csv_column",
    help="The tags column name in the csv")
def report_tag(**kwargs):
    """Search tags in the tests code and generate reports."""
    csv_tags = []

    if kwargs["csv"] is not None:
        if kwargs["csv_column"] is not None:
            try:
                with open(kwargs["csv"], "r") as csv:

                    csv_tags = read_csv_column(csv, kwargs["csv_column"],
                                               kwargs["ts"])
            except:
                raise click.ClickException("Error on read csv")

    test_obj = TagsReport(kwargs["project_path"], kwargs["ts"], csv_tags)
    test_tags = test_obj.get_report()

    if not test_tags["details_paths"]:
        raise click.ClickException("Tests files not found")

    if kwargs["format"] == "json":
        with open("report.json", "w") as report:
            report.write(json.dumps(test_tags))
    else:
        generate_report_html(**test_tags)

    click.echo("Successfully generated report")


if __name__ == "__main__": # pragma: no cover
    report_tag()
