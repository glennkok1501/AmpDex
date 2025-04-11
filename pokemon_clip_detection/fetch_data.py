import requests
import json 
import os

endpoint = "https://pokeapi.co/api/v2/pokemon"
pokemons = []
limit = 1025

files = os.listdir('./data')
if files:
	for i in files:
		os.remove(f'./data/{i}')
	print("data cleared")

for i in range(limit):
	pokemon = requests.get(f"{endpoint}/{i+1}").json()
	name = pokemon['species']["name"]

	with open(f"./data/{pokemon['id']}_{name}.json", 'w+') as f:
		json.dump(pokemon, f)

	print(f"{name} - Loaded")