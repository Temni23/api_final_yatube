from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .variables import comments_actions, comment_ations
from .views import PostViewSet, GroupViewSet, CommentModelViewSet

v1_router = DefaultRouter()
v1_router.register(r"posts", PostViewSet)
v1_router.register(r"groups", GroupViewSet)

app_name = "api"

urlpatterns = [
    path("v1/", include(v1_router.urls)),
    path('v1/', include('djoser.urls.jwt')),
    path("v1/posts/<int:post_id>/comments/",
         CommentModelViewSet.as_view(comments_actions)),
    path("v1/posts/<int:post_id>/comments/<int:pk>/",
         CommentModelViewSet.as_view(comment_ations)),
]
