from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class NoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Note
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'user')
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')

class NoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('title', 'content')
    
    def create(self, validated_data):
        user = self.context['request'].user
        return Note.objects.create(user=user, **validated_data)
