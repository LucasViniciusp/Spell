from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    AllowAny,
)

from spell.models import User, Post, Follower
from spell.permissions import UserObjectPermission
from spell.serializers import (
    RegisterSerializer,
    FollowerSerializer,
    UserSerializer,
    PostSerializer,
)


# Create your views here.
class RegisterViewSet(CreateAPIView, GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    permission_classes = (IsAuthenticatedOrReadOnly, UserObjectPermission)

    queryset = User.objects.filter(is_active=True)
    filterset_fields = ("username",)
    search_fields = "content"
    serializer_class = UserSerializer


class FollowerViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, UserObjectPermission)

    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    filterset_fields = ("user",)
    search_fields = (
        "follow__username",
        "follow__last_name",
        "follow__first_name",
    )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, UserObjectPermission)

    queryset = Post.objects.filter(is_active=True)
    filterset_fields = ("user",)
    search_fields = "content"
    serializer_class = PostSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
