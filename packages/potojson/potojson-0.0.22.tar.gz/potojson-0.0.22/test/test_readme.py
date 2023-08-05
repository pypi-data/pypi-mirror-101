"""README tests for potojson."""

import os
import subprocess
import sys

import pytest


@pytest.mark.skipif(
    sys.version_info < (3, 9),
    reason=(
        "CLI usage in README follows convention of argparse HelpFormatter"
        " for Python >= 3.9"
    ),
)
def test_readme_cli_usage():
    """Tests if the content of the CLI usage (help printed) is the same as
    that shown in the README of the project inside the CLI section.
    """
    with open("README.md") as f:
        readme_content = f.read()

    _inside_cli_usage, _inside_cli_section = (False, False)
    readme_usage_lines = []
    for line in readme_content.splitlines():
        if _inside_cli_section:
            if _inside_cli_usage:
                if line == "```":
                    break
                readme_usage_lines.append(line)
            elif line == "```":
                _inside_cli_usage = True
        elif line == "### CLI":
            _inside_cli_section = True
    assert readme_usage_lines

    os.environ["COLUMNS"] = "999"
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "potojson",
            "-h",
        ],
        check=False,
        stdout=subprocess.PIPE,
    )
    os.environ["COLUMNS"] = ""

    output = (
        proc.stdout.decode("utf-8")
        .replace(
            "__main__.py",
            "potojson",
        )
        .splitlines()
    )
    assert output

    assert output == readme_usage_lines
