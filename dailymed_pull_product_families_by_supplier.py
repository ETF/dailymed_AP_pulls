"""
This script pulls a list of supplier's drug families listed on DailyMed.
Change supplier object as needed.

"""

import requests
from pandas.io.json import json_normalize
from time import strftime
import pandas as pd

supplier = 'Sandoz'

def how_many_pages():
    """How many pages of information exist?"""

    query = 'http://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?labeler=%s' % supplier
    text = requests.get(query)
    api_response = text.json()
    global num_elements
    num_elements = int(api_response['metadata']['total_elements'])
    number_of_pages, remainder = divmod(num_elements, 100)

    if remainder > 0:
        number_of_pages += 1

    return number_of_pages, num_elements

def dailymed_lookup(number_of_pages, num_elements):
    """Execute API call, massage data, and export pandas DataFrame"""

    blue_list = []

    for page in xrange(1, (number_of_pages + 1)):
        query = 'http://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?labeler=%s&page=%s' % (supplier, page)
        text = requests.get(query)
        api_response = text.json()
        blue_list.append(json_normalize(api_response['data']))

    blue_data = pd.concat(blue_list)
    s = pd.DataFrame(blue_data.title.str.split('[').tolist())
    s.rename(columns={0: 'DRUG_FAMILY', 1 :'SUPPLIER'}, inplace=True)

    replace_stuff = [']', ',', '.']
    for item in replace_stuff:
        s['SUPPLIER'] = s['SUPPLIER'].str.replace(item, '')
    blue_data = blue_data.drop(['title'], axis=1)

    blue_data.columns = [x.upper() for x in blue_data.columns]
    blue_data.to_csv('%s_dailymed_%s_drug_list_pulled.csv' %
                                (strftime('%Y%m%d'), supplier))
    if supplier == 'Bluepoint':
        num_elements = num_elements - 1
    print '%s elements returned by API call for %s' % (num_elements, supplier)

number_of_pages, num_elements = how_many_pages()
dailymed_lookup(number_of_pages, num_elements)
