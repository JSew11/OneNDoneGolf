from rest_framework.serializers import (
    ModelSerializer,
    ReadOnlyField,
    PrimaryKeyRelatedField,
    SerializerMethodField,
)

from core.models import User
from ..models import UserSeason
from core.serializers import (
    UserSerializer
)

class UserSeasonSerialier(ModelSerializer):
    """Serializer for the golfer season model.
    """
    user = PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    user_details = SerializerMethodField()

    prize_money = ReadOnlyField()
    tournaments_won = ReadOnlyField()

    class Meta:
        model = UserSeason
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']
    
    def get_user_details(self, obj: UserSeason):
        """Get serialized details of the user associated with this serializer's
        UserSeason model.
        """
        return UserSerializer(User.objects.get(id=obj.user.id)).data