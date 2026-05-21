#!/usr/bin/env python3
"""Collect Git commits across local repositories for weekly reports."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable


FIELD_SEP = "\x1f"


def run_command(cmd: list[str], cwd: Path | None = None) -> str | None:
    try:
        result = subprocess.run(
            cmd,
            check=False,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None

    if result.returncode != 0:
        return None

    value = result.stdout.strip()
    return value or None


def week_bounds(now: datetime, offset_weeks: int = 0) -> tuple[str, str]:
    monday = now - timedelta(days=now.weekday())
    start = monday.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(
        weeks=offset_weeks
    )
    if offset_weeks == 0:
        end = now
    else:
        end = start + timedelta(days=6, hours=23, minutes=59, seconds=59)
    return start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S")


def find_git_repos(root: Path, max_depth: int) -> list[Path]:
    root = root.resolve()
    repos: list[Path] = []

    for current, dirnames, _ in os.walk(root):
        current_path = Path(current)
        rel = current_path.relative_to(root)
        depth = 0 if str(rel) == "." else len(rel.parts)

        if ".git" in dirnames:
            repos.append(current_path)
            dirnames[:] = []
            continue

        if depth >= max_depth:
            dirnames[:] = []
            continue

        dirnames[:] = [
            name
            for name in dirnames
            if name
            not in {
                ".cache",
                ".next",
                ".venv",
                "dist",
                "node_modules",
                "venv",
            }
        ]

    return sorted(repos, key=lambda path: path.name)


def run_git_log(repo: Path, since: str, until: str, include_merges: bool) -> list[dict]:
    pretty = f"%H{FIELD_SEP}%h{FIELD_SEP}%ad{FIELD_SEP}%an <%ae>{FIELD_SEP}%s"
    cmd = [
        "git",
        "-C",
        str(repo),
        "log",
        "--all",
        f"--since={since}",
        f"--until={until}",
        "--date=short",
        f"--pretty=format:{pretty}",
    ]
    if not include_merges:
        cmd.insert(5, "--no-merges")

    try:
        result = subprocess.run(
            cmd,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        print(f"warning: failed to run git in {repo}: {exc}", file=sys.stderr)
        return []

    if result.returncode != 0:
        print(
            f"warning: skipped {repo}: {result.stderr.strip()}",
            file=sys.stderr,
        )
        return []

    commits = []
    for line in result.stdout.splitlines():
        parts = line.split(FIELD_SEP, 4)
        if len(parts) != 5:
            continue
        full_hash, short_hash, date, author, subject = parts
        commits.append(
            {
                "repo": repo.name,
                "repo_path": str(repo),
                "hash": full_hash,
                "short_hash": short_hash,
                "date": date,
                "author": author,
                "subject": subject,
            }
        )
    return commits


def collect_git_config_identities(root: Path) -> list[str]:
    identities: list[str] = []
    for scope in ([], ["--global"]):
        for key in ("user.name", "user.email"):
            value = run_command(["git", "config", *scope, "--get", key], cwd=root)
            if value:
                identities.append(value)
    return identities


def collect_github_identities() -> list[str]:
    if not shutil.which("gh"):
        return []

    identities: list[str] = []
    login = run_command(["gh", "api", "user", "--jq", ".login"])
    if login:
        identities.append(login)

    public_email = run_command(["gh", "api", "user", "--jq", ".email"])
    if public_email and public_email != "null":
        identities.append(public_email)

    emails = run_command(["gh", "api", "user/emails", "--jq", ".[].email"])
    if emails:
        identities.extend(line for line in emails.splitlines() if line)

    return identities


def unique_values(values: Iterable[str]) -> list[str]:
    seen = set()
    unique = []
    for value in values:
        normalized = value.strip()
        if not normalized:
            continue
        key = normalized.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(normalized)
    return unique


def detect_author_patterns(root: Path) -> list[str]:
    identities = unique_values(
        [
            *collect_git_config_identities(Path.cwd()),
            *collect_git_config_identities(root),
            *collect_github_identities(),
        ]
    )
    return [re.escape(identity) for identity in identities]


def compile_patterns(values: Iterable[str]) -> list[re.Pattern[str]]:
    return [re.compile(value, re.IGNORECASE) for value in values if value]


def matches_any(value: str, patterns: list[re.Pattern[str]]) -> bool:
    return any(pattern.search(value) for pattern in patterns)


def filter_commits(
    commits: list[dict],
    author_patterns: list[re.Pattern[str]],
    exclude_author_patterns: list[re.Pattern[str]],
    exclude_subject_patterns: list[re.Pattern[str]],
) -> list[dict]:
    filtered = []
    seen: set[tuple[str, str]] = set()

    for commit in commits:
        key = (commit["repo"], commit["hash"])
        if key in seen:
            continue
        seen.add(key)

        if author_patterns and not matches_any(commit["author"], author_patterns):
            continue
        if exclude_author_patterns and matches_any(
            commit["author"], exclude_author_patterns
        ):
            continue
        if exclude_subject_patterns and matches_any(
            commit["subject"], exclude_subject_patterns
        ):
            continue

        filtered.append(commit)

    return sorted(
        filtered,
        key=lambda item: (item["date"], item["repo"], item["subject"], item["hash"]),
        reverse=True,
    )


def print_markdown(commits: list[dict], scanned: int, since: str, until: str) -> None:
    by_repo: dict[str, list[dict]] = defaultdict(list)
    for commit in commits:
        by_repo[commit["repo"]].append(commit)

    print(f"# Weekly Commit Report ({since} - {until})")
    print()
    print(f"- Scanned repos: {scanned}")
    print(f"- Repos with matching commits: {len(by_repo)}")
    print(f"- Unique commits: {len(commits)}")
    print()

    for repo in sorted(by_repo):
        repo_commits = by_repo[repo]
        print(f"## {repo} ({len(repo_commits)})")
        for commit in repo_commits:
            print(
                f"- {commit['date']} `{commit['short_hash']}` "
                f"{commit['author']}: {commit['subject']}"
            )
        print()


def print_tsv(commits: list[dict]) -> None:
    for commit in commits:
        print(
            "\t".join(
                [
                    commit["repo"],
                    commit["date"],
                    commit["short_hash"],
                    commit["author"],
                    commit["subject"],
                ]
            )
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect commits from multiple local Git repos for a weekly report."
    )
    parser.add_argument("--root", default="..", help="Directory to scan for Git repos.")
    parser.add_argument(
        "--max-depth",
        type=int,
        default=2,
        help="Maximum directory depth while discovering Git repos.",
    )
    parser.add_argument("--since", help="Start datetime passed to git log.")
    parser.add_argument("--until", help="End datetime passed to git log.")
    parser.add_argument(
        "--last-week",
        action="store_true",
        help="Use the previous Monday through Sunday as the reporting window.",
    )
    parser.add_argument(
        "--author",
        action="append",
        default=[],
        help="Regex for authors to include. Repeat for multiple filters.",
    )
    parser.add_argument(
        "--all-authors",
        action="store_true",
        help="Do not auto-filter to the local Git/GitHub user.",
    )
    parser.add_argument(
        "--exclude-author",
        action="append",
        default=["vscode@users.noreply.github.com"],
        help="Regex for authors to exclude.",
    )
    parser.add_argument(
        "--exclude-subject",
        action="append",
        default=["checkpoint turn"],
        help="Regex for commit subjects to exclude.",
    )
    parser.add_argument(
        "--no-merges",
        action="store_true",
        help="Exclude merge commits from git log.",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "tsv", "json"],
        default="markdown",
        help="Output format.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    now = datetime.now()
    default_since, default_until = week_bounds(now, -1 if args.last_week else 0)
    since = args.since or default_since
    until = args.until or default_until
    root = Path(args.root)
    author_patterns = args.author
    if not author_patterns and not args.all_authors:
        author_patterns = detect_author_patterns(root)

    repos = find_git_repos(root, args.max_depth)
    commits = []
    for repo in repos:
        commits.extend(run_git_log(repo, since, until, include_merges=not args.no_merges))

    filtered = filter_commits(
        commits,
        compile_patterns(author_patterns),
        compile_patterns(args.exclude_author),
        compile_patterns(args.exclude_subject),
    )

    if args.format == "json":
        print(
            json.dumps(
                {
                    "since": since,
                    "until": until,
                    "scanned_repos": len(repos),
                    "matching_repos": len({commit["repo"] for commit in filtered}),
                    "unique_commits": len(filtered),
                    "author_filters": author_patterns,
                    "commits": filtered,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    elif args.format == "tsv":
        print_tsv(filtered)
    else:
        print_markdown(filtered, len(repos), since, until)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
