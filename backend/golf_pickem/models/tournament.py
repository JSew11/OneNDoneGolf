from django.db import models
from safedelete.models import SafeDeleteModel
from safedelete import SOFT_DELETE_CASCADE

class Tournament(SafeDeleteModel):
    """Model for a tournament.
    """