---
name: weekly-tech-report-confluence
description: >
  Tạo và đăng báo cáo tuần công việc của team Technical lên Confluence để gửi CEO.
  Kích hoạt skill này bất cứ khi nào người dùng đề cập đến: "báo cáo tuần", "weekly report tech",
  "tổng hợp công việc tuần", "viết báo cáo cho CEO", "đẩy báo cáo lên Confluence",
  "báo cáo kỹ thuật", "báo cáo technical", hoặc upload file báo cáo tuần dạng PDF/text.
  Skill này xử lý toàn bộ luồng: đọc dữ liệu đầu vào → chuẩn hóa nội dung → tạo/cập nhật
  trang Confluence theo đúng cấu trúc template Onflow → thông báo kết quả.
compatibility:
  mcp_servers:
    - name: Atlassian Rovo
      url: https://mcp.atlassian.com/v1/mcp
---

# Skill: Báo cáo tuần Technical → Confluence

Skill này nhận nội dung báo cáo tuần của team Technical (từ PDF, text, hoặc input trực tiếp),
chuẩn hóa theo template Onflow, và đăng lên Confluence để CEO review.

---

## Luồng thực hiện

### Bước 1 — Thu thập thông tin đầu vào

Xác định các thông tin sau từ nội dung người dùng cung cấp:

| Trường | Nguồn | Ghi chú |
|---|---|---|
| Tuần số | Tiêu đề báo cáo hoặc hỏi người dùng | VD: Tuần 23 |
| Khoảng thời gian | Nội dung hoặc tính từ số tuần | VD: 01/06 – 05/06/2026 |
| Tên người tổng hợp | Nội dung | VD: Nguyễn Quang Minh Trí – Lê Thị Bích Hạnh |
| Số nhân sự | Phần Tóm tắt chung | VD: 20 thành viên |
| Nội dung công việc | Toàn bộ phần II (các hệ thống) | Xem cấu trúc bên dưới |
| Rủi ro/vấn đề | Phần Rủi ro | Có thể để trống |
| Kế hoạch tuần tới | Phần Kế hoạch | Bắt buộc |

Nếu người dùng upload PDF, đọc toàn bộ nội dung trước khi tiến hành các bước tiếp theo.
Nếu thiếu thông tin quan trọng (số tuần, khoảng ngày), hỏi lại người dùng trước khi tiếp tục.

---

### Bước 2 — Chuẩn hóa nội dung theo template

Tổ chức nội dung vào đúng các section sau (xem template chi tiết ở `references/template.md`):

1. **Thông tin chung** — Metadata: tuần, ngày, người tổng hợp, số nhân sự, hệ thống liên quan
2. **Điểm nổi bật tuần** — Tóm tắt bullet điểm nhấn theo từng nhóm hệ thống/dự án
3. **Chi tiết công việc theo hệ thống** — Mỗi hệ thống/dự án là một subsection riêng
4. **Rủi ro / Vấn đề ghi nhận** — Nếu không có thì ghi rõ "Không có rủi ro đáng kể"
5. **Kế hoạch tuần tới** — Nhóm theo hệ thống/dự án, giống cấu trúc phần chi tiết
6. **Thông tin bổ sung** (tuỳ chọn) — Link JIRA, PR đáng chú ý, v.v.

---

### Bước 3 — Xác định vị trí trên Confluence

Trước khi tạo trang, cần xác định:

1. Gọi `getAccessibleAtlassianResources` để lấy `cloudId`
2. Tìm Space chứa báo cáo tuần Technical:
   - Dùng `searchConfluenceUsingCql` với query: `type = "space" AND space.title ~ "Technical"` hoặc `space.title ~ "Onflow"`
   - Nếu không tìm được, hỏi người dùng tên Space hoặc URL trang cha
3. Tìm trang cha (parent page):
   - CQL gợi ý: `title = "Báo cáo tuần Technical" AND type = page`
   - Hoặc: `title ~ "Báo cáo tuần" AND space.key = "<KEY>"`
4. Kiểm tra xem trang cho tuần này đã tồn tại chưa:
   - CQL: `title ~ "Tuần <N>" AND title ~ "2026" AND space.key = "<KEY>"`
   - Nếu đã tồn tại → hỏi người dùng: cập nhật hay tạo mới?

---

### Bước 4 — Tạo/cập nhật trang Confluence

**Tiêu đề trang chuẩn:**
```
Báo cáo tuần <N> – <YYYY> | Technical
```
Ví dụ: `Báo cáo tuần 23 – 2026 | Technical`

**Tạo trang mới** (nếu chưa tồn tại):
- Dùng `createConfluencePage`
- `contentFormat`: `"html"` (để giữ định dạng bảng, heading, màu sắc)
- `parent`: ID của trang cha tìm được ở Bước 3
- Nội dung: render theo template HTML ở `references/template.md`

**Cập nhật trang đã tồn tại:**
- Dùng `updateConfluencePage`
- Giữ nguyên `pageId`, tăng `version`
- Cẩn thận không mất dữ liệu cũ (lấy nội dung hiện tại trước khi ghi đè)

---

### Bước 5 — Xác nhận và thông báo

Sau khi tạo/cập nhật thành công:
1. Hiển thị link trang Confluence vừa tạo
2. Tóm tắt ngắn: trang mới hay cập nhật, tiêu đề, space, trang cha
3. Gợi ý bước tiếp theo nếu cần (VD: share link cho CEO, thêm watcher, v.v.)

---

## Quy tắc chất lượng nội dung

- **Ngôn ngữ**: Toàn bộ viết bằng **tiếng Việt**, thuật ngữ kỹ thuật giữ nguyên tiếng Anh (WMS, OMS, API, v.v.)
- **Tone**: Chuyên nghiệp, súc tích, phù hợp đọc ở cấp CEO — tránh quá chi tiết kỹ thuật
- **Bullet points**: Dùng cho điểm nổi bật và kế hoạch; dùng bảng cho thông tin có cấu trúc
- **Không bịa**: Nếu thông tin không có trong nguồn, để trống hoặc đánh dấu `[Cần bổ sung]`
- **Rủi ro**: Phải luôn có section này, dù chỉ ghi "Không ghi nhận rủi ro đáng kể trong tuần"

---

## Xử lý edge cases

| Tình huống | Hành động |
|---|---|
| Không tìm được Space | Hỏi người dùng tên Space hoặc page ID trang cha |
| Trang đã tồn tại | Hỏi: "Trang này đã tồn tại, bạn muốn cập nhật hay tạo bản mới?" |
| Thiếu section trong báo cáo đầu vào | Điền `[Cần bổ sung]` và thông báo cho người dùng |
| Nhiều team trong cùng báo cáo | Tạo một trang, dùng heading H2 cho từng team/hệ thống |
| Nội dung quá dài (>5000 từ) | Tóm lược phần chi tiết, giữ nguyên điểm nổi bật và kế hoạch |

---

## Tham chiếu

- `references/template.md` — Template HTML đầy đủ để render trang Confluence
- `references/section-guide.md` — Hướng dẫn viết từng section cho phù hợp với CEO Onflow