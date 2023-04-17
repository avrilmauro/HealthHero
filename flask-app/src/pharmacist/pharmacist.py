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


@pharmacist.route('/update_medication_inventory', methods=['PUT'])
def update_medication_inventory():
    
    req_data = request.get_json()

    # get a cursor object from the database
    cursor = db.get_db().cursor()

    MedID = req_data['MedID']
    PharmID = req_data['PharmID']
    new_qty = req_data['new_qty']

    query = 'UPDATE Pharmacy_contains_Medication '
    query += "SET QtyInStock = " + str(new_qty) + " "
    query += 'WHERE MedID = ' + str(MedID) + " AND PharmID = " + str(PharmID) + ""
    
    cursor.execute(query)
    db.get_db().commit()

    return 'Successfully updated medicine stock'


# @pharmacist.route('/add', methods=['POST'])
# def delete_():
    

# @pharmacist.route('/delete', methods=['DELETE'])
# def delete_():
    