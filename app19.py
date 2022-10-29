# App to collect all the stats from the JSON report created 
import json

with open("allAddressesData.json") as f:
    data = json.load(f)



totalNumberOfTargetAddresses = 1251
totalNumberOfTargetAddressesWithData = len(data)

# To be computed
totalNumberOfNeighbours = 0
totalNumberOfNeighboursWithReports = 0
totalNumberOfReportsPerTargetAddress = 0
totalNumberOfRerportsInNeighbours = 0
totalNumberOfNeighboursWithReportsPerTargetAddress = 0

averageNumberOfNeighboursPerAddress = 0
averageNumberOfReportsPerTargetAddress = 0
averageNumberOfRerportsInNeighbours = 0
averageNumberOfNeighboursWithReportsPerTargetAddress = 0
commonDataPerAddress = []

for x in data:
    address = x[0]['address']
    numofScamsInAddress = x[5]['numberOfScamsInAddress']
    numofNeighbours = x[2]['numberOfNeighbours']
    numofNeighboursWithScams = x[3]['numberOfNeighboursWithScams']
    numberOfScamsInNeighbours = x[4]['numberOfScamsInNeighbours']
    ipAddressesFromAddress = extractItems(x[6]['parsedAddressData']['ipAddresses'])
    ipAddressesFromNeighbours = extractItems(x[7]['parsedNeighbourData'][0]['ipAddresses'])
    urlsFromAddress = extractItems(x[6]['parsedAddressData']['urls'])
    urlsFromNeighbours = extractItems(x[7]['parsedNeighbourData'][0]['urls'])
    
    totalNumberOfNeighbours += numofNeighbours
    totalNumberOfNeighboursWithReports += numofNeighboursWithScams
    totalNumberOfReportsPerTargetAddress += numofScamsInAddress
    totalNumberOfRerportsInNeighbours += numberOfScamsInNeighbours
    
averageNumberOfReportsPerTargetAddress = totalNumberOfReportsPerTargetAddress/totalNumberOfTargetAddressesWithData
averageNumberOfNeighboursPerAddress = totalNumberOfNeighbours/totalNumberOfTargetAddressesWithData
averageNumberOfRerportsInNeighbours = totalNumberOfRerportsInNeighbours/totalNumberOfTargetAddressesWithData