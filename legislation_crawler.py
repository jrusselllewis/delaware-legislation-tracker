import csv
import glob
import io
import json
import socket
import sys
import urllib
from datetime import date
from datetime import datetime
from helpers import *

def get_latest_legislation():
  url = 'http://legis.delaware.gov/json/AllLegislation/GetAllLegislation'
  print('\nretrieving latest legislation from %s' % url)
  payload = {
    'sort':'',
    'page':'1',
    'pageSize':'200',
    'selectedGA[0]':'150',
    'coSponsorCheck':'false',
  }
  req = urllib.request.Request(url, json.dumps(payload).encode("utf-8"))
  req.add_header('Content-Type', 'application/json')
  resp = urllib.request.urlopen(req).read()
  return json.loads(resp.decode('utf-8'))

def get_prior_legislation(date=date.today()):
  print('\nreading last file from s3...')
  files = s3.list_files('json/delaware_legislation_%i' % date.today().year)
  files.sort(reverse=True)
  prior_json = files[1]
  return json.loads(s3.get_file_content(prior_json))

def diff_legislation(old_legislation_json, new_legislation_json):  
  # find new and updated bills
  changes = 0
  print('\ncomparing latest legislation to last download...')
  for latest_info in new_legislation_json['Data']:
    latest_info['Updates'] = ''
    bill_id = latest_info['LegislationNumber']
    old_info = find_bill(old_legislation_json, bill_id)

    if old_info is None:
      latest_info['Updates'] += '** NEW BILL **'
      changes += 1
    else:
      for field in bill_fields:
        if old_info[field] != latest_info[field]:
          latest_info['Updates'] += ' [%s changed] ' % field
          changes += 1

  # find deleted bills
  # TODO: figure out why appended items aren't being written
  #       to the csv file.
  deleted_bills = list(filter(lambda b: find_bill(new_legislation_json, b['LegislationNumber']) is None, old_legislation_json['Data']))
  changes += len(deleted_bills)
  for deleted_bill in deleted_bills:
    deleted_bill['Updates'] = 'DELETED'
    new_legislation_json['Data'].append(deleted_bill)

  # return latest legislation with updates flagged
  print(' - %i changes found' % changes)
  return new_legislation_json

def find_bill(json_data, id):
  for bill in json_data["Data"]:
    if bill["LegislationNumber"] == id:
      return bill

def write_legislation_csv(legislation_info):
  print('\nwriting latest legislation info and changes to %s.csv' % base_filename)
  legislation_csv = io.StringIO()
  csv_writer = csv.writer(legislation_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  
  # write header row
  bill_fields.append('Updates')
  csv_writer.writerow(bill_fields)

  # write records
  for l in legislation_info['Data']:
    #write line to csv file
    dtStr = l['IntroductionDateTime'].replace("/Date(","")
    dtStr.replace(")/","")
    dtStr = datetime.utcfromtimestamp(int(dtStr[:10])).strftime('%m/%d/%Y')

    csv_writer.writerow([
      l['LegislationNumber'],
      dtStr,
      l['LongTitle'],
      l['StatusName'],
      l['ChamberName'],
      l['Sponsor'],
      l['Updates'],
    ])
  s3.write_file(legislation_csv.getvalue(), '%s.csv' % base_filename)

bill_fields = [
  'LegislationNumber',
  'IntroductionDateTime',
  'LongTitle',
  'StatusName',
  'ChamberName',
  'Sponsor']

def whine(e):
  # TODO: email exception info to Russ
  raise NotImplementedError

def handler(event, context):
  try:
    print('-------------------------\n%s\n%s\n-------------------------' % (date.today(), socket.gethostname()))
    global s3
    global base_filename
    
    s3 = S3Helper('delaware-legislation-2')
  
    datestamp = date.today().strftime("%Y%m%d")
    base_filename = 'delaware_legislation_%s' % datestamp
  
    new_legislation_json = get_latest_legislation()
    s3.write_file(json.dumps(new_legislation_json), 'json/%s.json' % base_filename)
  
    prior_legislation_json = get_prior_legislation()
  
    changes = diff_legislation(prior_legislation_json, new_legislation_json)
    write_legislation_csv(changes)
  except Exception as ex:
    print('*** %s ERROR *** %s \n  on line %s' % (type(ex).__name__, ex, sys.exc_info()[-1].tb_lineno))
    # whine(e)

handler(None, None)