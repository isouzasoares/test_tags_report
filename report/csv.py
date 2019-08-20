import csv

def read_csv_column(csv_file, column_name, js=False):
    reader = csv.DictReader(csv_file)
    csv_tags = []
    for row in reader:
        if "FRONT" in row.keys() or "BACK" in row.keys():
            if row.get(column_name, None) and (
                js and row.get("FRONT", None) or \
                not js and row.get("BACK", None)):
                csv_tags.append(row[column_name])
        else:
                csv_tags.append(row[column_name])
    return csv_tags
