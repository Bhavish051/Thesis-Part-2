import requests

TARGET_ADDRESS = "1pSw6eh5GoWtBrETzPbM36DGxc6Tes5Mp"

def extractHTML(address) : 
    btcWhoIsWhoUrl = "https://www.bitcoinwhoswho.com/address/" + address
    data = requests.request("GET", btcWhoIsWhoUrl)
    return data.text

html = extractHTML(TARGET_ADDRESS)

with open("TARGET_ADDRESS.html", "w") as f:
    f.write(html)