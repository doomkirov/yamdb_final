from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    MyTokenObtainPairView,
    ReviewViewSet,
    SignUpViewSet,
    TitleViewSet,
    UsersViewSet
)

app_name = 'api'

router = DefaultRouter()

router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register('users', UsersViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

auth_endpoints = [
    path('token/',
         MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('signup/',
         SignUpViewSet.as_view({'post': 'create'})),
    path('token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth_endpoints)),
]
