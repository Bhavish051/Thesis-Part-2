# Get HTML Data for the corresponding neighbours

import json

FILE_NAME = "neighborData.json"

with open(FILE_NAME, "r") as f :
    data = f.read()
    data = json.loads(data)
    
for x in data :
    if len(x["neighbours"]) > 0 :
        for x in x["neighbours"] :
            print(x)

