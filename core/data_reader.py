import csv
import os

def read_test_data(env):
    file_name = "qa_data.csv" if env == "QA" else "uat_data.csv"

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_root, "data", file_name)

    data = {}

    with open(file_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        # Clean fieldnames (remove empty columns)
        fieldnames = [col.strip() for col in reader.fieldnames if col.strip()]

        if fieldnames != ["key", "value"]:
            raise Exception(
                f"Invalid CSV format in {file_name}. "
                f"Expected header: key,value but got {reader.fieldnames}"
            )

        for row in reader:
            key = row.get("key")
            value = row.get("value")

            if key:
                data[key.strip()] = value.strip() if value else ""

    return data