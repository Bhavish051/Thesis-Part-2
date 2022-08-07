import requests
import json

knownAddresses = ["a1", "a2"] # Need to figure out how to get addresses of like BTC atms and stuff otherwise will need to spend an entire day just to go around sydney and get BTC ATMs Addresses

blockUrl = "https://blockchain.info/latestblock"
exchangeUrl = "https://rest-sandbox.coinapi.io/v1/exchanges"
bitcoinAbuseUrl = "https://www.bitcoinabuse.com/api/reports/check"
bitcoinWhoSWhoUrl = ""

def extractTransactions(data) :
    result = []
    if (data.__contains__("txs")):
        for x in data["txs"]:
            for y in x["out"]:
                if(y.__contains__("addr")):
                    if(y["addr"] is not None):
                        result.append(y["addr"])
    else :
        print("no data found for the given address")
    return result

payload={}

# exchangeHeaders = {
#   'X-CoinAPI-Key': 'AB56A202-FE3F-4007-AFDB-28BF268BB3DA',
#   'Accept': 'application/json',
#   'Accept-Encoding': 'deflate, gzip'
# }

# exhanges = requests.request("GET", exchangeUrl, headers=exchangeHeaders, data=payload)

# print(exhanges.text)


blockHeaders = {
    
}

latestBlock = requests.request("GET", blockUrl, headers=blockHeaders, data=payload).json()
# print(latestBlock.text)

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

# print(address)

# addressFromUser = input("What is the address you want to check? \n")

# print(addressFromUser)

# if(addressFromUser is not None):
#     address = addressFromUser

print(address)

addressUrl = "https://blockchain.info/rawaddr/" + address

addressHeaders = {
    
}

addressData = requests.request("GET", addressUrl, headers=addressHeaders, data=payload)
if addressData is not None :
    addressData = addressData.json()

# print(float(addressData["final_balance"])/100000000)

fileName = "./data/" + str(address) + ".json"

abuseDBParams = {
    'address' : address,
    'api_token' : 'AypnQ9bsgY931zWSAK8NdErbZl9wf9SDrG9RI3qW'
}

isAbuseAddress = requests.request("GET", bitcoinAbuseUrl, params=abuseDBParams, headers=addressHeaders, data=payload).json()

# print(isAbuseAddress)
addressData.update(isAbuseAddress)

isMaliciousAddress = {"isMaliciousAddress" , isAbuseAddress["count"] > 0 }

# print(isMaliciousAddress)

# Known Address like BTC ATM
# Probably filter through all the transaction addresses and then see if any is either malicious or known

# deanonymizationUrls = ["", ""]

interactedAddresses = extractTransactions(addressData)

for x in interactedAddresses : 
    interactedAddressUrl = "https://blockchain.info/rawaddr/" + x
    intereactedAddressData = requests.request("GET", interactedAddressUrl, headers=addressHeaders, data=payload)
    if (intereactedAddressData is not None) :
        interactedJson = intereactedAddressData.json()
        print(intereactedAddressData)    
# def checkIfIteractedWithAbuseAddress(data) :
#     print(len(data))
#     i = 0
#     for x in data :
#         res = []
#         result =requests.request("GET", bitcoinAbuseUrl, 
#                                  params={
#                                     'address':x,
#                                     'api_token' : 'AypnQ9bsgY931zWSAK8NdErbZl9wf9SDrG9RI3qW'
#         }, headers=addressHeaders, data=payload).json()
#         i = i + 1
#         print(i)
#         print(result)
#         res.append(result)
#     return res

# hasInteractedWithAbuseAddress = checkIfIteractedWithAbuseAddress(interactedAddresses)

abuseDBReportURL = "https://www.bitcoinabuse.com/api/download/30d"

# def downloadFullAbuseDBReport() :
#     res = requests.request("GET", abuseDBReportURL, params={
#             'time_period' : '30d',
#             'api_token' : 'AypnQ9bsgY931zWSAK8NdErbZl9wf9SDrG9RI3qW'
#         }, headers=addressHeaders, data=payload)
#     print(res)
#     f = open("./reports/abuseDBReport.csv", "w")
#     writer = csv.writer(f)
#     writer.writerows(res)
#     f.close()

# downloadFullAbuseDBReport()

# hasInteractedWithAbuseAddress = True

# jS = json.dumps(hasInteractedWithAbuseAddress, indent=4)
# jF = open("interaction.json", "w")
# jF.write(jS)
# jF.close()

# print(interactedAddresses)
# print(hasInteractedWithAbuseAddress)

if (addressData.__contains__("message")) :
    if (addressData["message"].__eq__("Item not found or argument invalid")) :
        print("No Data")    
        

print(addressData)
jsonString = json.dumps(addressData, indent=4)
jsonFile = open(fileName, "w")
jsonFile.write(jsonString)
jsonFile.close()