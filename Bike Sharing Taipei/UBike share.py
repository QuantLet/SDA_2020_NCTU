import requests
import json
import pprint
import pandas as pd
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import folium

response=requests.get('https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.json')
content = response.content
json_tree = json.loads(content)

df=pd.DataFrame(json_tree)

df=pd.read_csv('youbike-taipei.csv',sep=';')

leftRatio=df['sbi']/df['tot']*100
df['lat']=pd.to_numeric(df['lat'])
df['lng']=pd.to_numeric(df['lng'])

loc=df[['lat','lng']].values.tolist()
mapit = folium.Map( location=loc[6], zoom_start=6 )
for point in range(0, len(loc)):
    folium.Marker(loc[point], popup=[leftRatio[point],df['snaen'][point],df['sarean'][point]]).add_to(mapit)
mapit

