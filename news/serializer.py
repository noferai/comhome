from rest_framework.serializers import HyperlinkedModelSerializer
from news.models import Entry


class EntrySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = ('title', 'created_on', 'text', 'id')
