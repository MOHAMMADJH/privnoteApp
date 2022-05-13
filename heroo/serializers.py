from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        # email = serializers.CharField()
        # password = serializers.CharField(required=False)
        # self_d = serializers.CharField(required=False)
        # note_name = serializers.CharField(required=False)
        model = Note
        fields = ['note', 'email', 'password', 'self_d', 'note_name']
        # exclude = ['note_id', 'is_d']
        optional_fields = []
