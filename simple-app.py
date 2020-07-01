import sys
import os
from flask import Flask
from flask_restful import reqparse, Api, Resource
import json
import pyodbc

# This is a simplified example that only support GET request.
# It is meant to help you to get you started if you're new to development
# and to show how simple is using Azure SQL with Python
# A more complete example is in "app.py"
# To run this simplified sample follow the README, but instead of running "flask run"
# just run "python ./simple-app.py"
# Enjoy!

# Initialize Flask
app = Flask(__name__)

# Setup Flask Restful framework
api = Api(app)
parser = reqparse.RequestParser()
# parser.add_argument('customer')

# Create connection to Azure SQL
conn = pyodbc.connect(os.environ['SQLAZURECONNSTR_WWIF'])

# Customer Class
class Rowinfo(Resource):
    def get(self):     
        # customer = {"CustomerID": customer_id}
        cursor = conn.cursor()    
        cursor.execute("SELECT * FROM BatchSummaryLive")
        result = json.loads(cursor.fetchall)        
        cursor.close()
        return result, 200
    
# Create API route to defined Customer class
api.add_resource(Rowinfo, '/rowinfo')

# Start App
if __name__ == '__main__':
    app.run()