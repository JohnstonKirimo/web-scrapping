import pandas as pd
import requests
import json
import numpy as np
import os

def replace(x):
    try:
        f = float(x)
    except:
        f = 0.0
        
    return f

urls=open('urls1.json', 'r')
urls = json.load(urls)

#fetching all data into one dict 
tables = {}
for key in urls.keys():
    my_html = requests.get(urls[key]).content
    tables[key] = pd.read_html(my_html)
    
#replace non-numeric values
for key in tables.keys():
    for col in tables[key][1].columns:
        if 'Province' not in str(col):
            tables[key][1][col] = tables[key][1][col].apply(replace)
        else:
            pass
        

# reduce tables to keep only first two columns
new_tables = {}

for month in tables.keys():
    new_tables[month] = []
    count = 1
    for table in tables[month]:
        new_df = table[list(table.columns)[:2]]
        new_tables[month].append(new_df)
        
        name = str(month)+'-'+str(count)+'.xlsx'
        new_df.to_excel(os.path.join(os.getcwd(),'data', name))
        print('saved: '+name)
        count += 1

'''
# get and concatenate all index 1 tables, for all months & years

table1 =[]

for month in list(new_tables.keys())[:-1]:
    
    table = new_tables[month][1]
    cols = list(table.columns)
    provinces = pd.Series(np.array(table[cols[0]]), name=cols[0][1])
    totals = pd.Series(np.array(table[cols[1]]), name=cols[1][1])
  

    month = pd.Series([totals.name[:3] for i in table.index], index=table.index, name='month')
    
    year = pd.Series([totals.name[-4:] for i in table.index], index=table.index, name='year')
    totals.name = 'totals'
    new_df = pd.concat([provinces, totals, month, year], axis=1)
    table1.append(new_df)
    
table1 = pd.concat(table1, axis=0).reset_index(drop=True)

table1.to_excel('table1.xlsx')

'''
