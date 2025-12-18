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
