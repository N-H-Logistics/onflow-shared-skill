# Hướng dẫn viết từng Section — Phù hợp với CEO Onflow

Mục tiêu: CEO đọc báo cáo trong < 5 phút, nắm được toàn bộ bức tranh tuần.

---

## Nguyên tắc chung

1. **Viết cho người bận** — Mỗi bullet tối đa 2 dòng. Không giải thích kỹ thuật thừa.
2. **Kết quả trước, chi tiết sau** — "Hoàn thành tích hợp GHN" tốt hơn "Đã thực hiện việc tích hợp với đối tác GHN theo phương pháp..."
3. **Số liệu khi có** — "20 thành viên", "3 hãng vận chuyển mới", "hoàn thành 80% module X"
4. **Cấu trúc nhất quán tuần này sang tuần khác** — Giúp CEO nhận ra pattern

---

## Section I — Tóm tắt chung & Điểm nổi bật

**Mục đích**: CEO scan 30 giây biết ngay tuần này team làm được gì lớn.

**Cách viết bullet**:
- Format: `[Hệ thống/Dự án]: [Thành tựu cụ thể]`
- Tốt: `Open API: Hoàn thiện giao diện OA Portal cho 5 module phục vụ khách hàng Intrepid`
- Không tốt: `Đã làm việc với Open API và cải thiện nhiều thứ`

**Số lượng**: 4–8 bullet. Không liệt kê tất cả, chỉ chọn điểm nổi bật nhất.

**Nhóm theo theme nếu nhiều item**:
- Nhóm theo: Sản phẩm mới / Cải tiến UX / Hạ tầng / Tích hợp đối tác / Dữ liệu

---

## Section II — Chi tiết công việc theo hệ thống / Dự án

**Mục đích**: Bằng chứng cụ thể cho phần tóm tắt. CEO đọc khi muốn drill down.

**Thứ tự ưu tiên hệ thống** (liệt kê theo thứ này nếu có):
1. Dự án chiến lược (Billing Engine, Packing V2, TMS V2)
2. Hệ thống core (WMS, OMS, OPS)
3. Tích hợp/kết nối (Open API, TMS carriers)
4. Hạ tầng & Data (Data Platform, Mobile)

**Cách viết từng item**:
- Dùng verb hoàn thành: "Hoàn thành", "Triển khai", "Xây dựng", "Cải thiện"
- Nếu đang dang dở: "Đang phát triển", "Hoàn thành X%, còn lại Y"
- Nếu là thiết kế/phân tích: "Hoàn thành phân tích & thiết kế quy trình..."

**Không cần viết**:
- Fix bug nhỏ lẻ (gộp thành "Xử lý các lỗi phát sinh trên hệ thống X")
- Họp nội bộ, review code thường xuyên
- Công việc hành chính

---

## Section III — Rủi ro / Vấn đề ghi nhận

**Khi không có rủi ro**:
> ✅ Trong tuần qua không ghi nhận rủi ro nào đáng kể.

**Khi có rủi ro, dùng bảng với 4 cột**:
- **Hệ thống**: Tên hệ thống bị ảnh hưởng
- **Mô tả**: Mô tả ngắn gọn vấn đề (1-2 câu)
- **Mức độ**: Cao / Trung bình / Thấp
- **Trạng thái**: Đã xử lý / Đang xử lý / Cần hỗ trợ

**Phân loại mức độ**:
| Mức | Tiêu chí |
|---|---|
| Cao | Ảnh hưởng đến vận hành thực tế, khách hàng bị tác động |
| Trung bình | Ảnh hưởng nội bộ, chưa đến khách hàng, cần xử lý trong 1-3 ngày |
| Thấp | Rủi ro tiềm ẩn, theo dõi, chưa cần xử lý ngay |

---

## Section IV — Kế hoạch tuần tới

**Mục đích**: Minh bạch với CEO về cam kết tuần sau.

**Cấu trúc giống Section II** — nhóm theo hệ thống/dự án.

**Cách viết**:
- Dùng verb tiếp diễn: "Tiếp tục", "Hoàn thiện", "Triển khai", "Bắt đầu"
- Cụ thể nhất có thể: "Triển khai module Nhập giá (F26)" tốt hơn "Tiếp tục làm F26"
- Nếu phụ thuộc bên ngoài: ghi rõ "(chờ xác nhận từ [tên đối tác/phòng ban])"

**Không nên**:
- Liệt kê quá nhiều (max 3-4 item mỗi hệ thống)
- Viết kế hoạch quá xa (chỉ tuần tới, không phải tháng tới)
- Hứa hẹn không chắc chắn

---

## Checklist trước khi đẩy lên Confluence

- [ ] Tiêu đề trang đúng format: `Báo cáo tuần N – YYYY | Technical`
- [ ] Metadata đầy đủ: tuần, ngày, người tổng hợp, headcount, hệ thống
- [ ] Section I: 4-8 bullet điểm nổi bật
- [ ] Section II: Mỗi hệ thống có ít nhất 1 item
- [ ] Section III: Có nội dung (dù chỉ là "không có rủi ro")
- [ ] Section IV: Có kế hoạch cho ít nhất các dự án đang chạy
- [ ] Không có lỗi chính tả tiếng Việt
- [ ] Trang được đặt đúng dưới parent page