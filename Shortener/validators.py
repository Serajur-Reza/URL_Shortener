from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def valid(value):
    url_validator=URLValidator()

    reg_val=value
    if "http" in reg_val:
        new_value=reg_val
    else:
        new_value="http://"+ value

    try:
        url_validator(new_value)
    except:
        raise ValidationError("Invalid URL")

    return new_value

"""def validate_dot_com(value):
    if not ".com" in value:
        raise ValidationError("There is no .com in url")
    return value"""
