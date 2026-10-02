"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    readings = []
    for encounter in encounters:
        readings.append(encounter["systolic"])
    return readings


def mean_systolic(readings):
    if not readings:          # empty list: nothing to average
        return None
    return sum(readings) / len(readings)


def count_patients(encounters):
    patient_ids = set()       # a set keeps each ID once
    for encounter in encounters:
        patient_ids.add(encounter["patient_id"])
    return len(patient_ids)


def patients_at_or_above(encounters, cutoff):
    flagged = set()
    for encounter in encounters:
        if encounter["systolic"] >= cutoff:
            flagged.add(encounter["patient_id"])
    return sorted(flagged)