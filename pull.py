import feedparser
import csv

def get_latest_legislation():
	del_leg_rss_url = "http://legis.delaware.gov/rss/RssFeeds/IntroducedLegislation"
	return feedparser.parse( del_leg_rss_url )

#def load_introduced_legislation():
	# load old xml file

def update_legislation():
	# loop through new legislation
	L = get_latest_legislation()
	with open('legPull.csv', mode='w') as latest_legislation_csv:
	
		latest_legislation_csv_writer = csv.writer(latest_legislation_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


		for item in L.entries:
			#print item
			
			link = item['title']
			category = item['category']
			title = item['title']
			description = item['description']
			#pubdate = item['pubdate']
			session = item['legislativesession']


			#write line to csv file
			latest_legislation_csv_writer.writerow([link, category, title, description, session])
	
	#print link + ',' + category + ',' + title + "," + description

update_legislation()

