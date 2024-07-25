import csv


def convert_records_to_csv(records, filename="records.csv"):
    # Define the header
    header = ["Method", "Endpoint", "Resource", "Querystring", "Encoding"]

    with open(filename, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)  # Write the header row

        for record in records:
            writer.writerow(record)  # Write each record


def read_records_from_csv(filename):
    records = []
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip the header row if there is one
        for row in reader:
            records.append(row)

    return records
