"""
Nytimes Best Sellers extract script

Author : Harshith Uppula
Date created: 08/09/2022
Date modified: 08/11/2022
"""

import requests
from datetime import timedelta
import datetime

def nytimes_api_trigger():

  """
    Triggering API and extracting best sellers
    :return: final_str(bestsellers containing string), last_modified(modified date of API)

  """

  data = {"list": "combined-print-and-e-book-fiction", "bestsellers-date": "", "published-date" : "", "offset" : 0 }
  requestUrl = 'https://api.nytimes.com/svc/books/v3/lists.json?list=combined-print-and-e-book-fiction&api-key=uZfQUCfEZMqoctAXEO35JrlUX6MIB6wj'
  requestHeaders = {
    "Accept": "application/json"
  }

  response = requests.get(requestUrl, headers=requestHeaders)
  last_modified = response.json()['last_modified']
  last_modified_dt = datetime.datetime.strptime(last_modified, '%Y-%m-%dT%H:%M:%S-%f:00')
  week_date = last_modified_dt - timedelta(days=last_modified_dt.weekday())
  week_date = week_date.date()

  fiction_str_old = ""
  for i in range(0,15):
    fiction_str= f"""Rank - {i+1}
Book Title - {response.json()['results'][i]['book_details'][0]['title']} 
Author - {response.json()['results'][i]['book_details'][0]['author']}
Amazon Link - {response.json()['results'][i]['amazon_product_url']}"""
    fiction_str_old = fiction_str_old + "\n" + "\n" + fiction_str

  data = {"list": "combined-print-and-e-book-nonfiction", "bestsellers-date": "", "published-date" : "", "offset" : 0 }
  requestUrl = 'https://api.nytimes.com/svc/books/v3/lists.json?list=combined-print-and-e-book-nonfiction&api-key=uZfQUCfEZMqoctAXEO35JrlUX6MIB6wj'
  requestHeaders = {
    "Accept": "application/json"
  }

  response = requests.get(requestUrl, headers=requestHeaders)
  nonfiction_str_old = ""
  for i in range(0,15):
    nonfiction_str= f"""Rank - {i+1}
Book Title - {response.json()['results'][i]['book_details'][0]['title']} 
Author - {response.json()['results'][i]['book_details'][0]['author']}
Amazon Link - {response.json()['results'][i]['amazon_product_url']}"""
    nonfiction_str_old = nonfiction_str_old + "\n" + "\n" + nonfiction_str

  

  final_str = f"""    Combined Print & E-Book Fiction Best Sellers for week {week_date}
  {fiction_str_old}
  
  Combined Print & E-Book Non-Fiction Best Sellers for week {week_date}
  {nonfiction_str_old} """



  return final_str, last_modified

