from rest_framework import viewsets
from core.models import Post, Comment, Profile
from core.api.serializers import PostSerializer, CommentSerializer,UserSerializer,ProfileSerializer
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from core.api.permissions import IsAuthorOrReadOnly
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from core.api.authentication import APIKeyAuthentication




class PostListAPI(APIView):
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        posts = Post.objects.filter(is_published=True)
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return User.objects.all()

        return User.objects.filter(id=user.id)


    permission_classes = [IsAuthenticated]

    

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Profile.objects.all()
        return Profile.objects.filter(user=user)



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related('author')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related('user', 'post')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
