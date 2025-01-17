import csv


def read_csv_column(csv_file, column_name, ts=False):
    """
    Responsible to the read csv
    returns csv tags and validate column BACK and FRONT
    :param csv_file: The csv file obj
    :type csv_file: file
    :param column_name: The csv column with the tags
    :type column_name: str
    :param ts: if True the code validates from csv FRONT column else BACK
    :type ts: bool

    :returns: csv tags
    :rtype: list
    """
    reader = csv.DictReader(csv_file)
    csv_tags = []
    for row in reader:
        row_column = row[column_name]
        if "FRONT" in row.keys() or "BACK" in row.keys():
            if row_column and (
                ts and row.get("FRONT", None) or not ts and row.get("BACK",
                                                                    None)
            ):
                csv_tags.append(row[column_name])
        else:
            csv_tags.append(row[column_name])
    return csv_tags
