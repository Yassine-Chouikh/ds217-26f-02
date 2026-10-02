#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """Return the usable encounters and the number of skipped data rows."""
    with data_path.open("r", encoding="utf-8") as data_file:
        rows = data_file.readlines()

    encounters = []
    skipped = 0
    for row in rows[1:]:
        if not row.strip():
            print("Skipping a blank row.")
            skipped += 1
            continue
        fields = row.strip().split(",")
        if len(fields) != 3:
            print(f"Skipping a row with {len(fields)} fields: {row.strip()}")
            skipped += 1
            continue
        patient_id, visit_date, raw_systolic = fields
        try:
            systolic = int(raw_systolic)
        except ValueError as error:
            print(f"Skipping {patient_id}: {error}")
            skipped += 1
            continue
        if systolic < 60 or systolic > 250:
            print(f"Skipping {patient_id}: {systolic} mmHg is out of range")
            skipped += 1
            continue
        encounters.append(
            {"patient_id": patient_id, "visit_date": visit_date, "systolic": systolic}
        )
    return encounters, skipped


def main():
    """Write output/vitals_report.txt and output/followup_list.txt."""
    encounters, skipped = read_encounters(DATA_PATH)

    readings = systolic_readings(encounters)
    lines = [
        f"Usable encounters: {len(encounters)}",
        f"Skipped rows: {skipped}",
        f"Patients seen: {count_patients(encounters)}",
        f"Mean systolic: {mean_systolic(readings):.1f} mmHg",
        f"Highest systolic: {max(readings)} mmHg",
        f"Lowest systolic: {min(readings)} mmHg",
    ]

    OUTPUT_DIR.mkdir(exist_ok=True)
    report_path = OUTPUT_DIR / "vitals_report.txt"
    with open(report_path, "w", encoding="utf-8") as report_file:
        report_file.write("\n".join(lines) + "\n")

    with open(report_path, "r", encoding="utf-8") as report_file:
        print(report_file.read(), end="")
    cutoff = 140
    reason = "Apparently 140 mmHg is the stage 2 hypertension threshold... So it flags patients who probably need treatment while keeping the call list short enough for one week."
    followup_lines = [f"Cutoff: {cutoff} mmHg", f"Reason: {reason}"]
    followup_lines.extend(patients_at_or_above(encounters, cutoff))
    with open(OUTPUT_DIR / "followup_list.txt", "w", encoding="utf-8") as followup_file:
        followup_file.write("\n".join(followup_lines) + "\n")


if __name__ == "__main__":
    main()
