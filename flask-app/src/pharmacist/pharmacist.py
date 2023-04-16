from flask import Blueprint, request, jsonify, make_response
import json
from src import db


pharmacist = Blueprint('pharmacist', __name__)

# Get a list of all the medications that are supplied by the pharmacy that a pharmacist works at
@pharmacist.route('/pharmacy_meds', methods=['GET'])
def get_pharmacy_medications():
    
    req_data = request.get_json()
    
    EmployeeID = req_data['EmployeeID']
    
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    
    query = 'Select GenericName as MedicationName, BrandName as Manufacturer, Med_Description as Description, QtyInStock, UnitCost '
    query += 'FROM Pharmacist join Pharmacy using(PharmID) join Pharmacy_contains_Medication using(PharmID) '
    query += 'join Medication using(MedID) '
    query += 'WHERE EmployeeID = ' + str(EmployeeID) + ''
    
    cursor.execute(query)

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
       json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)