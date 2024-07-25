# See this as a reference: https://mockend.com/

import os
import glob
import argparse

import dex.utils

from dex.utils.customrequest import CustomRequest
from dex.utils.postman import generate_collections_by_status_code
from dex.utils.translation import read_records_from_csv

DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


def main():
    parser = argparse.ArgumentParser(description="Send a batch of requests to a target servers.")
    parser.add_argument("input_file", type=str, help="Path to the input CSV file containing request records.")

    args = parser.parse_args()

    cleanup_collections()

    records = read_records_from_csv(args.input_file)
    requests = collect_reqeusts_from_records(DEFAULT_HEADERS, records)

    batch_send_requests(requests)
    batch_print_requests(requests)
    generate_collections_by_status_code(requests)

    print("Done.")


def batch_print_requests(requests):
    """Print all requests in the batch"""
    for req in requests:
        print(req)


def collect_reqeusts_from_records(headers, records) -> list:
    requests = []
    # Collect all request objects
    for record in records:
        method = record[0]
        endpoint = record[1]
        resource = record[2]
        querystring = record[3]
        encoding = record[4]

        req = CustomRequest(method, endpoint, resource, encoding, headers, querystring)
        requests.append(req)

    return requests


def batch_send_requests(requests):
    # Send all requests
    for req in requests:
        try:
            res = req.send()
        except ValueError as e:
            print(f"Error: {e}")
            continue

        print(req)


def cleanup_collections():
    # Delete collections from the last run.
    for filename in glob.glob("collection_status_*.json"):
        os.remove(filename)


if __name__ == "__main__":
    main()
