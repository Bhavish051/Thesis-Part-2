import re
from turtle import pen
# import nltk
import os
import spacy
import requests
from progressbar import Percentage, ProgressBar,Bar,ETA
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
# import locationtagger
import nltk
import sqlite3

conn = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + "/locationdata.db")

# nltk.download('punkt')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
# nltk.download('averaged_perceptron_tagger')

# GeoPy gives the extact address as well.

pbar = ProgressBar(widgets=[Bar('>', '[', ']'), ' ',Percentage(), ' ',ETA()])

# nltk.download('punkt')

# nltk.download('averaged_perceptron_tagger')

# nlp = spacy.load('en_core_web_lg')
nlp = spacy.load('en_core_web_trf')

# TARGET_FILE = "1pSw6eh5GoWtBrETzPbM36DGxc6Tes5MpTARGET_ADDRESS.json"
# print("============NEIGHBOURS===============")

# TARGET_FILE = "./btcabuseaddresses/1pSw6eh5GoWtBrETzPbM36DGxc6Tes5Mp.html"
# print("============ADDRESS===============")


TARGET_FILE = "1pSw6eh5GoWtBrETzPbM36DGxc6Tes5MpCSVData.txt"
print("============BTCABUSECSVData===============")

with open (TARGET_FILE, "r") as f:
    string = f.readlines()
    
# tokens = nlkt.word_tokenize(string)

pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
ipAddresses = []

sents = []

urls = []
emails = []
ipList = []

with open(TARGET_FILE) as file:
        for line in file:
            # \b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b

            # link_regex = re.compile(‘((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)’, re.DOTALL)
            url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', line)
            # urls = re.findall('\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b', line)
            # url = re.findall((r'(https?://\S+)'), line)
            if url is not None and len(url) > 0:
                urls.append(url[0])
            email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", line)
            if email is not None and len(email) > 0:
                emails.append(email[0])


# for url in urls:
    # print(url)
    # Can use Geekflare to get A record for the domain
    # Remember the rate limiter 1 request per second
    # ipList.append()

for line in string:
    if pattern.search(line) is not None:
        ipAddresses.append(pattern.findall(line))
    # sents.append(nlp(line))
    # for entity in nlp(line).ents:
        # print(f'Found: {entity.text} of type: {entity.label_}')

# ip = requests.get('https://api.ipify.org?format=json')
# print(ipAddresses)
# print(ip.json())
# print(sents)


for ip in ipAddresses:
    for i in ip:
        ipList.append(i)
        
print(ipList)

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

# data = '["208.80.152.201", "91.198.174.192"]'
if len(ipList) > 0:
    data = "["
    for x in ipList:
        data = data + '"' + x + '"' + ", "

    data = data + '"' + ipList[0] + '"' + "]"

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    ipData = session.post('http://ip-api.com/batch', headers=headers, data=data).json()

    # ipData = requests.request("POST", "http://ip-api.com/batch", headers = headers , data = data)

    print(ipData)

# with open('data.json', 'w') as f:
#     f.write(str(ipData))

    for x in ipData :
        if (x['status'].lower() == 'success'):
            print(x['query'] + " : " + x['country'] + " : " + x['city'] + " : " + x['isp'] + " : " + x['zip'] + ":" + str(x['lat']) + ":" + str(x['lon']))
        


# Get the A record for each URL and get the IP Address and can get data from there as well.
print(urls)

# place_entity = locationtagger.find_locations(text = string)
# print(place_entity)


# TODO: Need to check issue here what is going on, it is not working, sqlite3.OperationalError: unable to open database file
# "/Users/bhavish051/micromamba/lib/python3.9/site-packages/locationtagger/locationextractor.py", line 71, in __init__
# "/Users/bhavish051/micromamba/lib/python3.9/site-packages/locationtagger/__init__.py", line 7, in find_locations
# loc = []
# for line in pbar(string):
#     loc.append(locationtagger.find_locations(text = line))
    
# print(loc)

print(emails)

# for url in urls:
    
# names = []

# spacy_parser = nlp(string)

# for entity in spacy_parser.ents:
    # print(f'Found: {entity.text} of type: {entity.label_}')
    
spacy_data = []

for line in string:
    spacy_parser = nlp(line)
    for entity in spacy_parser.ents:
        spacy_data.append({'text': entity.text, 'label': entity.label_})
        print(f'Found: {entity.text} of type: {entity.label_}')
        
# print(spacy_data)