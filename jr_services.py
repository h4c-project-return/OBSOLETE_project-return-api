from flask import Flask, url_for, json, make_response, request
from flask_cors import CORS
from google_sheets import get_sheet_values
from opportunity_parsing import parse_opportunities, get_opportunities_criteria
from opportunity_filtering import filter_opportunities


def get_all_opportunities():
    sheet = get_sheet_values('1s_EC5hn-A-yKFUYWKO3RZ768AVW9FL-DKNZ3QBb0tls', 'Job Opportunities')
    return parse_opportunities(sheet)


def build_json_response_success(data, request_body, request_method, request_url):
    return json.dumps({
        "data": data,
        "request": {
            "body": request_body,
            "method": request_method,
            "url": request_url
        },
        "exception": None
    })


def build_json_response_failure(exception, request_body, request_method, request_url):
    return json.dumps({
        "data": None,
        "request": {
            "body": request_body,
            "method": request_method,
            "url": request_url
        },
        "exception": exception
    })


app = Flask(__name__)
CORS(app)


@app.route('/')
def api_root():
    return 'These are not the droids you are looking for.'


@app.route('/opportunities', methods=['GET'])
def api_opportunities():
    resp = make_response(build_json_response_success(
        list(get_all_opportunities()),
        None,
        "GET",
        url_for('api_opportunities')))
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/opportunities/search', methods=['POST'])
# E.g.,  {"convictions":[{"type":"Sex","year":2004}],"partTimeOnly":False,"hasDriversLicense":True,
# "industries":["Building Construction/Skilled Trade"],"abilities":['Standing for 8hrs',
# '_Heavy Lifting', 'capable with tools and machinery', 'Attention to Detail']}
def api_opportunities_search():
    resp = make_response(build_json_response_success(
        list(filter_opportunities(request.json, get_all_opportunities())),
        request.data,
        "POST",
        url_for('api_opportunities_search')))
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/opportunities/criteria', methods=['GET'])
def api_opportunities_criteria():
    sheet_values = get_sheet_values('1s_EC5hn-A-yKFUYWKO3RZ768AVW9FL-DKNZ3QBb0tls', 'Job Opportunities')
    resp = make_response(build_json_response_success(
        get_opportunities_criteria(sheet_values),
        None,
        "GET",
        url_for('api_opportunities_criteria')))
    resp.headers['Content-Type'] = 'application/json'
    return resp

    if __name__ == '__main__':
        app.run(host="0.0.0.0", port="80")
