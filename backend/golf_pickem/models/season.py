from datetime import datetime
from django.db.models import (
    BigAutoField,
    PositiveSmallIntegerField,
    DateTimeField,
    CharField,
)
from safedelete.models import SafeDeleteModel
from safedelete import SOFT_DELETE_CASCADE

class Season(SafeDeleteModel):
    """Model for a season.
    """
    deleted_by_cascade = None # removes this default field from the db table
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        ordering = ['created']
        verbose_name = 'Season'
        verbose_name_plural = 'Seasons'

    # database info
    id = BigAutoField(primary_key=True, editable=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    # season info
    name = CharField(max_length=255)
    alias = CharField(max_length=255)
    year = PositiveSmallIntegerField()
    start_date = DateTimeField(blank=True, null=True)
    end_date = DateTimeField(blank=True, null=True)

    @property
    def status(self) -> str:
        """Gets the status of the season based on the start and end dates.
        """
        current_date = datetime.now().date()
        if current_date < self.start_date:
            return 'upcoming'
        elif current_date < self.end_date:
            return 'in progress'
        else:
            return 'finished'