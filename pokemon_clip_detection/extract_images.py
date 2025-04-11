import os
import json
import requests
from PIL import Image
from io import BytesIO

folder = './data'

datasets = os.listdir(folder)

def download(url, filename):
		
		response = requests.get(url)

		if response.status_code == 200:
			img = Image.open(BytesIO(response.content))
			# resized_img = img.resize((640, 640))
			img.save(f"./images/{filename}")
			print(f"{filename} - saved")

for i in datasets:
	with open(f"{folder}/{i}", 'r') as f:
		pokemon = json.load(f)
		
		download((pokemon["sprites"]["other"]["official-artwork"]['front_default']), f'{i.split(".")[0]}.png')
		f.close()