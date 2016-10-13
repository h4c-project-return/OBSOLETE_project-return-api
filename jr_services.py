from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
def api_root():
    return 'These are not the droids you are looking for.'

@app.route('/opportunities', methods=['GET'])
def api_opportunities():
    return 'List of ' + url_for('api_opportunities')

@app.route('/opportunities/search', methods=['POST'])
def api_opportunities_search():
    return 'You are reading ' + articleid

if __name__ == '__main__':
    app.run()
