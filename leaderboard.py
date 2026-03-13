from collections import defaultdict

file_path = "weekly_shorts.txt"
max_points_file = "max_points.txt"

week_wins = defaultdict(int)
map_wins = defaultdict(int)
top5 = defaultdict(int)
max_points = {}  # Max Points metric

# ---------- Parse weekly data ----------
with open(file_path, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

for line in lines:

    # Week winner
    if line.startswith("Week"):
        parts = line.split()
        winner = parts[-1]
        week_wins[winner] += 1

    # Map placements
    elif line[0].isdigit() and "." in line:
        position, player = line.split(".", 1)
        position = int(position)
        player = player.strip()

        # Count top5
        top5[player] += 1

        # Count map wins
        if position == 1:
            map_wins[player] += 1

players = set(list(week_wins.keys()) + list(map_wins.keys()) + list(top5.keys()))

# ---------- Read Max Points from separate file ----------
max_points_file = "max_points.txt"
max_points = {}
max_points_week = {}

with open(max_points_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            if '(' in line and ')' in line:
                main, week_part = line.split('(', 1)
                week_part = week_part.replace(')','').strip()
                week_num = ''.join(filter(str.isdigit, week_part))
            else:
                main = line
                week_num = ""
            
            parts = main.strip().split()
            player = parts[0]
            points = int(parts[1])
            
            max_points[player] = points
            max_points_week[player] = week_num
        except Exception as e:
            print(f"Failed to parse line: {line} ({e})")

# ---------- Console leaderboard ----------
print("\nLEADERBOARD\n")
ranking = sorted(
    players,
    key=lambda p: (week_wins[p], map_wins[p], top5[p]),
    reverse=True
)

print(f"{'RANK':<5} {'PLAYER':<18} {'WEEKS':<6} {'MAPS':<6} {'TOP5':<6}")
print("-" * 45)

for i, p in enumerate(ranking, start=1):
    print(
        f"{i:<5} "
        f"{p:<18} "
        f"{week_wins[p]:<6} "
        f"{map_wins[p]:<6} "
        f"{top5[p]:<6}"
    )

# ---------- Rankings ----------
def print_ranking(title, stat_dict):
    print(f"\n{title}")
    print("-" * 30)
    ranking = sorted(stat_dict.items(), key=lambda x: x[1], reverse=True)
    for i, (player, value) in enumerate(ranking, start=1):
        print(f"{i:2}. {player:15} {value}")

print_ranking("WEEKLY WINNERS RANKING", week_wins)
print_ranking("MAP WINS RANKING", map_wins)
print_ranking("TOP5 APPEARANCES RANKING", top5)

# ---------- HTML leaderboard with Max Points ----------
html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Greece Shorts Leaderboard</title>
<style>
body{
    font-family: Arial;
    background:#0f172a;
    color:white;
    text-align:center;
}
h1{
    margin-top:40px;
}
.container{
    display:flex;
    justify-content:center;
    gap:30px;
    margin-top:30px;
    align-items:flex-start;
}
table{
    border-collapse:collapse;
    background:#1e293b;
}
th, td{
    padding:8px 12px;
    border-bottom:1px solid #334155;
}
th{
    background:#334155;
    cursor:pointer;
}
tr:hover{
    background:#475569;
}
.rank1{color:gold;font-weight:bold;}
.rank2{color:silver;font-weight:bold;}
.rank3{color:#cd7f32;font-weight:bold;}

.sort-arrow{
    font-size:0.7em;
    opacity:0.7;
    margin-left:4px;
}

.tooltip{
    position:relative;
}

.tooltip-icon svg{
    vertical-align: middle;
    margin-left: 4px;
    opacity:0.8;
    cursor: pointer;
}

.tooltip:hover::after{
    content:attr(data-tooltip);
    position:absolute;
    bottom:120%;
    left:50%;
    transform:translateX(-50%);
    background:#020617;
    color:white;
    padding:6px 8px;
    font-size:0.8em;
    border-radius:6px;
    white-space:nowrap;
    border:1px solid #334155;
}

.refresh-icon svg {
    vertical-align: middle;
    margin-left: 4px;
    opacity: 0.7;
    cursor: pointer;
    transition: transform 0.2s ease;
}

.refresh-icon svg:hover {
    transform: rotate(20deg);
    opacity: 1;
}

/* Max Points table specific */
.maxpoints-table{
    min-width:180px;
    font-size:0.9em;
}
.maxpoints-table th{
    background:#334155;
}
.maxpoints-table tr:hover{
    background:#475569;
}
</style>
</head>
<body>
<h1>🏆 Greece Weekly Shorts Leaderboard</h1>
<div class="container">

<!-- Main leaderboard -->
<table id="leaderboard">
<thead>
<tr>
<th>Rank</th>
<th>Player</th>
<th onclick="sortTable(2)" title="Reset leaderboard to original ranking">
  Weeks Won
  <span class="refresh-icon">
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="23 4 23 10 17 10"></polyline>
      <path d="M20.49 15a9 9 0 1 1-2.21-9.79"></path>
    </svg>
  </span>
</th>
<th onclick="sortTable(3)" class="tooltip" data-tooltip="Total #1 Greece finishes on maps">Greece Records <span class="sort-arrow">▲▼</span></th>
<th onclick="sortTable(4)" class="tooltip" data-tooltip="Total top5 Greece finishes on maps">Top5 <span class="sort-arrow">▲▼</span></th>
</tr>
</thead>
<tbody>
"""

ranking = sorted(
    players,
    key=lambda p: (week_wins[p], map_wins[p], top5[p]),
    reverse=True
)

for i, p in enumerate(ranking, start=1):
    rank_class = ""
    if i == 1: rank_class = "rank1"
    elif i == 2: rank_class = "rank2"
    elif i == 3: rank_class = "rank3"
    html += f"<tr class='{rank_class}'><td>{i}</td><td>{p}</td><td>{week_wins[p]}</td><td>{map_wins[p]}</td><td>{top5[p]}</td></tr>\n"

html += """
</tbody>
</table>
"""

# Max Points table
html += """
<table class="maxpoints-table">
<tr>
<th>Rank</th>
<th>Player</th>
<th>
Max Points
<span class="tooltip tooltip-icon" data-tooltip="Highest score achieved in a single week">
<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"></circle>
  <line x1="12" y1="16" x2="12" y2="12"></line>
  <line x1="12" y1="8" x2="12" y2="8"></line>
</svg>
</span>
</th>
<th>Week</th>
</tr>
"""

for i, (player, points) in enumerate(sorted(max_points.items(), key=lambda x: x[1], reverse=True), start=1):
    rank_class = ""
    if i == 1: rank_class = "rank1"
    elif i == 2: rank_class = "rank2"
    elif i == 3: rank_class = "rank3"
    
    week_str = max_points_week.get(player, "")
    html += f"<tr class='{rank_class}'><td>{i}</td><td>{player}</td><td>{points}</td><td>{week_str}</td></tr>\n"

html += """
</table>

</div>

<script src="sort.js"></script>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("HTML leaderboard generated → index.html")