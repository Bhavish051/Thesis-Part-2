import re
import requests
import json

# exchangeUrl = "https://rest-sandbox.coinapi.io/v1/exchanges"



def extractTransactions(data) :
    result = []
    for x in data["txs"]:
        for y in x["out"]:
            if(y.__contains__("addr")):
                if(y["addr"] is not None):
                    result.append(y["addr"])
    return result

payload={}
# exchangeHeaders = {
#   'X-CoinAPI-Key': 'AB56A202-FE3F-4007-AFDB-28BF268BB3DA',
#   'Accept': 'application/json',
#   'Accept-Encoding': 'deflate, gzip'
# }

# exhanges = requests.request("GET", exchangeUrl, headers=exchangeHeaders, data=payload)

# print(exhanges.text)


blockUrl = "https://blockchain.info/latestblock"

blockHeaders = {
    
}

latestBlock = requests.request("GET", blockUrl, headers=blockHeaders, data=payload).json()

# print(latestBlock.json())

# for key, value in latestBlock.items():
#     print(key, ":", value)

# print(latestBlock["txIndexes"][0])

fisrtTxIndexInLatestBlock = str(latestBlock["txIndexes"][0])

txUrl = "https://blockchain.info/rawtx/" + fisrtTxIndexInLatestBlock

# print(txUrl)

txHeaders = {
    
}

transactionInfo = requests.request("GET", txUrl, headers=txHeaders, data=payload).json()

# print(transactionInfo["out"][0]["addr"])

address = str(transactionInfo["out"][0]["addr"])

print(address)


addressUrl = "https://blockchain.info/rawaddr/" + address


addressHeaders = {
    
}

addressData = requests.request("GET", addressUrl, headers=addressHeaders, data=payload).json()

print(float(addressData["final_balance"])/100000000)

fileName = "./data/" + str(address) + ".json"



bitcoinAbuseUrl = "https://www.bitcoinabuse.com/api/reports/check"

abuseDBParams = {
    'address' : address,
    'api_token' : 'AypnQ9bsgY931zWSAK8NdErbZl9wf9SDrG9RI3qW'
}

isAbuseAddress = requests.request("GET", bitcoinAbuseUrl, params=abuseDBParams, headers=addressHeaders, data=payload).json()

# print(isAbuseAddress)
addressData.update(isAbuseAddress)

isMaliciousAddress = {"isMaliciousAddress" , isAbuseAddress["count"] > 0 }

print(isMaliciousAddress)



# Known Address like BTC ATM
# Probably filter through all the transaction addresses and then see if any is either malicious or known

deanonymizationUrls = ["", ""]

interactedAddresses = extractTransactions(addressData)

print(interactedAddresses)

jsonString = json.dumps(addressData, indent=4)
jsonFile = open(fileName, "w")
jsonFile.write(jsonString)
jsonFile.close()
