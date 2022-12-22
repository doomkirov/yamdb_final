import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


from reviews.models import Category, Genre, Review, Title
from .filters import TitleFilter
from .mixins import CreateListDeleteViewSet
from .permissions import (
    IsAdministratorRole,
    IsAdminOrReadOnly,
    IsSuperuserAdminModeratorAuthorOrReadOnly,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    CredentialsSerializer,
    GenreSerializer,
    GetTitleSerializer,
    MyTokenObtainPairSerializer,
    PostTitleSerializer,
    ReviewSerializer,
    UserRoleSerializer,
    UserSerializer,
)

User = get_user_model()


class SignUpViewSet(viewsets.ModelViewSet):
    """Обработка принимает на вход параметры POST запросом:
    email и username, генерирует verification_code,
    создает пользователя и отправляет
    код по указаноий в параметре почте.
    Данный узел свободен от аутентификации и разрешений.
    """
    queryset = User.objects.all()
    serializer_class = CredentialsSerializer
    permission_classes = ()
    authentication_classes = ()

    def create(self, request):
        serializer = CredentialsSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = uuid.uuid4()
            serializer.save(confirmation_code=confirmation_code)

            mail_text = f'Код подтверждения {confirmation_code}'
            mail_theme = 'Код подтверждения'
            mail_from = settings.MAIL_FROM
            mail_to = serializer.data['email']
            send_mail(
                mail_theme, mail_text, mail_from, [mail_to],
                fail_silently=False
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    """Обработка выдачи токенов."""
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer


class UsersViewSet(viewsets.ModelViewSet):
    """Операции связананные с Users"""
    lookup_field = 'username'
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    permission_classes = (IsAdministratorRole,)

    @action(
        detail=False, methods=['PATCH', 'GET'], url_path='me',
        permission_classes=[IsAuthenticated]
    )
    def me_user(self, request, pk=None):
        """Обработка узла users/me"""
        user = get_object_or_404(User, username=request.user)
        serializer = UserRoleSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(CreateListDeleteViewSet):
    """Операции связананные с категориями"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class GenreViewSet(CreateListDeleteViewSet):
    """Операции связананные с жанрами"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Операции связананные с названиями произведений"""
    queryset = Title.objects.all().annotate(
        Avg('reviews__score')).order_by('name')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return PostTitleSerializer
        return GetTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Операции связананные с отзывами"""
    serializer_class = ReviewSerializer
    permission_classes = (IsSuperuserAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title_obj = get_object_or_404(Title, id=title_id)
        return title_obj.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title_obj = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title_obj)


class CommentViewSet(viewsets.ModelViewSet):
    """Операции связананные с комменатриями"""
    serializer_class = CommentSerializer
    permission_classes = (IsSuperuserAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review_obj = get_object_or_404(Review, id=review_id, title=title_id)
        return review_obj.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review_obj = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review_obj)
