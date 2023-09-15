from django.db import models
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

    # database info
    id = models.BigAutoField(primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # tournament info
    name = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    purse = models.PositiveIntegerField()
    year = models.PositiveIntegerField()