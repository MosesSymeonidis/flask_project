class RequestValidation():
    @staticmethod
    def parameters_assertion(parameters):
        def assertions(func):
            def func_wrapper(self):
                for parameter in parameters:
                    if parameter not in self.request.args:
                        raise Exception('Error parameter')
                func(self)

            return func_wrapper

        return assertions

    def parameter_existance(self, parameter, dict):
        if parameter in dict:
            return True
        else:
            raise Exception('Error parameter')

    def parameters_existance(self, parameters, dict):
        for parameter in parameters:
            self.parameter_existance(parameter, dict)

        return True
