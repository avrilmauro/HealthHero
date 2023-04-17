from flask import Blueprint, request, jsonify, make_response
import json
from src import db


doctors = Blueprint('doctors', __name__)

# Get a list of of a doctor's patients name, appoitmentdates, and DOB
@doctors.route('/patient_names', methods=['GET'])
def get_patient_name_list():
    
    req_data = request.get_json()
    
    DoctorID = req_data['DoctorID_patient_names']
    
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    
    query = 'Select Patient.fName as PatientFirstName, Patient.lName as PatientLirstName, SSN, DOB '
    query += 'FROM Doctor join Doctor_treats_Patient using(DoctorID) '
    query += 'join Patient using(SSN) '
    query += 'Where Doctor.DoctorID = ' + str(DoctorID)
    
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
    PatientSSN = req_data['Patient_SSN']
    
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products

    query = 'SELECT ConditionName, DateDiscovered, Prevalence, TreatmentOptions, Transmissible, Causes, Severity '
    query += 'FROM Doctor join Doctor_treats_Patient using(DoctorID) '
    query += 'join Patient using(SSN) '
    query += 'join Patient_diagnosed_MedicalCondition PdMC on Patient.SSN = PdMC.SSN '
    query += 'join MedicalCondition using(ConditionID) '
    query += 'Where Patient.SSN = (SELECT SSN FROM Patient '
    query += 'Where (Patient.SSN = ' + str(PatientSSN) + ') AND (Doctor.DoctorID = ' + str(DoctorID) + '))'
    
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
 
 # erfef
# Daignose a patient with a new medical condition
@doctors.route('/view_medical_conditions_in_database', methods=['GET'])
def view_medical_conditions_in_database():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    query = 'Select * From MedicalCondition'
    
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
 
 # Daignose a patient with a new medical condition
@doctors.route('/diagnose', methods=['POST'])
def diagnose():
    req_data = request.get_json()
    
    ConditionID = req_data['ConditionID']
    SSN = req_data['SSN_diagnose']
    
    insert_stmt = 'INSERT INTO Patient_diagnosed_MedicalCondition (ConditionID, SSN) '
    insert_stmt += 'VALUES (' + str(ConditionID) + ', ' + str(SSN) + ')'
    
    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)
    db.get_db().commit()
    
    output = 'Successfully diagnose patinet: ' + str(SSN) + ', with condition: ' + str(ConditionID)
    return output
 
 
 # Cancel an appoitment with a Patient
@doctors.route('/cancel_appointment', methods=['DELETE'])
def cancel_appointment():
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

    return 'Successfully canceled the appointment'
 
 
 # Get more information about a specific patient
@doctors.route('/update_specialty', methods=['PUT'])
def update_specialty():
   # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    
    req_data = request.get_json()
    DoctorID = req_data['DoctorID_update_specialty']
    Specialty = req_data['Specialty_update']

    query = 'UPDATE Doctor '
    query += "SET Specialty = '" + Specialty + "' "
    query += 'WHERE DoctorID = ' + str(DoctorID)
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return 'Successfully changed specialty to: ' + str(Specialty) + ', Doctor: ' + str(DoctorID)
 
 
 
 # View the medications that are being prescribed to one of your patients
@doctors.route('/view_medication_prescribed_to_patient', methods=['GET'])
def view_medication_prescribed_to_patient():
    # get a cursor object from the database
    cursor = db.get_db().cursor()
    
    req_data = request.get_json()
    DoctorID = req_data['DoctorID_medications']
    SSN = req_data['SSN_medications']

    # use cursor to query the database for a list of products
    query = 'Select MedicationCommonName, BrandName, Dosage, '
    query += 'GenericName, Med_Description, DoctorID, Patient.SSN '
    query += 'FROM Doctor join Doctor_treats_Patient using(DoctorID) '
    query += 'join Patient using(SSN) '
    query += 'join Prescription using(DoctorID) '
    query += 'join Medication using(MedID) '
    query += 'WHERE Patient.SSN = ' + str(SSN) + ' AND Doctor.DoctorID = ' + str(DoctorID)
    
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
 
 
# View the medications that are being prescribed to one of your patients
@doctors.route('/see_what_pharmacies_have_medications_for_patient', methods=['GET'])
def see_what_pharmacies_have_medications_for_patient():
    # get a cursor object from the database
    cursor = db.get_db().cursor()
    
    req_data = request.get_json()
    DoctorID = req_data['DoctorID_meds_pharms']
    SSN = req_data['SSN_meds_pharms']

    # use cursor to query the database for a list of products
    query = 'Select CompanyName, City, State, Zip, P.Phone '
    query += 'FROM Doctor join Doctor_treats_Patient using(DoctorID) '
    query += 'join Patient using(SSN) '
    query += 'join Prescription using(DoctorID) '
    query += 'join Medication using(MedID) '
    query += 'join Pharmacy_contains_Medication using(MedID) '
    query += 'join Pharmacy P on Pharmacy_contains_Medication.PharmID = P.PharmID '
    query += 'WHERE Patient.SSN = ' + str(SSN) + ' AND Doctor.DoctorID = ' + str(DoctorID)

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
 
 