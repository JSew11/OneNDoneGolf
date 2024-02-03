from datetime import datetime
from django.db.models import (
    BigAutoField,
    DateTimeField,
    CharField,
    BooleanField
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
    active = BooleanField(default=False)
    start_date = DateTimeField(blank=True, null=True)
    end_date = DateTimeField(blank=True, null=True)

    def next_tournament_id(self, after_date: datetime = None) -> int:
        """Get the next tournament in the season's schedule.
        """
        date = datetime.now() if after_date is None else after_date
        tournament_season = self.schedule.filter(start_date__gt=date).order_by('start_date').first()
        if tournament_season:
            return tournament_season.tournament.id