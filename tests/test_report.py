from pytest import fixture

from pathlib import Path

from tags_report.report.tags_report import TagsReport

DETAIL_PATH_BACKEND = [{
    "total_tags": 2,
    "total_defs": 2,
    "component": 0,
    "ut": 1,
    "it": 1,
    "path": "tests/examples/",
    "tags": ["# #test_example_1::ut",
                "# #test_example_1_2::it"],
    "tag_names": ["test_example_1::ut",
                    "test_example_1_2::it"],
    "def_names": ["test_example_1",
                  "test_example_1_2"],
    "count_tags": [{'count': 1, 'name': 'test_example_1::ut'},
                   {'count': 1, 'name': 'test_example_1_2::it'}],
    "filename": "test_example.py",
    "filepath": "tests/examples/"},

    {"total_tags": 2,
    "total_defs": 2,
    "component": 0,
    "ut": 1,
    "it": 1,
    "path": "tests/examples/",
    "tags": ["# #test_example_2::it",
            "# #test_example_2_2::it"],
    "tag_names": ["test_example_2::it",
                "test_example_2_2::it"],
    "def_names": ["test_example_2",
                  "test_example_2_2"],
    "count_tags": [{'count': 1, 'name': 'test_example_2::ut'},
                   {'count': 1, 'name': 'test_example_2_2::it'}],
    "filename": "test_example_1.py",
    "filepath": "tests/examples/"}]


@fixture(autouse=True)
def backend_instance():
    test_report = TagsReport("tests/examples/")
    return test_report

@fixture(autouse=True)
def frontend_instance():
    test_report = TagsReport("tests/examples/", True)
    return test_report

def test_type_regex_backend(backend_instance):
    assert backend_instance.function_pattern == r"def test_\w+"
    assert backend_instance.tag_pattern == r"\# \#test_\w+::\w+"
    assert backend_instance.test_files == "**/test_*.py"
    assert len(list(backend_instance.tests_paths)) == 2

def test_type_regex_frontend(frontend_instance):
    assert frontend_instance.function_pattern == r" it\("
    assert frontend_instance.tag_pattern == r"(?:\s+ | *)/\/\ \#test_\w+::\w+"
    assert frontend_instance.test_files == "**/*.spec.ts"
    assert len(list(frontend_instance.tests_paths)) == 1

def test_tag_and_type_backend(backend_instance):
    mock = {"original_name": "# #test_get_user_info_with_access::ut",
            "name": "test_get_user_info_with_access",
            "type": "ut"}
    tag = backend_instance.get_tag_and_type(
        "# #test_get_user_info_with_access::ut")
    assert tag == mock

def test_tag_and_type_frontend(frontend_instance):
    mock = {"original_name": "/ #test_get_user_info_with_access::ut",
            "name": "test_get_user_info_with_access",
            "type": "ut"}
    tag = frontend_instance.get_tag_and_type(
        "/ #test_get_user_info_with_access::ut")
    assert tag == mock

def test_count_tags_path(backend_instance):
    tags = ["test_get_user_info_with_access",
            "test_get_user_info_with_access",
            "test_get_user_info_with_accesss"]
    mock = [{"name": "test_get_user_info_with_access", "count": 2},
             {"name": "test_get_user_info_with_accesss", "count": 1}]
    assert backend_instance.count_tags_for_path(tags) == mock

def test_consolidate_data(backend_instance):
    path_data = [
        {"total_defs": 3, "total_tags": 6, "ut": 1, "it": 2,
         "component": 0},
        {"total_defs": 4, "total_tags": 1, "ut": 0, "it": 3,
        "component": 2}]
    mock = {"total_tags": 7, "total_defs": 7,
            "count_for_type": [["ut", 1], ["it", 5], ["component", 2]]}
    assert backend_instance.consolidate_data(path_data) == mock

def test_get_test_tag_backend(backend_instance):
    text = """# #test_example_2::ut
              def test_example_2"""
    mock = ["# #test_example_2::ut"]
    assert backend_instance.get_test_tags(text) == mock

def test_get_test_tag_frontend(frontend_instance):
    text = """// #test_validate_answered_questions::ut
              it('should save answers successfully', () => {});"""
    mock = ["// #test_validate_answered_questions::ut"]
    assert frontend_instance.get_test_tags(text) == mock

def test_get_test_def_backend(backend_instance):
    text = """# #test_example_2::ut
              def test_example_2"""
    mock = ["test_example_2"]
    assert backend_instance.get_test_def(text) == mock

def test_get_report_backend(backend_instance):
    report_mock = {}
    report = backend_instance.get_report()
    assert len(report["details_paths"]) == 2

def test_get_report_frontend(frontend_instance):
    report = frontend_instance.get_report()
    assert len(report["details_paths"]) == 1