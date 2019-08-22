
from tags_report.report.csv import read_csv_column

def test_csv_column_tag():
    with open("tests/examples/csv/tags.csv", "r") as csv:
        tags = read_csv_column(csv, "tags")
        assert tags == ["#tag_1:ut", "#tag_2:it"]

def test_csv_column_tag_backend():
    with open("tests/examples/csv/tags_front_back.csv", "r") as csv:
        tags = read_csv_column(csv, "tags")
        assert tags == ["#tag_2:it"]

def test_csv_column_tag_front():
    with open("tests/examples/csv/tags_front_back.csv", "r") as csv:
        tags = read_csv_column(csv, "tags", js=True)
        assert tags == ["#tag_1:ut"]

#def test_csv_column_tag_not_tag():
#    with open("tests/examples/csv/tags.csv", "r") as csv:
#        tags = read_csv_column(csv, "a")
#        assert tags == []