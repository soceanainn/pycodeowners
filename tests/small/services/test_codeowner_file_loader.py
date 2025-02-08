from pycodeowners._pycodeowners.models.file_type import FileType
from pycodeowners._pycodeowners.models.owner import (
    Owner,
    GithubOwnerType,
    BitbucketOwnerType,
    BitbucketOwner,
    GitlabOwnerType,
)
from pycodeowners._pycodeowners.models.pattern import Pattern
from pycodeowners._pycodeowners.models.rule import Rule
from pycodeowners._pycodeowners.models.section import Section
from pycodeowners._pycodeowners.services.codeowner_file_loader import (
    CodeownerFileLoader,
)


class TestLoad:
    def test_loads_github_style_files(self) -> None:
        ruleset = CodeownerFileLoader.load(
            ("tests/codeowners_examples/github", FileType.Github)
        )
        rules = ruleset.rules
        sections = ruleset.sections

        assert len(rules) == 14
        assert len(sections) == 0

        assert rules[0] == Rule(
            line_number=8,
            pattern=Pattern("*"),
            owners=[
                Owner(
                    owner_type=GithubOwnerType.USERNAME,
                    value="@global-owner1",
                    parsed_value="global-owner1",
                ),
                Owner(
                    owner_type=GithubOwnerType.USERNAME,
                    value="@global-owner2",
                    parsed_value="global-owner2",
                ),
            ],
        )

        assert rules[1] == Rule(
            line_number=14,
            pattern=Pattern("*.js"),
            owners=[
                Owner(
                    owner_type=GithubOwnerType.USERNAME,
                    value="@js-owner",
                    parsed_value="js-owner",
                ),
            ],
            comment="#This is an inline comment.",
        )

        assert rules[2] == Rule(
            line_number=19,
            pattern=Pattern("*.go"),
            owners=[
                Owner(
                    owner_type=GithubOwnerType.EMAIL,
                    value="docs@example.com",
                    parsed_value="docs@example.com",
                ),
            ],
        )
        assert rules[3] == Rule(
            line_number=25,
            pattern=Pattern("*.txt"),
            owners=[
                Owner(
                    owner_type=GithubOwnerType.TEAM,
                    value="@octo-org/octocats",
                    parsed_value="octo-org/octocats",
                ),
            ],
        )
        assert rules[4] == Rule(
            line_number=30,
            pattern=Pattern("/build/logs/"),
            owners=[
                Owner(
                    owner_type=GithubOwnerType.USERNAME,
                    value="@doctocat",
                    parsed_value="doctocat",
                ),
            ],
        )
        assert rules[5] == Rule(
            line_number=35,
            pattern=Pattern("docs/*"),
            owners=[
                Owner(
                    owner_type=GithubOwnerType.EMAIL,
                    value="docs@example.com",
                    parsed_value="docs@example.com",
                ),
            ],
        )
        assert rules[6] == Rule(
            line_number=39,
            pattern=Pattern("apps/"),
            owners=[
                Owner(
                    owner_type=GithubOwnerType.USERNAME,
                    value="@octocat",
                    parsed_value="octocat",
                ),
            ],
        )
        assert rules[7] == Rule(
            line_number=44,
            pattern=Pattern("/docs/"),
            owners=[
                Owner(
                    owner_type=GithubOwnerType.USERNAME,
                    value="@doctocat",
                    parsed_value="doctocat",
                ),
            ],
        )
        assert rules[8] == Rule(
            line_number=48,
            pattern=Pattern("/scripts/"),
            owners=[
                Owner(
                    owner_type=GithubOwnerType.USERNAME,
                    value="@doctocat",
                    parsed_value="doctocat",
                ),
                Owner(
                    owner_type=GithubOwnerType.USERNAME,
                    value="@octocat",
                    parsed_value="octocat",
                ),
            ],
        )
        assert rules[9] == Rule(
            line_number=53,
            pattern=Pattern("**/logs"),
            owners=[
                Owner(
                    owner_type=GithubOwnerType.USERNAME,
                    value="@octocat",
                    parsed_value="octocat",
                ),
            ],
        )
        assert rules[10] == Rule(
            line_number=60,
            pattern=Pattern("/apps/"),
            owners=[
                Owner(
                    owner_type=GithubOwnerType.USERNAME,
                    value="@octocat",
                    parsed_value="octocat",
                ),
            ],
        )
        assert rules[11] == Rule(
            line_number=61,
            pattern=Pattern("/apps/github"),
        )
        assert rules[12] == Rule(
            line_number=66,
            pattern=Pattern("/apps/"),
            owners=[
                Owner(
                    owner_type=GithubOwnerType.USERNAME,
                    value="@octocat",
                    parsed_value="octocat",
                )
            ],
        )
        assert rules[13] == Rule(
            line_number=67,
            pattern=Pattern("/apps/github"),
            owners=[
                Owner(
                    owner_type=GithubOwnerType.USERNAME,
                    value="@doctocat",
                    parsed_value="doctocat",
                )
            ],
        )

    def test_loads_gitlab_style_files(self) -> None:
        ruleset = CodeownerFileLoader.load(
            ("tests/codeowners_examples/gitlab", FileType.Gitlab)
        )
        rules = ruleset.rules
        sections = ruleset.sections

        assert len(rules) == 12
        assert len(sections) == 2

        assert rules[0] == Rule(
            line_number=5,
            pattern=Pattern("*"),
            owners=[
                Owner(
                    owner_type=GitlabOwnerType.GROUP_OR_USERNAME,
                    value="@default-codeowner",
                    parsed_value="default-codeowner",
                )
            ],
        )
        assert rules[1] == Rule(
            line_number=8,
            pattern=Pattern("*"),
            owners=[
                Owner(
                    owner_type=GitlabOwnerType.GROUP_OR_USERNAME,
                    value="@multiple",
                    parsed_value="multiple",
                ),
                Owner(
                    owner_type=GitlabOwnerType.GROUP_OR_USERNAME,
                    value="@code",
                    parsed_value="code",
                ),
                Owner(
                    owner_type=GitlabOwnerType.GROUP_OR_USERNAME,
                    value="@owners",
                    parsed_value="owners",
                ),
            ],
        )
        assert rules[2] == Rule(
            line_number=12,
            pattern=Pattern("*.rb"),
            owners=[
                Owner(
                    owner_type=GitlabOwnerType.GROUP_OR_USERNAME,
                    value="@ruby-owner",
                    parsed_value="ruby-owner",
                )
            ],
        )
        assert rules[3] == Rule(
            line_number=15,
            pattern=Pattern("\\#file_with_pound.rb"),
            owners=[
                Owner(
                    owner_type=GitlabOwnerType.GROUP_OR_USERNAME,
                    value="@owner-file-with-pound",
                    parsed_value="owner-file-with-pound",
                )
            ],
        )
        assert rules[4] == Rule(
            line_number=18,
            pattern=Pattern("LICENSE"),
            owners=[
                Owner(
                    owner_type=GitlabOwnerType.GROUP_OR_USERNAME,
                    value="@legal",
                    parsed_value="legal",
                ),
                Owner(
                    owner_type=GitlabOwnerType.EMAIL,
                    value="janedoe@gitlab.com",
                    parsed_value="janedoe@gitlab.com",
                ),
            ],
        )
        assert rules[5] == Rule(
            line_number=21,
            pattern=Pattern("README"),
            owners=[
                Owner(
                    owner_type=GitlabOwnerType.GROUP_OR_USERNAME,
                    value="@group",
                    parsed_value="group",
                ),
                Owner(
                    owner_type=GitlabOwnerType.NESTED_GROUP,
                    value="@group/with-nested/subgroup",
                    parsed_value="group/with-nested/subgroup",
                ),
            ],
        )
        assert rules[6] == Rule(
            line_number=24,
            pattern=Pattern("/docs/"),
            owners=[
                Owner(
                    owner_type=GitlabOwnerType.GROUP_OR_USERNAME,
                    value="@all-docs",
                    parsed_value="all-docs",
                ),
            ],
        )
        assert rules[7] == Rule(
            line_number=25,
            pattern=Pattern("/docs/*"),
            owners=[
                Owner(
                    owner_type=GitlabOwnerType.GROUP_OR_USERNAME,
                    value="@root-docs",
                    parsed_value="root-docs",
                ),
            ],
        )
        assert rules[8] == Rule(
            line_number=26,
            pattern=Pattern("/docs/**/*.md"),
            owners=[
                Owner(
                    owner_type=GitlabOwnerType.GROUP_OR_USERNAME,
                    value="@root-docs",
                    parsed_value="root-docs",
                ),
            ],
        )
        assert rules[9] == Rule(
            line_number=29,
            pattern=Pattern("lib/"),
            owners=[
                Owner(
                    owner_type=GitlabOwnerType.GROUP_OR_USERNAME,
                    value="@lib-owner",
                    parsed_value="lib-owner",
                ),
            ],
        )
        assert rules[10] == Rule(
            line_number=32,
            pattern=Pattern("/config/"),
            owners=[
                Owner(
                    owner_type=GitlabOwnerType.GROUP_OR_USERNAME,
                    value="@config-owner",
                    parsed_value="config-owner",
                ),
            ],
        )
        assert rules[11] == Rule(
            line_number=35,
            pattern=Pattern("path\\ with\\ spaces/"),
            owners=[
                Owner(
                    owner_type=GitlabOwnerType.GROUP_OR_USERNAME,
                    value="@space-owner",
                    parsed_value="space-owner",
                ),
            ],
        )

        assert sections["documentation"] == Section(
            line_number=38,
            name="Documentation",
            rules=[
                Rule(
                    line_number=39,
                    pattern=Pattern("ee/docs"),
                    owners=[
                        Owner(
                            owner_type=GitlabOwnerType.GROUP_OR_USERNAME,
                            value="@docs",
                            parsed_value="docs",
                        ),
                    ],
                ),
                Rule(
                    line_number=40,
                    pattern=Pattern("docs"),
                    owners=[
                        Owner(
                            owner_type=GitlabOwnerType.GROUP_OR_USERNAME,
                            value="@docs",
                            parsed_value="docs",
                        ),
                    ],
                ),
                Rule(
                    line_number=49,
                    pattern=Pattern("README.md"),
                    owners=[
                        Owner(
                            owner_type=GitlabOwnerType.GROUP_OR_USERNAME,
                            value="@docs",
                            parsed_value="docs",
                        ),
                    ],
                ),
            ],
        )

        assert sections["development"] == Section(
            line_number=42,
            name="Development",
            default_owners=[
                Owner(
                    owner_type=GitlabOwnerType.GROUP_OR_USERNAME,
                    value="@dev-team",
                    parsed_value="dev-team",
                ),
            ],
            rules=[
                Rule(
                    line_number=43,
                    pattern=Pattern("*"),
                    owners=[
                        Owner(
                            owner_type=GitlabOwnerType.GROUP_OR_USERNAME,
                            value="@dev-team",
                            parsed_value="dev-team",
                        ),
                    ],
                ),
                Rule(
                    line_number=44,
                    pattern=Pattern("README.md"),
                    owners=[
                        Owner(
                            owner_type=GitlabOwnerType.GROUP_OR_USERNAME,
                            value="@docs-team",
                            parsed_value="docs-team",
                        ),
                    ],
                ),
                Rule(
                    line_number=45,
                    pattern=Pattern("data-models/"),
                    owners=[
                        Owner(
                            owner_type=GitlabOwnerType.GROUP_OR_USERNAME,
                            value="@data-science-team",
                            parsed_value="data-science-team",
                        ),
                    ],
                ),
            ],
        )

    def test_loads_bitbucket_style_files(self) -> None:
        ruleset = CodeownerFileLoader.load(
            ("tests/codeowners_examples/bitbucket", FileType.BitBucket)
        )
        rules = ruleset.rules
        sections = ruleset.sections

        assert len(rules) == 9
        assert len(sections) == 0

        assert rules[0] == Rule(
            line_number=14,
            pattern=Pattern("*"),
            owners=[
                Owner(
                    owner_type=BitbucketOwnerType.EMAIL,
                    value="global-owner1@example.com",
                    parsed_value="global-owner1@example.com",
                ),
                Owner(
                    owner_type=BitbucketOwnerType.EMAIL,
                    value="global-owner2@example.com",
                    parsed_value="global-owner2@example.com",
                ),
            ],
        )
        assert rules[1] == Rule(
            line_number=21,
            pattern=Pattern("*.js"),
            owners=[
                Owner(
                    owner_type=BitbucketOwnerType.EMAIL,
                    value="js-owner@example.com",
                    parsed_value="js-owner@example.com",
                )
            ],
            comment="# This is an inline comment.",
        )
        assert rules[2] == Rule(
            line_number=28,
            pattern=Pattern("/src/pullrequests/drift.js"),
            owners=[
                Owner(
                    owner_type=BitbucketOwnerType.EMAIL,
                    value="stevedriftexpert@example.com",
                    parsed_value="stevedriftexpert@example.com",
                )
            ],
        )
        assert rules[3] == Rule(
            line_number=34,
            pattern=Pattern("*.js"),
            owners=[
                BitbucketOwner(
                    owner_type=BitbucketOwnerType.GROUP,
                    value="@workspace-slug/frontenders",
                    parsed_value="workspace-slug/frontenders",
                )
            ],
        )
        assert rules[4] == Rule(
            line_number=49,
            pattern=Pattern("*.py"),
            owners=[
                BitbucketOwner(
                    owner_type=BitbucketOwnerType.GROUP,
                    value="@workspace-slug/py-owners:random",
                    parsed_value="workspace-slug/py-owners",
                    selection_strategy="random",
                )
            ],
            comment="# same as random(1)",
        )
        assert rules[5] == Rule(
            line_number=50,
            pattern=Pattern("*.py"),
            owners=[
                BitbucketOwner(
                    owner_type=BitbucketOwnerType.GROUP,
                    value="@workspace-slug/py-owners:random(3)",
                    parsed_value="workspace-slug/py-owners",
                    selection_strategy="random(3)",
                )
            ],
            comment="# 3 random users",
        )
        assert rules[6] == Rule(
            line_number=55,
            pattern=Pattern("*.py"),
            owners=[
                BitbucketOwner(
                    owner_type=BitbucketOwnerType.GROUP,
                    value="@workspace-slug/py-owners:least_busy",
                    parsed_value="workspace-slug/py-owners",
                    selection_strategy="least_busy",
                )
            ],
            comment="# Same as least_busy(1)",
        )
        assert rules[7] == Rule(
            line_number=56,
            pattern=Pattern("*.py"),
            owners=[
                BitbucketOwner(
                    owner_type=BitbucketOwnerType.GROUP,
                    value="@workspace-slug/py-owners:least_busy(3)",
                    parsed_value="workspace-slug/py-owners",
                    selection_strategy="least_busy(3)",
                )
            ],
            comment="# least-busy 3 people",
        )
        assert rules[8] == Rule(
            line_number=60,
            pattern=Pattern("*.py"),
            owners=[
                BitbucketOwner(
                    owner_type=BitbucketOwnerType.GROUP,
                    value="@workspace-slug/py-owners:all",
                    parsed_value="workspace-slug/py-owners",
                    selection_strategy="all",
                )
            ],
        )
