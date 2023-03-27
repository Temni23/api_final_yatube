from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, \
    IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from posts.models import Post, Group
from .permissions import IsAuthorOrReadOnly
from .serializers import (PostSerializer, GroupSerializer, CommentSerializer,
                          FollowSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly)
    pagination_class = LimitOffsetPagination


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                    GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("following__username", "user__username")

    def get_queryset(self):
        user = self.request.user
        return user.follows.all()
