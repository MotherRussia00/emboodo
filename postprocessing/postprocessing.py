import pandas as pd
import re
from scraping.parse_datarade import categories, cases
from datasets_custom_description import *

'''this script takes a dataset and perofrms the following steps: 
1. inserts commas in the 
'''

filepath = '/Users/leo_z/Downloads/Datahunters Working station - datahunter - datarade full scrape - scraping.csv'
fp2 = '/Users/leo_z/Downloads/Datahunters Working station - removed_links.csv'
eurostat = '/Users/leo_z/Downloads/Scraping-data-europe - Eurostat.csv'
demographic = '/Users/leo_z/Downloads/Scraping-data-europe - Demographic Datasets.csv'
data_gov_lt = '/Users/leo_z/Downloads/Scraping-data-europe - data.gov.lt.csv'
instituto_nacional = '/Users/leo_z/Downloads/Scraping-data-europe - Instituto Nacional de Estadistica.csv'
def checked_for_existence(list_, d):
    new_list = []
    for i in list_:
        if i.lower() in d.keys() and d[i.lower()] not in new_list:
            new_list.append(d[i.lower()])
        elif i.lower() in [i.lower() for i in list(d.values())] and i not in new_list:
            new_list.append(i)
    if '' in new_list:
        new_list.remove('')
    return new_list

def check_cases(st):
    lis = st.split(',')
    return ','.join(checked_for_existence(lis,cases))

def check_cat(st):
    lis = st.split(',')
    return ','.join(checked_for_existence(lis, categories))

def delete_links(filepath):
    print('lol')
    df = pd.read_csv(filepath)
    df['related_data_sets']=df['related_data_sets'].str.replace(r'http\S+(?=,)', '', regex=True).replace(r' : ,',',', regex=True)
    # print(df['related_data_sets'].iloc[0])
    df.to_csv('removed_links.csv',index=False)
    return 0

def insert_comma(column):
    return column.str.replace(r'([a-z])([A-Z])', r'\1,\2', regex=True)

def flatten(t): #makes lists from comma-separated strings and then flattens the list of such lists
    # print('T',t)
    return [item for sublist in t for item in sublist.split(',')]

def unique_entries(column):
    return list(set(flatten(column.tolist())))


def form_list_of_datasets(fp, exitname):
    df = pd.read_csv(fp).fillna('')
    df['Use cases'] = insert_comma(df['Use cases'])
    df['Use cases'] = df['Use cases'].apply(check_cases)
    df['Data Categories']= insert_comma(df['Data Categories'])
    df['Data Categories'] = df['Data Categories'].apply(check_cat)
    df_new = form_description(df)
    df_new.to_csv('results/' + exitname + '.csv', index=False)

def form_list_of_providers(filepath, exit_name):
    print('lol')
    # columns = ['logo','data_provider','use_case','data_category']
    df = pd.read_csv(filepath).fillna('')
    df['use_case'] = insert_comma(df['use_case'])
    df['data_category']= insert_comma(df['data_category'])
    providers = df['data_provider'].unique()
    newdf_list = []
    for provider in providers[:]:
        dff = df[df['data_provider']==provider]
        # print('DFF',dff)
        dict_new = {}
        uc = unique_entries(dff['use_case'])
        dc = unique_entries(dff['data_category'])
        print('PROVIDER', provider)
        print('scraped use cases',uc)
        print('scraped data categories', dc)
        use_cases = checked_for_existence(unique_entries(dff['use_case']),cases)
        data_categories = checked_for_existence(unique_entries(dff['data_category']),categories)
        print('existing use csases', use_cases)
        print('existing datsa categories', data_categories)
        if '' in use_cases:
            use_cases.remove('')
        if '' in categories:
            data_categories.remove('')
        print(use_cases, data_categories)
        print(provider)
        logo = dff.iloc[0]['logo']
        dict_new['data_provider'] = provider
        dict_new['use_case'] = ','.join(use_cases)
        dict_new['logo'] = logo
        dict_new['data_category'] = ','.join(data_categories)
        newdf_list.append(dict_new)
    newdf = pd.DataFrame(newdf_list)
    newdf.to_csv('results/'+ exit_name + '.csv', index=False)
    return 0




form_list_of_datasets(data_gov_lt, 'data.gov.lt')