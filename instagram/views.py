from django.contrib.auth.models import User
from instagram.models import Post
from rest_framework import viewsets
from instagram.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission, SAFE_METHODS
from .serializers import UserSerializer, PostSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

class CustomPermission(BasePermission):
    """
    Custom permission which allows user to only edit his profile
    """
    def has_permission(self, request, view):
        print(request.method)
        if request.method != "GET" and not request.user.is_authenticated:
            return False
        return True
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return obj.username == request.user.username

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [CustomPermission]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer



class PostPublicViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving posts.
    """
    queryset = Post.objects.all()
    def list(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

class PostPrivateViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing of private timeline.
    """
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    def list(self, request):
        print(str(request.user))
        user = User.objects.get(username=request.user)
        users = user.following
        queryset = Post.objects.all().filter(owner__in=users.all())
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

class PostView(APIView):
    """
    A simple APIView for publishing a post
    Use username and password for auth, put photo to "photo" field, and caption to "text" field
    """
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        owner = User.objects.get(username=request.user)
        file_serializer = PostSerializer(data=request.data)
        if (Post.objects.all().filter(owner = owner)):
            return Response({"Fail":"Max limit (1) of posts reached!"}, status=status.HTTP_400_BAD_REQUEST)
        if file_serializer.is_valid():
            file_serializer.save(owner = owner)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
