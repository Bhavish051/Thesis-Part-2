from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests

def postProcessIPs(ipAddresses) :
    result = []
    print("Post Processing IPs")
    ipList = []
    for ip in ipAddresses:
        for i in ip:
            ipList.append(i)
    
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
        ipData = session.post('http://ip-api.com/batch', headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=data).json()
        for x in ipData :
            if (x['status'].lower() == 'success'):
                result.append(x['query'] + " : " + x['country'] + " : " + x['city'] + " : " + x['isp'] + " : " + x['zip'] + ":" + str(x['lat']) + ":" + str(x['lon']))
    
    return result        


# Read the IPs from the reports and then send a batch request.
# But first need to fix the output JSON.