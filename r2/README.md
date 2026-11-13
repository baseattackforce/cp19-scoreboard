# CP19 Round 2 scoreboard snapshot

Snapshot of the public CyberPatriot scoreboard (scoreboard.uscyberpatriot.org), pulled **2026-11-13 09:39 CT**.
The round was still open (it runs through Sunday 2026-11-15), so these are partial results. Scores are unofficial:
penalties and adjustments are applied later by the CyberPatriot Program Office.

| File | Rows | What |
|---|---|---|
| `cp19_r2_all_teams.csv` | 1106 | every team, in scoreboard order (Rank = overall, Division Rank within its division) |
| `cp19_r2_image_scores.csv` | 2979 | every team x image: time, found, remaining, penalties, warnings, score |
| `cp19_r2_image_stats.csv` | 3 | per image, all divisions: teams, min, max, std dev, average |
| `cp19_r2_timelines.csv` | 10603 | score-over-time points (5-minute steps) for the top 100 Open teams |
| `overlay_data.json` | 100 teams | same timelines, re-based to minutes since each team started, plus the pace/plateau analysis |
| `raw/` | | the API responses as returned |

Endpoints (GET, public): `/api/team/scores.php`, `/api/image/scores.php`,
`/api/image/stats.php?division=All&tier=All&image=Any`, `/api/image/chart.php?team[]=...` (accepts up to 10 teams).

Images: `Debian12_cp19_intro_r2_hsms` (19 items), `Windows11_cp19_intro_r2_hsms` (19), `Server2022_cp19_r2_hs` (23).
