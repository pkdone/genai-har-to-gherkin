import json
from util.utils import get_arguments, read_content


##
# Main function to reduce down the size of a HTTP archive (HAR) file recorded by a browser to just
# the important entiries (HTTP requests and responses).
##
def main():
    args = get_arguments("Filter HTTP Archive (HAR) JSON content from standard input or a file and"
                         " log to standard ouput.")
    payload = read_content(args.input)
    filtered_json = filter_http_archive_entries(payload)
    echo_payload(filtered_json)


##
# Echoes the given content.
##
def echo_payload(payload):
    print(json.dumps(payload, indent=2))


##
# Parses and filters a HAR file's JSON content extracting a filtered list of entries sub-documents.
##
def filter_http_archive_entries(payload):
    har_data = json.loads(payload)
    entries = har_data.get("log", {}).get("entries", [])
    return filter_entries(entries)


##
# Filters entries in the HAR data to meet specified criteria.
##
def filter_entries(entries):
    filtered_entries = []

    for entry in entries:
        try:
            request = entry.get("request", {})
            response = entry.get("response", {})
            mime_type = response.get("content", {}).get("mimeType", "")
            status = response.get("status")

            if (status not in IGNORE_HTTP_STATUSES) and (mime_type not in EXCLUDED_MIME_TYPES):
                filtered_entry = {
                    "request": {
                        "method": request.get("method"),
                        "url": request.get("url"),
                        "postData": request.get("postData")
                    },
                    "response": {
                        "status": status,
                        "content": redact_content_if_required(response.get("content"))
                    }
                }
                filtered_entries.append(filtered_entry)
        except Exception as e:
            print(f"Error processing entry: {e}")
            continue

    return {"log": {"entries": filtered_entries}}


##
# Redacts content if the MIME type does not start with specified values.
##
def redact_content_if_required(content):
    mime_type = content.get("mimeType", "")
    size = content.get("size", 0)
    redacted_content = {
        "mimeType": mime_type,
        "size": size,
    }

    if not mime_type.startswith(NON_REDACT_MIME_TYPES):
        redacted_content["text"] = "BINARY_CONTENT"
    elif size > 1000:
        redacted_content["text"] = "TOO_BIG_TO_LOG_HERE"

    return redacted_content


# Constants
EXCLUDED_MIME_TYPES = (
    "application/javascript", "application/x-javascript", "text/javascript", "text/css",
    "image/jpeg", "image/png", "image/gif", "image/svg+xml",
    "font/ttf", "font/otf", "font/woff", "font/woff2",
    "application/octet-stream", "application/x-binary", "application/x-hex"
)
NON_REDACT_MIME_TYPES = ("text/plain", "text/html", "application/json", "application/gzip")
IGNORE_HTTP_STATUSES = (404,)


##
# Main
##
if __name__ == "__main__":
    main()
