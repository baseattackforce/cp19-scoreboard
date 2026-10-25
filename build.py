# Builds data.json for the site from the exported CSVs in ~/cyberpatriot.
import csv, json, glob, os, collections

SRC = os.path.expanduser('~/cyberpatriot')
CHUNKS = os.environ.get('CHUNKS', '')
EXPORTED = '2026-10-25 2:02 PM CT'

def rows(name):
    return list(csv.reader(open(os.path.join(SRC, name))))

per_image = collections.defaultdict(dict)
for r in rows('cp19_r1_image_scores.csv')[1:]:
    key = 'win' if r[1].startswith('Windows') else 'mint'
    per_image[r[0]][key] = {'image': r[1], 'time': r[2], 'found': int(r[3]), 'remain': int(r[4]),
                            'pen': int(r[5]), 'warn': r[6], 'score': int(r[7])}

teams = []
for r in rows('cp19_r1_all_teams.csv')[1:]:
    imgs = per_image.get(r[1], {})
    teams.append({'rank': int(r[0]), 'team': r[1], 'loc': r[2], 'div': r[3], 'tier': r[4], 'imgs': int(r[5]),
                  'play': r[6], 'scoreTime': r[7], 'warn': r[8], 'score': int(r[9]),
                  'win': imgs.get('win', {}).get('score'), 'mint': imgs.get('mint', {}).get('score'),
                  'detail': [imgs[k] for k in ('win', 'mint') if k in imgs]})

img = rows('cp19_r1_image_stats.csv')

schools = []
for f in sorted(glob.glob(os.path.join(CHUNKS, 'chunks_*.csv'))):
    for lat, lon, n, matches in csv.reader(open(f)):
        m = json.loads(matches)
        schools.append({'name': m[0][1] if m else '(no school found nearby)',
                        'dist': m[0][0] if m else None,
                        'teams': int(n), 'lat': lat, 'lon': lon})

json.dump({'exported': EXPORTED, 'total': len(teams), 'teams': teams,
           'imageCols': img[0], 'images': img[1:], 'schools': schools},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json'), 'w'), separators=(',', ':'))
print(len(teams), 'teams,', sum(1 for t in teams if t['detail']), 'with image detail,', len(schools), 'school locations')
