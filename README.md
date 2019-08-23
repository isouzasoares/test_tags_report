# Tests tags report


[![Build Status](https://travis-ci.org/isouzasoares/test_tags_report.svg?branch=master)](https://travis-ci.org/isouzasoares/test_tags_report)

### Requirements
- Python 3+

### Installing
Install and update using pip:

```sh
pip install git+https://github.com/isouzasoares/test_tags_report.git
```

# Tests


### Usage
Accessing the help:
```sh
$ tagsreport --help
Usage: tagsreport [OPTIONS]

  Search tags in the tests code and generate reports.

Options:
  -p, --project_path TEXT  The project path where containing the tests
                           [required]
  -f, --format TEXT        The format of output (.json or .html, .html is
                           default)
  -ts, --ts                If placed the command will validate the tag in
                           files extensions .spec.ts else validate in
                           test_*.py
  -c, --csv TEXT           The csv with tags column for the comparator
  -cc, --csv_column TEXT   The tags column name in the csv
  --help                   Show this message and exit.
```

Usage example:
```sh
$ tagsreport -p test/
Successfully generated report
$ ls
report_backend.html
```

Usage example with csv comparator:
```sh
$ tagsreport -p test/ -c ../../Downloads/test.csv  -cc 'Tags_names'
Successfully generated report

```









