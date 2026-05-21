---
name: weekly-commit-report
description: Generate a weekly work summary from Git commits across one or many local repositories. Use when the user asks to summarize weekly work, create a week report, compile tasks from commits, review commits across all repos, or produce a status update based on Git history.
---

# Weekly Commit Report

## Workflow

Use this skill to turn local Git history into a concise weekly work report.

1. Determine the reporting window.
   - If the user says "this week", use the current local timezone and start from Monday 00:00 through now.
   - If the user gives dates, use those exact dates and state them in the final report.
   - If the user asks for "last week", use the previous Monday through Sunday.

2. Determine repository scope.
   - If the current directory is one repo among many sibling repos, scan the parent directory with `--root .. --max-depth 2`.
   - If the current directory is a monorepo, scan the current directory with `--root . --max-depth 4`.
   - Do not include generated or dependency folders unless the user explicitly asks.

3. Determine author filtering.
   - Prefer filtering to the user's Git identities when the report is "my weekly work".
   - Use known local identities from recent commits if the user does not provide an author.
   - Exclude automated checkpoint commits such as `VS Code <vscode@users.noreply.github.com>` unless the user asks for all commits.

4. Collect commits with the bundled script:

```bash
python3 skills/weekly-commit-report/scripts/collect_weekly_commits.py \
  --root .. \
  --max-depth 2 \
  --since "2026-05-18 00:00:00" \
  --until "2026-05-21 23:59:59" \
  --author "chuongpdh|hoangchuongk10@gmail.com|chuongpdh@nandh.vn" \
  --format markdown
```

5. Convert commit messages into a report.
   - Group by business outcome first, then repo.
   - Merge duplicate or repeated commit subjects into one work item.
   - Keep merge commits only when they represent shipped or reviewed work.
   - Mention repository counts as supporting detail, not the main story.
   - If the raw commit messages are vague, state the likely scope conservatively.

## Output Style

Write in the user's language. For Vietnamese reports, prefer:

- `Tổng Hợp Tuần`
- `Theo Repo`
- `Ghi chú`

Include:

- Exact date range.
- Number of scanned repos and repos with matching commits.
- Total unique commits.
- Grouped work summary.
- Any caveats, such as duplicated branch commits, merge-only evidence, or excluded automation commits.

Avoid dumping the full commit log unless the user asks for raw details.

## Script

Use `scripts/collect_weekly_commits.py` to discover local Git repos and print commits as `markdown`, `tsv`, or `json`. Read the script only if the default options do not cover the request.
