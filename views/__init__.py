from Utils.utils import json_response


class BaseView():
    def __init__(self, request):

        self.request = request

    @json_response
    def dispatcher(self):
        if self.request.method == 'GET':
            return self.get()

        elif self.request.method == 'POST':
            return self.post()

        elif self.request.method == 'PATCH':
            return self.patch()

        elif self.request.method == 'PUT':
            return self.put()

        elif self.request.method == 'DELETE':
            return self.delete()

    def get(self):
        return "ECHO: GET\n"

    def post(self):
        return "ECHO: POST\n"

    def patch(self):
        return "ECHO: PACTH\n"

    def put(self):
        return "ECHO: PUT\n"

    def delete(self):
        return "ECHO: DELETE"
