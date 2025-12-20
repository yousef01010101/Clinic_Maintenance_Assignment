from flask import Flask, request, redirect, url_for, render_template, jsonify
import datetime

app = Flask(__name__)
patients = []
appointments = []
_next_id = 1

def add_patient_record(name, age, phone):
    global _next_id
    
from flask import Flask, request, redirect, url_for, render_template, jsonify
from services.patient_service import (
    add_patient, find_patient, delete_patient, patients
)
from services.appointment_service import (
    add_appointment, delete_appointment, appointments
)
from validators.patient_validator import validate_patient_form
from validators.appointment_validator import validate_appointment_data

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', patients=patients, appointments=appointments)


@app.route('/patients')
def list_patients():
    return render_template('patients.html', patients=patients)


@app.route('/patients/add', methods=['GET', 'POST'])
def patient_add():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        phone = request.form.get('phone')
        errors = validate_patient_form(name, age, phone)
        if errors:
            return render_template('patient_add.html', errors=errors)
        add_patient(name.strip(), str(int(age)), phone.strip())
        return redirect(url_for('list_patients'))
    return render_template('patient_add.html')


@app.route('/patients/<int:pid>/edit', methods=['GET', 'POST'])
def patient_edit(pid):
    p = find_patient(pid)
    if not p:
        return "Not Found", 404
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        phone = request.form.get('phone')
        errors = validate_patient_form(name, age, phone)
        if errors:
            return render_template('patient_edit.html', patient=p, errors=errors)
        p['name'] = name.strip()
        p['age'] = str(int(age))
        p['phone'] = phone.strip()
        return redirect(url_for('list_patients'))
    return render_template('patient_edit.html', patient=p)


@app.route('/appointments')
def list_appointments():
    return render_template('appointments.html', appointments=appointments)


@app.route('/appointments/create', methods=['GET', 'POST'])
def appointment_create():
    if request.method == 'GET':
        return render_template('appointment_create.html', patients=patients)
    pid = request.form.get('patient_id')
    date = request.form.get('date')
    desc = request.form.get('description')
    errors = validate_appointment_data(pid, date)
    if errors:
        return render_template('appointment_create.html', errors=errors, patients=patients)
    patient = find_patient(int(pid))
    add_appointment(patient, date, desc)
    return redirect(url_for('list_appointments'))


@app.route('/appointments/<int:aid>/delete', methods=['POST'])
def appointment_delete(aid):
    from services.appointment_service import delete_appointment
    delete_appointment(aid)
    return redirect(url_for('list_appointments'))


@app.route('/del_patient/<int:pid>')
def del_patient(pid):
    delete_patient(pid)
    delete_appointment(pid)
    return redirect(url_for('list_patients'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
