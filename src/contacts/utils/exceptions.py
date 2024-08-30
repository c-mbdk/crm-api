class RecordExists(Exception):
    """Raised when the record already exists."""
    default_message = 'Contact already exists with this email address'

    def __init__(self, email_address):
        self.email_address = email_address

    def __str__(self):
        return f"{self.default_message}: {self.email_address}"


class InvalidRecord(Exception):
    """Raised when the record does not exist."""
    default_message = 'No contact found with this id'

    def __init__(self, id):
        self.id = id

    def __str__(self):
        return f"{self.default_message}: {self.id}"