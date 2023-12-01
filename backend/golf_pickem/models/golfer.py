from django.db.models import (
    BigAutoField,
    DateTimeField,
    CharField,
)
from django.core.validators import RegexValidator
from safedelete.models import SafeDeleteModel
from safedelete import SOFT_DELETE_CASCADE

class Golfer(SafeDeleteModel):
    """Model for a golfer.
    """
    deleted_by_cascade = None # removes this default field from the db table
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        ordering = ['created']
        verbose_name = 'Golfer'
        verbose_name_plural = 'Golfers'

    # database info
    id = BigAutoField(primary_key=True, editable=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    # golfer info
    first_name = CharField(max_length=255, validators=[RegexValidator(r'^[a-zA-Z]+$')])
    last_name = CharField(max_length=255, validators=[RegexValidator(r'^[a-zA-Z .]+$')])
    country = CharField(max_length=255, validators=[RegexValidator(r'^[a-zA-Z .,]+$')])