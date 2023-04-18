from flask import Blueprint, request, jsonify, make_response
import json
from src import db
import random
import datetime

patients = Blueprint('patients', __name__)

# Get all of the doctor names in the database, and if they are MD or DO
@patients.route('/doctornames', methods=['GET'])
def get_doctor_names():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('Select fName as FirstName, lName as LastName, MDorDO FROM Doctor')

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

# Get all of the doctor names in the database, and if they are MD or DO
@patients.route('/view_medical_conditions', methods=['GET'])
def view_medical_conditions():
    # get a cursor object from the database
    cursor = db.get_db().cursor()
    
    req_data = request.get_json()
    SSN = req_data['SSN_view_medical_conditinos']

    # use cursor to query the database for a list of products
    query =  'Select ConditionName, DateDiscovered, TreatmentOptions, Transmissible, Causes, Severity '
    query += 'FROM Patient join Patient_diagnosed_MedicalCondition PdMC using(SSN) '
    query += 'join MedicalCondition using(ConditionID) '
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

# Get all of the doctor names in the database, and if they are MD or DO
@patients.route('/view_your_appointments', methods=['GET'])
def view_your_appointments():
     # get a cursor object from the database
    cursor = db.get_db().cursor()
    
    req_data = request.get_json()
    patient_SSN = req_data['SSN_appointment_view']

    # use cursor to query the database for a list of products
    query = 'Select AppointmentDate, DoctorID, Doctor.fName as DoctorFirstName, Doctor.lName as DoctorLastName, Cost '
    query += 'FROM Patient join Doctor_treats_Patient using(SSN) '
    query += 'join Doctor using(DoctorID) '
    query += 'WHERE SSN = ' + str(patient_SSN)

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

# Schedule an appointment for a Patient
@patients.route('/make_an_appointment', methods=['POST'])
def make_an_appointment():
    req_data = request.get_json()
    
    appointmentDate = req_data['AppointmentDate']
    doctor_id = req_data['DoctorID_make_appointment']
    SSN = req_data['SSN_make_appointment']
    Cost = round(random.uniform(1000.00, 10000.00), 2)
    
    insert_stmt = 'INSERT INTO Doctor_treats_Patient (DoctorID,SSN,AppointmentDate,Cost) '
    insert_stmt += 'VALUES (' + str(doctor_id) + ", " + str(SSN) + ', "' + appointmentDate + '", ' + str(Cost) + ")"
    
    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)
    db.get_db().commit()
    
    output = 'Successfully scheduled an appoitment with ' + str(doctor_id) + ' on + ' + appointmentDate + "."
    return output

# Get more information about a specific patient
@patients.route('/get_prescription_list', methods=['GET'])
def get_prescription_list():
   # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    
    req_data = request.get_json()
    SSN_1 = req_data['SSN_get_prescription']

    query = 'Select MedicationCommonName, Dosage '
    query += 'FROM Patient join Prescription using (SSN) '
    query += 'WHERE SSN = ' + str(SSN_1)
    
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

# Get more information about a specific patient
@patients.route('/delete_appointment', methods=['DELETE'])
def delete_appoitment():
   # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    
    req_data = request.get_json()
    SSN_1 = req_data['SSN_delete']
    doctor_ID = req_data['DoctorID_delete']
    appointment_data = req_data['AppointmentDate_delete']

    query = 'Delete From Doctor_treats_Patient '
    query += 'WHERE SSN = ' + str(SSN_1) + ' AND DoctorID = ' + str(doctor_ID) + " AND AppointmentDate = '" + appointment_data + "'"
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return 'Successfully deleted the appoitment'


# Get more information about a specific patient
@patients.route('/update_email', methods=['PUT'])
def update_email():
   # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    
    req_data = request.get_json()
    SSN = req_data['SSN_email']
    new_email = req_data['new_email']
    old_emal = req_data['old_email']

    query = 'UPDATE Emails '
    query += "SET Email = '" + new_email + "' "
    query += 'WHERE SSN = ' + str(SSN) + " AND Email = '" + old_emal + "'"
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return 'Successfully updated email'

# Get more information about a specific patient
@patients.route('/get_insurance_info', methods=['GET'])
def get_insurance_info():
   # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    
    req_data = request.get_json()
    SSN = req_data['SSN_insurance']

    query = 'Select CompanyName, Coverage, Expiration, PlanType '
    query += 'FROM Patient join Insurance using (CompanyID) '
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




