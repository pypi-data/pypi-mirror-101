splits = 5

teams = [('team1', 'random_source'), ('team2', 'random_source2'), ('team3', 'random_source3')]
maps = ['1.txt', '2.txt', '3.txt', '4.txt', '5.txt', '6.txt', '7.txt']

total_games = (len(maps) * (len(teams) * (len(teams) - 1)) // 2)
games = [None] * total_games

index = 0
for i, (name1, script1) in enumerate(teams):
    for j, (name2, script2) in enumerate(teams[i+1:], start=i+1):
        for m in maps:
            command = f"{script1} {name1} {script2} {name2} {m}"
            games[index] = command
            index += 1

for s in range(splits):
    if s == splits - 1:
        string = "\n".join(games[(total_games//splits)*s:])
    else:
        string = "\n".join(games[(total_games//splits)*s:(total_games//splits)*(s+1)])
    with open(f"games-{s}.txt", "w") as f:
        f.write(string)

