import mysql.connector
import requests
from bs4 import BeautifulSoup
from progressbar import Percentage, ProgressBar,Bar,ETA
import pandas as pd
import time
import aiohttp
import asyncio


db = mysql.connector.connect(user='root', password='1234', host='Bhavishs-MacBook-Air.local')
dbCursor = db.cursor()
dbCursor.execute("USE btc;")

pbar = ProgressBar(widgets=[Bar('>', '[', ']'), ' ',Percentage(), ' ',ETA()])

async def extractHTML(session, address) : 
    btcWhoIsWhoUrl = "https://www.bitcoinwhoswho.com/address/" + address
    async with session.get(btcWhoIsWhoUrl) as response:
        data = await response.text()
        return data

async def findIfBtcWhoIsWhoHasReport(address,session) : 
    html = await extractHTML(session, address)
    # parsedHtml = BeautifulSoup(html, "html.parser")
    # writeToFile(parsedHtml, address)
    
    # if parsedHtml.body is not None :
    #     res = parsedHtml.body.find_all("div", {"id": "wrapper"})
    # # Loop now
    #     finalSection = []
    #     numScamAlerts = 0
    #     for result in res : 
    #         for d in result.find_all("section", {"id": "content"}) :
    #             for x in d.find_all("div", {"id" : "search_address_index", "class" : "container"}) :
    #                 for y in x.find_all("div", {"class" : "row"}) :
    #                     for z in y.find_all("div", {"class" : "col-lg-12"}) :
    #                         for w in z.find_all("div", {"class" : "row"}) :
    #                             for z in w.find_all("div", {"class" : "col-lg-12 float_left_box"}) :
    #                                 for x in z.find_all("div", {"class" : "row text-center"}) :
    #                                     for z in x.find_all("div", {"class" : "col-lg-12"}) :
    #                                         for y in z.find_all("div", {"class" : "float_left_box flb_scam_records_table"}) :
    #                                             for x in y.find_all("div", {"class" : "collapse", "id" : "scam_records_table"}) :
    #                                                 # for z in x.find_all("div", {"class" : "row row_odd hide", "id":lambda x: x and x.startswith('scam_info')}) :
    #                                                 numScamAlerts = len(x.find_all("div", {"class" :lambda x: x and x.startswith('row row_')}))/2
    #                                                 for z in x.find_all("div", {"class" :lambda x: x and x.startswith('row row_')}) :
    #                                                     finalSection.append(z.find_all("div", {"class" : "col-md-11"}))
    
    # return {"numScamAlerts" : numScamAlerts, "finalSection" : finalSection}

def extractNeighbours(address) :
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
    return result
    
def writeToFile(addressData, x) :
    print("Writing to file for " + x)
    with open("./finalAddressAndNeighbourData/" + str(x) + ".html", "w") as outfile :
        outfile.write(str(addressData))

async def validateResults(data) :
    async with aiohttp.ClientSession() as session:
        print(len(data))
        addresses = []
        addresswithNeighbours = []
        tasks = []
        for x in pbar(data) :
            print(x)
            addressData = []
            result = asyncio.ensure_future(findIfBtcWhoIsWhoHasReport(x, session))
            tasks.append(result)
            print("Address : " + x + " scam alerts")
            # if (result['numScamAlerts'] > 0) :
                # addresses.append(x)
                # addressData.append({"address" : x, "data" : result['finalSection']})
                # Check NeighBourData
            neighbours = set(extractNeighbours(x))
            for y in neighbours :
                neighBourData = asyncio.ensure_future(findIfBtcWhoIsWhoHasReport(y, session))
                tasks.append(neighBourData)
                print("Neighbour : " + y + " scam alerts of " + x)
                # if (neighBourData['numScamAlerts'] > 0) :
                    # addressData.append({"address" : y, "data" : neighBourData['finalSection']})
            # print(addressData)
            print(len(neighbours))
            addresswithNeighbours.append({"address":x,"neighbours": neighbours})
            if addressData :
                writeToFile(addressData, x)
                
        await asyncio.gather(*tasks)
    return {"addresses" : addresses, "addresswithNeighbours" : addresswithNeighbours}
        
dbCursor.execute("SELECT label,count(*) FROM bitcoinheistdata group by label;")

result = dbCursor.fetchall()

classifiedAddresses = pd.DataFrame(result)

dbCursor.execute("SELECT address FROM bitcoinheistdata where label = 'white';")

legitAddressesToInvestigate = []

legitAddresses = dbCursor.fetchall()

if legitAddresses is not None : 
    for x in set(legitAddresses) :
        legitAddressesToInvestigate.append((str(x)).replace("(''","").replace("',)",""))


dbCursor.execute("select address from bitcoinheistdata where label = 'montrealSamSam' order by neighbors asc limit 100;")
# Correct addresses this way but very slow

maliciousAddresses = dbCursor.fetchall()

maliciousAddressesToInvestigate = []
if maliciousAddresses is not None :
    for x in maliciousAddresses :
        maliciousAddressesToInvestigate.append((str(x)).replace("('","").replace("',)",""))


maliciousWithScamData = asyncio.run(validateResults(set(maliciousAddressesToInvestigate)))
print("Malicious Addresses with Scams : " + str(maliciousWithScamData['addresses']))
print(maliciousWithScamData["addresswithNeighbours"])
TruePositives = len(maliciousWithScamData['addresses'])/len(maliciousAddressesToInvestigate)
print("True Positives : " + str(TruePositives))