# find the number of scam alerts recieved from BTC who is WHO
# Cross check that with BTCAbuseDB to see what it says
# Create stats on the number of scam alerts recieved from BTC who is WHO based on what AbuseDB say 
# Ie these many legal addresses have scam alerts (False Positives) and these many illegal addresses have scam alerts (True Positives)

import requests

def extractNeighbours(data) :
    result = []
    if (data.__contains__("txs")):
        print("Extracting Neighbours now")
        for x in data["txs"]:
            for y in x["out"]:
                if(y.__contains__("addr")):
                    if(y["addr"] is not None):
                        result.append(y["addr"])
            for y in x["inputs"]:
                if(y.__contains__("addr")):
                    if(y["addr"] is not None):
                        result.append(y["addr"])
    else :
        print("No Neighbours found")
    return result


address =  input("What is the address you want to check? \n")

addressUrl = "https://blockchain.info/rawaddr/" + address
addressData = requests.request("GET", addressUrl).json()

neighbours = set(extractNeighbours(addressData))

