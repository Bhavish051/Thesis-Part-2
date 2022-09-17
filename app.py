import requests
import json
from bs4 import BeautifulSoup
import os
import spacy
from progressbar import ProgressBar, Percentage, Bar, ETA

pbar = ProgressBar()

spacy.load('en_core_web_sm')

knownAddresses = ["a1", "a2"] # Need to figure out how to get addresses of like BTC atms and stuff otherwise will need to spend an entire day just to go around sydney and get BTC ATMs Addresses

blockUrl = "https://blockchain.info/latestblock"
exchangeUrl = "https://rest-sandbox.coinapi.io/v1/exchanges"
bitcoinAbuseUrl = "https://www.bitcoinabuse.com/api/reports/check"


def checkIsAddressKnownOrHasInteractedWithKnown(set, address) :
    res = False
    for x in knownAddresses :
        if x in set :
            print("Our address has interacted with " + x + "which is known")
            res = True
    if address in knownAddresses :
        print("Our address is known")
        res = True
    return res


def extractTransactions(data) :
    result = []
    if (data.__contains__("txs")):
        print("Extracting Neighbours now")
        for x in pbar(data["txs"]):
            for y in x["out"]:
                if(y.__contains__("addr")):
                    if(y["addr"] is not None):
                        result.append(y["addr"])
            for y in x["inputs"]:
                if(y.__contains__("addr")):
                    if(y["addr"] is not None):
                        result.append(y["addr"])
    else :
        print("no data found for the given address")
    return result

def extractAddressMetaData(address) : 
    btcWhoIsWhoUrl = "https://www.bitcoinwhoswho.com/address/" + address
    data = requests.request("GET",btcWhoIsWhoUrl, headers={}, data={})
    # print(data.status_code)
    if (data is not None) :
        with open(address + ".html", "w") as outfile:
            outfile.write(data.text)
    # print(btcWhoIsWhoUrl)
    return data.text

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

testUrl = "https://www.bitcoinwhoswho.com/address/16bHkVFULVmxTGVi2XKpwzkt5KrRnThzPg"

data = requests.request("GET", testUrl, headers=addressHeaders, data=payload).text

# os.remove("data.html")

with open("data.html", "w") as fp:
    fp.write(data)

with open("data.html") as fp:
    soup = BeautifulSoup(fp, "html.parser")
    # print("Head tag is : \n")
    # print(soup.body)

html = extractAddressMetaData(address)

parsedHtml = BeautifulSoup(open(str(address) + ".html"), "html.parser")

# print()

res = parsedHtml.body.find_all("div", {"id": "wrapper"})

finalSection = object()

for result in res : 
    for d in result.find_all("section", {"id": "content"}) :
        for x in d.find_all("div", {"id" : "search_address_index", "class" : "container"}) :
            for y in x.find_all("div", {"class" : "row"}) :
                for z in y.find_all("div", {"class" : "col-lg-12"}) :
                    for w in z.find_all("div", {"class" : "row"}) :
                        for z in w.find_all("div", {"class" : "col-lg-12 float_left_box"}) :
                            for x in z.find_all("div", {"class" : "row text-center"}) :
                                for z in x.find_all("div", {"class" : "col-lg-12"}) :
                                    for y in z.find_all("div", {"class" : "float_left_box flb_scam_records_table"}) :
                                        for x in y.find_all("div", {"class" : "collapse", "id" : "scam_records_table"}) :
                                            for z in x.find_all("div", {"class" : "row row_odd hide", "id" : "scam_info_71212"}) :
                                    # Working till here something going on down here for some addresses
                                                if z is not None : 
                                                    finalSection = z.find_all("div", {"class" : "col-md-11"})[0]

htmlData = []
# htmlData   {str(address), finalSection}
htmlData.append({str(address), finalSection})

if (open("Parsed.html") is not None) :
    os.remove("Parsed.html")

Func = open("Parsed.html", "w")
Func.write(str(finalSection))
Func.close()


# print(finalSection)
# .results.find("section")

if (addressData.status_code != 200) :
    raise Exception("There was an error with the request")

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

interactedAddresses = set(extractTransactions(addressData))
# interactedAddressesSet = set(interactedAddresses)

print("Number of addresses the target address has interacted with is: " + str(len(interactedAddresses)))
# print(interactedAddresses.__sizeof__())
# print(len(interactedAddresses))

# i = 0
print("Check data about the neighbours now")

for x in interactedAddresses :
    # print(x)
    # i = i + 1
    # print(i)
    # print(interactedAddresses.index(x))
    # Get HTML for each page and then extract the data from there into an object
    htmlfile = extractAddressMetaData(x)
    parsedFile = BeautifulSoup(open(str(x) + ".html"), "html.parser")
    r = parsedFile.body.find_all("div", {"id": "wrapper"})
    finalData = object()
    # print(res.__sizeof__())
    # i = 0
    for result in res : 
        # i = i + 1
        # print(i)
        for d in result.find_all("section", {"id": "content"}) :
            for x in d.find_all("div", {"id" : "search_address_index", "class" : "container"}) :
                for y in x.find_all("div", {"class" : "row"}) :
                    for z in y.find_all("div", {"class" : "col-lg-12"}) :
                        for w in z.find_all("div", {"class" : "row"}) :
                            for z in w.find_all("div", {"class" : "col-lg-12 float_left_box"}) :
                                for x in z.find_all("div", {"class" : "row text-center"}) :
                                    for z in x.find_all("div", {"class" : "col-lg-12"}) :
                                        for y in z.find_all("div", {"class" : "float_left_box flb_scam_records_table"}) :
                                            for x in y.find_all("div", {"class" : "collapse", "id" : "scam_records_table"}) :
                                                for z in x.find_all("div", {"class" : "row row_odd hide", "id" : "scam_info_71212"}) :
                                                    if z is not None : 
                                                        finalData = z.find_all("div", {"class" : "col-md-11"})[0]
    htmlData.append({str(x), finalData})

    

    
# print(htmlData)
# htmlData
knownAddress = checkIsAddressKnownOrHasInteractedWithKnown(interactedAddresses, address)

fileName = "finalData" + str(address) + ".html"
with open(fileName, "w") as outfile :
    for x in htmlData :
        for key,val in x.items():
            outfile.write({key + ":" + val})

# print(interactedAddresses)

# for x in interactedAddresses :
#     data = extractAddressMetaData(x)
#     if (data is not None) :
#         with (open(x + ".html", "w")) as fp:
#             fp.write(data)

# Throwing 429 error for too many requests
# for x in interactedAddresses : 
#     interactedAddressUrl = "https://blockchain.info/rawaddr/" + x
#     intereactedAddressData = requests.request("GET", interactedAddressUrl, headers=addressHeaders, data=payload)
#     if (intereactedAddressData is not None) :
#         interactedJson = intereactedAddressData.json()
#         print(intereactedAddressData)  
        
  
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
        

# print(addressData)
jsonString = json.dumps(addressData, indent=4)
jsonFile = open(fileName, "w")
jsonFile.write(jsonString)
jsonFile.close()