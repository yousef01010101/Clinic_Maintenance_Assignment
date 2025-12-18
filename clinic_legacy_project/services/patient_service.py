patients = []
_next_id = 1


def add_patient(name, age, phone):
    global _next_id
    p = {
        'id': _next_id,
        'name': name,
        'age': age,
        'phone': phone,
        'notes': ''
    }
    patients.append(p)
    _next_id += 1
    return p


def find_patient(pid):
    for p in patients:
        if p['id'] == pid:
            return p
    return None


def delete_patient(pid):
    global patients
    patients[:] = [p for p in patients if p['id'] != pid]
