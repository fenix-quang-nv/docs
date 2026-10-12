# Redmine W41 — 05/10 → 09/10/2026

Mục tiêu **8 h/ngày**. Đã ghi đủ 8 h × 5 ngày = 40 h.

---

# Tickets

## A · `[TAS] Welcome & Onboarding flow` — #A (parent)
```
Marketing's "Welcome & Onboarding Flow - Overview" document (Sep 2026) describes the
pre-purchase Welcome series (Mailchimp) and the post-purchase Onboarding series (TAS),
and lists the IT requests in two sprints: Sprint 1 (approved, immediate) and Sprint 2
(pending Sales alignment). Each sprint is a subtask; time is logged on the subtasks.
```
Tracker Task · Assignee Quang · Start 07/10 · % Done 45. Không log giờ trực tiếp.

### A1 · #A1 `[TAS] Welcome & Onboarding — Sprint 1 (IT-01, IT-02, IT-03, IT-CONF-01..04)`
```
Sprint 1 asks IT for: IT-01 a daily alert to support@ listing paid accounts whose welcome
email was not sent for more than 24h; IT-02 the parent's welcome email to carry the
children's myTA logins and a CTA to add the child's email; IT-03 a portal nudge 7 days
after the welcome email when nobody in the family has logged in; and written answers to
IT-CONF-01..04 (architecture sign-off, Email 3 timing, resend safety of Email 1,
Mailchimp sync coverage).
```
Tracker Task · Parent A · Assignee Quang · Start 07/10 · Due 09/10 · % Done 90 (PR open, waiting for Marketing wording + prod release).

### A2 · #A2 `[TAS] Welcome & Onboarding — Sprint 2 (IT-04, IT-05, IT-06, IT-CONF-05)`
```
Sprint 2, pending the Sales & Advising alignment meeting: IT-04 embed the myTA
walkthrough video and login reminders in post-trial lesson report emails and sales
collateral; IT-05 tailor Onboarding Emails 2 and 3 by purchased service line (Private
Tutoring, Group Classes, Admissions, Research) with cross-service trial prompts and a
3-month check-in link; IT-06 evaluate pivoting Email 3 (Day 45-90) from a Roadmapping
Call to a CX Progress Review Call; IT-CONF-05 welcome-email suppression rule for Group
Class entries.
```
Tracker Task · Parent A · Assignee Quang · Status New · % Done 0. Chưa log giờ.

## B · #B `[TA] Code review & release` (ticket dùng chung các tuần)
```
Release the CX-01..09 myTA package/offer changes to production; review and release the
tutor-link fix; handle the regression found on production after the release; answer
Ops questions on the big-meeting alert (#80) and on who can edit System Parameters;
review the Sprint 1 onboarding alert from the team.
```
Tracker Task · Assignee Quang · Start 05/10 · Due 09/10 · % Done 100.

## C1 · #C1 `[Support] a tutor auto-assigned to 4F while her preference is 3F only`
```
Ops reported on Slack that the room auto-assign put tutor the tutor on 4F even
though her profile lists 3F as the only preferred floor. Asked to find out why and
whether the allocation rule changed recently.
```
Tracker Support · Assignee Quang · Start 06/10 · Due 06/10 · % Done 100.

## C2 · #C2 `[Support] Test entries for a test parent to verify Cancel and Reschedule on production`
```
Customer asked for test lessons on production under test a test parent so they can
verify the Cancel and Reschedule requests from myTA for a package-backed and a normal
session, in two rounds (tutor reschedule flag off, then on).
```
Tracker Support · Assignee Quang · Start 07/10 · Due 07/10 · % Done 100.

## C3 · #C3 `[Support] 20-hour package: billing email shows the student's address instead of the parent's `
```
Customer flagged that after a family bought the 20-Hour University Admissions Support
package, the payment page shows the student's email  as the billing email instead
of the parent's . Asked to confirm, and whether billing should always go to the
parent.
```
Tracker Support · Assignee Quang · Start 09/10 · Due 09/10 · % Done 80 (data fix and small code fix proposed).

## C4 · #C4 `[Support] Request sheet triage — #88 consultant self-removal, #89 capability export, #90 second Robotics Lab room, #91 export log`
```
Four new rows on the request sheet: #88 allow Admissions Consulting - Miscellaneous
consultants to remove themselves from appointments; #89 exporting tutors with their
capabilities returns technical strings; #90 add a second TCC Robotics Lab room in TCCS;
#91 keep a log of data exports and prevent mass download.
```
Tracker Support · Assignee Quang · Start 09/10 · Due 09/10 · % Done 100 (answers ready, waiting on customer confirmations).

