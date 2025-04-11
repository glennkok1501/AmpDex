import os
import json

IMAGES = "./images"
DATA = "./data"

def numerically_sorted_files(folder):
    files = os.listdir(folder)
    sorted_files = sorted(files, key=lambda x: int(x.split('_')[0]))
    return sorted_files

pokemons = [i.split('.')[0] for i in numerically_sorted_files(DATA)]
descriptions = open("summarized_pokemon.txt", "r").read().split("\n")
formatted = []
for i in range(len(pokemons)):
    des = descriptions[i]
    name = pokemons[i].split("_")[1].title()

    formatted.append(
        {
            "id": i+1,
            "name": name,
            "description": des,
            "image": f"{IMAGES}/{pokemons[i]}.png"
        }
    )

with open("pokedex.json", 'w+') as f:
    f.write(json.dumps(formatted, indent=4))
    f.close()