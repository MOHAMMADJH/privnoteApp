from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.views import APIView

from heroo.models import Note
from heroo.serializers import NoteSerializer
from rest_framework.response import Response


class MarketingMeetingPagination(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class NoteList(APIView):
    def get(self, request, format=None):
        snippets = Note.objects.all()
        serializer = NoteSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print(dict(request.data))
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

