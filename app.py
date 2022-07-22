from numpy import block
import requests

# exchangeUrl = "https://rest-sandbox.coinapi.io/v1/exchanges"

payload={}
# exchangeHeaders = {
#   'X-CoinAPI-Key': 'AB56A202-FE3F-4007-AFDB-28BF268BB3DA',
#   'Accept': 'application/json',
#   'Accept-Encoding': 'deflate, gzip'
# }

# exhanges = requests.request("GET", exchangeUrl, headers=exchangeHeaders, data=payload)

# print(exhanges.text)


blockUrl = "https://blockchain.info/latestblock"

blockHeaders = {
    
}

latestBlock = requests.request("GET", blockUrl, headers=blockHeaders, data=payload).json()

# print(latestBlock.json())

# for key, value in latestBlock.items():
#     print(key, ":", value)

# print(latestBlock["txIndexes"][0])

fisrtTxIndexInLatestBlock = str(latestBlock["txIndexes"][0])

txUrl = "https://blockchain.info/rawtx/" + fisrtTxIndexInLatestBlock

# print(txUrl)

txHeaders = {
    
}

transactionInfo = requests.request("GET", txUrl, headers=txHeaders, data=payload).json()

# print(transactionInfo["out"][0]["addr"])

address = str(transactionInfo["out"][0]["addr"])

addressUrl = "https://blockchain.info/rawaddr/" + address



addressHeaders = {
    
}