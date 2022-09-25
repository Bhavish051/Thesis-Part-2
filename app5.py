import mysql.connector
import requests
from bs4 import BeautifulSoup
import pandas as pd

db = mysql.connector.connect(user='root', password='1234', host='Bhavishs-MacBook-Air.local')
dbCursor = db.cursor()
dbCursor.execute("USE btc;")

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
    print(address)
    return {"numScamAlerts" : numScamAlerts, "finalSection" : finalSection}



# dbCursor.execute("SELECT count(distinct(address)) FROM bitcoinheistdata;")
dbCursor.execute("SELECT label,count(*) FROM bitcoinheistdata group by label;")

result = dbCursor.fetchall()

classifiedAddresses = pd.DataFrame(result)

dbCursor.execute("SELECT address FROM bitcoinheistdata where label = 'white';")

legitAddressesToInvestigate = []

legitAddresses = dbCursor.fetchall()

for x in legitAddresses :
    legitAddressesToInvestigate.append((str(x)).replace("(''","").replace("',)",""))


dbCursor.execute("SELECT address FROM bitcoinheistdata where label != 'white';")
# Correct addresses this way but very slow

maliciousAddresses = dbCursor.fetchall()

maliciousAddressesToInvestigate = []

for x in maliciousAddresses :
    maliciousAddressesToInvestigate.append((str(x)).replace("('","").replace("',)",""))

validateResults(legitAddressesToInvestigate)
validateResults(maliciousAddressesToInvestigate)