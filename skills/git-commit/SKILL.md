---
name: commit
description: Commit staged or unstaged changes with an AI-generated commit message in Conventional Commits format (`type: summary`). Use when the user asks to "commit", "commit changes", "create a commit", "save my work", or "check in code".
---

# Commit Changes

Help the user commit code changes with a well-crafted commit message that follows the Conventional Commits specification.

## Commit Message Format

All commit messages **must** follow this format:

```text
<type>: <summary>
```

Where:

- `type` is one of:
  - `feat` — New feature
  - `fix` — Bug fix
  - `refactor` — Code refactoring without behavior changes
  - `perf` — Performance improvement
  - `docs` — Documentation only
  - `test` — Add or update tests
  - `style` — Formatting or code style changes only
  - `build` — Build system or dependency changes
  - `ci` — CI/CD changes
  - `chore` — Maintenance, tooling, dependency updates, miscellaneous work
  - `revert` — Revert a previous commit

The summary must:

- Be written in English.
- Be concise (maximum 72 characters).
- Describe the intent of the change.
- Use the imperative mood.
- Not end with a period.
- Not include file names unless necessary.
- Not include emojis.

Examples:

```text
feat: add inventory transfer validation
fix: handle empty barcode input
refactor: simplify order synchronization flow
perf: optimize product cache lookup
docs: update deployment guide
test: add unit tests for shipment service
build: upgrade Go to 1.25
ci: improve GitHub Actions caching
chore: remove unused dependencies
```

For non-trivial changes, include an optional commit body explaining **why** the change was made rather than listing modified files.

If an issue or ticket number appears in the current branch name or user context, include it following the repository's existing convention.

---

# Guidelines

- **Never amend existing commits** without asking.
- **Never force-push or push** without explicit user approval.
- **Never skip pre-commit hooks** (do not use `--no-verify`).
- **Never skip signing commits** (do not use `--no-gpg-sign`).
- **Never revert, reset, or discard user changes** unless explicitly requested.
- Check for obvious secrets, credentials, generated artifacts, or large binaries that should not be committed. If anything looks suspicious, ask the user before committing.
- If there is any ambiguity about staging, ask the user.

---

# Workflow

## 1. Check repository status

Run:

```bash
git status --short
```

Behavior:

- If there are **no changes**, inform the user and stop.
- If there are **staged changes**, commit only those changes.
- If there are **only unstaged changes**, stage everything:

```bash
git add -A
```

---

## 2. Review the changes

Generate the commit from the staged changes only.

Run:

```bash
git diff --cached --stat
git diff --cached
```

Carefully understand the intent of the change before generating the commit message.

Do **not** simply describe the files that changed.

---

## 3. Generate the commit message

Generate a commit message using the Conventional Commits format:

```text
<type>: <summary>
```

Select the most appropriate type.

If the change is significant, include an optional body explaining:

- Why the change was needed.
- What problem it solves.
- Any important implementation decisions.

Do not produce unnecessary commit bodies.

---

## 4. Commit

Execute:

```bash
git commit -m "<type>: <summary>"
```

If a body exists:

```bash
git commit \
  -m "<type>: <summary>" \
  -m "<body>"
```

Never use:

- `--amend`
- `--no-verify`
- `--no-gpg-sign`

unless the user explicitly requests them.

---

## 5. Verify

After committing, run:

```bash
git status --short
git log --oneline -1
```

Then report:

- The generated commit message.
- The new commit hash.
- Whether the working tree is clean.

If pre-commit hooks:

- block the commit,
- modify files,
- format code,
- or generate new changes,

do **not** automatically recommit.

Instead:

1. Explain exactly what happened.
2. Show which files changed.
3. Ask the user whether those follow-up changes should also be committed.

---

# General Principles

- Generate commit messages based on the intent of the code changes, not filenames.
- Always use Conventional Commits (`type: summary`).
- Keep summaries concise and meaningful.
- Prefer clarity over clever wording.
- Never invent issue numbers.
- Never push automatically.
- Never discard user work.
```
