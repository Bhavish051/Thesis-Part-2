import mysql.connector
import pandas as pd
import matplotlib.pyplot as plot

db = mysql.connector.connect(user='root', password='1234', host='Bhavishs-MacBook-Air.local')
dbCursor = db.cursor()
dbCursor.execute("USE btc;")


dbCursor.execute("SELECT count(*) as Count, label FROM bitcoinheistdata group by label;")

result = dbCursor.fetchall()

df = pd.DataFrame(result, columns=['Count', 'Label'], index=None)

plot = df.plot.pie(y = 'Count' , figsize=(11, 6))
plot.show()