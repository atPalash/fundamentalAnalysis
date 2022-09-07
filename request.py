import json
import traceback
from enum import IntEnum

import requests


class ErrorCode(IntEnum):
    OK = 1
    Warning = 2
    Error = 3
    Critical = 4


class Request:
    @staticmethod
    def post(url, data):
        err = ""
        body = ""
        error_code = ErrorCode.OK
        try:
            response = requests.post(url=url, json=data, timeout=60)
            body = json.loads(response.content)['body']
            if response.status_code != 200:
                error_code = ErrorCode.Error
                err = f"Post to {url} with {data} failed"
        except Exception as e:
            error_code = ErrorCode.Critical
            err = f"Post to {url} with {data} failed due to {e.args}"
            body = traceback.format_exc()
        return Request.make_response(error_code=error_code, err_message=err, body=body)

    @staticmethod
    def get(url):
        err = ""
        body = ""
        error_code = ErrorCode.OK
        try:
            response = requests.get(url=url)
            body = response.json()
            if response.status_code != 200:
                error_code = ErrorCode.Error
                err = f"Get to {url} failed"
        except Exception as e:
            error_code = ErrorCode.Critical
            err = f"Get to {url} failed due to {e.args}"
        return Request.make_response(error_code=error_code, err_message=err, body=body)

    @staticmethod
    def make_response(error_code=None, err_message=None, body=None):
        return {"error_code": json.dumps(error_code), "error": err_message, "body": body}
