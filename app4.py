# find the number of scam alerts recieved from BTC who is WHO
# Cross check that with BTCAbuseDB to see what it says
# Create stats on the number of scam alerts recieved from BTC who is WHO based on what AbuseDB say 
# Ie these many legal addresses have scam alerts (False Positives) and these many illegal addresses have scam alerts (True Positives)

import requests
from bs4 import BeautifulSoup
import time

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

def extractHTML(address) : 
    btcWhoIsWhoUrl = "https://www.bitcoinwhoswho.com/address/" + address
    time.sleep(1)    
    data = requests.request("GET",btcWhoIsWhoUrl, headers={}, data={})
    # print(data.status_code)
    # Add a delay to avoid getting banned 
    # Check 503 error code... 
    # Sleep of 1 second
    if (data is not None) :
        with open("/app4/" + address + ".html", "w") as outfile:
            outfile.write(data.text)
    # print(btcWhoIsWhoUrl)
    return data.text

address =  input("What is the address you want to check? \n")

addressUrl = "https://blockchain.info/rawaddr/" + address
addressData = requests.request("GET", addressUrl).json()

neighbours = set(extractNeighbours(addressData))

html = extractHTML(address)

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
                                                if z is not None : 
                                                    finalSection = z.find_all("div", {"class" : "col-md-11"})[0]



# Need to figure out the number of scam alerts recieved from BTC who is WHO