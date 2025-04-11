from poke_clip import detect
import time
from datetime import datetime

ARTWORK_LINK = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home"
# ARTWORK_LINK = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork"

results = []
TOTAL = 1025
accuracy = TOTAL

now = datetime.now()
print("Running...")

for i in range(1, TOTAL+1):
    data = {
        "id": i,
        "confidence": "0",
        "result": "FAIL",
        "score": 1
    }

    image_url = f"{ARTWORK_LINK}/{i}.png"
    top_results = detect(image_url, 10)

    for result in top_results:
        if int(result["id"]) == i:
            data["result"] = "PASS"
            data["confidence"] = result["conf"]
            break
        else:
            data["score"] -= 0.1

    if data["score"] < 0:
        data["score"] = 0

    current_acc = (1 - data["score"])
    results.append(data)
    accuracy -= current_acc
    print(f"{i}/{TOTAL} ({round((i/TOTAL) * 100, 2)}%) - [{data['result']} ({round(data['score']*100,3)}%)] | current accuracy: {round((accuracy / TOTAL) *100 , 3)}%")

    # time.sleep(1.5)

    # For testing
    # if i == 3:
    #     break

formatted = now.strftime("%Y-%m-%d-%H-%M-%S")
with open(f"benchmark_results_{formatted}.csv", "w") as f:
    f.write(f"Accuracy: {(accuracy / TOTAL) * 100}%\n")
    
    f.write(f"id,confidence,score,result\n")
    for i in results:
        f.write(f"{i['id']},{round(float(i['confidence']),3)},{round(i['score'],3)},{i['result']}\n")
    f.close()
print("completed")