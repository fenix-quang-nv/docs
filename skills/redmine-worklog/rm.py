# -*- coding: utf-8 -*-
"""Redmine worklog helper: create tickets and log time entries through the
normal web forms, using a browser session cookie (no API key needed).

    python3 rm.py ids                       # print tracker/status/priority/activity ids of the project
    python3 rm.py create tickets.json       # create tickets (skips subjects that already exist) -> ids.json
    python3 rm.py log worklog.csv [ids.json]# log time entries from CSV (skips duplicates)
    python3 rm.py verify 2026-10-05 2026-10-09   # totals per day / ticket / activity

Files next to this script:
    config.json   base url, project, user id, activity map (see config.example.json)
    cookie.txt    the `_redmine_session=...` cookie value, one line (delete it when done)
"""
import re, html, sys, json, csv, io, os, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, 'config.json')))
B = CFG['base_url'].rstrip('/')
P = CFG['project']
CK = open(os.path.join(HERE, 'cookie.txt')).read().strip()
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36'


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


op = urllib.request.build_opener(NoRedirect)


def req(path, data=None, referer=None):
    h = {'Cookie': CK, 'User-Agent': UA, 'Accept': 'text/html'}
    if referer:
        h['Referer'] = B + referer
    if data is not None:
        data = urllib.parse.urlencode(data, doseq=True).encode()
        h['Content-Type'] = 'application/x-www-form-urlencoded'
    r = urllib.request.Request(B + path, data=data, headers=h)
    try:
        resp = op.open(r)
        return resp.status, {k.lower(): v for k, v in resp.headers.items()}, resp.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, {k.lower(): v for k, v in e.headers.items()}, e.read().decode('utf-8', 'replace')


def token(page):
    m = re.search(r'name="authenticity_token" value="([^"]+)"', page)
    if not m:
        sys.exit('no authenticity_token on the form: session expired? (cookie.txt)')
    return m.group(1)


def opts(page, name):
    m = re.search(r'<select[^>]*(?:id|name)="%s"[^>]*>(.*?)</select>' % re.escape(name), page, re.S)
    if not m:
        return None
    return [(v, html.unescape(t.strip())) for v, t in re.findall(r'<option[^>]*value="([^"]*)"[^>]*>([^<]*)', m.group(1))]


def errors(body):
    errs = re.findall(r'<div id="errorExplanation"[^>]*>(.*?)</div>', body, re.S)
    return re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', errs[0]))[:300] if errs else body[:200]


def find_issue(subject):
    q = urllib.parse.urlencode({'set_filter': 1, 'f[]': ['subject', 'status_id'], 'op[subject]': '=',
                                'v[subject][]': subject, 'op[status_id]': '*', 'c[]': ['subject', 'status']}, doseq=True)
    st, h, s = req('/projects/%s/issues?%s' % (P, q))
    return re.findall(r'<tr id="issue-(\d+)"', s)


def create_issue(t, parent=''):
    ex = find_issue(t['subject'])
    if ex:
        return 'exists', ex[0]
    st, h, page = req('/projects/%s/issues/new' % P)
    data = {'authenticity_token': token(page),
            'issue[tracker_id]': t.get('tracker', CFG['tracker_id']),
            'issue[subject]': t['subject'], 'issue[description]': t['description'],
            'issue[status_id]': t.get('status', CFG['status']['new']),
            'issue[priority_id]': t.get('priority', CFG['priority_id']),
            'issue[assigned_to_id]': t.get('assignee', CFG['user_id']),
            'issue[parent_issue_id]': parent, 'issue[start_date]': t.get('start', ''),
            'issue[due_date]': t.get('due', ''), 'issue[estimated_hours]': t.get('est', ''),
            'issue[done_ratio]': t.get('done', '0'), 'commit': 'Create'}
    st, h, body = req('/projects/%s/issues' % P, data, referer='/projects/%s/issues/new' % P)
    m = re.search(r'/issues/(\d+)', h.get('location', ''))
    if st in (302, 303) and m:
        return 'created', m.group(1)
    return 'error %s' % st, errors(body)


