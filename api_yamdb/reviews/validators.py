import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    if dt.date.today().year < value:
        raise ValidationError(
            'Год создания не может быть больше текущего'
        )
    return value
