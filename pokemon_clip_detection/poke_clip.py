import json
import torch
import clip
from PIL import Image
import requests
from io import BytesIO
from torchvision import models, transforms
from scipy.spatial.distance import cosine
from torchvision.models import ResNet50_Weights
import os

# ==== Configurable Weights ====
CLIP_WEIGHT = 0.8
RESNET_WEIGHT = 0.3
TOP_N = 3

# ==== Device Setup ====
device = "cuda" if torch.cuda.is_available() else "cpu"

# ==== Load Models ====
clip_model, clip_preprocess = clip.load("ViT-B/32", device=device)
resnet = models.resnet50(weights=ResNet50_Weights.DEFAULT).eval().to(device)

# ==== Preprocessing ====
resnet_preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# ==== Load Pokédex ====
with open("pokemon_clip_data.json", "r") as f:
    pokedex = json.load(f)

# ==== Preload Pokédex Images and Embeddings ====
pokedex_embeddings = []

@torch.inference_mode()
def preprocess_pokedex():
    descriptions = [entry["description"][:77] for entry in pokedex]
    text_tokens = clip.tokenize(descriptions).to(device)
    text_features = clip_model.encode_text(text_tokens)
    text_features /= text_features.norm(dim=-1, keepdim=True)

    for i, entry in enumerate(pokedex):
        image_path = entry["image"]
        if not os.path.exists(image_path):
            print(f"Missing image: {image_path}")
            continue
        img = Image.open(image_path).convert("RGB")

        clip_img_embed = clip_model.encode_image(clip_preprocess(img).unsqueeze(0).to(device))
        clip_img_embed /= clip_img_embed.norm(dim=-1, keepdim=True)

        resnet_embed = resnet(resnet_preprocess(img).unsqueeze(0).to(device)).squeeze().cpu().numpy()

        pokedex_embeddings.append({
            "id": entry["id"],
            "name": entry["name"],
            "clip_text": text_features[i].cpu(),
            "clip_img": clip_img_embed.squeeze(0).cpu(),
            "resnet": resnet_embed
        })

preprocess_pokedex()

# ==== Utility Functions ====

@torch.inference_mode()
def get_clip_embedding(image):
    tensor = clip_preprocess(image).unsqueeze(0).to(device)
    emb = clip_model.encode_image(tensor)
    return (emb / emb.norm(dim=-1, keepdim=True)).squeeze(0).cpu()

@torch.inference_mode()
def get_resnet_embedding(image):
    tensor = resnet_preprocess(image).unsqueeze(0).to(device)
    return resnet(tensor).squeeze().cpu().numpy()

def load_image(input_path, from_url=True):
    data = requests.get(input_path).content if from_url else open(input_path, "rb").read()
    return Image.open(BytesIO(data)).convert("RGB")

def cosine_similarity(v1, v2):
    return 1 - cosine(v1, v2)

# ==== Detection ====
def detect(image_input, top_n=TOP_N, image_from_url=True):
    image = load_image(image_input, from_url=image_from_url)
    clip_embed = get_clip_embedding(image)
    resnet_embed = get_resnet_embedding(image)

    results = []
    for entry in pokedex_embeddings:
        clip_score = torch.dot(clip_embed, entry["clip_text"]).item()
        resnet_score = cosine_similarity(resnet_embed, entry["resnet"])
        score = CLIP_WEIGHT * clip_score + RESNET_WEIGHT * resnet_score
        results.append((score, entry["id"], entry["name"]))

    results.sort(reverse=True)
    return [{"id": id_, "pokemon": name, "conf": score} for score, id_, name in results[:top_n]]
