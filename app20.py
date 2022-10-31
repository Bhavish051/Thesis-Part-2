# App to store all IP Addresses and their data in KV pairs in a JSON file.
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests

with open("allAddressesData.json") as f:
    data = json.load(f)
    
with open("allUrlsData.json") as f:
    data = json.load(f)
    ips = []
    for x in data :
        for y in x['aRec']:
            ips.append(y['address'])
    print(ips)
    
def extractItems(data) :
    result = []
    for x in data : 
        result.append(x)
    return result

allIps = []
    
for x in data :
    ipAddressesFromNeighbours = []
    urlsFromNeighbours = []
    ipAddressesFromAddress = extractItems(x[6]['parsedAddressData']['ipAddresses'])
    if (len(x[7]['parsedNeighbourData']) > 0) :
        ipAddressesFromNeighbours = extractItems(x[7]['parsedNeighbourData'][0]['ipAddresses'])
    urlsFromAddress = extractItems(x[6]['parsedAddressData']['urls'])
    if (len(x[7]['parsedNeighbourData']) > 0) :
        urlsFromNeighbours = extractItems(x[7]['parsedNeighbourData'][0]['urls'])
    allIps = allIps + ipAddressesFromAddress + ipAddressesFromNeighbours
    
    
print(allIps)

l1 = allIps[0:50]
l2 = allIps[50:116]
allIpData = []

if len(l1) > 0:
    data = "["
    for x in l1:
        data = data + '"' + x + '"' + ", "

    data = data + '"' + "1.1.1.1" + '"' + "]"

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    ipData = session.post('http://ip-api.com/batch', headers= {'Content-Type': 'application/x-www-form-urlencoded'}
                    , data=data).json()
    allIpData = allIpData + ipData


if len(l2) > 0:
    data = "["
    for x in l2:
        data = data + '"' + x + '"' + ", "

    data = data + '"' + "1.1.1.1" + '"' + "]"

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    ipData = session.post('http://ip-api.com/batch', headers= {'Content-Type': 'application/x-www-form-urlencoded'}
                    , data=data).json()
    allIpData = allIpData + ipData


if len(ips) > 0:
    data = "["
    for x in ips:
        data = data + '"' + x + '"' + ", "

    data = data + '"' + "1.1.1.1" + '"' + "]"

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    ipData = session.post('http://ip-api.com/batch', headers= {'Content-Type': 'application/x-www-form-urlencoded'}
                    , data=data).json()
    allIpData = allIpData + ipData

print(allIpData)

with open('allIpData.json', 'w') as f:
    json.dump(allIpData, f)