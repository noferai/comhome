from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from news.models import Entry
from news.serializer import EntrySerializer
import textwrap

def news_list(request):
    return render(request, 'news.html', {})


class NewsGetApi(APIView):
    def get(self, request):
        news = Entry.objects.all()

        serializer = EntrySerializer(news, many=True)

        data_res = serializer.data

        for ind in range(len(data_res)):
            data_res[ind]['short_description'] = textwrap.wrap(data_res[ind]['text'], 30)[0]
            del data_res[ind]['text']

        return Response(data_res)


class NewsGetByIdApi(APIView):
    def get(self, request):
        id_entry = request.data['id']
        print(id_entry)
        news = Entry.objects.get(id=id_entry)
        serializer = EntrySerializer(news)

        return Response(serializer.data)
