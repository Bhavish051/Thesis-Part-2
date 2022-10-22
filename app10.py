import json
from os.path import exists
from bs4 import BeautifulSoup
from progressbar import Percentage, ProgressBar,Bar,ETA

pbar = ProgressBar(widgets=[Bar('>', '[', ']'), ' ',Percentage(), ' ',ETA()])

def processHTML(x) :
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


TARGET_ADDRESS = "1pSw6eh5GoWtBrETzPbM36DGxc6Tes5Mp"
FILE_NAME = "neighborData.json"

with open(FILE_NAME, "r") as f :
    data = f.read()
    data = json.loads(data)
    
for x in data :
    if len(x["neighbours"]) > 0 and x["address"] == TARGET_ADDRESS :
        targetNeighbours = x["neighbours"]
        

print(len(set(targetNeighbours)))

count = 0

html = []

for x in pbar(set(targetNeighbours)) :
    file_exists = exists("./btcabuseNeighbours/" + x + ".html")
    if file_exists :
        count = count + 1
        with open("./btcabuseNeighbours/" + x + ".html") as f :
            data = processHTML(f.read())
            if data["numberOfAlerts"] > 0 :
                html.append({"address" : x, "HTML" : data["HTML"]})


with open (TARGET_ADDRESS + "TARGET_ADDRESS" + ".json", "w") as f :
    f.write(json.dumps(str(html)))