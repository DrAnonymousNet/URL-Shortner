from rest_framework.exceptions import APIException
from rest_framework import status


class AvailableAlready(APIException):
    status_code = status.HTTP_208_ALREADY_REPORTED


class LinkTooLong(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
