from django.db.models import (
    BigAutoField,
    DateTimeField,
    CharField
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

    # database info
    id = BigAutoField(primary_key=True, editable=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    # tournament info
    name = CharField(max_length=255)
    alias = CharField(max_length=4, blank=True, null=True)
    course = CharField(max_length=255)
    location = CharField(max_length=255)
    external_id = CharField(max_length=3) # id used in external api calls

    @staticmethod
    def create_from_external_data(external_api_data: dict) -> Tournament:
        """Creates a Tournament model from external api data taken from json.
        """
        return Tournament.objects.create(
            name=external_api_data['name'],
            course=external_api_data['courses'][0]['courseName'] if len(external_api_data['courses']) == 1 else 'Multiple',
            location=external_api_data['courses'][0]['location']['country'] if len(external_api_data['courses']) == 1 else 'Earth',
            external_id=external_api_data['tournId']
        )