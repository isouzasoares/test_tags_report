import re

from copy import deepcopy
from pathlib import Path

PYRAMID_TESTS = ("ut", "it", "component")

class TestReport:

    def __init__(self, project_path, js=False, tags_for_diff=None):
        self.project_path = project_path
        self.tags_for_diff = tags_for_diff
        self.pyramide_tests = {}
        self.js = js
        self.function_name_pattern = r"test_\w+" if not js else r"test_\w+"
        self.function_pattern = r"def test_\w+" if not js else r" it\("
        self.tag_pattern = r"\# \#test_\w+::\w+" \
            if not js else r"(?:\s+ | *)/\/\ \#test_\w+::\w+"
        self.test_files = '**/test_*.py' if not js else '**/*.spec.ts'
        self.tests_paths = self.get_tests_files(self.project_path)
        [self.pyramide_tests.update({i: 0}) for i in PYRAMID_TESTS]

    def get_tests_files(self, project_path):
        project_path = Path(project_path)
        return project_path.glob(self.test_files)
    
    def tags_diff(self, tag_names):
        tags_names = set(tag_names)
        tags_diff = set(
            [i.replace("#", "").lstrip() for i in self.tags_for_diff])
        tags_not_found = tags_diff - tags_names
        new_tags_found = tags_names - tags_diff
        return {"tags_not_found": list(tags_not_found),
                "total_tags_not_found": len(tags_not_found),
                "total_csv_tags": len(self.tags_for_diff),
                "new_tags_found": new_tags_found,
                "total_new_tags_found": len(new_tags_found)}


    def get_tag_and_type(self, tag):
        tag_obj = {}
        name = type_tag = ""
        tag_name = tag.lstrip()
        tag = tag.split("::")

        if tag:
            name = re.findall(self.function_name_pattern, tag[0])
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

        find = re.findall(self.tag_pattern, text)
        return find

    def get_test_def(self, text):

        find = re.findall(self.function_pattern, text)
        return [i.replace("def ", "") for i in find]

    def get_report(self):

        tags_file = []
        all_tags = []
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
            tags_names = [
                    i.pop("original_name", "").replace("# #", "").\
                        replace("// #", "").lstrip()
                          for i in tags]
            all_tags += tags_names

            count_tags = self.count_tags_for_path(tags_names)
            tags_dict.update({"total_tags": len(tags),
                              "total_defs": len(find_def),
                              "path": path, "tags": tags,
                              "tag_names": list(set(tags_names)),
                              "def_names": find_def,
                              "count_tags": count_tags,
                              "filename": test.name,
                              "filepath": str(test.parent)})
            tags_file.append(tags_dict)

        report = self.consolidate_data(tags_file)
        report.update(self.tags_diff(all_tags))
        report["frontend"] = True if self.js else False
        return {"details_paths": tags_file, "report": report}
