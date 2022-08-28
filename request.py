import json
from enum import Enum

import requests


class ErrorCode(Enum):
    OK = "1"
    Warning = "2"
    Error = "3"
    Critical = "4"


class Request:
    @staticmethod
    def post(url, data):
        err = ""
        response = ""
        error_code = ErrorCode.OK
        try:
            response = requests.post(url=url, json=data)

            if response.status_code != 200:
                error_code = ErrorCode.Error
                err = f"Post to {url} with {data} failed"
        except Exception as e:
            error_code = ErrorCode.Critical
            err = f"Post to {url} with {data} failed due to {e.args}"
            response = e
        return Request.make_response(error_code=error_code, err_message=err, body=response)

    @staticmethod
    def get(url):
        err = ""
        response = ""
        error_code = ErrorCode.OK
        try:
            response = requests.get(url=url)

            if response.status_code != 200:
                error_code = ErrorCode.Error
                err = f"Get to {url} failed"
        except Exception as e:
            error_code = ErrorCode.Critical
            err = f"Get to {url} failed due to {e.args}"
            response = e
        return Request.make_response(error_code=error_code, err_message=err, body=response)

    @staticmethod
    def make_response(error_code=None, err_message=None, body=None):
        return {"error": err_message, "body": body}
