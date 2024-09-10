from flask_marshmallow import Marshmallow

from marshmallow import validate
from src.contacts.domain.model import Contact

ma = Marshmallow()

class ContactSchema(ma.Schema):
    class Meta:
        model = Contact

        load_instance = True
        fields = ("id", "first_name", "last_name", "birthday", "email_address", "created_at")

    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    birthday = ma.Date(required=True, format="%Y-%m-%d")
    email_address = ma.String(validate=[validate.Email(error='Email address must be valid'), validate.Length(min=3, max=255, error='Email address must be provided.')], required=True)