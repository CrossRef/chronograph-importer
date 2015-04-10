import simplejson
import mysql.connector
import requests
import iso8601

REQUIRED_KEYS = ["username",
                 "password",
                 "database",
                 "table",
                 "doi_select",
                 "doi_row_name",
                 "type_column_mapping",
                 "doi-endpoint"]

def strip_prefixes(prefixes, input):
  for prefix in prefixes:
    if input.startswith(prefix):
      input = input[len(prefix):]
  return input
 
with open('config.json') as config_file:    
    config = simplejson.load(config_file)

missing = False
for key in REQUIRED_KEYS:
  if key not in config:
    print "Key %s missing from config" % key
    missing = True

if missing:
  exit()

cnx = mysql.connector.connect(user=config["username"], password=config["password"], database=config["database"], buffered=True)
read_cursor = cnx.cursor()
write_cursor = cnx.cursor()

print config["doi_select"]
read_cursor.execute(config["doi_select"])

num_good_dois = 0
bad_dois = []

for row in read_cursor:
  # Database may have non-standard DOI syntax. 
  # Transform for use in the API, but keep for insertion later.
  db_doi = row[0]

  doi = strip_prefixes(["http://", "https://", "dx.", "doi.org/", "doi:"], db_doi)

  url = config["doi-endpoint"] % {"doi": doi}

  response = requests.get(url, headers={"Accept": "application/json"})

  print "Fetch %s" % url
  if response.status_code == 200:
    response_json = simplejson.loads(response.text)

    # The various types are split into the three categories. Just combine them.
    data = response_json['milestones'] + response_json['events'] + response_json['facts']

    for (type_name, db_row_name) in config["type_column_mapping"].items():

      item = next((x for x in data if x['type-name'] == type_name), None)

      if item:
        # Some of these are templated with config values, some are for prepared statement templating.
        q = "UPDATE %s SET %s = %%(value)s where %s = %%(doi)s" % (config["table"], db_row_name, config["doi_row_name"])

        event_date = iso8601.parse_date(item["event"])

        d = {"value": event_date, "doi": db_doi}

        write_cursor.execute(q, d)
        cnx.commit()
        num_good_dois += 1

      else:
        bad_dois.append(doi)

cnx.close()

print "Processed %d good DOIs, %d unrecognised ones" % (num_good_dois, len(bad_dois))

print "Unrecognised:"
for doi in bad_dois:
  print doi