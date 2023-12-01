from django.db.models import (
    UniqueConstraint,
    Q,
    BigAutoField,
    DateTimeField,
    ForeignKey,
    CASCADE,
)
from safedelete.models import SafeDeleteModel
from safedelete import SOFT_DELETE_CASCADE

from .golfer import Golfer
from .season import Season

class GolferSeason(SafeDeleteModel):
    """Model for a golfer playing in a season.
    """
    deleted_by_cascade = None # removes this default field from the db table
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        ordering = ['created']
        verbose_name = 'Golfer'
        verbose_name_plural = 'Golfers'
        constraints = [
            UniqueConstraint(
                fields=['golfer', 'season'],
                condition=Q(deleted__isnull=True),
                name='unique_golfer_season'
            )
        ]

    # database info
    id = BigAutoField(primary_key=True, editable=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    # related models
    golfer = ForeignKey(Golfer, on_delete=CASCADE, related_name='seasons')
    season = ForeignKey(Season, on_delete=CASCADE, related_name='golfers')