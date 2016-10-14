from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
   import argparse
   flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
   flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

KNOWN_HEADERS = {
    "name" : "Company Name",
    "convictionThreshold": "Conviction Threshold (Yrs)",
    "convictionRestrictions": "Conviction Restrictions",
    "schedule": "Part Time / Full Time",
    "industry": "Industry",
    "type": "Type",
    "requiredAbilities": "Required Abilities",
    "driversLicenseRequired": "Requires Driver's License",
}


def get_credentials():
   """Gets valid user credentials from storage.

   If nothing has been stored, or if the stored credentials are invalid,
   the OAuth2 flow is completed to obtain the new credentials.

   Returns:
       Credentials, the obtained credential.
   """
   home_dir = os.path.expanduser('./')
   credential_dir = os.path.join(home_dir, '.credentials')
   if not os.path.exists(credential_dir):
       os.makedirs(credential_dir)
   credential_path = os.path.join(credential_dir, 'client_secret.json')

   store = Storage(credential_path)
   credentials = store.get()
   if not credentials or credentials.invalid:
       flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
       flow.user_agent = APPLICATION_NAME
       if flags:
           credentials = tools.run_flow(flow, store, flags)
       else: # Needed only for compatibility with Python 2.6
           credentials = tools.run(flow, store)
       print('Storing credentials to ' + credential_path)
   return credentials


def fill_none(iterable):
    last_item = None
    for item in iterable:
        last_item = item or last_item
        yield last_item


def strip(iterable):
    return map(lambda s: s.strip(), iterable)


def parse_headers(sheet_values):
   return zip(fill_none(strip(sheet_values[0])), strip(sheet_values[1]))


def parse_value(primary_header, sheet_row, sheet_headers):
    header_value_pairs = zip(sheet_headers, sheet_row)
    return filter(lambda item: item[0][0] == primary_header, header_value_pairs)[0][1]


def parse_value_pairs(primary_header, parser, sheet_row, sheet_headers):
    header_value_pairs = zip(sheet_headers, sheet_row)
    return map(lambda (hdr, value): (hdr[1], parser(value)), filter(lambda item: item[0][0] == primary_header, header_value_pairs))


def parse_boolean(s):
    return s.lower == "true"


def key_val_dict_list(iterable):
    return map(lambda (k, v): { "key" : k, "value" : v }, iterable)


def parse_opportunity(sheet_row, sheet_headers):
   return {
      "name":
         parse_value("Company Name", sheet_row, sheet_headers),
      "convictionThreshold":
         parse_value("Conviction Threshold (Yrs)", sheet_row, sheet_headers),
      "convictionRestrictions":
         dict(parse_value_pairs("Conviction Restrictions", parse_boolean, sheet_row, sheet_headers)),
      "partTimeAvailable":
         "PT" in parse_value("Part Time / Full Time", sheet_row, sheet_headers),
      "industry":
         parse_value("Industry", sheet_row, sheet_headers),
      "type":
         parse_value("Type", sheet_row, sheet_headers),
      "schedule":
         parse_value("Part Time / Full Time", sheet_row, sheet_headers),
      "requiredAbilities":
         dict(parse_value_pairs("Required Abilities", parse_boolean, sheet_row, sheet_headers)),
      "driversLicenseRequired":
         parse_boolean(parse_value("Requires Driver's License", sheet_row, sheet_headers)),
      "humanFriendly":
         key_val_dict_list(
            map(
               lambda hdr: (
                  hdr[0],
                  parse_value_pairs(
                     hdr[0],
                     lambda x: x,
                     sheet_row,
                     sheet_headers)),
               filter(lambda hdr: hdr[0] not in KNOWN_HEADERS.values(), sheet_headers))),
   }


def main():
   """Shows basic usage of the Sheets API.

   Creates a Sheets API service object and prints the names and majors of
   students in a sample spreadsheet:
   https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
   """
   credentials = get_credentials()
   http = credentials.authorize(httplib2.Http())
   discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                   'version=v4')
   service = discovery.build('sheets', 'v4', http=http,
                             discoveryServiceUrl=discoveryUrl)

   ## This is where the querying starts..
   spreadsheetId = '1s_EC5hn-A-yKFUYWKO3RZ768AVW9FL-DKNZ3QBb0tls'

   ## https://developers.google.com/sheets/samples/reading
   rangeName = 'Job Opportunities'
   result = service.spreadsheets().values().get(
       spreadsheetId=spreadsheetId, range=rangeName).execute()
   values = result.get('values', [])

   if not values:
       print('No data found.')
   else:
#       print(values)
       headers = parse_headers(values)
       print(headers)
       print(parse_opportunity(values[2], headers))
       """
       for row in values:
           # Print columns A and E, which correspond to indices 0 and 4.
           print('%s, %s' % (row[0], row[4]))
"""

if __name__ == '__main__':
   main()
