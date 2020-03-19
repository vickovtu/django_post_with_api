from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.contrib.auth import get_user_model
from rest_framework import viewsets

from rest_framework import generics
from post.models import Post
from .serialilizers import PostSerializers, UserSerializers
from .permissions import IsAuthorOrReadOnly


class PostLikeUnlike(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        post = get_object_or_404(Post, id=request.data.get('post_id'))
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            content = {'like': 'unlike'}
        else:
            post.likes.add(request.user)
            content = {'like': 'add like'}
        return Response(content, status=status.HTTP_200_OK)


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializers


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializers


class UserList(generics.ListCreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializers


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializers
