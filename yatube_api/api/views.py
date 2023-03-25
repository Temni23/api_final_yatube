from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from posts.models import Post, Group, Follow
from .permissions import IsAuthorOrReadOnly
from .serializers import (PostSerializer, GroupSerializer, CommentSerializer,
                          FollowSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.action == "create":
            return (IsAuthenticated(),)
        return super().get_permissions()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        serializer.save(author=self.request.user, post=post)

    def get_permissions(self):
        if self.action == "create":
            return (IsAuthenticated(),)
        return super().get_permissions()


class FollowViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                    GenericViewSet):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("following__username", "user__username")

    def create(self, request, *args, **kwargs):
        following = request.data.get("following")
        if following == request.user.username:
            return Response({"detail": "Нельзя подписаться на самого себя"},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
