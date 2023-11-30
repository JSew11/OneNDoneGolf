from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from ..models.pick import Pick

class PickSerializer(ModelSerializer):
    """Serializer for the pick model.
    """

    class Meta:
        model = Pick
        exclude = ['created', 'updated', 'deleted']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Overwritten create method to work with the custom PickManager class.
        """
        user_id = validated_data['user'].id
        tournament_golfer_id = validated_data['tournament_golfer'].id
        return Pick.objects.create(user_id=user_id, tournament_golfer_id=tournament_golfer_id)