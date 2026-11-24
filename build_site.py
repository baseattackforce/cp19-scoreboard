# Builds the site's data (site/...) from every round's snapshots. Open Division only.
#   r1/snapshots/<id>/  cp19_r1_*.csv (+ cp19_r1_team_3818_timeline.csv)
#   r2/snapshots/<id>/  cp19_r2_*.csv (+ cp19_r2_timelines.csv, long format)
#   shared/             registration list + inferred school names
# Run:  python3 build_site.py
import csv, json, os, re, glob, collections

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'site')
OURS = '19-3818'
ROUNDS = {
    1: {'label': 'Round 1', 'images': [('win', 'Windows 11', 'Windows11'), ('mint', 'Mint 21', 'Mint21')]},
    2: {'label': 'Round 2', 'images': [('deb', 'Debian 12', 'Debian12'), ('win', 'Windows 11', 'Windows11'),
                                       ('srv', 'Server 2022', 'Server2022')]},
}
# Snapshots taken while the round was still open (anything after the round closed is final).
ROUND_CLOSES = {1: '2026-10-27', 2: '2026-11-15'}


def read(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def pick(r, *names):
    for n in names:
        if n in r and r[n] not in (None, ''):
            return r[n]
    return ''


def num(v):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


def img_key(rnd, image):
    for k, _, prefix in ROUNDS[rnd]['images']:
        if image.startswith(prefix):
            return k
    return None


def tomin(ts):  # "11/12 21:50" -> absolute minutes (good enough within one round)
    d, t = ts.split()
    mo, da = map(int, d.split('/'))
    h, m = map(int, t.split(':'))
    return ((mo * 31 + da) * 24 + h) * 60 + m


def compact(series):
    """[(abs_min, score)] -> (t0_minutes, 'off,score,...') keeping only changes plus the last point."""
    out, last = [], None
    for i, (m, s) in enumerate(series):
        if s != last or i == len(series) - 1:
            out.append((m, s))
            last = s
    return out


# ---- shared: schools ----
inferred = json.load(open(os.path.join(HERE, 'shared', 'inferred_schools.json')))
inferred[OURS] = {'org': 'Jordan High School', 'city': 'Fulshear', 'conf': 'confirmed', 'why': 'our team'}
schools = [{'org': r['Organization'] if 'Organization' in r else list(r.values())[0],
            'nick': pick(r, 'Team Nickname', 'Nickname'), 'city': pick(r, 'City'), 'state': pick(r, 'State'),
            'zip': pick(r, 'Zip', 'ZIP', 'Postal Code'), 'country': pick(r, 'Country')}
           for r in read(os.path.join(HERE, 'shared', 'cp19_registered_open_teams.csv'))]
os.makedirs(OUT, exist_ok=True)
json.dump({'schools': schools, 'inferred': inferred}, open(os.path.join(OUT, 'schools.json'), 'w'), separators=(',', ':'))

index = {'ours': OURS, 'rounds': []}
for rnd, meta in ROUNDS.items():
    snaps = []
    for d in sorted(glob.glob(os.path.join(HERE, f'r{rnd}', 'snapshots', '*'))):
        sid = os.path.basename(d)
        m = re.match(r'(\d{4})-(\d\d)-(\d\d)_(\d\d)(\d\d)$', sid)
        if not m:
            continue
        teams_csv = glob.glob(os.path.join(d, f'cp19_r{rnd}_all_teams.csv'))
        if not teams_csv:
            continue
        # per-image rows
        per = collections.defaultdict(dict)
        for r in read(os.path.join(d, f'cp19_r{rnd}_image_scores.csv')):
            k = img_key(rnd, pick(r, 'image', 'Image'))
            if not k:
                continue
            per[pick(r, 'team_number', 'Team Number')][k] = {
                'time': pick(r, 'duration', 'Time'), 'found': num(pick(r, 'found', 'Found')),
                'remain': num(pick(r, 'remaining', 'Remain')), 'pen': num(pick(r, 'penalties', 'Pen')),
                'warn': pick(r, 'code', 'Warnings'), 'score': num(pick(r, 'ccs_score', 'Score'))}
        teams = []
        for r in read(teams_csv[0]):
            if pick(r, 'division', 'Division') != 'Open':
                continue
            tn = pick(r, 'team_number', 'Team Number')
            t = {'rank': len(teams) + 1, 'overall': num(pick(r, 'Rank')), 'team': tn,
                 'loc': pick(r, 'location', 'Location'), 'imgs': num(pick(r, 'images', 'Scored Images')),
                 'play': pick(r, 'play_time', 'Play Time'), 'scoreTime': pick(r, 'score_time', 'Score Time'),
                 'warn': pick(r, 'code', 'Warnings'), 'score': num(pick(r, 'ccs_score', 'CCS Score')),
                 'img': per.get(tn, {})}
            q, p, tot = pick(r, 'NetAcad Quiz'), pick(r, 'NetAcad Packet Tracer'), pick(r, 'Total')
            if tot:
                t['quiz'], t['pt'], t['total'] = round(float(q or 0), 2), round(float(p or 0), 2), round(float(tot), 2)
            r1, comb, tier = pick(r, 'R1 Score'), pick(r, 'Combined'), pick(r, 'Tier')
            if tier:
                t['tier'] = tier
            if comb:
                t['combined'], t['r1'] = round(float(comb), 2), round(float(r1 or 0), 2)
            teams.append(t)
        stats = read(os.path.join(d, f'cp19_r{rnd}_image_stats.csv'))
        # timelines
        tl = {}
        long_csv = os.path.join(d, f'cp19_r{rnd}_timelines.csv')
        if os.path.exists(long_csv):
            raw = collections.defaultdict(lambda: collections.defaultdict(list))
            for r in read(long_csv):
                k = img_key(rnd, r['Image'])
                if k and r['Score'] not in ('', 'null'):
                    raw[r['Team Number']][k].append((tomin(r['Time']), num(r['Score'])))
            for tn, imgs in raw.items():
                t0 = min(m for s in imgs.values() for m, _ in s)
                tl[tn] = {'t0': t0, **{k: ','.join(f'{m - t0},{s}' for m, s in compact(sorted(v))) for k, v in imgs.items()}}
        ours_csv = os.path.join(d, f'cp19_r{rnd}_team_{OURS[3:]}_timeline.csv')
        if os.path.exists(ours_csv) and OURS not in tl:
            imgs = collections.defaultdict(list)
            for r in read(ours_csv):
                for col, v in r.items():
                    k = img_key(rnd, col or '')
                    if k and v not in ('', 'null', None):
                        imgs[k].append((tomin(r['Time']), num(v)))
            if imgs:
                t0 = min(m for s in imgs.values() for m, _ in s)
                tl[OURS] = {'t0': t0, **{k: ','.join(f'{m - t0},{s}' for m, s in compact(sorted(v))) for k, v in imgs.items()}}
        date = f'{m.group(1)}-{m.group(2)}-{m.group(3)}'
        sdir = os.path.join(OUT, f'r{rnd}', sid)
        os.makedirs(sdir, exist_ok=True)
        json.dump({'teams': teams, 'stats': stats}, open(os.path.join(sdir, 'teams.json'), 'w'), separators=(',', ':'))
        json.dump(tl, open(os.path.join(sdir, 'timelines.json'), 'w'), separators=(',', ':'))
        snaps.append({'id': sid, 'label': f'{m.group(2)}/{m.group(3)} {m.group(4)}:{m.group(5)} CT',
                      'final': date >= ROUND_CLOSES[rnd], 'teams': len(teams), 'timelines': len(tl),
                      'official': os.path.exists(os.path.join(d, 'OFFICIAL'))})
        print(f'r{rnd} {sid}: {len(teams)} Open teams, {len(tl)} timelines, {len(stats)} stat rows')
    for s_ in snaps[:-1]:
        s_['final'] = False  # only the newest post-close pull is the final one
    if any(s_['official'] for s_ in snaps):  # official results supersede every unofficial pull
        for s_ in snaps:
            s_['final'] = s_['official']
    index['rounds'].append({'round': rnd, 'label': meta['label'],
                            'images': [[k, label] for k, label, _ in meta['images']], 'snapshots': snaps})
json.dump(index, open(os.path.join(OUT, 'index.json'), 'w'), indent=1)
print('wrote site/index.json')
