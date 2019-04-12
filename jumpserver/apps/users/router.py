from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, UserListViewSet, UserInfoViewSet

user_router = DefaultRouter()

user_router.register('users', UserViewSet, base_name='users')
user_router.register('userlists', UserListViewSet, base_name='userlists')
user_router.register('userinfo', UserInfoViewSet, base_name='userinfo')
