appointments = []


def add_appointment(patient, date, description):
    ap = {
        'id': len(appointments) + 1,
        'patient': patient,
        'date': date,
        'description': description
    }
    appointments.append(ap)
    return ap


def delete_appointments_for_patient(pid):
    global appointments
    appointments[:] = [a for a in appointments if a['patient']['id'] != pid]
