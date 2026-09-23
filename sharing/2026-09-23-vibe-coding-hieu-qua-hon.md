# Vibe coding hiệu quả hơn: bớt chờ AI, làm nhiều việc song song

Khoảng một năm trước, workflow của mình với AI vẫn là kiểu quen thuộc: mở VS Code, bật extension, chat bên sidebar, chờ nó sửa code, review, rồi lại chat tiếp. Nó chạy được, nhưng càng dùng agent nhiều thì càng lộ ra mấy vấn đề mà công cụ cũ không giải được. Bài này kể mình gặp gì, đã thử gì, và vì sao cuối cùng dừng ở [Superset](https://github.com/superset-sh/superset), công cụ mình dùng hằng ngày từ khá lâu rồi.

Ví dụ trong bài lấy từ một dự án tài chính mình đang làm (portal cho khách xem hoá đơn, sao kê, thanh toán). Tên nhánh và đường dẫn đã đổi.

---

## 1. Vấn đề mình gặp

**Mỗi dự án một cửa sổ.** Có những giai đoạn mình được assign 2 đến 3 dự án cùng lúc. Mỗi repo một cửa sổ VS Code hoặc một cửa sổ terminal. Cả ngày Cmd+Tab qua lại, không nhớ cửa sổ nào đang chạy gì.

**Mỗi dự án chỉ làm được một task.** Một checkout, một branch, một agent. Nhận 3 ticket nhỏ cùng lúc thì vẫn phải làm tuần tự: ticket 1 xong, đổi branch, ticket 2. Mở thêm terminal trên cùng thư mục thì hai agent đè code nhau.

**Không biết agent nào đang cần mình.** Agent chạy 5 đến 10 phút rồi dừng lại hỏi. Mình đang ở cửa sổ khác, không thấy. Kết quả là ngồi chờ cho chắc, và phần lớn thời gian trong ngày là chờ.

Tóm lại: công cụ được thiết kế cho **một người, một dự án, một việc**. Còn giờ là một người, nhiều dự án, mỗi dự án nhiều agent.

## 2. Đã thử gì trước Superset

**VS Code + extension AI.** Chat ở sidebar, agent sửa file trong workspace hiện tại. Tốt cho một task. Nhưng mỗi cửa sổ là một checkout, muốn hai task song song trên một repo thì phải tự tạo worktree rồi mở thêm cửa sổ. Không có chỗ nào nhìn được "agent nào xong, agent nào đang hỏi".

**Warp.** Terminal có agent tích hợp, tab và split pane, giao diện đẹp. Mở nhiều tab là chạy được nhiều agent. Nhưng Warp không lo phần worktree hay branch, mình vẫn tự tách thư mục làm việc. Gần đây Warp đi theo hướng "fleet of agents" chạy trên cloud gắn với Jira, Slack, GitHub, hợp với team lớn hơn là một dev muốn chạy vài agent trên máy mình.

**Tự làm bằng tmux + git worktree.** Chạy được, nhưng mỗi task lại tạo worktree, copy config, đặt tên branch, mở pane, và xong thì phải nhớ dọn. Làm 2 tuần thì bỏ.

So sánh theo đúng ba vấn đề ở trên:

| | VS Code + extension | Warp | Superset |
|---|---|---|---|
| Nhiều dự án trong một cửa sổ | mỗi repo một cửa sổ | tab, tự quản lý | sidebar, gom theo repo |
| Nhiều task song song trên một repo | tự tạo worktree | tự tạo worktree | tự động, một click |
| Biết agent nào xong, agent nào cần mình | không | có thông báo khi lệnh xong | sidebar hiện trạng thái, âm báo, badge dock |
| Review thay đổi của agent | source control của VS Code | không | diff viewer theo workspace |
| Setup môi trường cho worktree mới | tự làm | tự làm | script theo repo |
| Chạy agent nào | theo extension | agent của Warp hoặc CLI | bất kỳ CLI nào |
| Nền tảng | mọi OS | mọi OS | macOS chính, Linux thử nghiệm |

VS Code và Warp không tệ, chúng chỉ giải bài toán khác. Bài toán của mình là điều phối, và Superset làm đúng cái đó.

## 3. Superset là gì?

Một câu: **Superset là app desktop để chạy nhiều coding agent CLI song song, mỗi agent trên một git worktree riêng, nhiều repo trong một cửa sổ, và theo dõi tất cả từ một chỗ.**

Nó không thay Claude Code. Nó là lớp điều phối bên trên. Claude Code, Codex, Gemini CLI hay agent tự viết đều dùng được, miễn chạy được trong terminal.

Ý tưởng cốt lõi là `git worktree`: một repo, nhiều thư mục làm việc, mỗi thư mục một branch. Superset tự động hoá phần tạo, cấu hình, theo dõi và dọn các worktree đó.

```
Superset (một cửa sổ)
│
├── repo A: portal tài chính (dự án chính)
│   ├── main checkout ................... develop   ← mình: review, merge, release
│   └── worktrees/
│       ├── t01-expired-link-popup/ ..... feature/t01   agent  ● đang chạy
│       ├── t02-expired-link-standalone/  feature/t02   agent  ● đang chạy
│       ├── t03-invoice-overdue-status/ . feature/t03   agent  ✓ xong, chờ review
│       └── t04-statement-download-hint/  feature/t04   agent  ! cần hỏi mình
│
├── repo B: dự án thứ hai
│   └── worktrees/
│       └── fix-export-csv/ ............. fix/export    agent  ✓ xong
│
└── repo C: dự án thứ ba
    └── worktrees/
        └── report-v2/ .................. feat/report   agent  ● đang chạy
```

## 4. Những tính năng mình dùng mỗi ngày

**Workspace: một task, một worktree, một agent.** Bấm "New workspace", gõ tên task, Superset tạo worktree và branch. Tên branch sinh từ câu mình gõ: gõ "sửa lại popup link thanh toán hết hạn" thì ra `sa-li-popup-link-thanh-ton-ht-hn`. Xấu nhưng khỏi nghĩ, không trùng. Trong workspace có terminal sẵn, gõ `claude` là bắt đầu.

**Sidebar theo dõi agent.** Mỗi workspace một dòng, gom theo repo. Hiện agent đang chạy, đã xong, hay đang chờ trả lời. Xong thì âm báo, cần mình thì badge trên dock. Đây là thứ giải vấn đề số 3.

**Diff viewer.** Mỗi workspace có tab diff so với branch gốc. Review được, sửa nhỏ được ngay trong đó.

**Mở sang IDE khi cần.** Một click mở worktree trong VS Code hay editor bất kỳ. Không bỏ hẳn IDE, chỉ không để nó làm trung tâm.

**Browser tích hợp.** Phát hiện port mà process trong workspace đang lắng nghe, mở được ngay trong app. Mỗi worktree chạy dev server port khác nhau thì vẫn xem riêng từng cái.

**Setup script theo repo.** File cấu hình nhỏ trong `.superset/` khai báo script chạy lúc tạo workspace, lúc bấm run, lúc xoá. Mình dùng để copy config local vào worktree mới và link thư mục evidence dùng chung. Worktree vừa tạo là chạy được.

**Terminal có tab, split, giữ session.** Đóng app mở lại, terminal vẫn còn.

Ngoài ra có automation chạy agent định kỳ và remote access từ máy khác, mình chưa dùng nhiều.

## 5. Cài đặt

Bản desktop chủ yếu build và test trên macOS (Apple Silicon và Intel). Linux có bản thử nghiệm, Windows chưa có. Cài bằng một dòng lệnh hoặc Homebrew, xem README của repo Superset. Cài xong thêm repo, chỉ vào thư mục checkout chính là dùng được, không phải đổi gì trong repo.

## 6. Một ngày dùng Superset

Một ngày điển hình: nhận một lô ticket cho portal và trang thanh toán, mở 4 workspace:

| Workspace | Việc | Đụng |
|---|---|---|
| t01 | Popup "link thanh toán hết hạn" trong portal, bỏ footer và nút đổi ngôn ngữ | 2 template |
| t02 | Trang standalone cùng nội dung, mở từ email, thêm nút liên hệ hỗ trợ | 2 file, cùng thư mục t01 |
| t03 | Hoá đơn quá hạn không còn hiện "chờ thanh toán" | 3 file backend |
| t04 | Hướng dẫn khách mới tự tải sao kê | 3 file |

Mỗi workspace gõ một prompt rồi chuyển sang cái tiếp theo. Vòng lặp của một task:

```
mình gõ prompt ──► agent sửa code ──► agent tự verify ──► evidence/<số>-<tên>/
   (workspace)      (worktree riêng)    (Playwright)          ├── ảnh before/after
                                                              ├── README
                                                              └── body PR soạn sẵn
                                                                      │
 merge ◄── mình review diff trong Superset ◄── âm báo "xong" ◄─────────┘
```

Prompt mẫu cho t03:

> Trong portal, tab Hoá đơn, hoá đơn đã quá hạn vẫn hiện chấm xanh "chờ thanh toán". Sửa để không hiện nữa. Verify trên local bằng Playwright: đăng nhập tài khoản test, chụp danh sách hoá đơn trước và sau, lưu vào `evidence/12-t03-invoice-overdue/`.

Trong lúc 4 agent chạy, mình ở main checkout review PR của team hoặc viết spec cho task tiếp theo. Có âm báo thì bấm vào workspace đó, xem diff, góp ý hoặc merge. Task nào hỏng thì xoá workspace làm lại, không ảnh hưởng ba cái còn lại.

## 7. Từ giao task đến lúc test

Superset lo phần điều phối, nhưng chạy 4 agent song song chỉ có ích nếu **mỗi agent tự đi được từ đầu đến cuối** mà không cần mình ngồi kèm. Phần này là cách mình giao task để agent tự làm, tự test, tự để lại bằng chứng.

### Prompt luôn có ba phần

1. **Ticket nói gì.** Chép nguyên văn hoặc tóm tắt, kèm bước tái hiện.
2. **Sửa ở đâu**, nếu biết. Không biết thì để agent tự tìm, nhưng ghi rõ phạm vi không được đụng.
3. **Verify cách nào, evidence lưu đâu.** Đây là phần hay bị bỏ, và là phần quyết định agent có tự chạy hết được hay không.

Thiếu phần 3 thì agent sửa xong sẽ báo "đã test" mà không có gì chứng minh, mình lại phải tự mở browser kiểm tra, tức là quay về ngồi chờ.

### Agent tự test bằng Playwright

Với thay đổi trên UI, mình bắt agent viết một script Playwright dùng xong bỏ. Script đó đăng nhập bằng tài khoản test, đi đúng luồng của ticket, kiểm tra điều kiện, rồi chụp màn hình. Ví dụ với t01: đăng nhập portal, mở tab Hoá đơn, bấm hoá đơn có link thanh toán đã hết hạn, kiểm tra trong iframe popup không còn footer và thanh đổi ngôn ngữ, chụp ảnh mỗi ngôn ngữ một bản, có ảnh cận và ảnh toàn trang.

Với thay đổi backend không có UI, agent gọi thẳng hàm hoặc API rồi in kết quả trước và sau, cũng lưu vào evidence.

### Thư mục evidence

Mỗi task một thư mục `evidence/<số>-<tên>/`, nằm ngoài git:

```
evidence/10-t01-t02-expired-link/
├── before-popup-prod.png ........ chụp prod trước khi sửa
├── before-standalone-client.png . ảnh trong tài liệu khách gửi
├── t01-popup-en.png, -jp.png .... after, popup trong portal
├── t01-popup-en-full.png ........ after, toàn màn hình
├── t02-standalone-en.png, -jp.png
├── README.md .................... đổi gì, gotcha gặp phải, data test còn để lại
└── PR-t01.md, PR-t02.md ......... body PR soạn sẵn, chỗ trống để kéo ảnh vào
```

Hai quy ước quan trọng:

- **Ảnh "before" là baseline.** Chụp từ prod hoặc lấy ngay trong tài liệu khách gửi, trước khi agent sửa. Agent chỉ cần chụp "after" cùng góc, mình đặt cạnh nhau so.
- **Ảnh không commit vào repo.** Kéo thả vào PR description. Body PR agent soạn sẵn, mình chỉ dán và kéo ảnh.

### Playwright bắt được bug mà đọc code không thấy

Lúc verify t02, agent chạy 5 request liên tiếp vào trang ở ngôn ngữ thứ hai và thấy **lúc đúng, lúc rơi về ngôn ngữ mặc định.** Đọc template thì đúng hết. Nguyên nhân là nginx SSI xử lý include bằng subrequest bất đồng bộ, nên điều kiện kiểm tra ngôn ngữ đặt ngay sau header có thể chạy trước khi biến ngôn ngữ kịp set. Fix là một thuộc tính bắt include đó chờ xong mới đi tiếp.

Sau fix 5/5 request đúng trên cả hai URL. Nếu chỉ review diff và tin câu "đã test xong", bug này lên prod.

### Lúc review mình làm gì

Có âm báo, bấm vào workspace, đọc README trong evidence trước, rồi xem diff trong Superset, rồi mở ảnh before/after. Ba thứ khớp nhau thì merge. Không khớp thì gõ tiếp vào cùng workspace, agent còn nguyên ngữ cảnh.

### Kết quả

| | Hồi còn VS Code, làm tuần tự | Giờ với Superset, 3 đến 4 worktree |
|---|---|---|
| Ticket nhỏ / ngày | 2 đến 3 | 5 |
| Thời gian chờ agent | phần lớn buổi | gần như không |
| Cửa sổ mở cùng lúc | 4 đến 6 | 1 |
| Conflict lúc merge | thỉnh thoảng | 1 lần (t01 và t02 chung một file, gộp thành 1 PR) |

Số ticket không tăng vì agent nhanh hơn. Nó tăng vì mình **không còn nghẽn ở một luồng**.

## 8. Lưu ý khi dùng

- **3 đến 4 workspace là đủ.** 10 agent là 10 diff phải review.
- **Chia task ít đụng nhau.** Worktree tách môi trường, không tách logic. t01 và t02 chung một file, cuối cùng phải gộp PR.
- **Đóng workspace cũ.** Có hôm gần 40 process Claude Code còn sống, hơn 2 GB RAM, swap đầy. Xong task thì đóng.
- **Quota.** 4 agent cùng lúc chạm giới hạn 5 giờ của Claude Max khá nhanh. Theo dõi usage tuần đầu.
- **Data test.** Chỉ đụng tài khoản test, ghi lại cái gì đã sửa, trả lại khi xong. Dữ liệu tài chính thì càng phải kỹ.

## 9. Kết

Khi AI viết code, công cụ nên xoay quanh **giao việc, chờ, review** thay vì gõ code. Claude Code làm, Superset điều phối, mình quyết cái gì đáng làm.

Nếu bạn đang mở 4 cửa sổ cho 4 dự án và vẫn ngồi chờ agent, cài Superset, mở hai workspace song song thử xem.

---

Repo Superset: https://github.com/superset-sh/superset
Bạn chạy Claude Code kiểu gì? Mấy workspace một lúc là vừa? Mở issue hoặc PR vào repo này để chia sẻ.
