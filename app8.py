import requests
import time

with open("addressesWithData.txt", "r") as f :
    lines = f.readlines()
    
lines = lines[0].split(",")


def extractNeighbours(address) :
    time.sleep(10)
    addressUrl = "https://blockchain.info/rawaddr/" + address
    data = requests.request("GET", addressUrl)
    result = []
    if (data.status_code == 200) :
        data = data.json()
        if (data.__contains__("txs")):
            for x in data["txs"]:
                for y in x["out"]:
                    if(y.__contains__("addr")):
                        if(y["addr"] is not None):
                            result.append(y["addr"])
                for y in x["inputs"]:
                    if(y.__contains__("addr")):
                        if(y["addr"] is not None):
                            result.append(y["addr"])
    print(result)
    return result


neighborData = []

for x in lines :
    x = x.split(".")[0]
    neighborData.append({"address" : x, "neighbours" : extractNeighbours(x)})
    
with open("neighborData.json", "w") as f :
    f.write(str(neighborData))