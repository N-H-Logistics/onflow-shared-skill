# Template HTML — Báo cáo tuần Technical (Confluence)

Dùng template này khi gọi `createConfluencePage` hoặc `updateConfluencePage`.
Thay thế các placeholder `{{...}}` bằng dữ liệu thực tế.

---

## Template HTML đầy đủ

```html
<h1>BÁO CÁO TỔNG HỢP CÔNG VIỆC — PHÒNG TECHNICAL</h1>

<!-- ===== METADATA ===== -->
<table>
  <tbody>
    <tr>
      <th>Thời gian</th>
      <td>Tuần {{WEEK_NUMBER}} (Từ ngày {{DATE_FROM}} đến {{DATE_TO}})</td>
    </tr>
    <tr>
      <th>Phòng ban</th>
      <td>Technical</td>
    </tr>
    <tr>
      <th>Người tổng hợp</th>
      <td>{{AUTHORS}}</td>
    </tr>
    <tr>
      <th>Tổng nhân sự</th>
      <td>{{HEADCOUNT}} thành viên</td>
    </tr>
    <tr>
      <th>Hệ thống liên quan</th>
      <td>{{SYSTEMS_LIST}}</td>
    </tr>
  </tbody>
</table>

<hr/>

<!-- ===== I. TÓM TẮT CHUNG & ĐIỂM NỔI BẬT ===== -->
<h2>I. Tóm tắt chung &amp; Điểm nổi bật</h2>

<p><em>Tổng quan các thành tựu chính trong tuần:</em></p>

<ul>
  <!-- Mỗi dòng là 1 bullet điểm nổi bật, nhóm theo dự án/hệ thống -->
  <!-- Ví dụ: -->
  <li><strong>{{PROJECT_OR_SYSTEM_1}}:</strong> {{HIGHLIGHT_SUMMARY_1}}</li>
  <li><strong>{{PROJECT_OR_SYSTEM_2}}:</strong> {{HIGHLIGHT_SUMMARY_2}}</li>
  <!-- ... thêm dòng tương tự ... -->
</ul>

<hr/>

<!-- ===== II. CHI TIẾT CÔNG VIỆC THEO HỆ THỐNG / DỰ ÁN ===== -->
<h2>II. Chi tiết công việc theo hệ thống / Dự án</h2>

<!-- Lặp lại block dưới đây cho mỗi hệ thống hoặc dự án -->

<h3>🔧 {{SYSTEM_OR_PROJECT_NAME_1}}</h3>
<ul>
  <li>{{TASK_DETAIL_1}}</li>
  <li>{{TASK_DETAIL_2}}</li>
  <!-- ... -->
</ul>

<h3>🔧 {{SYSTEM_OR_PROJECT_NAME_2}}</h3>
<ul>
  <li>{{TASK_DETAIL_1}}</li>
  <li>{{TASK_DETAIL_2}}</li>
</ul>

<!-- Thêm các block H3 tương tự cho mỗi hệ thống/dự án khác -->

<hr/>

<!-- ===== III. RỦI RO / VẤN ĐỀ GHI NHẬN ===== -->
<h2>III. Rủi ro / Vấn đề ghi nhận</h2>

<!-- Nếu không có rủi ro: -->
<p>✅ Trong tuần qua không ghi nhận rủi ro nào đáng kể.</p>

<!-- Nếu có rủi ro, dùng bảng: -->
<!--
<table>
  <thead>
    <tr>
      <th>Hệ thống</th>
      <th>Mô tả vấn đề</th>
      <th>Mức độ</th>
      <th>Trạng thái xử lý</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>{{SYSTEM}}</td>
      <td>{{ISSUE_DESCRIPTION}}</td>
      <td>{{SEVERITY: Cao / Trung bình / Thấp}}</td>
      <td>{{STATUS: Đã xử lý / Đang xử lý / Chờ phê duyệt}}</td>
    </tr>
  </tbody>
</table>
-->

<hr/>

<!-- ===== IV. KẾ HOẠCH TUẦN TỚI ===== -->
<h2>IV. Kế hoạch tuần tới</h2>

<!-- Nhóm theo hệ thống/dự án, cấu trúc giống phần II -->

<h3>📌 {{SYSTEM_OR_PROJECT_NAME_1}}</h3>
<ul>
  <li>{{PLAN_ITEM_1}}</li>
  <li>{{PLAN_ITEM_2}}</li>
</ul>

<h3>📌 {{SYSTEM_OR_PROJECT_NAME_2}}</h3>
<ul>
  <li>{{PLAN_ITEM_1}}</li>
  <li>{{PLAN_ITEM_2}}</li>
</ul>

<!-- Thêm các block tương tự cho hệ thống/dự án khác -->

<hr/>

<!-- ===== V. THÔNG TIN BỔ SUNG (tuỳ chọn) ===== -->
<!--
<h2>V. Thông tin bổ sung</h2>
<ul>
  <li><a href="{{JIRA_LINK}}">JIRA Sprint {{SPRINT_NUMBER}}</a></li>
  <li>Pull Request đáng chú ý: <a href="{{PR_LINK}}">{{PR_TITLE}}</a></li>
</ul>
-->

<p><em>Báo cáo tổng hợp bởi: {{AUTHORS}} — Ngày cập nhật: {{UPDATE_DATE}}</em></p>
```

---

## Hướng dẫn dùng icon emoji

Dùng nhất quán để CEO scan nhanh:

| Icon | Ý nghĩa |
|---|---|
| 🔧 | Hệ thống / Dự án đang phát triển |
| 📌 | Kế hoạch / Todo |
| ✅ | Hoàn thành / Không có vấn đề |
| ⚠️ | Rủi ro / Cần chú ý |
| 🚀 | Launch / Go-live |
| 📊 | Data / Báo cáo / Analytics |
| 🔗 | Tích hợp bên ngoài / API |

---

## Mapping hệ thống → Icon gợi ý

| Hệ thống / Dự án | Icon |
|---|---|
| WMS | 🔧 |
| OMS | 🔧 |
| OPS | 🔧 |
| TMS / TMS V2 | 🔗 |
| Open API / OA Portal | 🔗 |
| Billing Engine (F26) | 💰 |
| Data Platform | 📊 |
| Mobile | 📱 |
| Packing V2 | 📦 |
| Accounting (ACC) | 💰 |