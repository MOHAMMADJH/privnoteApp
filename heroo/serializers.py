from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        note = serializers.TimeField(required=True)
        email = serializers.EmailField(required=False)
        password = serializers.CharField(required=False)
        self_d = serializers.DateField(required=False)
        note_name = serializers.CharField(required=False)
        model = Note
        fields = ['note', 'email', 'password', 'self_d', 'note_name', 'note_id']

        # exclude = ['note_id', 'is_d']
        # optional_fields = []
        def get_validation_exclusions(self):
            exclusions = super(Note, self).get_validation_exclusions()
            return exclusions + ['owner']
