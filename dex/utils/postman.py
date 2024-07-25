
import json


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

    print("Postman collections saved.")
