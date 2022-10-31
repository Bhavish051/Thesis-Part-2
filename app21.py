import json
import validators
import requests

with open("allAddressesData.json") as f :
    data = json.load(f)
    
API_KEY = "29c8509c-6105-42c6-a7c1-1e5cf5699960"

allUrls = []

def extractItems(data) :
    result = []
    for x in data : 
        result.append(x)
    return result

whiteListedUrls = ["https://www.iplocation.net", "https://whatismyip.live", "https://bitcoinwhoswho.com", "https://blockchain.info", "https://support.google.com", "https://community.mimecast.com", "https://twitter.com", "https://www.blockchain.com", "https://aim2dchinabusinessnews.wordpress.com"]

def fixList(data) :
    result = []
    for x in data :
        for y in x :
            result.append(y)
    finalResult = []
    for x in result :
        if (validators.url(x)) and x not in whiteListedUrls :
            finalResult.append(x)
    return finalResult

def performReverseDNS(data): 
    print("Performing reverse DNS lookup")

    aRec = []
    for x in data :
        d = requests.post("https://api.geekflare.com/dnsrecord", json={"url": x}, headers={"x-api-key" : API_KEY}).json()
        if (d.__contains__('apiStatus') and d['apiStatus'] == 'success') :
            aRec.append({'address' : x , 'aRec' : d['data']['A']})
            print(aRec)
    return aRec
    
for x in data : 
    urlsFromAddress = extractItems(x[6]['parsedAddressData']['urls'])
    urlsFromNeighbours = []
    if (len(x[7]['parsedNeighbourData']) > 0) :
        urlsFromNeighbours = extractItems(x[7]['parsedNeighbourData'][0]['urls'])
    allUrls = allUrls + urlsFromAddress + urlsFromNeighbours

allUrls = fixList(allUrls)

data = performReverseDNS(allUrls)
with open("allUrlsData.json", "w") as f :
    json.dump(data, f)
# print(allUrls)