ALEXA_TOP_1M = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

import pandas as pd

top_sites = pd.read_csv(ALEXA_TOP_1M, header=None)

print(top_sites.head())