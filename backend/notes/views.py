from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Note
from .serializers import NoteSerializer, NoteCreateSerializer, UserSerializer

class IsOwner(permissions.BasePermission):
    """Разрешение: только владелец может редактировать/удалять"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        
        if not username or not password:
            return Response(
                {'error': 'Необходимо указать username и password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Пользователь с таким именем уже существует'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response(UserSerializer(request.user).data)

class NoteListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NoteCreateSerializer
        return NoteSerializer

class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = NoteSerializer
    
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
