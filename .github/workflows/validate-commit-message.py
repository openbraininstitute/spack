#!/usr/bin/env python

# requires: gitpython

import fileinput
import json
import logging
import os
import textwrap
from argparse import ArgumentParser

from git import Repo

EXISTING_PACKAGES = []

logger = logging.getLogger(__name__)
sh = logging.StreamHandler()
fmt = logging.Formatter("%(asctime)s %(message)s")
sh.setFormatter(fmt)
sh.setLevel(logging.DEBUG)
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)


def get_changed_tags(changed_files: list[str]) -> set[str]:
    """
    Return all packages changed by the commit
    """

    changed_packages = []
    changed_package_paths = [path for path in changed_files if "/packages/" in path]
    logger.debug("Changed package paths: %s", changed_package_paths)
    for package_path in changed_package_paths:
        path_components = package_path.split("/")
        changed_packages.append(path_components[path_components.index("packages") + 1])

    logger.debug("Changed packages: %s", changed_packages)

    if any("documentation" in changed_file for changed_file in changed_files):
        changed_packages.append("docs")
    if any(
        changed_file.endswith("yml")
        or changed_file.endswith("yaml")
        and "github" not in changed_file
        for changed_file in changed_files
    ):
        changed_packages.append("deploy")
    if any("github" in changed_file for changed_file in changed_files):
        changed_packages.append("ci")
    return set(changed_packages)


def collect_prefixes(message: str) -> set[str]:
    """
    Collect all prefixes in the commit message
    """
    prefixes = []

    for line in message.splitlines():
        if ":" in line:
            prefix = message.split(":")[0]
            prefix_items = [item.strip() for item in prefix.split(",")]
            prefixes.extend(prefix_items)

    logger.debug("Prefixes: %s", prefixes)
    return set(prefixes)


def suggested_solution(tags: list[str], inline: bool) -> str:
    if len(tags) > 5:
        return ""

    if inline:
        return f"""\
#### Suggested solution:
```
{', '.join(tags)}: <description (optional)>
```
"""

    ss = "\n".join(f"{item}: <description (optional)>" for item in tags)
    return f"""\
#### Suggested solution:
```
{', '.join(tags)}: <description (optional)>
```

or

```
{ss}
```
"""


def process_title(message: str, changed_tags: set[str]) -> str:
    prefixes = collect_prefixes(message)
    if prefixes & changed_tags:
        return ""

    tags = list(changed_tags)

    return f"""\
## PR title issues

None of the modified packages or code regions: `{', '.join(tags)}` were mentioned. Please,
mention at least one of them.

#### Tips:

It is suggested to mention the most important package(s) and describe why the change is necessary.

#### Example:

```
package1, package2, package3: <description (optional)>
```
{suggested_solution(tags, True)}
"""


def process_commit_message(message: str, changed_tags: set[str]) -> str:
    prefixes = collect_prefixes(message)
    if prefixes & changed_tags:
        return ""

    tags = list(changed_tags)

    return f"""\
## Commit Message issues

None of the modified packages or code regions: `{', '.join(tags)}` were mentioned in the commit:

```
{message}
```

Please, mention at least one of them.

#### Tips:

It is suggested to mention the most important package(s) and describe why the change is necessary.

#### Example:

```
package1, package2, package3: <description (optional)>
```

or:

```
package1: <description (optional)>
package2: <description (optional)>
package3: <description (optional)>
```
{suggested_solution(tags, False)}
"""


def main(title: str, changed_files: list[str], commits: int) -> None:
    logger.info(
        "Setting fail state to make sure we catch any script failures- we'll clean up at the end"
    )
    with open(os.environ["GITHUB_OUTPUT"], "a") as fp:
        fp.write("script-failure=true\n")
    repo = Repo(".")

    logger.debug("Title: %s", title)
    logger.debug("Changed files: %s", changed_files)

    message_issues = ""
    commit_issue = None
    title_issue = None
    changed_tags = get_changed_tags(changed_files)

    if commits > 1:
        title_issue = process_title(title, changed_tags)
    else:
        title_issue = process_title(title, changed_tags)

        commit = next(repo.iter_commits())
        logger.info(f"Checking commit: {commit.message} (parents: {commit.parents})")

        commit_issue = process_commit_message(commit.message, changed_tags)

    if title_issue:
        message_issues += title_issue

    if commit_issue:
        message_issues += commit_issue

    if len(message_issues):
        with open("message_issues.txt", "w") as fp:
            fp.write(textwrap.dedent(message_issues))
        with open(os.environ["GITHUB_OUTPUT"], "a") as fp:
            fp.write("faulty-commits=true")

    with fileinput.FileInput(os.environ["GITHUB_OUTPUT"], inplace=True) as file:
        for line in file:
            print(line.replace("script-failure=true", "script-failure=false"))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--title", required=True, help="PR title")
    parser.add_argument(
        "--changed-files", required=True, help="JSON formatted list of files changed in PR"
    )

    parser.add_argument("--commits", required=True, help="Number of commits in the PR")

    args = parser.parse_args()

    for spack_repo in [
        "./var/spack/repos/builder.test",
        "./var/spack/repos/builtin",
        "./var/spack/repos/builtin.mock",
        "./var/spack/repos/tutorial",
        "./bluebrain/repo-bluebrain",
        "./bluebrain/repo-patches",
    ]:
        try:
            EXISTING_PACKAGES.extend(next(os.walk(f"{spack_repo}/packages"))[1])
        except StopIteration:
            logger.critical(f"No packages under {spack_repo}")
            pass

    main(args.title, json.loads(args.changed_files), int(args.commits))
