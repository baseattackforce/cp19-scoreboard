# Builds data.json for the site from the exported CSVs in ~/cyberpatriot. Open Division only.
import csv, json, os, collections

SRC = os.path.expanduser('~/cyberpatriot')
EXPORTED = '2026-10-25 2:02 PM CT'
REG_UPDATED = '2026-10-14'

def rows(name):
    return list(csv.reader(open(os.path.join(SRC, name))))

per_image = collections.defaultdict(dict)
for r in rows('cp19_r1_image_scores.csv')[1:]:
    key = 'win' if r[1].startswith('Windows') else 'mint'
    per_image[r[0]][key] = {'image': r[1], 'time': r[2], 'found': int(r[3]), 'remain': int(r[4]),
                            'pen': int(r[5]), 'warn': r[6], 'score': int(r[7])}

teams = []
for r in rows('cp19_r1_all_teams.csv')[1:]:
    if r[3] != 'Open':
        continue
    imgs = per_image.get(r[1], {})
    teams.append({'rank': len(teams) + 1, 'overall': int(r[0]), 'team': r[1], 'loc': r[2], 'tier': r[4],
                  'imgs': int(r[5]), 'play': r[6], 'scoreTime': r[7], 'warn': r[8], 'score': int(r[9]),
                  'win': imgs.get('win', {}).get('score'), 'mint': imgs.get('mint', {}).get('score'),
                  'detail': [imgs[k] for k in ('win', 'mint') if k in imgs]})

img = rows('cp19_r1_image_stats.csv')
images = [r for r in img[1:] if r[0] == 'Open']

schools = [{'org': r[0], 'nick': r[1], 'city': r[5], 'state': r[6], 'zip': r[7], 'country': r[8], 'coe': r[4]}
           for r in rows('cp19_registered_open_teams.csv')[1:]]

json.dump({'exported': EXPORTED, 'regUpdated': REG_UPDATED, 'teams': teams,
           'imageCols': img[0], 'images': images, 'schools': schools},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json'), 'w'), separators=(',', ':'))
print(len(teams), 'Open teams on scoreboard,', len(images), 'image stat rows,', len(schools), 'registered Open teams')
