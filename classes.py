#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 23:32:16 2018

@author: Looker
"""

class sf_lead:
    def __init__(self
                 , account_name=None
                 , first_name=None, last_name=None
                 , date=None, timestamp=None ):
        if account_name is None:
            tmp = get_random_account()
            self.account_name = tmp[0]
        else:
            self.account_name = account_name
        if first_name is None or last_name == None:
            name = get_random_name()
            if first_name is None:
                self.first_name = str(name['first_name'])
            if last_name is None:
                self.last_name = str(name['last_name'])
        else:
            self.first_name = first_name
            self.last_name = last_name
        self.email = self.first_name.split(' ',1)[0].lower() + '.' + self.last_name.split(' ',1)[0].lower() + '@' + self.account_name.split(' ',1)[0].lower() + '.com'
#        self.account_id = hashlib.sha224(self.account_name).hexdigest()
        if timestamp is None:
            if date is None:
                date = datetime.datetime.now().strftime("%Y-%m-%d")
            seconds = generate_triangular_seconds()
            self.created_at = datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(0,seconds)
        else:
            date = timestamp.strftime("%Y-%m-%d")
            self.created_at = timestamp
        self.id = hashlib.sha224(self.email+date+'lead').hexdigest()
        
    def convert_to_contact(self, date_converted=None, timestamp_converted=None):
        self.__class__ = sf_contact
        self.from_lead = True
        self.converted_lead_id = self.id
        self.account_id = hashlib.sha224(self.account_name).hexdigest()
        
        if timestamp_converted is None:
            if date_converted is None:
                date_converted = datetime.datetime.now().strftime("%Y-%m-%d")
            seconds = generate_triangular_seconds()
            self.created_at = datetime.datetime.strptime(date_converted, "%Y-%m-%d") + datetime.timedelta(0,seconds)
        else:
            date = timestamp_converted.strftime("%Y-%m-%d")
            self.created_at = timestamp_converted

        self.id = hashlib.sha224(self.email+date_converted+'contact').hexdigest()
                
                
    def write_lead(self):
        out = {
              "id": str(self.id)
            , "first_name": str(self.first_name)
            , "last_name": str(self.last_name)
            , "created_at": str(self.created_at)
#            , "account_id": str(self.account_id)
            , "account_name": str(self.account_name)
            , "email": str(self.email)
            }
        out = dict((k, v) for k, v in out.iteritems() if v !='None')
        with nlj.open('data/outputs/leads.json', 'a') as dst:
            dst.write(out)

        
class sf_contact:
    def __init__(self
                 , first_name = None, last_name = None
                 , account_name=None, account_id=None 
                 , date=None, timestamp=None):
        
        if account_name is None:
            tmp = get_random_account()
            self.account_name = tmp[0]
        else:
            self.account_name = account_name
            
        if first_name is None or last_name == None:
            name = get_random_name()
            if first_name is None:
                self.first_name = str(name['first_name'])
            if last_name is None:
                self.last_name = str(name['last_name'])
                
        self.email = self.first_name.split(' ',1)[0].lower() + '.' + self.last_name.split(' ',1)[0].lower() + '@' + self.account_name.split(' ',1)[0].lower() + '.com'
        self.account_id = hashlib.sha224(self.account_name).hexdigest()
        
        if timestamp is None:
            if date is None:
                date = datetime.datetime.now().strftime("%Y-%m-%d")
            seconds = generate_triangular_seconds()
            self.created_at = datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(0,seconds)
        else:
            date = timestamp.strftime("%Y-%m-%d")
            self.created_at = timestamp
        self.id = hashlib.sha224(self.email+date+'contact').hexdigest()
        self.converted_lead_id = None
        self.from_lead = False
        
    def write_contact(self):
        out = {
              "id": str(self.id)
            , "first_name": str(self.first_name)
            , "last_name": str(self.last_name)
            , "created_at": str(self.created_at)
            , "account_id": str(self.account_id)
            , "account_name": str(self.account_name)
            , "email": str(self.email)
            , "converted_lead_id": str(self.converted_lead_id)
            , "from_lead": str(self.from_lead)
            }
        out = dict((k, v) for k, v in out.iteritems() if v !='None')
        with nlj.open('data/outputs/contacts.json', 'a') as dst:
            dst.write(out)
        
        
class sf_account:
    def __init__(self
                 , account_name=None
                 , homepage_url=None, category_list=None
                 , funding_total_usd=None, status=None
                 , country_code=None, state_code=None, region=None, city=None
                 , funding_rounds=None, founded_at=None
                 , first_funding_at=None, last_funding_at=None
                 , date=None, timestamp=None):
        
        if account_name is None:
            tmp = get_random_account()
            self.account_name = tmp[0]
        else:
            self.account_name = account_name
                
        self.id = hashlib.sha224(self.account_name).hexdigest()
        
        account = find_account_in_company_csv(self.account_name)
        account_list = [e for e in list(account) if e not in ('permalink', 'name')]
        for item in account_list:
            setattr(self, item, str(account[[item]].iloc[-1].values[0]))
        
        if timestamp is None:
            if date is None:
                self.date = datetime.datetime.now().strftime("%Y-%m-%d")
            seconds = generate_triangular_seconds()
            self.created_at = datetime.datetime.strptime(self.date, "%Y-%m-%d") + datetime.timedelta(0,seconds)
        else:
            self.created_at = timestamp
        
    def write_account(self):
        out = {
              "id": str(self.id)
            , "account_name": str(self.account_name)
            , "category_list": str(self.category_list)
            , "created_at": str(self.created_at)
            , "funding_total_usd": str(self.funding_total_usd)
            , "country_code": str(self.country_code)
            , "state_code": str(self.state_code)
            , "region": str(self.region)
            , "city": str(self.city)
            , "funding_rounds": str(self.funding_rounds)
            , "founded_at": str(self.founded_at)
            , "first_funding_at": str(self.founded_at)
            , "last_funding_at": str(self.founded_at)
            }
        out = dict((k, v) for k, v in out.iteritems() if v not in ['None','nan','-'] )
        with nlj.open('data/outputs/accounts.json', 'a') as dst:
            dst.write(out)
            
class sf_opportunity:
    def __init__(self
                 , account_name=None, contact_id=None
                 , amount=None, typ=None
                 , date=None, timestamp=None):
        
        # typ > self.type ['New Business', 'Expansion', 'Contraction', 'Cancellation', 'Renewal']
        # stage > self.stage ['1. Qualification', '2. Discovery', '3. Evaluation', '4. Approval Process', '5. Buying Process', '6. Deal' ]
        
        if account_name is None:
            tmp = get_random_account()
            self.account_name = tmp[0]
        else:
            self.account_name = account_name
            
        self.amount = amount if amount else generate_amount()
        self.type = typ if typ else 'New Business'
        self.account_id = hashlib.sha224(self.account_name).hexdigest()
        self.name = self.type + ' - ' + self.account_name
        self.is_closed = False
        self.is_won = False
        self.stage = '1. Qualification'
        
        if timestamp is None:
            if date is None:
                date = datetime.datetime.now().strftime("%Y-%m-%d")
            seconds = generate_triangular_seconds()
            self.created_at = datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(0,seconds)
        else:
            date = timestamp.strftime("%Y-%m-%d")
            self.created_at = timestamp
        self.id = hashlib.sha224(self.account_id+date+self.type).hexdigest()
        self.close_date = get_close_date_estimate(self.created_at)

    def update(self, date=None, new_value=None, attr=None):
  ## NEED TO FINISH      
  
        old_value = getattr(self, attr)
        if old_value != new_value:
            setattr(self, attr, new_value)  
            if date is None:
                date = date if date else datetime.datetime.now().strftime("%Y-%m-%d")
            seconds = generate_triangular_seconds()     
            created_at = datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(0,seconds)
    
            opp_hist = opportunity_history(created_at = created_at
                                          , field=attr
                                          , old_value=old_value
                                          , new_value=new_value
                                          , source_id=self.id)
            
            return opp_hist
        
                            
        
    def write_opportunity(self):
        out = {
              "id": str(self.id)
            , "account_name": str(self.account_name)
            , "account_id": str(self.account_id)
            , "created_at": str(self.created_at)
            , "amount": int(self.amount)
            , "name": str(self.name)
            , "is_closed": str(self.is_closed)
            , "is_won": str(self.is_won)
            , "stage": str(self.stage)
            , "close_date": str(self.close_date)
            }
        out = dict((k, v) for k, v in out.iteritems() if v not in ['None','nan','-'] )
        with nlj.open('data/outputs/opportunities.json', 'a') as dst:
            dst.write(out)


#NEED TO CREATE CLASS FOR HISTORY
class opportunity_history:
    def __init__(self
                  , created_at=None, field=None
                  , old_value=None, new_value=None
                  , source_id=None
                          ):
        self.created_at = created_at
        self.field = field
        self.old_value = old_value
        self.new_value = new_value
        self.source_id = source_id
        self.id = hashlib.sha224(self.source_id+str(created_at)+self.field).hexdigest()
    
    def write_history(self):
        out = {
              "id": str(self.id)
            , "field": str(self.field)
            , "old_value": str(self.old_value)
            , "created_at": str(self.created_at)
            , "new_value": str(self.new_value)
            , "source_id": str(self.source_id)
            , "id": str(self.id)
            }
        out = dict((k, v) for k, v in out.iteritems() if v not in ['None','nan','-'] )
        with nlj.open('data/outputs/opportunity_history.json', 'a') as dst:
            dst.write(out)
    
    
    
    
    