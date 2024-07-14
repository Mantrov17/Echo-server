import os
import re
allowed_extensions = ["htm", "html", "css", "png", "jpg"]

def code_request(url):
    body=""
    content_type = "text/html"
    extension = url.split(".")[-1]
    if extension[-1]=="/" or extension in allowed_extensions:
        if os.path.exists(url):
            if extension in ("png", "jpg"):
                content_type = f"image/{extension}"
                body = open(url, "rb").read()
            else:
                body = open(url, "r").read()
            return "200 OK", body, content_type
        return "404 Not Found", body, content_type
    return "403 Forbidden", body, content_type


def check_file_type(url):
    if url[-1] == "/" or url.split(".")[-1] in allowed_extensions:
        return True
    return False