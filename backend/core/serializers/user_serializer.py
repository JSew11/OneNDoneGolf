from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ..models.user import User
from golf_pickem.models import Season, UserSeason

class UserSerializer(ModelSerializer):
    """Serializer for the user model.
    """
    active = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'payment_method',
            'referred_by',
            'active'
        ]
        read_only_fields = ['id']

    def get_active(self, obj: User):
        """Method to tell if a user is a participant in the currently active season.
        """
        active_season = Season.active_season()
        return None if active_season is None else UserSeason.objects.filter(deleted__isnull=True, season=active_season.id, user=obj.id).count() > 0