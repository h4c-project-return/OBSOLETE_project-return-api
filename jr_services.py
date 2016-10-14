from flask import Flask, url_for, json
from opportunity_parsing import parse_opportunities
from google_sheets import get_sheet_values

def get_all_opportunities():
    sheet = get_sheet_values('1s_EC5hn-A-yKFUYWKO3RZ768AVW9FL-DKNZ3QBb0tls', 'Job Opportunities')
    return parse_opportunities(sheet)

def build_json_response_success(data, requestBody, requestMethod, requestUrl):
    return json.dumps({
        "data": data,
        "request": {
            "body": requestBody,
            "method": requestMethod,
            "url": requestUrl
        },
        "exception": None
    })

def build_json_response_failure(exception, requestBody, requestMethod, requestUrl):
    return json.dumps({
        "data": None,
        "request": {
            "body": requestBody,
            "method": requestMethod,
            "url": requestUrl
        },
        "exception": exception
    })


app = Flask(__name__)

@app.route('/')
def api_root():
    return 'These are not the droids you are looking for.'

@app.route('/opportunities', methods=['GET'])
def api_opportunities():
    return build_json_response_success(
        list(get_all_opportunities()),
        None,
        "GET",
        url_for('api_opportunities'))

@app.route('/opportunities/search/articleid', methods=['POST'])
def api_opportunities_search(articleid):
    return 'You are reading ' + articleid

if __name__ == '__main__':
    app.run()
