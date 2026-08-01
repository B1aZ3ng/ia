import json
with open("src/games.json") as file:
    games = json.load(file)

print (games["Minecraft"]['ServerTypes'])