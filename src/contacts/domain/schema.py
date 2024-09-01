from flask_marshmallow import Marshmallow

from marshmallow import fields, validate
from src.contacts.domain.model import Contact

ma = Marshmallow()

class ContactSchema(ma.Schema):
    class Meta:
        model = Contact

        load_instance = True
        fields = ("id", "first_name", "last_name", "birthday", "email_address", "created_at")

    id = ma.auto_field()
    first_name = ma.auto_field(required=True)
    last_name = ma.auto_field(required=True)
    birthday = ma.auto_field(required=True, format="%Y-%m-%d")
    email_address = fields.String(validate=[validate.Email(error='Email address must be valid'), validate.Length(min=3, max=255, error='Email address must be provided.')], required=True)
    created_at = ma.auto_field()
