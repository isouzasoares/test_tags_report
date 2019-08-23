from click.testing import CliRunner

from report.cli import report_tag


def test_success_command_backend():
    runner = CliRunner()
    result = runner.invoke(report_tag, ["-p", "tests/examples/"])
    assert result.exit_code == 0
    assert result.output == 'Successfully generated report\n'


def test_success_command_frontend():
    runner = CliRunner()
    result = runner.invoke(report_tag, ["-p", "tests/examples/",
                                        "-ts"])
    assert result.exit_code == 0
    assert result.output == 'Successfully generated report\n'


def test_success_command_json():
    runner = CliRunner()
    result = runner.invoke(report_tag, ["-p", "tests/examples/",
                                        "-f", "json"])
    assert result.exit_code == 0
    assert result.output == 'Successfully generated report\n'


def test_success_command_csv():
    runner = CliRunner()
    result = runner.invoke(report_tag, ["-p", "tests/examples/",
                                        "-c", "tests/examples/csv/tags.csv",
                                        "-cc", "tags"])
    assert result.exit_code == 0
    assert result.output == 'Successfully generated report\n'


def test_error_command_csv_col():
    runner = CliRunner()

    result = runner.invoke(report_tag, ["-p", "tests/examples/",
                                        "-c", "tests/examples/csv/tags.csv",
                                        "-cc", "aa"])
    assert result.exit_code != 0
    assert result.output == "Error: Error on read csv\n"


def test_error_command_csv_read():
    runner = CliRunner()

    result = runner.invoke(report_tag, ["-p", "tests/examples/",
                                        "-c", "tests/examples/csv/tags",
                                        "-cc", "tags"])
    assert result.exit_code != 0
    assert result.output == "Error: Error on read csv\n"


def test_error_command_test_read():
    runner = CliRunner()

    result = runner.invoke(report_tag, ["-p", "file/"])
    assert result.exit_code != 0
    assert result.output == "Error: Tests files not found\n"