## D · #D `[Infra] AI classification service — prompt audit; anti-bot plan after the Sogou spider incident`
```
Audit the prompts of the AI classification/extraction service against current guidance
(model, thinking budget, tool forcing, wording) and propose changes; restate the
anti-bot plan for the website after the Sogou spider incident of 27/09.
```
Tracker Task · Assignee Quang · Start 06/10 · Due 06/10 · % Done 100.

---

# Log theo ngày

## Mon 05/10 · 8 h

| Ticket | Log | Activity | Comment |
|---|---|---|---|
| B | 3 h | Analysis | Release list for CX-01..09 checked against what is already on production vs only on dev; release notes written per CX item; reviewed the "link a tutor only when the family has worked with them" fix and verified it on dev. |
| B | 4 h | Development | CX-01, 02, 03, 04, 05, 07, 09 squashed into the release branch and released to production (code + static); smoke-checked the offer screens, checkout page and Plans & Bundles on production. |
| B | 1 h | Documentation | Release record and open items after the CX release (QA feedback on CX-03 still pending from the team). |

## Tue 06/10 · 8 h

| Ticket | Log | Activity | Comment |
|---|---|---|---|
| C1 | 4 h | Analysis | Read the room-allocation rules and the production data for that day (read only); reproduced the 4F result on dev with test data: it happens when 3F's three booths are already taken during her 16:30-22:00 window (online lessons also reserve a booth), or when a lesson was saved at floor level, which the algorithm treats as the whole floor being booked. With the current data the algorithm returns 3F, which Ops confirmed after re-running. No rule change was made recently. |
| C1 | 1.5 h | Documentation | Comment for the PM in plain language, what to ask the customer, and the proposed changes: a floor-level booking should count as one seat, show the unexpected-tutor list in the UI, and register more 3F booths. |
| D | 1.5 h | Analysis | Prompt audit of the four AI steps: found forced tool use in classification, no reasoning budget with a low output cap, a weaker model allowed by the allowlist, and pressure wording; wrote the report with a proposed diff, nothing applied yet. |
| D | 1 h | Analysis | Anti-bot plan for the Sogou spider case restated for the team: rate limits at the edge, bot user-agent rules, and what to watch on the web server. |

## Wed 07/10 · 8 h

| Ticket | Log | Activity | Comment |
|---|---|---|---|
| A1 | 2 h | Analysis | Read the onboarding document and split Sprint 1 into code items (IT-01/02/03) and questions (IT-CONF); reviewed IT-01 (paid accounts with no login details sent) from the team: the alert, the SQL behind it and the new list filters, with one note on list-view cost to measure on production data. |
| C2 | 3 h | Analysis | Wrote the manual test plan for the customer (read only on production): which placeholder tutor and services to use, concrete dates from the 14th, round 1 and round 2 expectations, and substitutes for the two services that cannot be booked (hidden service, package-hour gate). |
| B | 2 h | Development | Production regression from the CX-07 release: Cancel and Reschedule disappeared from the Upcoming Lessons page for all clients; restored the buttons with the same rules as the Upcoming widget, released to dev then production static. |
| C2 | 1 h | Testing | Read the customer's screenshots after each round; both rounds matched the expected buttons once the regression was fixed; evidence saved and clean-up steps listed for Ops. |

## Thu 08/10 · 8 h

| Ticket | Log | Activity | Comment |
|---|---|---|---|
| A1 | 1.5 h | Analysis | Answered IT-CONF-01..04 from the code and the production configuration: Emails 2/3 run from the profile creation date (3 and 42 days, grades 1-8 / 9-12), resending Email 1 never duplicates them, Mailchimp sync only exists for forms that carry a Mailchimp tag (listed which forms do and do not). |
| A1 | 4 h | Development | IT-02: parent welcome email now carries each child's myTA ID and PIN (EN/JA), children get marked as welcomed; IT-03: daily nudge 7 days after the welcome email when nobody in the household opened myTA, with a 48h sign-in link and an editable template; both released to dev. Found and fixed one issue in review: the sign-in link lost its second parameter, so it now carries only the token. |
| A1 | 2 h | Testing | Dev verification: alert mail with 13 accounts and the two list filters, welcome mail with 5 children, nudge sent once and suppressed after a child logs in, sign-in button signs the parent in; screenshots attached to the PR. |
| A1 | 0.5 h | Documentation | PR description with release notes (module upgrade, crons installed off, template placeholder for Marketing) and the IT-CONF answers as a text file for the PM. |

## Fri 09/10 · 8 h

