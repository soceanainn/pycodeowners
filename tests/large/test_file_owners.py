import re

import pytest

from pycodeowners.__main__ import main


class TestFileOwners:
    def test_works_for_this_repo(self, capsys: pytest.CaptureFixture) -> None:
        assert main("files") == 0

        capture_result = capsys.readouterr()
        assert not capture_result.err

        stdout = capture_result.out

        assert re.compile("tests/large/test_file_owners\\.py\\s*@soceanainn\\n").search(stdout) is not None
        assert re.compile("\\.github/CODEOWNERS\\s*@soceanainn\\n").search(stdout) is not None
        assert re.compile("pycodeowners/__main__\\.py\\s*@soceanainn\\n").search(stdout) is not None

    def test_works_with_multiple_path_filters(self, capsys: pytest.CaptureFixture) -> None:
        assert main("files", ".github", "tests/large/test_file_owners.py") == 0

        capture_result = capsys.readouterr()
        assert not capture_result.err

        stdout = capture_result.out
        assert re.compile("tests/large/test_file_owners\\.py\\s*@soceanainn\\n").search(stdout) is not None
        assert re.compile("\\.github/CODEOWNERS\\s*@soceanainn\\n").search(stdout) is not None

        assert re.compile("pycodeowners/__main__\\.py\\s*@soceanainn\\n").search(stdout) is None

    def test_works_with_single_path_filter(self, capsys: pytest.CaptureFixture) -> None:
        assert main("files", "tests/") == 0

        capture_result = capsys.readouterr()
        assert not capture_result.err

        stdout = capture_result.out
        assert re.compile("tests/large/test_file_owners\\.py\\s*@soceanainn\\n").search(stdout) is not None

        assert re.compile("\\.github/CODEOWNERS\\s*@soceanainn\\n").search(stdout) is None
        assert re.compile("pycodeowners/__main__\\.py\\s*@soceanainn\\n").search(stdout) is None
