# onflow-shared-skill

Shared agent skills for Onflow workflows.

Repo này dùng layout chuẩn:

```text
skills/<skill-name>/SKILL.md
```

Một số skill có thêm tài liệu phụ trợ như `references/`, `rules/`, hoặc template markdown. Khi copy/cài skill, hãy copy cả thư mục skill, không chỉ riêng `SKILL.md`.

## Cách Dùng

### Dùng trong Codex

Copy skill cần dùng vào thư mục skills của Codex:

```bash
mkdir -p ~/.codex/skills
cp -R skills/<skill-name> ~/.codex/skills/
```

Ví dụ:

```bash
cp -R skills/django ~/.codex/skills/
cp -R skills/celery ~/.codex/skills/
```

Sau đó mở session Codex mới để agent nạp skill.

### Dùng trong Claude Code

Copy skill cần dùng vào thư mục skills của Claude:

```bash
mkdir -p ~/.claude/skills
cp -R skills/<skill-name> ~/.claude/skills/
```

Ví dụ:

```bash
cp -R skills/react ~/.claude/skills/
cp -R skills/react-native ~/.claude/skills/
```

Sau đó mở session Claude Code mới để Claude nạp skill.

Nếu muốn cài skill ở phạm vi project, copy vào thư mục `.claude/skills` của repo đang làm việc:

```bash
mkdir -p .claude/skills
cp -R /path/to/onflow-shared-skill/skills/<skill-name> .claude/skills/
```

### Dùng trong repo khác

Copy thư mục skill vào repo đích:

```bash
mkdir -p skills
cp -R /path/to/onflow-shared-skill/skills/<skill-name> skills/
```

Khi prompt agent, có thể gọi trực tiếp theo tên skill, ví dụ:

```text
Use the django skill to review this model design.
Use the celery skill to design a retry-safe background task.
Use the request-code-review skill before merging.
Use the react-performance skill to review this Next.js page.
```

### Dùng bằng Git Submodule

Cài repo này vào repo khác dưới dạng submodule:

```bash
git submodule add git@github.com:N-H-Logistics/onflow-shared-skill.git .agents/onflow-shared-skill
git commit -m "chore: add shared skills submodule"
```

Khi cần copy một skill từ submodule vào thư mục skills của repo hiện tại:

```bash
mkdir -p skills
cp -R .agents/onflow-shared-skill/skills/<skill-name> skills/
```

Hoặc copy vào Claude project skills:

```bash
mkdir -p .claude/skills
cp -R .agents/onflow-shared-skill/skills/<skill-name> .claude/skills/
```

Ví dụ:

```bash
cp -R .agents/onflow-shared-skill/skills/django skills/
cp -R .agents/onflow-shared-skill/skills/request-code-review skills/
```

Cập nhật submodule lên commit mới nhất:

```bash
git submodule update --remote .agents/onflow-shared-skill
git add .agents/onflow-shared-skill
git commit -m "chore: update shared skills"
```

Clone repo có submodule:

```bash
git clone --recurse-submodules <repo-url>
```

Nếu đã clone nhưng thiếu submodule:

```bash
git submodule update --init --recursive
```

## Skills

### Onflow Workflow

| Skill | Trạng thái | Dùng khi |
| --- | --- | --- |
| `git-commit` | Có nội dung | Tạo commit message theo style repo và commit thay đổi. |
| `release-notes` | Placeholder | Dự kiến dùng để tạo release note. |
| `confluence-report` | Placeholder | Dự kiến dùng để viết report Confluence. |
| `request-code-review` | Có nội dung + template | Yêu cầu subagent review code sau task lớn hoặc trước merge. |
| `prd` | Có nội dung | Viết Product Requirements Document với discovery, user stories, technical specs, risks. |

### Django / Python Backend

| Skill | Dùng khi |
| --- | --- |
| `django` | Thiết kế Django app, DRF API, ORM, caching, signals, middleware, production patterns. |
| `django-security` | Review hoặc cấu hình security: auth, permissions, CSRF, XSS, SQL injection, deployment hardening. |
| `django-performance-review` | Audit hiệu năng Django: N+1 queries, queryset không giới hạn, indexes, write loops. |
| `django-testing` | Viết test Django theo TDD với pytest-django, factory_boy, mocking, DRF tests. |
| `celery` | Thiết kế Django Celery tasks, retries, beat schedules, worker config, monitoring, production deployment. |
| `fastapi` | Xây FastAPI backend với async, Pydantic models, dependency injection, error handling. |
| `pydantic` | Validation, serialization, settings/config, Pydantic v2 patterns. |
| `python-performance-optimization` | Profile và tối ưu Python bằng cProfile, memory profilers, data structures, caching. |

### React / Frontend

| Skill | Dùng khi |
| --- | --- |
| `react-performance` | React/Next.js performance best practices: waterfalls, bundle size, server/client rendering. |
| `react-composition-patterns` | Refactor component APIs, tránh boolean prop explosion, dùng compound components/context patterns. |
| `frontend-code-review` | Review frontend `.tsx`, `.ts`, `.js` theo checklist code quality, performance, business logic. |
| `react-native` | React Native/Expo performance: FlashList, animations, navigation, native modules, monorepo setup. |

## Skill Có File Phụ Trợ

Các skill sau cần copy cả thư mục:

| Skill | File phụ trợ |
| --- | --- |
| `celery` | `references/*.md` |
| `python-performance-optimization` | `references/*.md` |
| `request-code-review` | `code-reviewer.md` |
| `react-performance` | `AGENTS.md`, `rules/*.md` |
| `react-composition-patterns` | `AGENTS.md`, `rules/*.md` |
| `frontend-code-review` | `references/*.md` |
| `react-native` | `AGENTS.md`, `rules/*.md` |

## Gợi Ý Chọn Skill

- Làm Django tổng quát: dùng `django`.
- Django chậm hoặc nghi N+1: dùng `django-performance-review`.
- Django bảo mật: dùng `django-security`.
- Django test/TDD: dùng `django-testing`.
- Background jobs trong Django: dùng `celery`.
- API Python không dùng Django: dùng `fastapi` và `pydantic`.
- Code Python chậm: dùng `python-performance-optimization`.
- React/Next.js performance: dùng `react-performance`.
- Component API khó maintain: dùng `react-composition-patterns`.
- Review frontend staged changes hoặc file cụ thể: dùng `frontend-code-review`.
- Mobile app React Native/Expo: dùng `react-native`.
- Trước khi merge hoặc sau task lớn: dùng `request-code-review`.
- Viết PRD hoặc làm rõ scope feature: dùng `prd`.

## Quy Ước Khi Thêm Skill Mới

1. Tạo thư mục `skills/<skill-name>/`.
2. Đặt file chính là `skills/<skill-name>/SKILL.md`.
3. Giữ `name:` trong frontmatter khớp với `<skill-name>`.
4. Nếu skill tham chiếu file phụ trợ, thêm chúng trong cùng thư mục skill.
5. Cập nhật README ở đúng nhóm skill.
