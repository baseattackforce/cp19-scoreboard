# Builds data_r2.json for the site from the Round 2 CSVs in r2/ (Open Division only).
# School names and the registration list are reused from data.json (built by build.py for Round 1).
import csv, json, os, collections

HERE = os.path.dirname(os.path.abspath(__file__))
R2 = os.path.join(HERE, 'r2')
EXPORTED = '2026-11-13 9:39 AM CT'
IMGS = [('deb', 'Debian12', 'Debian'), ('win', 'Windows11', 'Windows'), ('srv', 'Server2022', 'Server')]

def rows(name):
    with open(os.path.join(R2, name), newline='') as f:
        return list(csv.DictReader(f))

r1 = json.load(open(os.path.join(HERE, 'data.json')))
schools_by_team = {t['team']: t['school'] for t in r1['teams'] if t.get('school')}

per_image = collections.defaultdict(dict)
for r in rows('cp19_r2_image_scores.csv'):
    key = next(k for k, prefix, _ in IMGS if r['image'].startswith(prefix))
    per_image[r['team_number']][key] = {'image': r['image'], 'time': r['duration'], 'found': int(r['found']),
                                        'remain': int(r['remaining']), 'pen': int(r['penalties']),
                                        'warn': r['code'], 'score': int(r['ccs_score'])}

teams = []
for r in rows('cp19_r2_all_teams.csv'):
    if r['division'] != 'Open':
        continue
    imgs = per_image.get(r['team_number'], {})
    t = {'rank': len(teams) + 1, 'overall': int(r['Rank']), 'team': r['team_number'], 'loc': r['location'],
         'tier': r['tier'], 'imgs': int(r['images']), 'play': r['play_time'], 'scoreTime': r['score_time'],
         'warn': r['code'], 'score': int(r['ccs_score']),
         'detail': [imgs[k] for k, _, _ in IMGS if k in imgs], 'school': schools_by_team.get(r['team_number'])}
    for k, _, _ in IMGS:
        t[k] = imgs.get(k, {}).get('score')
    teams.append(t)

stats = rows('cp19_r2_image_stats.csv')
cols = ['division', 'tier', 'image', 'teams', 'images', 'min_score', 'max_score', 'std_dev', 'avg_score']
image_cols = ['Division', 'Tier', 'Image', 'Teams', 'Images', 'Min Score', 'Max Score', 'Std Dev', 'Avg Score']

out = {'round': 2, 'exported': EXPORTED, 'inProgress': True, 'regUpdated': r1['regUpdated'], 'teams': teams,
       'imgCols': [[k, label] for k, _, label in IMGS],
       'imageCols': image_cols, 'images': [[r[c] for c in cols] for r in stats],
       'schools': r1['schools']}
json.dump(out, open(os.path.join(HERE, 'data_r2.json'), 'w'), separators=(',', ':'))
print(len(teams), 'Open teams,', sum(1 for t in teams if t['school']), 'with a school name,', len(stats), 'image stat rows')
