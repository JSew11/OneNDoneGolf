from rest_framework.serializers import ModelSerializer

from ..models.user import User

class UserSerializer(ModelSerializer):
    """Serializer for the user model.
    """

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'payment_method',
            'referred_by'
        ]
        read_only_fields = ['id']