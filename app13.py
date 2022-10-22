import pandas as pd
TARGET_ADDRESS = "1pSw6eh5GoWtBrETzPbM36DGxc6Tes5Mp"

filename = 'latestReport.csv'
df = pd.read_csv(filename)

print("Data from CSV file:")

d = []

for index, row in df.iterrows():
    if row['address'] == TARGET_ADDRESS :
        d.append(row['description'])
        
with open(TARGET_ADDRESS + "CSVData.txt", "w") as f:
    f.write(str(d))