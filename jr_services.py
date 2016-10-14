from flask import Flask, url_for, json
from opportunity_parsing import parse_opportunities
from google_sheets import get_sheet_values

def get_all_opportunities():
    sheet = get_sheet_values('1s_EC5hn-A-yKFUYWKO3RZ768AVW9FL-DKNZ3QBb0tls', 'Job Opportunities')
    return parse_opportunities(sheet)

app = Flask(__name__)

@app.route('/')
def api_root():
    return 'These are not the droids you are looking for.'

@app.route('/opportunities', methods=['GET'])
def api_opportunities():
    return json.dumps(list(get_all_opportunities()))

@app.route('/opportunities/search', methods=['POST'])
def api_opportunities_search():
    return 'You are reading ' + articleid

if __name__ == '__main__':
    app.run()
