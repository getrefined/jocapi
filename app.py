import sys
import os
from flask import Flask
from flask_restful import reqparse, Api, Resource
import simplejson as json
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
        cursor.execute("SELECT BatchNumber, Location, Area, RowNumber, MRNote, BMNote, Name, GrillSize, Quantity, WeightPerBag, TotalWeight, Ploidy, CONVERT(CHAR(8), MovementDate, 112) AS MovementDate, Type, BagColor, MeshSize, SupplierName, NoPerBag, KgPerBag, RowID FROM BatchSummaryLive")

        rows = [x for x in cursor]
        cols = [x[0] for x in cursor.description]
        rowarray_list = []

        for row in rows:
            myRow = {}
            for prop, val in zip(cols, row):
                myRow[prop] = val
                rowarray_list.append(myRow)

        result = json.dumps(rowarray_list)

        #result = json.loads(cursor.fetchall)        
        cursor.close()
        return result, 200
    
# Create API route to defined Customer class
api.add_resource(Rowinfo, '/rowinfo')

# Start App
if __name__ == '__main__':
    app.run()