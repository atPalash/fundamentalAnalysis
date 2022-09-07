import traceback
from flask import Flask, request
from request import Request, ErrorCode
from serverIf import ServerIf
from stockNews.google_news_handler import GoogleNewsHandler
from utility import parser

master_server_url = "http://127.0.0.1:8000/"
this_server_url = "http://127.0.0.1:8002/"


class Server(ServerIf):
    def __init__(self):
        self.name = "Stock news server"
        self.services = {}
        self.routes = dict(url="", argument=dict(name="", type="", required=""))

        self.google_news_handler = GoogleNewsHandler()

        self.add_service("headlines", self.google_news_handler)
        self.add_service("sentiment", self.google_news_handler)

        self.register_routes_to_app()

    def get_services(self):
        return self.routes

    def add_service(self, service, obj):
        self.services[service] = obj
        self.routes[service] = this_server_url

    def register_routes_to_app(self):
        try:
            Request.post(master_server_url + "/route", data=self.routes)
        except Exception:
            raise


app = Flask(__name__)
server = Server()


@app.get("/service")
def get_service():
    global server
    return server.routes


@app.post("/service")
def call_service():
    global server
    if request.is_json:
        err = ""
        response = ""
        error_code = ErrorCode.OK
        try:
            data = request.get_json()
            command = data['command']
            args = parser.parse(data['args'])
            if command == "headlines":
                headlines = server.google_news_handler.get_headlines(ticker=args['ticker'],
                                                                     past_days=int(args.get('past_days', 30)),
                                                                     max_news_count=int(args.get('max_news_count', 10)))

                response = ""
                news_count = 0
                for news in headlines:
                    news_count += 1
                    response += f"[{news_count}. {news.title}]({news.link}) \n "
            elif command == "sentiment":
                response = server.google_news_handler.get_sentiment(ticker=args['ticker'])
            return Request.make_response(error_code=error_code, err_message=err, body=response)
        except Exception as e:
            error_code = ErrorCode.Critical
            err = f"{e.args}"
            return Request.make_response(error_code=error_code, err_message=err, body=traceback.format_exc())
    err = f"request must be json"
    return Request.make_response(error_code=ErrorCode.Critical, err_message=err), 415


if __name__ == '__main__':
    app.run(host="localhost", port=8002)
