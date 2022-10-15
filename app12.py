import json


with open("neighborData.json", "r") as f :
    data = f.read()
    data = json.loads(data)
    
allNeighbours = []

for x in data :
    for y in x["neighbours"] :
        allNeighbours.append(y)
    
allNeighbours = set(allNeighbours)
print(len(allNeighbours))