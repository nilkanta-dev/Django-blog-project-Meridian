
from django.core.exceptions import ValidationError
import re

def validate_username(value):
    if len(value) < 4:
        raise ValidationError("Username must be at least 4 characters long.")
    if value.isdigit():
        raise ValidationError("Username cannot contain only numbers.")
    if not re.match(r'^[A-Za-z0-9@._-]+$', value):
        raise ValidationError("Invalid characters in username.")
