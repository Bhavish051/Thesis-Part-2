# find the number of scam alerts recieved from BTC who is WHO
# Cross check that with BTCAbuseDB to see what it says
# Create stats on the number of scam alerts recieved from BTC who is WHO based on what AbuseDB say 
# Ie these many legal addresses have scam alerts (False Positives) and these many illegal addresses have scam alerts (True Positives)

import requests
from bs4 import BeautifulSoup
import time
from progressbar import Percentage, ProgressBar,Bar,ETA
from tabulate import tabulate
import pandas as pd

pbar = ProgressBar(widgets=[Bar('>', '[', ']'), ' ',Percentage(), ' ',ETA()])

BTC_ABUSE_ADDRESS_URL = "https://www.bitcoinabuse.com/api/reports/check"

def extractNeighbours(data) :
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
        print("No Neighbours found")
    return result

def extractHTML(address) : 
    btcWhoIsWhoUrl = "https://www.bitcoinwhoswho.com/address/" + address
    time.sleep(1)    
    data = requests.request("GET",btcWhoIsWhoUrl, headers={}, data={})
    return data.text

# address =  input("What is the address you want to check? \n")
address = "bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h"

addressUrl = "https://blockchain.info/rawaddr/" + address
addressData = requests.request("GET", addressUrl).json()

neighbours = set(extractNeighbours(addressData))

html = extractHTML(address)

parsedHtml = BeautifulSoup(html, "html.parser")

finalSection = []
numScamAlerts = 0

res = parsedHtml.body.find_all("div", {"id": "wrapper"})

# print(res)

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
                                            # for z in x.find_all("div", {"class" : "row row_odd hide", "id":lambda x: x and x.startswith('scam_info')}) :
                                            numScamAlerts = len(x.find_all("div", {"class" :lambda x: x and x.startswith('row row_')}))/2
                                            for z in x.find_all("div", {"class" :lambda x: x and x.startswith('row row_')}) :
                                                finalSection.append(z.find_all("div", {"class" : "col-md-11"}))

# Need to figure out the number of scam alerts recieved from BTC who is WHO
# Cross check that with BTCAbuseDB to see what it says

data = []
col_names = ["Address", "Scam Alerts", "Number of Scam Alerts from BTC Who is WHO", "Number of Scam Alerts from AbuseDB"]

print(numScamAlerts)

if (numScamAlerts > 0) :
    print("Scam Alerts Recieved from BTC Who is WHO")
    

btcAbuseResponse = requests.get(BTC_ABUSE_ADDRESS_URL, params={"address": address, 'api_token' : 'AypnQ9bsgY931zWSAK8NdErbZl9wf9SDrG9RI3qW'}).json()
print(btcAbuseResponse['count'])
if (btcAbuseResponse['count'] > 0):
    maliciousAddress = True
    print("This address has been reported as a scam address")
    
# print(tabulate(data, headers=col_names, tablefmt="fancy_grid", showindex="always"))

print(len(set(pd.read_csv("report.csv")['address'].values)))