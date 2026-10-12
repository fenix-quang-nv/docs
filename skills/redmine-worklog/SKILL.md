---
name: redmine-worklog
description: Weekly Redmine worklog — rebuild a week (8 h/day, 40 h) from git log, evidence folders and the session into docs/worklog/<year>-W<nn>-redmine.md, then create the tickets and log the time entries on Redmine using a browser session cookie the user pastes as a curl. Triggers on "log work tuần", "logwork", "worklog", "log Redmine", "import lên Redmine", "tôi đưa curl" (Redmine), or /redmine-worklog.
---

# redmine-worklog — dựng worklog tuần rồi đẩy lên Redmine

Hai pha, theo thứ tự. Pha 2 chỉ khi user đã dán curl có `_redmine_session`. Nếu chưa có curl, kết thúc pha 1 bằng hướng dẫn lấy curl (mục cuối).

## Pha 1 — dựng file worklog tuần

1. Tuần: "tuần vừa rồi" = Mon→Fri của ISO week trước hôm nay. File `docs/worklog/<year>-W<nn>-redmine.md` trong checkout chính của dự án (untracked, không commit). Có sẵn thì sửa, không tạo lại.
2. Nguồn, lấy hết trước khi viết:
   - `git log --all --since=<Mon> --until=<Sun+1> --format='%ad %h %an %s' --date=format:'%a %d/%m %H:%M'` ở repo code và repo release (release prod thường là commit squash trên repo release).
   - `ls -lT evidence/*` (ngày chụp ảnh), file tạm theo ngày, tài liệu vừa tải.
   - Memory có ngày trong tuần; file worklog tuần trước để giữ format và ticket đang dùng lại.
   - Nội dung phiên chat hiện tại (Slack, ticket sheet, câu hỏi khách).
3. Format file (mẫu: `example-week.md`):
   - Header: tuần, "8 h/ngày, 40 h".
   - **Tickets**: title có tiền tố `[TAS]` / `[TA]` / `[Support]` / `[Infra]`; description trong block ``` là **issue/yêu cầu như lúc được nêu** (không phải status, không "đã fix"); dòng Tracker · Assignee · Start · Due · % Done. Feature nhiều sprint: 1 ticket cha + subtask mỗi sprint, giờ log trên subtask.
   - **Log theo ngày**: bảng Mon→Fri, cột `Ticket | Log | Activity | Comment`, mỗi ngày đúng 8 h.
   - **Tổng**: bảng ngày × ticket, hàng tổng theo ticket = 40.
   - **CSV**: ```csv `Date,Hours,Activity,Comment,Issue` (Issue = key A1/B/C1…, thay bằng id sau khi tạo).
4. Comment high-level: *vấn đề gì → kết quả/kết luận gì*, 1–3 câu; không hash, branch, account id, tên tool nội bộ, chi tiết thao tác. Activity trong file: Analysis / Development / Testing / Documentation (map sang id Redmine ở `config.json`).
5. Kiểm: tổng CSV = 40, mỗi ngày = 8. Báo user bảng ngày → việc chính → giờ.
6. **Grill** (bắt buộc, trước khi coi file là xong): hỏi user theo round, mỗi câu kèm đề xuất của mình, chờ trả lời rồi mới hỏi round sau. Round 1 luôn có:
   ```
   ❓ Q1 - Thiếu việc gì: <liệt kê việc tôi dựng được theo ngày>. Có việc nào tuần này chưa thấy (họp, support ngoài chat, việc không để lại dấu vết trong git) không?
   ➡️ <đề xuất: không / có, ngày nào>
   ❓ Q2 - Chia giờ: <ngày nào tôi phải co/giãn để đủ 8 h, mục nào tôi ước lượng>. Có mục nào giờ lệch thực tế không?
   ➡️ <đề xuất>
   ❓ Q3 - Ticket: <ticket mới tôi định tạo / ticket cũ dùng lại / cái nào gộp thành cha-con>. Có muốn gộp, tách, đổi tên, đổi tracker-status không?
   ➡️ <đề xuất>
   ❓ Q4 - Comment: có mục nào cần nói rõ hơn hay bớt chi tiết không?
   ➡️ <đề xuất: giữ>
   ```
   Round sau chỉ hỏi phần phát sinh từ câu trả lời. Hết câu hỏi → sửa file theo kết luận → in lại bảng ngày + tổng, hỏi "File chốt chưa?" và chờ.

