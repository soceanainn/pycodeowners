import pytest
from pycodeowners.__main__ import main


class TestOwners:
    def test_automatically_finds_and_logs_owners_from_default_location(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        assert main("owners") == 0

        capture_result = capsys.readouterr()
        assert not capture_result.err

        stdout = capture_result.out
        assert stdout == "soceanainn(username)\n"

    def test_parses_github_example(self, capsys: pytest.CaptureFixture) -> None:
        assert main("owners", "-f", "tests/codeowners_examples/github") == 0

        capture_result = capsys.readouterr()
        assert not capture_result.err

        stdout = capture_result.out
        for owner in {
            "global-owner1    (username)\n",
            "global-owner2    (username)\n",
            "js-owner         (username)\n",
            "docs@example.com (email)\n",
            "octo-org/octocats(team)\n",
            "doctocat         (username)\n",
            "octocat          (username)\n",
        }:
            assert owner in stdout

    def test_parses_gitlab_example(self, capsys: pytest.CaptureFixture) -> None:
        assert (
            main("owners", "-f", "tests/codeowners_examples/gitlab", "-t", "gitlab")
            == 0
        )

        capture_result = capsys.readouterr()
        assert not capture_result.err

        stdout = capture_result.out
        for owner in {
            "default-codeowner         (group_or_username)\n",
            "multiple                  (group_or_username)\n",
            "code                      (group_or_username)\n",
            "owners                    (group_or_username)\n",
            "ruby-owner                (group_or_username)\n",
            "owner-file-with-pound     (group_or_username)\n",
            "legal                     (group_or_username)\n",
            "janedoe@gitlab.com        (email)\n",
            "group                     (group_or_username)\n",
            "group/with-nested/subgroup(nested_group)\n",
            "all-docs                  (group_or_username)\n",
            "root-docs                 (group_or_username)\n",
            "lib-owner                 (group_or_username)\n",
            "config-owner              (group_or_username)\n",
            "space-owner               (group_or_username)\n",
            "docs                      (group_or_username)\n",
            "dev-team                  (group_or_username)\n",
            "docs-team                 (group_or_username)\n",
            "data-science-team         (group_or_username)\n",
        }:
            assert owner in stdout

    def test_parses_bitbucket_example(self, capsys: pytest.CaptureFixture) -> None:
        assert (
            main(
                "owners", "-f", "tests/codeowners_examples/bitbucket", "-t", "bitbucket"
            )
            == 0
        )

        capture_result = capsys.readouterr()
        assert not capture_result.err

        stdout = capture_result.out
        for owner in {
            "global-owner1@example.com   (email)\n",
            "global-owner2@example.com   (email)\n",
            "js-owner@example.com        (email)\n",
            "stevedriftexpert@example.com(email)\n",
            "workspace-slug/frontenders  (group)\n",
            "workspace-slug/py-owners    (group)\n",
        }:
            assert owner in stdout
