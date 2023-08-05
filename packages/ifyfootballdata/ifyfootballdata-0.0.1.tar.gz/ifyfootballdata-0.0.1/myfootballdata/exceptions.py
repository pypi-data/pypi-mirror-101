class BaseException(Exception):

    @staticmethod
    def noConnection(errorMessage):
        return errorMessage

    @staticmethod
    def noToken(errorMessage):
        return errorMessage

    @staticmethod
    def error404(errorMessage):
        return errorMessage

    @staticmethod
    def maxRetriesExceeded(errorMessage):
        return errorMessage
