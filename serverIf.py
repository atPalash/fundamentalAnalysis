class ServiceArgs:
    def __init__(self, arg_name, arg_type, arg_req):
        self.name = arg_name
        self.type = arg_type
        self.required = arg_req


class ServerIf:
    def get_services(self):
        pass

    def add_service(self, service, obj):
        pass

    def register_routes_to_app(self):
        pass
