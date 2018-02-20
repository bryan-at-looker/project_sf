#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 19:30:43 2018

@author: Looker
"""


import pandas as pd
import requests
import json
import hashlib
import datetime
#import csv
import newlinejson as nlj
import math
import random


with open('helpers/config.json') as file:
    config = json.loads(file.read())


# API URL .json at the end refers to the expected format of the output
mockaroo_url = 'http://www.mockaroo.com/api/'
# API key
mockaroo_key = config.mockaroo_key  # your mockaroo key
mockaroo_name_schema = '0c2c12f0'

rw = {}

companies = pd.read_csv("data/inputs/companies.csv")

with open("data/inputs/companies.csv") as f:
    rw['companies'] = sum(1 for line in f)+1 # skips header

def get_random_account():
    line_number = random.randrange(rw['companies'])
    one_line = pd.read_csv("data/inputs/companies.csv", skiprows=range(1, line_number-1), nrows=1 )
    return one_line.name

def get_random_name():
    mock_url = mockaroo_url + mockaroo_name_schema + '?key=' + mockaroo_key + '&count=' + str(1)
    response = requests.post(mock_url)
    return response.json()[0]

def generate_triangular_seconds():
    return int(random.triangular(high=86400, mode=42300))
    
def find_account_in_company_csv(value=None):
    if not value:
        exit
    found = companies.loc[companies['name'] == value]
    if len(found) != 1:
        found = find_account_in_company_csv(get_random_account()[0])
    return found


def create_lead_or_contacts(times=1, tp='leads', date=None):

    for i in range(times):
        if tp == 'contacts':
            sf_contact(date=date).write_contact()
        if tp == 'leads':
            sf_lead(date=date).write_lead()
            
def create_accounts(times=None, names=None):
    if not times:
        if names:
            for x in names:
                sf_account(account_name=x).write_account()
    else:
        for i in range(times):
            sf_account().write_account()
                

def find_not_converted():
    
    with nlj.open('data/outputs/contacts.json') as src:
        lead_id_from_contact = []
        for line in src:
            if 'converted_lead_id' in line:
                lead_id_from_contact.append(line['converted_lead_id'])
                
    with nlj.open('data/outputs/leads.json') as src:
        lead_ids = []
        for line in src:
            if line['id'] not in lead_id_from_contact:
                lead_ids.append(line['id'])
                
#    not_converted = [x for x in lead_ids if x not in lead_id_from_contact]
    
    return lead_ids

def find_accounts_to_create():

    with nlj.open('data/outputs/accounts.json') as src:
        account_ids = []
        for line in src:
            account_ids.append(line['account_name'])

    with nlj.open('data/outputs/contacts.json') as src:
        contact_account_ids = []
        for line in src:
            if line['account_name'] not in account_ids:
                contact_account_ids.append(line['account_name'])
            
#    accounts_needed = [x for x in contact_account_ids if x not in account_ids]
    return contact_account_ids

def convert_leads(not_converted=None, percent=None, times=None):
    if not not_converted:
        exit

    if not times:
        if percent:
            times = math.floor(len(not_converted) * percent )
        else:
            times = math.floor(len(not_converted) * 0.1 )
    
    return random.sample(not_converted, int(times))

def convert_leads_by_id(find_id=None):
    if not find_id:
        exit
        
    remaining = len(find_id)
    with nlj.open('data/outputs/leads.json') as src:
        for line in src:
            if line['id'] in find_id:
                convert = sf_lead(account_name=line['account_name']
                                , first_name=line['first_name'], last_name=line['last_name']
                                , timestamp=datetime.datetime.strptime(line['created_at'], "%Y-%m-%d %H:%M:%S"))
                convert.convert_to_contact()
                convert.write_contact()
                remaining+=-1
                find_id.remove(line['id'])
                if remaining == 0:
                    break       

