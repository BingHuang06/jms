from django.shortcuts import render
from rest_framework import viewsets, mixins, response, status
from rest_framework_jwt.utils import jwt_decode_handler

from users.models import User
from users.serializers import UserSerializer, UserSimpleSerializer
from users.filters import UserFilter
# Create your views here.

from utils.usermanager import Bash, ServerUserManager
from django.conf import settings
import os

CONNECTPY_PATH = os.path.join(settings.PROJECT_DIR, 'init.sh')


class UserViewSet(viewsets.ModelViewSet):
    '''
    retrieve:
        返回指定用户信息
    list:
        返回用户列表
    update:
        更新用户信息
    destroy:
        删除用户
    create:
        创建用户
    partial_update:
        更新用户部分信息
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter

    def create(self, request, *args, **kwargs):
        # 密码不可读，需要单独获取
        password = request.data.get("password", None)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get("username")
        is_active = serializer.data.get("is_active")

        if username == "admin":
            return response.Response("不允许创建admin用户", status=status.HTTP_400_BAD_REQUEST)

        # 创建服务器账号
        user_in_server = ServerUserManager(Bash)
        ret, msg = user_in_server.present(username=username,
                                          password=password,
                                          shell=CONNECTPY_PATH,
                                          is_active=is_active)
        if ret:
            user_in_server.absent(username)
            return response.Response("用户创建失败", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # 密码不可读，需要单独获取
        password = request.data.get("password", None)
        username = request.data.get("username", None)
        is_active = request.data.get("is_active", None)
        if isinstance(is_active, str):
            return response.Response(status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()
        old_username = instance.username

        partial = kwargs.get('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        user_in_server = ServerUserManager(Bash)
        if username and username != old_username:
            if old_username == "admin":
                return response.Response("amin用户名不允许修改", status=status.HTTP_400_BAD_REQUEST)
            user_in_server.absent(username, force=True)

        if not username:
            username = old_username

        # 更新服务器账号密码
        ret, msg = user_in_server.present(username=username, password=password, is_active=is_active)
        if ret:
            return response.Response("用户密码修改失败", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        username = instance.username
        # 删除服务器账号
        user_in_server = ServerUserManager(Bash)
        user_in_server.absent(username, force=True)

        return super().destroy(request, *args, **kwargs)


class UserListViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    '''
    list:
        返回用户列表，不分页
    '''
    queryset = User.objects.all()
    serializer_class = UserSimpleSerializer
    pagination_class = None


class UserInfoViewSet(viewsets.ViewSet):
    '''
    list:
        获取用户信息
    '''
    def list(self, request, *args, **kwargs):
        token = request.auth
        jwt_user = jwt_decode_handler(token)

        user = User.objects.get(pk=jwt_user.get("user_id"))
        data = {
            'name': user.name
        }
        return response.Response(data)
