import re
import json
import click

from copy import deepcopy
from pathlib import Path

from report.html import generate_report_html

PYRAMID_TESTS = ("ut", "it")


class TestReport:

    def __init__(self, project_path):
        self.project_path = project_path
        self.tests_paths = self.get_tests_files(self.project_path)
        self.pyramide_tests = {}
        [self.pyramide_tests.update({i: 0}) for i in PYRAMID_TESTS]

    def get_tests_files(self, project_path):
        project_path = Path(project_path)
        return project_path.glob('**/test_*.py')

    def get_tag_and_type(self, tag):
        tag_obj = {}
        name = type_tag = ""
        tag_name = tag
        tag = tag.split("::")

        if tag:
            pattern = r"test_\w+"
            name = re.findall(pattern, tag[0])
            name = name[0] if name else ""

            if len(tag) >= 2:
                type_tag = tag[1]

        tag_obj["original_name"] = tag_name
        tag_obj["name"] = name
        tag_obj["type"] = type_tag
        return tag_obj

    def count_tags_for_path(self, tag_names):
        count = {}
        for tag in tag_names:
            if not count.get(tag, None):
                count[tag] = 0
            count[tag] += 1

        return [{"name": key, "count": value} for key, value in count.items()]

    def consolidate_data(self, path_data):

        total_tags = total_defs = 0
        count_type = deepcopy(self.pyramide_tests)

        for report in path_data:
            total_tags += report["total_tags"]
            total_defs += report["total_defs"]
            for key in count_type.keys():
                count_type[key] += report[key]

        report = {"total_tags": total_tags, "total_defs": total_defs}
        report["count_for_type"] = [list(i) for i in count_type.items()]
        return report

    def get_test_tags(self, text):

        pattern = r"\# \#test_\w+::\w{2}"
        find = re.findall(pattern, text)
        return find

    def get_test_def(self, text):

        pattern = r"def test_\w+"
        find = re.findall(pattern, text)
        return [i.replace("def ", "") for i in find]

    def get_report(self):

        tags_file = []
        for test in self.tests_paths:
            tags = []
            tags_dict = deepcopy(self.pyramide_tests)
            test_text = test.read_text()
            find = self.get_test_tags(test_text)
            path = str(test)
            find_def = self.get_test_def(test_text)

            for tag in find:
                tag_search = self.get_tag_and_type(tag)

                for tag_type in tags_dict.keys():
                    if tag_search["type"] == tag_type:
                        tags_dict[tag_type] += 1
                        break

                tags.append(tag_search)
            tags_names = [i.pop("original_name", "").replace("# #", "")
                          for i in tags]
            count_tags = self.count_tags_for_path(tags_names)
            tags_dict.update({"total_tags": len(tags),
                              "total_defs": len(find_def),
                              "path": path, "tags": tags,
                              "tag_names": set(tags_names),
                              "def_names": find_def,
                              "count_tags": count_tags,
                              "filename": test.name,
                              "filepath": str(test.parent)})
            tags_file.append(tags_dict)

        report = self.consolidate_data(tags_file)

        return {"details_paths": tags_file, "report": report}


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
