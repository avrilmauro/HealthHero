from flask import Blueprint, request, jsonify, make_response
import json
from src import db


doctors = Blueprint('doctors', __name__)

# Get a list of of a doctor's patients name, appoitmentdates, and DOB
@doctors.route('/patient_names', methods=['GET'])
def get_patient_name_list():
    
    req_data = request.get_json()
    
    DoctorID = req_data['DoctorID']
    
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products

    query = 'SELECT Patient.fName as FirstName, Patient.lName as LastName, AppointmentDate, DOB '
    query += 'FROM Doctor join Doctor_treats_Patient using(DoctorID) '
    query += 'join Patient using(SSN) '
    query += 'Where DoctorID = ' + str(DoctorID) + ' '
    query += 'ORDER BY AppointmentDate'
    
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
@doctors.route('/patient_medical_conditions', methods=['GET'])
def get_patient_medical_condtions():
    
    req_data = request.get_json()
    
    DoctorID = req_data['DoctorID_Med_Hist']
    PatientFirstName = req_data['Patient_FirstName']
    PatientLastName = req_data['Patient_LastName']
    
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products

    query = 'SELECT ConditionName, DateDiscovered, Prevalence, TreatmentOptions, Transmissible, Causes, Severity '
    query += 'FROM Doctor join Doctor_treats_Patient using(DoctorID) '
    query += 'join Patient using(SSN) '
    query += 'join Patient_diagnosed_MedicalCondition PdMC on Patient.SSN = PdMC.SSN '
    query += 'join MedicalCondition using(ConditionID) '
    query += 'Where Patient.SSN = (SELECT SSN FROM Patient '
    query += 'Where (Patient.fName = "' + PatientFirstName + '" AND Patient.lName = "' + PatientLastName + '") AND (Doctor.DoctorID = ' + str(DoctorID) + '))'
    
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