def existing_entries(date_from, date_to):
    q = urllib.parse.urlencode({'set_filter': 1, 'f[]': ['user_id', 'spent_on'], 'op[user_id]': '=', 'v[user_id][]': 'me',
                                'op[spent_on]': '><', 'v[spent_on][]': [date_from, date_to],
                                'c[]': ['spent_on', 'issue', 'activity', 'hours', 'comments'], 'per_page': 200, 'encoding': 'UTF-8'}, doseq=True)
    st, h, s = req('/projects/%s/time_entries.csv?%s' % (P, q))
    return list(csv.DictReader(io.StringIO(s.lstrip('﻿'))))


def log_time(issue_id, date, hours, activity_id, comment):
    st, h, page = req('/issues/%s/time_entries/new' % issue_id)
    data = {'authenticity_token': token(page), 'time_entry[issue_id]': issue_id, 'time_entry[spent_on]': date,
            'time_entry[hours]': hours, 'time_entry[activity_id]': activity_id, 'time_entry[comments]': comment, 'commit': 'Create'}
    st, h, body = req('/issues/%s/time_entries' % issue_id, data, referer='/issues/%s/time_entries/new' % issue_id)
    return 'ok' if st in (302, 303) else 'error %s %s' % (st, errors(body))


def same_day(redmine_date, iso_date):
    # Redmine CSV prints the user's date format; accept mm/dd/yyyy, dd/mm/yyyy and yyyy-mm-dd
    y, m, d = iso_date.split('-')
    return redmine_date in ('%s/%s/%s' % (m, d, y), '%s/%s/%s' % (d, m, y), iso_date)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'
    if cmd == 'ids':
        st, h, s = req('/projects/%s/issues/new' % P)
        for n in ('issue_tracker_id', 'issue_status_id', 'issue_priority_id', 'issue_assigned_to_id'):
            print(n, opts(s, n))
        st, h, t = req('/projects/%s/time_entries/new' % P)
        print('time_entry_activity_id', opts(t, 'time_entry_activity_id'))
    elif cmd == 'create':
        spec = json.load(open(sys.argv[2]))
        out = {}
        for key, t in spec.items():
            parent = out.get(t.get('parent_key'), t.get('parent', ''))
            res = create_issue(t, parent)
            print(key, res)
            if res[0] in ('created', 'exists'):
                out[key] = res[1]
        json.dump(out, open(os.path.join(HERE, 'ids.json'), 'w'), indent=1)
        print('ids.json', out)
    elif cmd == 'log':
        ids = json.load(open(sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, 'ids.json')))
        rows = list(csv.DictReader(open(sys.argv[2], encoding='utf-8')))
        dates = sorted(r['Date'] for r in rows)
        have = existing_entries(dates[0], dates[-1])
        print('existing entries in range:', len(have))
        for r in rows:
            iid = ids[r['Issue']]
            dup = [e for e in have if e['Issue'].startswith('%s #%s:' % (e['Issue'].split(' ')[0], iid))
                   and same_day(e['Date'], r['Date']) and float(e['Hours']) == float(r['Hours'])]
            if dup:
                print('skip dup', r['Date'], iid, r['Hours'])
                continue
            print(r['Date'], iid, r['Hours'], r['Activity'], log_time(iid, r['Date'], r['Hours'], CFG['activity'][r['Activity']], r['Comment']))
    elif cmd == 'verify':
        import collections
        rows = existing_entries(sys.argv[2], sys.argv[3])
        byday, byissue, byact = collections.defaultdict(float), collections.defaultdict(float), collections.defaultdict(float)
        for r in rows:
            byday[r['Date']] += float(r['Hours']); byissue[r['Issue'][:70]] += float(r['Hours']); byact[r['Activity']] += float(r['Hours'])
        print('entries', len(rows), 'total', sum(byday.values()))
        for d in sorted(byday): print(' ', d, byday[d])
        for i, v in sorted(byissue.items()): print(' ', v, i)
        print(' ', dict(byact))
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
