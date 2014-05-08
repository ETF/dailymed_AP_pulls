"""
This script pulls a list of supplier's drug families listed on DailyMed.
Change supplier object as needed.
Script can be modified for suppliers with more than 100 products or
more than one page of returned from API call.
"""

import requests
from pandas.io.json import json_normalize
from time import strftime
import pandas as pd

def dailymed_lookup():

    """Execute API call, massage and export pandas DataFrame"""
    supplier = 'Northstar'
    query = 'http://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?labeler=%s' % supplier
    text = requests.get(query)
    api_response = text.json()
    blue_data = json_normalize(api_response['data'])

    s = blue_data['title']
    s.name = 'manufacturer'
    del blue_data['title']

    blue_data = blue_data.join(s.apply(lambda x: pd.Series(x.split('['))))
    blue_data['drug_dose'] = blue_data[0]
    blue_data['manufacturer_dirty'] = blue_data[1]
    blue_data['manufacturer'] = blue_data['manufacturer_dirty'][0][:-1]
    blue_data = blue_data.drop([0, 1, 'manufacturer_dirty'], axis=1)
    blue_data.columns = [x.upper() for x in blue_data.columns]
    blue_data.to_csv('%s_dailymed_%s_drug_list_pulled.csv' %
                                (strftime('%Y%m%d'), supplier))

dailymed_lookup()
                                
