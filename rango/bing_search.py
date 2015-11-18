import json
import urllib, urllib2
import keys

# Have to add the bing API key, and know how to do it from keys.py
# BING_API_KEY = '<insert_big_api_key>'

def run_query(search_terms):
	rool_url = 'https://api.datamarket.azure.com/Bing/Search'
	source = 'Web'

	# Offset specifies where in results list to start from. IF offset was 11, it'll start in page 2
	results_per_page = 25
	offset = 0

	# This is used to wrap quotes ('') around the query required by Bing
	query = "'{0}'".format(search_terms)
	query = urllib.quote(query)

	search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
		root_url,
		source,
		results_per_page,
		offset,
		query)

	username = ''

	# Create a password manager which handles authentication for us
	password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
	password_mgr.add_password(None, search_url, username, BING_API_KEY)

	# This is the result list which'll be populated later
	results = []

	try:
		# Prepare for connecting to Bing's servers
		handler = urllib2.HTTPBasicAuthHandler(password_mgr)
		opener = urllib2.build_opener(handler)
		urllib2.install_opener(opener)

		# Connect to the server and read the response generated
		response = urllib2.urlopen(search_url).read()

		# Convert the string response to a Python dictionary object.
		json_response = json.loads(response)

		# Loop through each page returned, populating out results list
		for results in json_response['d']['results']:
			results.append({
				'title': result['Title'],
				'link': result['Url'],
				'summary': result['Description']
				})

	# Catch a URL Error exception - something went wrong when connecting!
	except urllib2.URLError, e:
		print "Error when querying the Bing API: ", e

	return results