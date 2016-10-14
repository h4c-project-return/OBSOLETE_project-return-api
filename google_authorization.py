from oauth2client import client
from apiclient import discovery
import httplib2


def build_auth_context(client_secret_filename, scope_uri, redirect_uri, user_agent):
    flow = client.flow_from_clientsecrets(
        client_secret_filename,  # "client_secret.json"
        scope = scope_uri,  # 'https://www.googleapis.com/auth/spreadsheets.readonly'
        redirect_uri = redirect_uri)  # 'http://localhost'
    flow.user_agent = user_agent  # 'Project Return JR Web Layer'
    return flow


def build_auth_uri(context):
    return context.step1_get_authorize_url()


def process_auth_response(context, auth_code):
    return context.step2_exchange(auth_code).to_json()


def credentials_are_current(credentials_json):
    try:
        credentials = client.OAuth2Credentials.from_json(credentials_json)
    except Exception as e:
        raise Exception("Invalid credentials.", e)
    return not credentials.access_token_expired

"""
auth_code = raw_input(build_auth_uri("http://localhost"))
credentials = process_auth_response(auth_code)


from google_sheets import *
result = get_sheet_values_cred('1s_EC5hn-A-yKFUYWKO3RZ768AVW9FL-DKNZ3QBb0tls', 'Job Opportunities', credentials)

print(result)
"""
