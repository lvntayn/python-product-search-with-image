from flask import Flask, Blueprint, request
from flask_restful import Api
from profind.resources.search import Search

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

""" Configs """
app.debug = True
app.testing = True
app.config['BUNDLE_ERRORS'] = True

""" Sources """
api.add_resource(Search, '/search')
app.register_blueprint(api_bp)

'''
@app.route('/')
def hello():
    return "hello"
'''

if __name__ == '__main__':
    app.run()