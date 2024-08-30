from datetime import date, datetime
import re

from abc import ABC, abstractmethod

def check_email_address_format(value):
    regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    if not re.match(regex, value):
        return False
    else:
        return True
        

class Validator(ABC):

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        return self.__getattribute__(self.name)

    def __set__(self, obj, value):
        self.validate(value)
        return super().__setattr__(self.name, value)

    @abstractmethod
    def validate(self, value):
        pass


class EmailValidator(Validator):

    def __init__(self, minsize=4, maxsize=255, predicate=check_email_address_format):
        self.minsize = minsize
        self.maxsize = maxsize
        self.predicate = predicate

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f'Expected {value!r} to be a string.')
        elif len(value) < self.minsize:
            raise ValueError(f'The provided email address {value!r} is smaller than the minimum of {self.minsize!r} characters.')
        elif len(value) > self.maxsize:
            raise ValueError(f'The provided email address {value!r} is bigger than the maximum of {self.maxsize!r} characters.')
        elif not self.predicate(value):
            raise ValueError(f'The provided email address {value!r} does not match the accepted email format.')
        else:
            self.value = value
            return None

class Name:
    def __get__(self, obj, objtype=None):
        return self.value
    
    def __set__(self, obj, value):
        if type(value) != str:
            raise TypeError("Name must be a string")
        self.value = value

class CustomDate:
    def __get__(self, obj, objtype=datetime.date):
        return self.value
    
    def __set__(self, obj, value):
        try:
            self.value = date.fromisoformat(value)
        except ValueError:
            raise ValueError('This value cannot be converted to a date')


class EmailAddress:
    def __get__(self, obj, objtype=None):
        return self.value
    
    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError(f'Expected {value!r} to be a string.')
        elif len(value) < 3:
            raise ValueError(f'The provided email address {value!r} is smaller than the minimum of 3 characters.')
        elif len(value) > 255:
            raise ValueError(f'The provided email address {value!r} is bigger than the maximum of 255 characters.')
        elif not check_email_address_format(value):
            raise ValueError(f'The provided email address {value!r} does not match the accepted email format.')
        else:
            self.value = value
            return None
