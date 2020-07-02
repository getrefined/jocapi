import sys
import os
from flask import Flask, send_file
from flask_restful import reqparse, Api, Resource
import simplejson as json
import pyodbc
import csv

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
       
        cursor.close()
        return result, 200

class RowinfoCSV(Resource):
    def get(self):     

        cursor = conn.cursor()    
        cursor.execute("SELECT BatchNumber, Location, Area, RowNumber, MRNote, BMNote, Name, GrillSize, Quantity, WeightPerBag, TotalWeight, Ploidy, CONVERT(CHAR(8), MovementDate, 112) AS MovementDate, Type, BagColor, MeshSize, SupplierName, NoPerBag, KgPerBag, RowID FROM BatchSummaryLive")

        csv_file_path = 'trac.csv'

        rows = cursor.fetchall()

        result = list()

        column_names = list()
        for i in cursor.description:
            column_names.append(i[0])

        result.append(column_names)

        for row in rows:
            result.append(row)

        with open(csv_file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in result:
                csvwriter.writerow(row)
       
        cursor.close()

        return send_file("trac.csv", mimetype='text/css', as_attachment=True)

    
# Create API route for JSON & CSV
api.add_resource(Rowinfo, '/rowinfo')

api.add_resource(RowinfoCSV, '/rowinfocsv')


# Start App
if __name__ == '__main__':
    app.run()