from flask import Flask, request, redirect, url_for, render_template, jsonify
import datetime

app = Flask(__name__)
patients = []
appointments = []
_next_id = 1


def add_patient_record(name, age, phone):
    global _next_id
    p = {'id': _next_id, 'name': name, 'age': age, 'phone': phone, 'notes': ''}
    patients.append(p)
    _next_id += 1
    return p

def _is_present(val):
    return bool(val and str(val).strip())


def validate_name(name):
    if not _is_present(name):
        return ['Name is required']
    return []

def validate_age(age):
    if not _is_present(age):
        return ['Age is required']
    try:
        age_int = int(str(age).strip())
    except ValueError:
        return ['Age must be an integer']
    if age_int < 0:
        return ['Age must be a non-negative integer']
    return []


def validate_phone(phone):
    if not _is_present(phone):
        return ['Phone is required']
    ph = str(phone).strip()
    if not ph.isdigit():
        return ['Phone must contain only digits']
    if len(ph) < 7:
        return ['Phone number is too short']
    return []


def validate_patient_form(name, age, phone):
    errors = []
    errors.extend(validate_name(name))
    errors.extend(validate_age(age))
    errors.extend(validate_phone(phone))
    return errors


def validate_appointment_data(pid_raw, date):
    """
    Validates appointment inputs and returns a list of errors.
    """
    errors = []
    try:
        pid = int(pid_raw)
        patient = find_patient(pid)
        if not patient:
            errors.append('Patient not found')
    except (ValueError, TypeError):
        errors.append('Invalid patient selected')

    if not _is_present(date):
        errors.append('Date is required')
    else:
        try:
            datetime.date.fromisoformat(date.strip())
        except ValueError:
            errors.append('Date must be YYYY-MM-DD')

    return errors


def find_patient(p_id):
    for p in patients:
        if p['id'] == p_id:
            return p
    return None


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
            return render_template('patient_add.html', errors=errors, name=name, age=age, phone=phone)
            
        add_patient_record(name.strip(), str(int(age.strip())), phone.strip())
        return redirect(url_for('list_patients'))
    return render_template('patient_add.html')


@app.route('/patients/<int:pid>/edit', methods=['GET', 'POST'])
def patient_edit(pid):
    p = find_patient(pid)
    if p is None:
        return "Not Found", 404
        
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        phone = request.form.get('phone')
        
        errors = validate_patient_form(name, age, phone)
        if errors:
            return render_template('patient_edit.html', patient=p, errors=errors, name=name, age=age, phone=phone)
            
        p['name'] = name.strip()
        p['age'] = str(int(age.strip()))
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

    pid_raw = request.form.get('patient_id')
    date = request.form.get('date')
    desc = request.form.get('description')

    errors = validate_appointment_data(pid_raw, date)

    if errors:
        return render_template('appointment_create.html', patients=patients, errors=errors, date=date, description=desc, patient_id=pid_raw)

    patient = find_patient(int(pid_raw))
    ap = {
        'id': len(appointments) + 1, 
        'patient': patient, 
        'date': date, 
        'description': desc
    }
    appointments.append(ap)
    
    return redirect(url_for('list_appointments'))


@app.route('/api/patients', methods=['GET'])
def api_get_patients():
    return jsonify(patients)


@app.route('/api/appointments', methods=['GET'])
def api_get_appointments():
    data = [
        {
            'id': a['id'], 
            'patient_id': a['patient']['id'], 
            'date': a['date'], 
            'description': a['description']
        } 
        for a in appointments
    ]
    return jsonify(data)


@app.route('/del_patient/<int:pid>')
def del_patient(pid):
    global patients, appointments
    patients[:] = [p for p in patients if p['id'] != pid]
    appointments[:] = [a for a in appointments if a['patient']['id'] != pid]
    return redirect(url_for('list_patients'))


add_patient_record('Ahmed Ali', '30', '091-111-222')
add_patient_record('Sara Omar', '25', '092-222-333')
appointments.append({'id': 1, 'patient': patients[0], 'date': '2025-10-22', 'description': 'General Checkup'})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)