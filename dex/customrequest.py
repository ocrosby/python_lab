import csv
import os
import glob
import urllib
import time
import json
import http.client

from urllib.parse import urljoin
from datetime import datetime


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
