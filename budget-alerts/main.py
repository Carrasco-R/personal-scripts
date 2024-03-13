import os
import requests
import json

YNAB_ACCESS_TOKEN=os.environ.get('YNAB_ACCESS_TOKEN')
BUDGET_ID=os.environ.get('BUDGET_ID')
DISCRETIONARY_SPENDING_CATEGORY_GROUP_ID=os.environ.get('DISCRETIONARY_SPENDING_CATEGORY_GROUP_ID')

response = requests.get(
  f'https://api.ynab.com/v1/budgets/{BUDGET_ID}/categories',
  headers={'Authorization': f'Bearer {YNAB_ACCESS_TOKEN}'}
)
json_response = response.json()
category_groups = json_response["data"]["category_groups"]

# print(json.dumps(category_groups))
def filter_by_category_group(category_group):
  if (category_group['id'] == DISCRETIONARY_SPENDING_CATEGORY_GROUP_ID):
    return True
  else:
    return False
    
[discretionary_category_group] = list(filter(filter_by_category_group,category_groups))
# print(json.dumps(discretionary_category_group["categories"]))

def map_category(category):
  name = category['name']
  target = category['budgeted'] / 1000
  target = round(target,2)
  balance = category['balance'] / 1000
  balance = round(balance,2)
  return f'{name}: ${balance:.2f} / ${target:.2f}'

report = list(map(map_category,discretionary_category_group["categories"]))

message = '\n'.join(report)
# print(message)
