from urllib.parse import urljoin
from datetime import datetime

import os
import glob
import time
import json
import http.client


def create_postman_collection(requests, collection_name="Custom Collection", collection_description="Generated from CustomRequest"):
    collection = {
        "info": {
            "name": collection_name,
            "description": collection_description,
            "_postman_id": "a unique identifier",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": []
    }

    for req in requests:
        request_data = {
            "name": req.full_url(),
            "request": {
                "method": req.method,
                "header": [{"key": k, "value": v} for k, v in req.headers.items()],
                "url": {
                    "raw": req.full_url(),
                    "protocol": req.protocol,
                    "host": [req.endpoint],
                    "path": req.resource.strip("/").split("/"),
                    "query": [{"key": k, "value": v} for k, v in parse_query_string(req.querystring).items()]
                }
            }
        }
        collection["item"].append(request_data)

    return collection


def parse_query_string(querystring):
    """A simple function to parse query strings into a dictionary."""
    if not querystring or querystring == "?":
        return {}
    queries = querystring.strip("?").split("&")
    return dict(query.split("=") for query in queries if "=" in query)


def save_collection_to_file(collection, filename="collection.json"):
    with open(filename, "w") as file:
        json.dump(collection, file, indent=4)


def group_requests_by_status_code(requests):
    status_code_groups = {}
    for req in requests:
        status_code = req.status_code()
        if status_code not in status_code_groups:
            status_code_groups[status_code] = []

        status_code_groups[status_code].append(req)

    return status_code_groups


def generate_collections_by_status_code(requests):
    grouped_requests = group_requests_by_status_code(requests)
    for status_code, reqs in grouped_requests.items():
        collection = create_postman_collection(reqs, f"Status Code {status_code} Collection")
        save_collection_to_file(collection, f"collection_status_{status_code}.json")


class CustomRequest:

    @staticmethod
    def format_size(size_bytes: int) -> str:
        if size_bytes < 1024:
            return f"{size_bytes:,} bytes"
        elif size_bytes < 1024 ** 2:
            return f"{size_bytes / 1024:,.2f} KB"
        elif size_bytes < 1024 ** 3:
            return f"{size_bytes / 1024 ** 2:,.2f} MB"
        elif size_bytes < 1024 ** 4:
            return f"{size_bytes / 1024 ** 3:,.2f} GB"
        else:
            return f"{size_bytes / 1024 ** 4:,.2f} TB"

    def __init__(self, method, endpoint, resource, encoding, headers=None, querystring=None):
        self.method = method
        self.encoding = encoding
        self.resource = resource
        self.querystring = querystring

        self.response = None
        self.raw_data = None
        self.decoded_data = None
        self.json_data = None
        self.headers = headers
        self.elapsed_time_ns = 0  # Attribute to store elapsed time in nanoseconds
        self.request_time = None  # Attribute to store the time of the request

        # Check and strip the protocol from the endpoint
        if endpoint.startswith("https://"):
            self.protocol = "https"
            self.endpoint = endpoint.replace("https://", "")
        elif endpoint.startswith("http://"):
            self.protocol = "http"
            self.endpoint = endpoint.replace("http://", "")
        else:
            self.protocol = "http"  # Default to http if no protocol is specified
            self.endpoint = endpoint

        # Ensure the querystring starts with a "?' if it exists
        if querystring:
            if not querystring.startswith("?"):
                self.querystring = f"?{querystring}"
            else:
                self.querystring = querystring
        else:
            self.querystring = None

    def __str__(self):
        if self.request_time:
            request_time_str = "'" + self.request_time.strftime("%A, %B %d, %Y %I:%M %p") + "'"
        else:
            request_time_str = "'None'"

        if self.response:
            status_code_str = str(self.status_code())
            response_size_str = CustomRequest.format_size(len(self.raw_data))
        else:
            status_code_str = "'None'"
            response_size_str = CustomRequest.format_size(0)

        output = "status=" + status_code_str
        output += ", when=" + request_time_str
        output += ", duration='" + str(self.elapsed_time_ms()) + " ms'"
        output += ", size='" + response_size_str + "'"
        output += ", url='" + self.method + " " + self.full_url() + "'"

        return output

    def base_url(self) -> str:
        return urljoin(f"{self.protocol}://{self.endpoint}", self.resource)

    def partial_url(self) -> str:
        return urljoin(self.base_url(), self.querystring)

    def full_url(self) -> str:
        if self.querystring:
            return f"{self.base_url()}{self.querystring}"
        else:
            return self.base_url()

    def send(self) -> http.client.HTTPResponse:
        self.reset()

        if self.headers is None:
            self.headers = {}

        if self.encoding is None:
            self.encoding = "utf-8"

        self.method = self.method.strip().upper()
        self.encoding = self.encoding.strip()
        self.request_time = datetime.now()

        if self.protocol == "http":
            conn = http.client.HTTPConnection(self.endpoint)
        else:
            conn = http.client.HTTPSConnection(self.endpoint)

        start_time = time.time()
        conn.request(self.method, self.full_url(), headers=self.headers)

        self.response = conn.getresponse()
        self.raw_data = self.response.read()
        self.decoded_data = self.raw_data.decode(self.encoding)
        conn.close()

        end_time = time.time()
        self.elapsed_time_ns = int((end_time - start_time) * 1_000_000_000)

        return self.response

    def get(self, encoding="utf-8"):
        self.encoding = encoding
        self.method = "GET"

        return self.send()

    def post(self, encoding="utf-8"):
        self.encoding = encoding
        self.method = "POST"

        return self.send()

    def put(self, encoding="utf-8"):
        self.encoding = encoding
        self.method = "PUT"

        return self.send()

    def patch(self, encoding="utf-8"):
        self.encoding = encoding
        self.method = "PATCH"

        return self.send()

    def delete(self, encoding="utf-8"):
        self.encoding = encoding
        self.method = "DELETE"

        return self.send()

    def head(self, encoding="utf-8"):
        self.encoding = encoding
        self.method = "HEAD"

        return self.send()

    def elapsed_time_ns(self) -> int:
        return self.elapsed_time_ns

    def elapsed_time_ms(self) -> float:
        return int(round(self.elapsed_time_ns / 1_000_000))

    def status_code(self) -> int:
        if self.response:
            return self.response.status
        else:
            raise ValueError("Response is not available. Make a request first using send().")

    def add_query_param(self, key, value):
        if self.querystring:
            self.querystring += f"&{key}={value}"
        else:
            self.querystring = f"?{key}={value}"

    def reset(self):
        """Resets response data and attributes"""
        self.method = "GET"
        self.encoding = None
        self.response = None
        self.raw_data = None
        self.decoded_data = None
        self.json_data = None
        self.elapsed_time_ns = 0
        self.request_time = None
        self.headers = {}

    def get_json(self):
        if self.response:
            self.json_data = json.loads(self.response.read().decode(self.encoding))
            return self.json_data
        else:
            raise ValueError("Response is not available. Make a request first using send().")


def main(records):
    # Delete collections from the last run.
    for filename in glob.glob("collection_status_*.json"):
        os.remove(filename)

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # See this as a reference: https://mockend.com/

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

    # Send all requests
    for req in requests:
        try:
            res = req.send()
        except ValueError as e:
            print(f"Error: {e}")
            continue

        print(req)

    # Print all the requests
    for req in requests:
        print(req)

    # Create the postman collection
    generate_collections_by_status_code(requests)

    print("Postman collections saved.")

    print("Done.")


if __name__ == "__main__":
    records = [
        ("GET", "https://jsonplaceholder.typicode.com", "/comments", "postId=1", "utf-8"),
        ("GET", "https://jsonplaceholder.typicode.com", "/comments", "?postId=1", "utf-8"),
        ("GET", "https://jsonplaceholder.typicode.com", "/comments", "postId=2", "utf-8"),
        ("GET", "https://jsonplaceholder.typicode.com", "/comments", "postId=3", "utf-8"),
        ("GET", "https://jsonplaceholder.typicode.com", "/albums", None, "utf-8"),
        ("GET", "https://jsonplaceholder.typicode.com", "/posts", None, "utf-8"),
        ("GET", "https://jsonplaceholder.typicode.com", "/comments", None, "utf-8"),
        ("GET", "https://jsonplaceholder.typicode.com", "/photos", None, "utf-8"),
        ("GET", "https://jsonplaceholder.typicode.com", "/todos", None, "utf-8"),
        ("GET", "https://jsonplaceholder.typicode.com", "/users", None, "utf-8"),
        ("GET", "https://jsonplaceholder.typicode.com", "/posts/1", None, "utf-8"),
        ("GET", "https://jsonplaceholder.typicode.com", "/posts/1/comments", None, "utf-8"),
        ("POST", "https://jsonplaceholder.typicode.com", "/posts/1", None, "utf-8"),
        ("PUT", "https://jsonplaceholder.typicode.com", "/posts/1", None, "utf-8"),
        ("PATCH", "https://jsonplaceholder.typicode.com", "/posts/1", None, "utf-8"),
        ("DELETE", "https://jsonplaceholder.typicode.com", "/posts/1", None, "utf-8"),
    ]

    main(records)

