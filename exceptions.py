
class ServiceException(Exception):
    def __init__(
        self,
        message: object,
        error_key: object,
        error_code: object = 'Service error"',
        response_message: object = None,
    ) -> object:
        super(ServiceException, self).__init__(message)
        self.response_message = response_message
        self.error_code = error_code
        self.message = message or message.detail
        self.error_key = error_key
