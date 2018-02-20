#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 19:11:49 2018

@author: Looker
"""

#import pandas as pd
#import helpers
execfile('helpers.py')
execfile('classes.py')



# step 1 create leads
    # is new account or current account?
    
# step 2 convert to account
    # create as contact
    # do I need to convert?
        # if yes, then create account
        # if no, then associate account_id

# step 3 create new business opportunities
    # go through all non-customers
    # is account a customer?
        # if no
        

create_lead_or_contacts(20,'leads')

convert_leads_by_id(convert_leads(not_converted=find_not_converted(), percent=0.1))
create_accounts(names=find_accounts_to_create())

tmp = sf_opportunity()
tmp2 = tmp.update(attr='amount', new_value=1)
tmp2.write_history()
tmp2 = tmp.update(attr='stage', new_value='2. Discovery')
tmp2.write_history()
tmp2 = tmp.update(attr='stage', new_value='2. Discovery')
tmp2.write_history()
tmp2 = tmp.update(attr='is_won', new_value=True)
tmp2.write_history()
tmp2 = tmp.update(attr='is_closed', new_value=True)
tmp2.write_history()