## Pha 2 — tạo ticket + log time lên Redmine

Không tạo gì trên Redmine khi chưa qua 2 cổng dưới. Mỗi cổng 1 câu hỏi, chờ user trả lời.

**Cổng Review (trước khi tạo)**: in ra đúng những gì sẽ POST, dạng bảng:
- Ticket sẽ tạo: key | subject | tracker/status | parent | start–due | est | done. Ticket dùng lại: key → #id.
- Time entry: ngày | #id | giờ | activity Redmine (đã map) | comment rút gọn.
- Tổng giờ theo ngày và theo ticket.
Hỏi: "Review xong: tạo N ticket, log M entry = 40 h. Sửa gì không?" Sửa theo yêu cầu rồi in lại cho tới khi user nói OK.

**Cổng Confirm (trước khi đẩy)**: sau khi đã có cookie và user đã OK review, hỏi đúng 1 câu: "Đẩy lên Redmine bây giờ? (tạo ticket + log time, không hoàn tác tự động)". Chỉ chạy `create`/`log` khi user xác nhận rõ ràng (ok / đẩy đi / yes). Trả lời khác → dừng, không đẩy.

1. (Sau 2 cổng trên.) Từ curl, lấy giá trị `_redmine_session=...` → ghi `cookie.txt` (chmod 600) cạnh `rm.py` trong thư mục tạm. **Không in cookie ra, xoá khi xong.** REST API không dùng được vì `/my/api_key` đòi nhập lại password; đi bằng form HTML + `authenticity_token` lấy từ chính trang form (token của session dùng lại được).
2. Chuẩn bị: copy `rm.py`, `config.json` (từ `config.example.json`, chỉnh `project`, `user_id`) vào thư mục tạm. Lần đầu với project mới: `python3 rm.py ids` để lấy tracker/status/priority/activity id rồi sửa `config.json`.
3. Tạo ticket: viết `tickets.json` (mẫu `tickets.example.json`; subtask dùng `parent_key` hoặc `parent: "<id>"`), chạy `python3 rm.py create tickets.json`. Script bỏ qua subject đã tồn tại và ghi `ids.json`. Ticket dùng chung nhiều tuần (vd "Code review & release") không tạo mới: thêm thẳng id vào `ids.json`.
4. Log time: xuất block CSV của file worklog ra `w.csv`, chạy `python3 rm.py log w.csv`. Script bỏ qua entry đã có cùng issue + ngày + giờ.
5. Verify: `python3 rm.py verify <Mon> <Fri>` → tổng 40, mỗi ngày 8, giờ theo ticket khớp file. Ghi id ticket vào file worklog (title + ghi chú "ĐÃ IMPORT ngày …" ở CSV). Xoá `cookie.txt`.
6. Báo user: ticket + giờ, mapping activity, cookie đã xoá.

## Hướng dẫn user lấy curl (gửi nguyên văn khi cần)

```
1. Mở Chrome, đăng nhập Redmine (https://fenixcorp.cloud.redmine.jp).
2. F12 (hoặc Cmd+Option+I) → tab Network → tick "Preserve log".
3. Bấm vào bất kỳ trang nào của Redmine (vd My account, hoặc một issue).
4. Trong Network, click dòng request đầu tiên (document, cùng tên trang vừa mở).
5. Chuột phải → Copy → "Copy as cURL (bash)".
6. Dán nguyên curl vào chat. Chỉ cần dòng -b '_redmine_session=...' là đủ.
Cookie sống theo session trình duyệt; đăng xuất là hết hạn. Tôi sẽ xoá cookie sau khi log xong.
```

## Guardrails
- Không commit `docs/worklog`. Không lưu cookie ngoài thư mục tạm. Không sửa ticket của người khác.
- Không bỏ qua Grill / Review / Confirm dù user nói "làm luôn": có thể gộp Review + Confirm thành 1 câu nếu user đã OK file, nhưng vẫn phải có 1 câu xác nhận trước khi POST.
- Xoá/sửa ticket hoặc time entry đã tạo chỉ khi user yêu cầu, và làm từng cái.
- Query Redmine có `f[]`/`c[]` phải `curl -g` hoặc dùng `rm.py`.
- POST trả 200 kèm form = lỗi validation: script in `errorExplanation`; thường là parent/id sai hoặc id enumeration đổi → chạy lại `rm.py ids`.
