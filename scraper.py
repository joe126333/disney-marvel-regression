import requests, json
import pandas as pd
from pandas import DataFrame
from bs4 import BeautifulSoup
from datetime import datetime

url = "https://en.wikipedia.org/wiki/List_of_Marvel_Cinematic_Universe_films#Box_office_performance"
headers = {'User-Agent': 'Mozilla/5.0'}

title_list = []
key_list = []
rows = []
dummy = []

response = requests.get(url, headers = headers)

soup = BeautifulSoup(response.content, 'html.parser')

#Locate table and run through each row looking for given tags, append to list
for item in soup.find('table', class_ = "wikitable plainrowheaders sortable").find_all('tr'):
    cells = item.find_all(['a', 'span', 'td'])
    dummy = []
    for itemss in cells:
        if itemss.string in ['[', ']']:  # remove non-data cells
            continue
        if itemss.string is None:  # remove none type cells
            continue
        if itemss.string.startswith('Phase'): # remove phases cells
            continue
        if itemss.string.startswith('U.S.'):  # remove u.s. and worldwide cells
            continue
        if itemss.string.startswith('Worldwide'):
            continue
        key_list.append(itemss.string)
        dummy.append(itemss.string)
    if dummy != [] and dummy != ['\n']:
        rows.append(dummy)

rows.pop(37) # Remove useless row
rows[23].insert(4, '379751655') # Fixed Black Widow Total

# Create data table,clean cells
labels = ['Title', 'Date', 'US', 'Other', 'Total', 'US Rank', 'World Rank', 'Budget']
df = pd.DataFrame.from_records(rows, columns = labels)

df['Date'] = pd.to_datetime(df.Date)
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
df['Date'] = pd.to_datetime(df.Date)

df['US'] = df['US'].str.replace(',', '')
df['US'] = df['US'].str.replace('$', '')
df['US'] = df['US'].astype(int)

df['Other'] = df['Other'].str.replace(',', '')
df['Other'] = df['Other'].str.replace('$', '')
df['Other'] = df['Other'].astype(int)

df['Total'] = df['Total'].str.replace(',', '')
df['Total'] = df['Total'].str.replace('$', '')
df['Total'] = df['Total'].astype(int)

df['US Rank'] = df['US Rank'].str.replace('\n', '')
df['US Rank'] = df['US Rank'].astype(int)

df['World Rank'] = df['World Rank'].str.replace('\n', '')
df['World Rank'] = df['World Rank'].astype(int)

df['Budget'] = df['Budget'].str.replace(r'[^A-Za-z0-9]', '', regex = True)
df['Budget'] = df['Budget'].str.replace('million', '')
df['Budget'] = df['Budget'].str.slice(0,3)   # round budget and use smallest budget estimate
df['Budget'] = df['Budget'] + '000000'

with open('mcu_movies_list.txt', 'w') as data_file:
    json.dump(rows, data_file)

df.to_csv('mcu_movies_table.csv', index = False)
