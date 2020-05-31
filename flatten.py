import pandas as pd
import os

region_locs = [i for i in range(2,41,3)]

def get_region_values(old_table, region_index, year, month):
    entries = []
    cols = old_table.columns
    
    for i in range(0,3):
        row = {}
        
        row['Region'] = old_table[cols[1]].loc[region_index]
        
        if i==0:
            row['Attribute'] = "insolvencies"
        else:
            row['Attribute'] = old_table[cols[1]].loc[region_index+i]
            
        row['Value'] = old_table[cols[2]].loc[region_index+i]
        row['Year'] = year
        row['Month'] = month
        
        entries.append(row)
        
    return pd.DataFrame(entries)
        

def flatten(table_name):
    
    old_table = pd.read_excel(os.path.join(os.getcwd(),'data', table_name))
    #print(old_table)
    
    cols = old_table.columns
    
    month_str = str(old_table[cols[2]].loc[0])
    year = month_str[-4:]
    month = month_str.replace(month_str[-5:], '')
    
    #print(month)
    #print(year)
    
    dfs = [get_region_values(old_table, i, year, month) for i in region_locs]
    
    return pd.concat(dfs, axis=0)
    
## SPECIFY the file to flatten here ##  
#data = flatten('apr_2012-2.xlsx')
#print(data)
