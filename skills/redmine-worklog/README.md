# redmine-worklog

Agent skill cho Claude Code: dựng worklog tuần (8 h/ngày, 40 h) từ git log + evidence + phiên chat, rồi tạo ticket và log time lên Redmine bằng cookie session của trình duyệt. Không cần API key.

## Cài

```bash
git clone git@github.com:fenix-quang-nv/docs.git
ln -s "$PWD/docs/skills/redmine-worklog" ~/.claude/skills/redmine-worklog
```

Trong Claude Code gõ `/redmine-worklog` hoặc nói "log work tuần vừa rồi".

## Dùng

1. **Dựng file**: agent đọc git log, evidence, memory và chat của tuần → viết `docs/worklog/<year>-W<nn>-redmine.md` (ticket + log theo ngày + CSV). Xem `example-week.md`.
2. **Đưa curl**: lấy cookie Redmine theo hướng dẫn dưới, dán vào chat.
3. Agent tạo ticket (kiểm trùng), log time, verify tổng giờ, ghi id ticket vào file, xoá cookie.

## Lấy curl từ Chrome

1. Đăng nhập Redmine trên Chrome.
2. F12 → tab **Network** → tick **Preserve log**.
3. Mở một trang bất kỳ của Redmine (My account, một issue…).
4. Click dòng request đầu tiên (type `document`).
5. Chuột phải → **Copy** → **Copy as cURL (bash)**.
6. Dán vào chat. Phần cần là `-b '_redmine_session=...'`.

Cookie hết hạn khi đăng xuất. Agent xoá `cookie.txt` sau khi xong.

## Chạy tay (không qua agent)

```bash
cp config.example.json config.json      # sửa project, user_id
echo '_redmine_session=...' > cookie.txt && chmod 600 cookie.txt
python3 rm.py ids                        # id tracker/status/activity của project
python3 rm.py create tickets.json        # -> ids.json
python3 rm.py log worklog.csv            # log time từ CSV, bỏ qua trùng
python3 rm.py verify 2026-10-05 2026-10-09
rm cookie.txt
```

Mẫu: `tickets.example.json`, `worklog.example.csv`. Activity trong CSV (Analysis / Development / Testing / Documentation) map sang id Redmine trong `config.json`; project TA hiện dùng Study spec (35), Development (9), Verify bug (34).

## Quy ước log

- Description ticket = issue/yêu cầu như lúc được nêu, không phải status.
- Comment time entry = *vấn đề gì → kết quả gì*, 1–3 câu, không hash/branch/tool nội bộ.
- Ticket dùng chung nhiều tuần (vd "Code review & release") log thẳng, không tạo mới.
- Feature nhiều sprint: ticket cha + subtask mỗi sprint, giờ log trên subtask.
