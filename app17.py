import json
import os.path
from bs4 import BeautifulSoup
from progressbar import Percentage, ProgressBar,Bar,ETA
import re
import spacy

# App to generate a report of the address
# Step 1: Open the address HTML file
# Step 2: Parse the HTML file
# Step 3: Extract the data
# Step 4: Get the list of neighbours
# Step 5: Open the neighbours HTML file one by one
# Step 6: Parse the HTML file
# Step 7: Extract the data
# Step 8: Write the data to a file

TargetAddresses = []
Neighbours = []
pbar = ProgressBar(widgets=[Bar('>', '[', ']'), ' ',Percentage(), ' ',ETA()])
nlp = spacy.load('en_core_web_trf')

with open( "neighborData.json", "r" )as f:
    data = json.load(f)
    for address in data:
        if len(address['neighbours']) > 0:
            TargetAddresses.append(address['address'])
            for x in address['neighbours']:
                Neighbours.append(x)

# I have 128 addresses with neighbours out of 182 reported malicious addresses
# I have 115289 Neighbours atm

def extractScamAlerts(html) :
    parsedHtml = BeautifulSoup(html, "html.parser")
    res = parsedHtml.body.find_all("div", {"id": "wrapper"})
    scamSection = []
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
                                                    scamSection.append(z.find_all("div", {"class" : "col-md-11"}))
    return {"scamSection" : scamSection,"numberOfAlerts" : numScamAlerts}

def extractNeighbours(x) :
    with open( "neighborData.json", "r" )as f:
        data = json.load(f)
        for address in data:
            if address['address'] == x:
                return address['neighbours']
finalReportData = []
def extractAddressData(x, folderName) :
    if (os.path.exists("./" + folderName + "/" + x + ".html")):
        with open("./" + folderName + "/" + x + ".html") as f :
            html = f.read()
            scamsHTML = extractScamAlerts(html)
            data = {"address" : x, "scams" : scamsHTML['scamSection'], "numberOfAlerts" : scamsHTML['numberOfAlerts']}
            finalReportData.append(data)
            return data



def parseHTML(html) :
    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    urls = []
    emails = []
    ipAddresses = []
    spacy_data = []
    
    for x in html :
        url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', str(x))
        if len(url) > 0 :
            urls.appendA(url)
        email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(x))
        if len(email) > 0 :
            emails.append(email)
        if pattern.search(x) is not None:
            ipAddresses.append(pattern.findall(x))
        spacy_parser = nlp(x)
        for entity in spacy_parser.ents:
            spacy_data.append({'text': entity.text, 'label': entity.label_})
            
    ipData = postProcessIPs(ipAddresses)
    return {"urls" : urls, "emails" : emails, "ipAddresses" : ipAddresses, "spacy_data" : spacy_data}

countOfNeighbours = 0
for x in pbar(set(TargetAddresses)):
    # Per address Execution
    addressReport = []
    neighbours = extractNeighbours(x)
    addressData = extractAddressData(x, "btcabuseaddresses")
    countOfNeighbours += len(set(neighbours))
    neighbourData = []
    numberOfNeighboursWithScams = 0
    numberOfScamsInNeighbours = 0
    numberOfScamsInAddress = addressData['numberOfAlerts']
    for y in set(neighbours):
        nData = extractAddressData(y, "btcabuseneighbours")
        neighbourData.append(nData)
        if (nData is not None and nData['numberOfAlerts'] > 0):
            numberOfNeighboursWithScams += 1
            numberOfScamsInNeighbours += nData['numberOfAlerts']
    addressReport.append(addressData)
    addressReport.append(neighbourData)
    addressReport.append({"numberOfNeighbours" : len(set(neighbours))})
    addressReport.append({"numberOfNeighboursWithScams" : numberOfNeighboursWithScams})
    addressReport.append({"numberOfScamsInNeighbours" : numberOfScamsInNeighbours})
    addressReport.append({"numberOfScamsInAddress" : numberOfScamsInAddress})
    parsedAddressData = parseHTML(addressData['scams'])
    # Append Extra Objects such as 
    # 1. Number of Neighbours --> Done
    # 2. Number of Neighbours with Scams --> Done
    # 3. Number of Scams in Neighbours -->Done
    # 4. Number of Scams in Address --> Done
    # 5. Parsed Data about the address
    # 6. Parsed Data about the neighbours
    # 7. Common Data among the neighbours and the address
    # Write to a file
    # print(addressReport)
    
# print(finalReportData)