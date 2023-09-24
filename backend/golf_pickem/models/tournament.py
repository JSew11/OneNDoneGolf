from django.db.models import (
    UniqueConstraint,
    Q,
    BigAutoField,
    DateTimeField,
    CharField,
    PositiveIntegerField
)
from safedelete.models import SafeDeleteModel
from safedelete import SOFT_DELETE_CASCADE

class Tournament(SafeDeleteModel):
    """Model for a tournament.
    """
    deleted_by_cascade = None # removes this default field from the db table
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        ordering = ['created']
        verbose_name = 'Tournament'
        verbose_name_plural = 'Tournaments'
        constraints = [
            UniqueConstraint(
                fields=['name', 'year'],
                condition=Q(deleted__isnull=True),
                name='unique_active_name_year'
            )
        ]

    # database info
    id = BigAutoField(primary_key=True, editable=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    # tournament info
    name = CharField(max_length=255)
    course = CharField(max_length=255)
    location = CharField(max_length=255)
    purse = PositiveIntegerField()
    year = PositiveIntegerField()