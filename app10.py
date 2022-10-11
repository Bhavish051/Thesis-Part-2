import json

TARGET_ADDRESS = "3My1dmytUPWZJa4zxsfAWBTtcwrGpDc85B"
FILE_NAME = "neighborData.json"

with open(FILE_NAME, "r") as f :
    data = f.read()
    data = json.loads(data)
    
for x in data :
    if len(x["neighbours"]) > 0 and x["address"] == TARGET_ADDRESS :
        targetNeighbours = x["neighbours"]
        

print(len(set(targetNeighbours)))
