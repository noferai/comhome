from rest_framework.serializers import HyperlinkedModelSerializer
from common.models import User


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')