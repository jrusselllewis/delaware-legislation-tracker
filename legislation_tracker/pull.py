import feedparser
import csv
import glob
import os
import time
from requests import get  # to make GET request

def newest_files():
	files = filter(os.path.isfile, glob.glob("./*.xml"))
	print(files)
	files.sort(key=lambda x: os.path.getmtime(x))
	print(files)

def download_feed(url, file_name):
	print("downloading feed xml from %s" % url)
	with open(file_name, "wb") as file:
		response = get(url)
		file.write(response.content)

def diff_feeds(old_feed_uri, new_feed_uri):
	# loop through new legislation
	new_feed = feedparser.parse( new_feed_uri )
	old_feed = feedparser.parse( old_feed_uri )
	latest_legislation_csv_writer = csv.writer(latest_legislation_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	for item in L.entries:
		#print item
		
		link = item['title']
		category = item['category']
		title = item['title']
		description = item['description']
		#pubdate = item['pubdate']
		session = item['legislativesession']


def write_csv(file_name):
	with open('legPull.csv', mode='w') as latest_legislation_csv:
		#write line to csv file
		latest_legislation_csv_writer.writerow([link, category, title, description, session])
	
# constants
FEED_URL = "http://legis.delaware.gov/rss/RssFeeds/IntroducedLegislation"

timestamp = time.strftime("%Y%m%d")
# download_feed(FEED_URL, "delaware_legislation_%s.xml" % timestamp)
new_file, old_file = newest_files()
