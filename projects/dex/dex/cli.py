# See this as a reference: https://mockend.com/

import os
import glob
import argparse
import statistics

from tools import *

DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


def batch_print_requests(requests):
    """Print all requests in the batch"""
    with open('requests.log', 'a') as log_file:
        for req in requests:
            print(req)
            log_file.write(str(req) + '\n')


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
    """Remove all collection status files"""
    for filename in glob.glob("collection_status_*.json"):
        print(f"Removing {filename} ...")
        os.remove(filename)


def ns_to_ms(nanoseconds) -> int:
    return int(round(nanoseconds / 1_000_000))


def display_request_statistics(requests):
    # Extract durations from the requests
    durations = [ns_to_ms(req.elapsed_time_ns) for req in requests]

    successful_requests = 0
    failed_requests = 0

    for req in requests:
        # Assuming `req` has a `status_code` attribute and considering 2xx codes as successful
        status = req.status_code()
        if 200 <= status < 300:
            successful_requests += 1
        else:
            failed_requests += 1

    # Calculate statistics
    min_duration = min(durations)
    max_duration = max(durations)
    mean_duration = statistics.mean(durations)
    median_duration = statistics.median(durations)
    mode_duration = statistics.mode(durations)
    std_deviation = statistics.stdev(durations)
    variance = statistics.variance(durations)

    # Summarize total requests and elapsed time
    total_requests = len(requests)
    total_elapsed_time = sum(durations)

    # Display statistics
    print()
    print("Request Statistics")
    print("=" * 50)
    print(f"Total Requests: {total_requests}")
    print(f"Successful Requests: {successful_requests}")
    print(f"Failed Requests: {failed_requests}")
    print(f"Total Elapsed Time: {total_elapsed_time} ms")
    print(f"Minimum Duration: {min_duration} ms")
    print(f"Maximum Duration: {max_duration} ms")
    print(f"Mean Duration: {mean_duration} ms")
    print(f"Median Duration: {median_duration:.2f} ms")
    print(f"Mode Duration: {mode_duration} ms")
    print(f"Standard Deviation: {std_deviation:.2f}")
    print(f"Variance: {variance:.2f}")
    print("=" * 50)
    print()


def main():
    parser = argparse.ArgumentParser(description="Send a batch of requests to a target servers.")
    parser.add_argument("input_file", type=str, help="Path to the input CSV file containing request records.")

    args = parser.parse_args()

    cleanup_collections()

    records = read_records_from_csv(args.input_file)
    requests = collect_reqeusts_from_records(DEFAULT_HEADERS, records)

    batch_send_requests(requests)
    batch_print_requests(requests)
    display_request_statistics(requests)
    generate_collections_by_status_code(requests)

    print("Done.")


if __name__ == "__main__":
    main()
