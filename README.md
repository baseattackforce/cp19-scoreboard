# CP19 Open Division scoreboard

Static site (`index.html`) over snapshots of the public CyberPatriot 19 scoreboard and registered-teams list.
Pick a round and a snapshot, then a view: **Teams** (search, sort, per-image breakdown and score graph per team),
**Overlay** (every team's score line on each image, lined up by minutes since start, with pace and finish stats),
**Image stats**, **Schools**. The view is kept in the URL, e.g. `#r2_2026-11-13_1020_overlay`.

## Data
- `r1/snapshots/<date_time>/`, `r2/snapshots/<date_time>/`: CSV exports per pull (teams, image scores, image stats,
  score timelines). Round 1 has a graph only for our team; Round 2 10:20 and later have graphs for every Open team.
- `shared/`: registration list and inferred school names.
- `site/`: built JSON the page loads. Rebuild after adding a snapshot: `python3 build_site.py`.

Unofficial pulls may not include penalties. Round 2 also has the official results (snapshot 2026-11-23_1023, from the CyberPatriot Program Office): totals, Round 1, combined score and tier.
