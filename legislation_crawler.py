import csv
import json
import requests
from datetime import date

def get_latest_legislation():
  payload = {
    'sort':'',
    'page':'1',
    'pageSize':'200',
    'selectedGA[0]':'150',
    'coSponsorCheck':'false',
  }
  headers = {'content-type': 'application/json'}
  url = 'http://legis.delaware.gov/json/AllLegislation/GetAllLegislation'
  resp = requests.post(url, data=json.dumps(payload), headers=headers)
  return resp.json()

def get_old_legislation(date=date.today()):
  with open('old-legislation.json') as f:
    data = json.load(f)
  return data

def diff_legislation(old_legislation_json, latest_legislation_json):  
  # find new and updated bills
  for latest_info in latest_legislation_json['Data']:
    latest_info['Updates'] = ''
    bill_id = latest_info['LegislationNumber']
    old_info = find_bill(old_legislation_json, bill_id)

    if old_info is None:
      latest_info['Updates'] += '** NEW BILL **'
    else:
      for field in bill_fields:
        if old_info[field] != latest_info[field]:
          latest_info['Updates'] += ' [%s changed] ' % field

  # find deleted bills
  # TODO: figure out why appended items aren't being written
  #       to the csv file.
  deleted_bills = list(filter(lambda b: find_bill(latest_legislation_json, b['LegislationNumber']) is None, old_legislation_json['Data']))
  print(len(deleted_bills))
  for deleted_bill in deleted_bills:
    deleted_bill['Updates'] = 'DELETED'
    latest_legislation_json['Data'].append(deleted_bill)

  # return latest legislation with updates flagged
  return latest_legislation_json

def find_bill(json_data, id):
  for bill in json_data["Data"]:
    if bill["LegislationNumber"] == id:
      return bill

def write_legislation_csv(legislation_info):
  # print(json.dumps(legislation_info, indent=4, sort_keys=True))
  with open(base_filename + '.csv', mode='w') as latest_legislation_csv:
    latest_legislation_csv_writer = csv.writer(latest_legislation_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for l in legislation_info['Data']:
      #write line to csv file
      latest_legislation_csv_writer.writerow([
        l['LegislationNumber'],
        l['IntroductionDateTime'],
        l['LongTitle'],
        l['StatusName'],
        l['ChamberName'],
        l['Sponsor'],
        l['Updates'],
      ])

bill_fields = [
  'LegislationNumber',
  'IntroductionDateTime',
  'LongTitle',
  'StatusName',
  'ChamberName',
  'Sponsor']

datestamp = date.today().strftime("%Y%m%d")
base_filename = 'delaware_legislation_%s' % datestamp
old = get_old_legislation()
changes = diff_legislation(old, get_latest_legislation())
print('%s changes found' % len(changes['Data']))
write_legislation_csv(changes)