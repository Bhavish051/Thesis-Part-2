import os
from typing import Set
from bs4 import BeautifulSoup
from progressbar import Percentage, ProgressBar,Bar,ETA

path = "btcabuseaddresses"
pbar = ProgressBar(widgets=[Bar('>', '[', ']'), ' ',Percentage(), ' ',ETA()])

def processHTML(x, y) :
    parsedHtml = BeautifulSoup(x, "html.parser")
    res = parsedHtml.body.find_all("div", {"id": "wrapper"})
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
    return {"HTML" : finalSection,"numberOfAlerts" : numScamAlerts}  

def read_file(file_path) :
    with open(file_path, "r") as f :
        return f.read()
    
x = 0
addressesWithData = []
    
for file in pbar(os.listdir(path)) : 
    if x == 0 :
        os.chdir(path)
        x = 1
    data = read_file(file)
    print(file)
    res = processHTML(data, file)
    print(res)
    if res["numberOfAlerts"] > 0 :
        addressesWithData.append(file)

print(len(set(addressesWithData)))
with open ("addressesWithData.txt", "w") as f :
    for address in set(addressesWithData) :
        f.write(address + ",")