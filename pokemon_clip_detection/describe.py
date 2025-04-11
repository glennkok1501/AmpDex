import re
import ollama
from io import BytesIO
import base64
import os
import json 
import time

def numerically_sorted_files(folder):
    files = os.listdir(folder)
    sorted_files = sorted(files, key=lambda x: int(x.split('_')[0]))
    return sorted_files

pokemons = [json.load(open(f"./data/{i}", "r")) for i in numerically_sorted_files('./data')]

with open("pokemon_clip_data.txt", "w") as f:
    try:
        for pokemon in pokemons:
            name = pokemon['species']["name"]

            image_path = f"./images/{pokemon['id']}_{name}.png"

            # Open the image file in binary mode and read it
            with open(image_path, "rb") as g:
                image_bytes = g.read()
                g.close()

            # Use BytesIO if needed elsewhere (not required for base64 encoding)
            buffer = BytesIO(image_bytes)

            # Encode to base64
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

            response = ollama.generate(
                    model="llava",
                    prompt=f'Describe the appearance of this Pokemon {name} in detail in a single paragraph: This Pokémon is a [size description, e.g., small, large, etc.] creature with a [color] body. Its [distinctive feature, e.g., long tail, wings, fins, etc.] is [description of how the feature looks]. The Pokémon has [eye shape, size, and color], and its [facial features or additional body features like horns, ears, etc.] are [description]. It has [distinctive markings, patterns, or textures] on its [body parts like legs, back, etc.], which make it easily recognizable. Its overall shape is [round, angular, etc.], and it typically appears [standing, flying, swimming, lying, sleeping, crawling etc.]',
                    images=[image_base64],
                    stream=False
                )

            result = (response.get("response", {}))
            result = re.sub(r'[^\x00-\x7F]+', '', result)

            f.write(f"{name}.{result}\n")

            print(f"{name} - {round((int(pokemon['id']) / len(pokemons)) * 100, 2)}%")
            time.sleep(3)
        f.close()
    except Exception as e:
        print(e)
        f.close()