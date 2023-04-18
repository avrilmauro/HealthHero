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

# Delete medication
@pharmacist.route('/delete_medication', methods=['DELETE'])
def delete_medication():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    
    req_data = request.get_json()
    MedID = req_data['MedID_delete']

    query = 'Delete From Medication '
    query += 'WHERE MedID = ' + str(MedID)
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return 'Successfully deleted the medication'

# Delete medication
@pharmacist.route('/delete_prescription', methods=['DELETE'])
def delete_prescription():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    
    req_data = request.get_json()
    Presc_ID = req_data['Presc_ID']

    query = 'Delete From Prescription '
    query += 'WHERE PrescID = ' + str(Presc_ID)
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return 'Successfully deleted the prescription'


# add medication
@pharmacist.route('/add_medication', methods=['POST'])
def add_medication():
    req_data = request.get_json()
    
    Med_ID = req_data['MedID_add']
    brandName = req_data['BrandName_add']
    genericName = req_data['genericName_add']
    medDescription = req_data['med_descriptionAdd']
    
    insert_stmt = 'INSERT INTO Medication (MedID,BrandName,GenericName,Med_Description) '
    insert_stmt += 'VALUES (' + str(Med_ID) + ", '" + brandName + "', '" + genericName + "', '" + medDescription + "')"
    
    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)
    db.get_db().commit()
    
    output = "Successfully added medication."
    return output



# Get perscriptions for a certain patient
@pharmacist.route('/get_prescription', methods=['GET'])
def get_pharmacy_medications_2():
    
    req_data = request.get_json()
    
    SSN = req_data['SSN_get_prescription']
    
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    
    query = 'Select * FROM Patient join Prescription using (SSN) '
    query += 'WHERE Patient.SSN = ' + str(SSN)
    
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


# Get perscriptions for a certain patient
@pharmacist.route('/get_chemicalcompounds', methods=['GET'])
def get_chemicalcompounds():
    
    req_data = request.get_json()
    
    SSN = req_data['SSN_getchemicalcompounds']
    
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    
    query = 'Select ScientificName, CommonName, MolecularWeight, BoilingPoint, MeltingPoint, ChemID '
    query += 'FROM Patient join Prescription using (SSN) '
    query += 'join Medication using(MedID) '
    query += 'join Medication_contains_ChemicalCompounds using(MedID) '
    query += 'join ChemicalCompounds using(ChemID) '
    query += 'Where Patient.SSN = ' + str(SSN)
    
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

# add new education
@pharmacist.route('/add_new_education', methods=['POST'])
def add_new_education():
    req_data = request.get_json()
    
    EmployeeID_add_education = req_data['EmployeeID_education_add']
    institution_id_education_add = req_data['InstitutionName_education_add']
    start_year = req_data['start_year']
    end_year = req_data['end_year']
    degree = req_data['degree']
    
    insert_stmt = 'INSERT INTO Pharmacist_attended_EducationalInstitute (EmployeeID,InstitutionID,startYear,endYear,Degree) '
    insert_stmt += 'VALUES (' + str(EmployeeID_add_education) + ', ' + str(institution_id_education_add)
    insert_stmt += ', ' + str(start_year) + ', ' + str(end_year) + ", '" + degree + "')"
    
    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)
    db.get_db().commit()
    
    output = "Successfully added education."
    return output