| Ticket | Log | Activity | Comment |
|---|---|---|---|
| A1 | 1 h | Documentation | Handover note for the customer to review Sprint 1 on dev: what to click, why dev does not deliver mail, what we need from Marketing and Ops before production. |
| B | 1 h | Analysis | #80 big-meeting alert: explained to Ops how the feature works and that the director/manager recipients are a System Parameter (comma-separated), plus which roles can open and edit System Parameters. |
| B | 0.5 h | Analysis | How to reset an internal TAS user's password: documented the admin "Change Password" action, the self-service path and the emergency path. |
| C3 | 2.5 h | Analysis | Traced which emails use which address: package confirmation and invoices go to the parent; the payment page and card-related mails use the family's billing record, which for this family carries the student's email. Cause is in the Student form: creating a billing record from the Billing field pre-fills the student's email, and later edits of the student's email overwrite it. Proposed: correct this family's billing record now, change the pre-fill to the parent's email, and audit other families with the same mismatch. |
| C4 | 3 h | Analysis | #88: the self-withdraw action exists but only shows with 3+ tutors; proposed a per-service switch, one question for the customer (keep or cancel the session when the only consultant leaves). #89: not a bug, the export was run in import-compatible mode; answer with the right export option. #90: rooms are contacts tagged as spaces, so a second room is configuration, no code. #91: export logging and the per-user export permission already exist; listed the export paths that are not logged or capped and proposed a row limit, pending the customer's threshold. |

---

# Tổng

| Ngày | A1 | B | C | D | Tổng |
|---|---|---|---|---|---|
| Mon 05/10 | | 8 | | | **8** |
| Tue 06/10 | | | 5.5 | 2.5 | **8** |
| Wed 07/10 | 2 | 2 | 4 | | **8** |
| Thu 08/10 | 8 | | | | **8** |
| Fri 09/10 | 1 | 1.5 | 5.5 | | **8** |
| **Ticket** | **11** | **11.5** | **15** | **2.5** | **40** |

---

# CSV — thay A1 / B / C1–C4 / D bằng ID ticket

```csv
Date,Hours,Activity,Comment,Issue
2026-10-05,3,Analysis,"CX-01..09 release list checked against production vs dev; release notes per item; tutor-link fix reviewed and verified on dev",B
2026-10-05,4,Development,"CX-01/02/03/04/05/07/09 released to production (code + static); offer screens, checkout and Plans & Bundles smoke-checked",B
2026-10-05,1,Documentation,"Release record and open items after the CX release",B
2026-10-06,4,Analysis,"the tutor 4F: allocation rules and that day's data reviewed; 4F reproduced on dev (3F booths full in her window, floor-level booking treated as whole floor); current data gives 3F, confirmed by Ops; no recent rule change",C1
2026-10-06,1.5,Documentation,"PM comment, customer questions and proposed allocation changes written",C1
2026-10-06,1.5,Analysis,"AI service prompt audit: forced tool use, missing reasoning budget, weaker model in allowlist, pressure wording; report with proposed diff",D
2026-10-06,1,Analysis,"Anti-bot plan after the Sogou spider incident restated for the team",D
2026-10-07,2,Analysis,"Onboarding document read; Sprint 1 split into code items (IT-01/02/03) and questions (IT-CONF); IT-01 alert from the team reviewed",A1
2026-10-07,3,Analysis,"Test plan for a test parent: tutor, services, dates from the 14th, round 1/2 expectations, substitutes for the two unbookable services",C2
2026-10-07,2,Development,"Production regression: Cancel/Reschedule missing on Upcoming Lessons after the CX-07 release; restored and released to dev and production",B
2026-10-07,1,Testing,"Customer screenshots checked after each round; both rounds match; clean-up steps listed",C2
2026-10-08,1.5,Analysis,"IT-CONF-01..04 answered from code and production configuration: Email 2/3 timing from profile creation (3/42 days, grades 1-8 and 9-12), resend safety, Mailchimp sync limited to tagged forms (list of covered and uncovered forms)",A1
2026-10-08,4,Development,"IT-02 parent welcome email with children's logins (EN/JA); IT-03 7-day myTA nudge with sign-in link and editable template; dev release; sign-in link fixed to carry only the token",A1
2026-10-08,2,Testing,"Dev verification of alert, list filters, welcome mail with children, nudge once/suppressed after login, sign-in button; screenshots for the PR",A1
2026-10-08,0.5,Documentation,"PR description, release notes and IT-CONF answers file for the PM",A1
2026-10-09,1,Documentation,"Handover note for the customer to review Sprint 1 on dev; what Marketing and Ops must provide before production",A1
2026-10-09,1,Analysis,"#80 big-meeting alert: how it works, recipients as a System Parameter, which roles can edit it",B
2026-10-09,0.5,Analysis,"Internal user password reset: admin action, self-service and emergency paths documented",B
2026-10-09,2.5,Analysis,"one family billing email: which mails use which address; cause in the Student form billing pre-fill and email overwrite; data fix, pre-fill fix and audit proposed",C3
2026-10-09,3,Analysis,"#88 self-withdraw gated at 3+ tutors, per-service switch proposed; #89 export mode, not a bug; #90 second room is configuration; #91 existing export log/permission and the gaps, row limit proposed",C4
```
