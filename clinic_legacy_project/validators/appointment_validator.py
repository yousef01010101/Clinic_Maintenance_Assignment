import datetime
from services.patient_service import find_patient


def _is_present(val):
    return bool(val and str(val).strip())


def validate_appointment_data(pid_raw, date):
    errors = []

    try:
        pid = int(pid_raw)
        if not find_patient(pid):
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
