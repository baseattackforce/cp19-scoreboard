# CP19 Round 2 scoreboard snapshot

Snapshot of the public CyberPatriot scoreboard (scoreboard.uscyberpatriot.org), pulled **2026-11-13 09:39 CT**.
The round was still open (it runs through Sunday 2026-11-15), so these are partial results. Scores are unofficial:
penalties and adjustments are applied later by the CyberPatriot Program Office.

Each pull is a folder in snapshots/<date_time>/ with cp19_r2_all_teams.csv, cp19_r2_image_scores.csv,
cp19_r2_image_stats.csv, cp19_r2_timelines.csv (score-over-time, long format) and raw/ (API responses).
- 2026-11-13_0939: 697 Open teams, graphs for the top 100 Open teams
- 2026-11-13_1020: 749 Open teams, graphs for all 749

Endpoints (GET, public): /api/team/scores.php, /api/image/scores.php,
/api/image/stats.php?division=All&tier=All&image=Any, /api/image/chart.php?team[]=... (up to 10 teams per call).
Images: Debian12_cp19_intro_r2_hsms (19 items), Windows11_cp19_intro_r2_hsms (19), Server2022_cp19_r2_hs (23).
