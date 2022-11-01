# App to collect all the stats from the JSON report created 
import json

with open("allAddressesData.json") as f:
    data = json.load(f)

def extractItems(data) :
    result = []
    for x in data : 
        result.append(x)
    return result

def extractLocationFromIps(data) :
    result = []
    with open("allIpData.json") as f:
        ipData = json.load(f)
    for x in data :
        for y in ipData :
            if (x == y['query']) :
                if (y['status'] == 'success') :
                    result.append(y['country'])
    return result

def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    if len(a_set.intersection(b_set)) > 0:
        return(True) 
    return(False)   

def getIpsFromUrls(urls) :
    result = []
    with open("allUrlsData.json") as f:
        data = json.load(f)
        for x in urls :
            for a in x :
                for y in data :
                    if (a == y['address']) :
                        for z in y['aRec'] :
                            result.append(z['address'])
    return result
    
totalNumberOfTargetAddresses = 1251
totalNumberOfTargetAddressesWithData = len(data)

# To be computed
totalNumberOfNeighbours = 0
totalNumberOfNeighboursWithReports = 0
totalNumberOfReportsPerTargetAddress = 0
totalNumberOfReportsInNeighbours = 0
totalNumberOfNeighboursWithReportsPerTargetAddress = 0
allCountriesFromAddress = []

averageNumberOfNeighboursPerAddress = 0
averageNumberOfReportsPerTargetAddress = 0
averageNumberOfReportsInNeighbours = 0
averageNumberOfNeighboursWithReportsPerTargetAddress = 0
commonDataPerAddress = []
numberOfAddressesWithCommonData = 0
allCountriesFromNeighbours = []

for x in data:
    address = x[0]['address']
    numofScamsInAddress = x[5]['numberOfScamsInAddress']
    numofNeighbours = x[2]['numberOfNeighbours']
    numofNeighboursWithScams = x[3]['numberOfNeighboursWithScams']
    numberOfScamsInNeighbours = x[4]['numberOfScamsInNeighbours']
    ipAddressesFromAddress = extractItems(x[6]['parsedAddressData']['ipAddresses'])
    ipAddressesFromNeighbours = []
    urlsFromNeighbours = []
    if (len(x[7]['parsedNeighbourData']) > 0) :
        ipAddressesFromNeighbours = extractItems(x[7]['parsedNeighbourData'][0]['ipAddresses'])
        urlsFromNeighbours = extractItems(x[7]['parsedNeighbourData'][0]['urls'])
        
    urlsFromAddress = extractItems(x[6]['parsedAddressData']['urls'])
    
    locDataFromAddr = extractLocationFromIps(ipAddressesFromAddress + getIpsFromUrls(urlsFromAddress))
    locationDataFromAddress = set(locDataFromAddr)
    locDataFromNeigh = extractLocationFromIps(ipAddressesFromNeighbours + getIpsFromUrls(urlsFromNeighbours))
    locationDataFromNeighbours = set(locDataFromNeigh)
    
    allCountriesFromAddress = allCountriesFromAddress + locDataFromAddr
    allCountriesFromNeighbours = allCountriesFromNeighbours + locDataFromNeigh
    
    commonElements = common_member(locationDataFromAddress, locationDataFromNeighbours)
    if (commonElements) :
        numberOfAddressesWithCommonData = numberOfAddressesWithCommonData + 1
    totalNumberOfNeighbours += numofNeighbours
    totalNumberOfNeighboursWithReports += numofNeighboursWithScams
    totalNumberOfReportsPerTargetAddress += numofScamsInAddress
    totalNumberOfReportsInNeighbours += numberOfScamsInNeighbours
    
averageNumberOfReportsPerTargetAddress = totalNumberOfReportsPerTargetAddress/totalNumberOfTargetAddressesWithData
averageNumberOfNeighboursPerAddress = totalNumberOfNeighbours/totalNumberOfTargetAddressesWithData
averageNumberOfReportsInNeighbours = totalNumberOfReportsInNeighbours/totalNumberOfNeighbours 
averageNumberOfNeighboursWithReportsPerTargetAddress = totalNumberOfNeighboursWithReports/totalNumberOfTargetAddressesWithData


countriesSetFromAddress = set(allCountriesFromAddress)
countriesSetFromNeighbours = set(allCountriesFromNeighbours)

countriesDictFromAddress = {}
countriesDictFromNeighbours = {}
for x in countriesSetFromAddress :
    countriesDictFromAddress[x] = allCountriesFromAddress.count(x)

for x in countriesSetFromNeighbours :
    countriesDictFromNeighbours[x] = allCountriesFromNeighbours.count(x)
    
print("totalNumberOfTargetAddresses : ", totalNumberOfTargetAddresses)
print("totalNumberOfTargetAddressesWithData : ", totalNumberOfTargetAddressesWithData)
print("averageNumberOfReportsPerTargetAddress : " + str(averageNumberOfReportsPerTargetAddress))
print("averageNumberOfNeighboursPerAddress : " + str(averageNumberOfNeighboursPerAddress))
print("averageNumberOfReportsInNeighbours : " + str(averageNumberOfReportsInNeighbours))
print("averageNumberOfNeighboursWithReportsPerTargetAddress : " + str(averageNumberOfNeighboursWithReportsPerTargetAddress))
print("totalNumberOfReportsInNeighbours : " + str(totalNumberOfReportsInNeighbours))
print("numberOfAddressesWithCommonData : " + str(numberOfAddressesWithCommonData))

print("allCountriesFromAddress : " )
for w in sorted(countriesDictFromAddress, key=countriesDictFromAddress.get, reverse=True):
    print(w, countriesDictFromAddress[w])
    
print("allCountriesFromNeighbours : " )
for w in sorted(countriesDictFromNeighbours, key=countriesDictFromNeighbours.get, reverse=True):
    print(w, countriesDictFromNeighbours[w])