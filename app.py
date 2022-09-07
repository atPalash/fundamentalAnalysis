import traceback

import requests
from flask import Flask, request, jsonify

from request import Request, ErrorCode

app = Flask(__name__)

routes = {}

master_server_url = "http://127.0.0.1:8000/"


@app.get("/route")
def get_routes():
    global routes
    return routes


@app.post("/route")
def add_route():
    global routes
    if request.is_json:
        err = ""
        error_code = ErrorCode.OK
        for rote, url in request.json.items():
            if routes.get(rote) is not None:
                err = f"Cannot register {rote} with similar name"

            routes[rote] = url
        if err != "":
            return Request.make_response(error_code=error_code, err_message=err), 415
        return {}
    err = f"request must be json"
    return Request.make_response(error_code=ErrorCode.Critical, err_message=err), 415


# e.g. <command> <arg name> <args> <arg name> <args> ...
# headlines -s Adani Reliance -n 10
@app.post("/service")
def call_service():
    global routes
    data = request.json
    try:
        command = data['command']
        ret = Request.post(routes[command] + "service", data=data)
        return ret
    except Exception as e:
        error_code = ErrorCode.Critical
        err = f"Post to {master_server_url} failed with {e.args}"
        return Request.make_response(error_code=error_code, err_message=err, body=traceback.format_exc())


if __name__ == '__main__':
    app.run(host="localhost", port=8000)
