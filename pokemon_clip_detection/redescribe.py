import ollama
import re
import time
# Read Pokémon data from file
with open('pokemon_clip_data.txt', 'r') as file:
    d = file.read().split('\n')

# List to store the shortened descriptions
new = []

# Loop over the lines in your file
count = 0
for i in d:
    try:
        # Generate a summarized version of each description using the model
        response = ollama.chat(
            model="llama3",
            messages=[{
                'role': 'user',
                'content': f'Summarize the following Pokémon description into a shorter version while keeping the same meaning. The summary should be concise, in a single sentence, no more than 50 words, and should highlight the most important features of the Pokémon: {i}'
            }]
        )

        # Extract the result from the response
        result = response["message"]["content"]
        # Clean up the result (remove non-ASCII characters)
        result = re.sub(r'[^\x00-\x7F]+', '', result)

        if len(result.split("\n")) > 1:
            result = result.split("\n")[2]

        new.append(result.strip())

        count += 1
        print(f"{result} - {round((count / len(d)) * 100, 2)}%")
        time.sleep(2.5)
    except Exception as e:
        print(f"Error summarizing description: {i}\nError: {e}")
        continue

# Optionally, save the summaries to a new file
with open('summarized_pokemon.txt', 'w') as f:
    for summary in new:
        f.write(summary + '\n')
    f.close()
