from poke_clip import detect


id = 754
# Example usage with an image URL
# image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{id}.png"
image_url = f"https://m.media-amazon.com/images/I/71nbfl-JklS.jpg"
top_results = detect(image_url, 10)
for result in top_results:
    print(f"Detected Pokémon: {result['pokemon']} with confidence: {result['conf']:.4f}")