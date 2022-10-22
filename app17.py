import json
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

with open( "neighborData.json", "r" )as f:
    data = json.load(f)
    for address in data:
        if len(address['neighbours']) > 0:
            TargetAddresses.append(address['address'])
            for x in address['neighbours']:
                Neighbours.append(x)

# I have 128 addresses with neighbours out of 182 reported malicious addresses
# I have 115289 Neighbours atm

for x in addressesToTarget:
    