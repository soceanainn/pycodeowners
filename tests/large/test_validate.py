import pytest

from pycodeowners.__main__ import main


class TestValidate:
    def test_validates_codeowners_in_default_location(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        assert main("validate", "--verbose") == 0

        capture_result = capsys.readouterr()
        assert not capture_result.err

        stdout = capture_result.out
        assert stdout.endswith("/.github/CODEOWNERS is valid\n")

    def test_logs_nothing_in_non_verbose_mode(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        assert main("validate") == 0

        capture_result = capsys.readouterr()
        assert not capture_result.err
        assert not capture_result.out

    def test_parses_github_example(self, capsys: pytest.CaptureFixture) -> None:
        assert main("validate", "-f", "tests/codeowners_examples/github", "-v") == 0

        capture_result = capsys.readouterr()
        assert not capture_result.err

        stdout = capture_result.out
        assert stdout == "tests/codeowners_examples/github is valid\n"

    def test_parses_gitlab_example(self, capsys: pytest.CaptureFixture) -> None:
        assert (
            main(
                "validate",
                "-f",
                "tests/codeowners_examples/gitlab",
                "-t",
                "gitlab",
                "-v",
            )
            == 0
        )

        capture_result = capsys.readouterr()
        assert not capture_result.err

        stdout = capture_result.out
        assert stdout == "tests/codeowners_examples/gitlab is valid\n"

    def test_parses_bitbucket_example(self, capsys: pytest.CaptureFixture) -> None:
        assert (
            main(
                "validate",
                "-f",
                "tests/codeowners_examples/bitbucket",
                "-t",
                "bitbucket",
                "-v",
            )
            == 0
        )

        capture_result = capsys.readouterr()
        assert not capture_result.err

        stdout = capture_result.out
        assert stdout == "tests/codeowners_examples/bitbucket is valid\n"
