from flask import current_app
from flask import make_response, jsonify
from typing import Any

class ErrorResponse:
    def __new__(self, status_code: int, data: Any):
        return make_response(jsonify(data), status_code)


class BaseCustomException(Exception):
    """Base class for custom Exceptions"""

    status_code: int
    message: str

    def __init__(self, *args) -> None:
        pass

    def __str__(self):
        return self.message

    @property
    def errors(self):
        return {"error": self.message}

    def _log(self):
        current_app.logger.debug(f"{type(self).__name__} - {self.message}")


class RecordExists(BaseCustomException):
    """Raised when the record already exists."""
    status_code = 400
    message = 'Contact already exists with this email address'

    def __init__(self, email_address):
        self.email_address = email_address
        self.message = f"{self.message} - {self.email_address}"


class InvalidRecord(BaseCustomException):
    """Raised when the record does not exist."""
    status_code = 404
    message = 'No contact found with this id'

    def __init__(self, id):
        self.id = id
        self.message = f"{self.message} - {self.id}"


class ServerError(BaseCustomException):
    """Raised for all other errors"""
    status_code = 500
    message = "Internal Server Error"

    def __init__(self):
        self.message = self.message


class BadRequestException(BaseCustomException):
    status_code = 400
    message = "Bad Request"

    def __init__(self, detail) -> None:
        self.detail = detail
        self.message = f"{self.message} - {self.detail}"