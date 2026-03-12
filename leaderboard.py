from collections import defaultdict

file_path = "weekly_shorts.txt"

week_wins = defaultdict(int)
map_wins = defaultdict(int)
top5 = defaultdict(int)

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


# ---------- RANKINGS ----------

def print_ranking(title, stat_dict):

    print(f"\n{title}")
    print("-" * 30)

    ranking = sorted(stat_dict.items(), key=lambda x: x[1], reverse=True)

    for i, (player, value) in enumerate(ranking, start=1):
        print(f"{i:2}. {player:15} {value}")


print_ranking("WEEKLY WINNERS RANKING", week_wins)
print_ranking("MAP WINS RANKING", map_wins)
print_ranking("TOP5 APPEARANCES RANKING", top5)

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

table{
    margin:auto;
    border-collapse:collapse;
    width:60%;
    background:#1e293b;
}

th, td{
    padding:10px;
    border-bottom:1px solid #334155;
}

th{
    background:#334155;
}

tr:hover{
    background:#475569;
}

.rank1{color:gold;font-weight:bold;}
.rank2{color:silver;font-weight:bold;}
.rank3{color:#cd7f32;font-weight:bold;}

</style>
</head>

<body>

<h1>🏆 Greece Shorts Leaderboard</h1>

<table>
<tr>
<th>Rank</th>
<th>Player</th>
<th>Weeks Won</th>
<th>Map Wins</th>
<th>Top5</th>
</tr>
"""
ranking = sorted(
    players,
    key=lambda p: (week_wins[p], map_wins[p], top5[p]),
    reverse=True
)

for i, p in enumerate(ranking, start=1):

    rank_class = ""
    if i == 1:
        rank_class = "rank1"
    elif i == 2:
        rank_class = "rank2"
    elif i == 3:
        rank_class = "rank3"

    html += f"""
<tr class="{rank_class}">
<td>{i}</td>
<td>{p}</td>
<td>{week_wins[p]}</td>
<td>{map_wins[p]}</td>
<td>{top5[p]}</td>
</tr>
"""

html += """
</table>

<p style="margin-top:40px;">Updated automatically</p>

</body>
</html>
"""

with open("index.html","w",encoding="utf-8") as f:
    f.write(html)

print("HTML leaderboard generated → index.html")