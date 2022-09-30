import mysql.connector
import requests
from bs4 import BeautifulSoup
from progressbar import Percentage, ProgressBar,Bar,ETA
import pandas as pd

db = mysql.connector.connect(user='root', password='1234', host='Bhavishs-MacBook-Air.local')
dbCursor = db.cursor()
dbCursor.execute("USE btc;")

pbar = ProgressBar(widgets=[Bar('>', '[', ']'), ' ',Percentage(), ' ',ETA()])

def extractHTML(address) : 
    btcWhoIsWhoUrl = "https://www.bitcoinwhoswho.com/address/" + address
    data = requests.request("GET",btcWhoIsWhoUrl, headers={}, data={})
    return data.text

def findIfBtcWhoIsWhoHasReport(address) : 
    html = extractHTML(address)
    parsedHtml = BeautifulSoup(html, "html.parser")
    res = parsedHtml.body.find_all("div", {"id": "wrapper"})
    # Loop now
    finalSection = []
    numScamAlerts = 0
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
    return {"numScamAlerts" : numScamAlerts, "finalSection" : finalSection}

def extractNeighbours(address) :
    addressUrl = "https://blockchain.info/rawaddr/" + address
    data = requests.request("GET", addressUrl).json()
    result = []
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
    with open("./finalAddressAndNeighbourData/" + str(x) + ".html", "w") as outfile :
        outfile.write(str(addressData))

def validateResults(addresses) :
    addresses = []
    print(len(maliciousAddressesToInvestigate))
    for x in pbar(addresses) :
        print(x)
        addressData = []
        result = findIfBtcWhoIsWhoHasReport(x)
        if (result['numScamAlerts'] > 0) :
            addresses.append(x)
            addressData.append(result['finalSection'])
            # Check NeighBourData
            neighbours = extractNeighbours(x)
            for x in neighbours :
                result = findIfBtcWhoIsWhoHasReport(x)
                neighBourData = findIfBtcWhoIsWhoHasReport(neighbours)
                if (neighBourData['numScamAlerts'] > 0) :
                    addressData.append(neighBourData['finalSection'])
                writeToFile(addressData, x)
    return {"addresses" : addresses}
        
dbCursor.execute("SELECT label,count(*) FROM bitcoinheistdata group by label;")

result = dbCursor.fetchall()

classifiedAddresses = pd.DataFrame(result)

dbCursor.execute("SELECT address FROM bitcoinheistdata where label = 'white';")

legitAddressesToInvestigate = []

legitAddresses = dbCursor.fetchall()

for x in set(legitAddresses) :
    legitAddressesToInvestigate.append((str(x)).replace("(''","").replace("',)",""))


dbCursor.execute("SELECT address FROM bitcoinheistdata where label != 'white';")
# Correct addresses this way but very slow

maliciousAddresses = dbCursor.fetchall()

print(len(maliciousAddresses))

maliciousAddressesToInvestigate = []

for x in set(maliciousAddresses) :
    maliciousAddressesToInvestigate.append((str(x)).replace("('","").replace("',)",""))


maliciousWithScamData = validateResults(maliciousAddressesToInvestigate)
print("Malicious Addresses with Scams : " + str(maliciousWithScamData['addresses']))
TruePositives = len(maliciousWithScamData['addresses'])/len(maliciousAddressesToInvestigate)
print("True Positives : " + str(TruePositives))


# legitWithScams = validateResults(legitAddressesToInvestigate)
# print("Legit Addresses with Scams : " + str(legitWithScams))
# FalsePositives = legitWithScams/len(legitAddressesToInvestigate)
# print("False Positives : " + str(FalsePositives))