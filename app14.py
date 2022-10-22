# Assumption is I have all the HTMLs at this point about the address
import json
import os.path

addressesToTarget = []
neighbours = []

with open( "neighborData.json", "r" )as f:
    data = json.load(f)
    for address in data:
        addressesToTarget.append(address['address'])
        for x in address['neighbours']:
            neighbours.append(x)
        
print(len(set(addressesToTarget)))
print(len(set(neighbours)))
# 633 Neighbours per address

# Check Do I have HTML for every address
addressesWithHtml = 0
for x in addressesToTarget:
    if (os.path.exists("btcabuseaddresses/" + x + ".html")):
        addressesWithHtml += 1

print("I have HTMLs for " + str(addressesWithHtml) + " addresses out of " + str(len(set(addressesToTarget))) + " addresses")
# Check how many neighbours I have HTML for

neighboursWithHtml = 0
for x in neighbours:
    if (os.path.exists("btcabuseneighbours/" + x + ".html")):
        neighboursWithHtml += 1
        
print("I have HTMLs for " + str(neighboursWithHtml) + " neighbours out of " + str(len(set(neighbours))) + " neighbours")