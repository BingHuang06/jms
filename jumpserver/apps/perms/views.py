from django.shortcuts import render
from rest_framework import viewsets, response, status

from perms.models import Perm
from perms.serializers import PermSerializer
from perms.filters import PermFilter
from assets.serializers import AssetSerializer
from users.serializers import UserSerializer
from assets.models import Asset
from users.models import User


# Create your views here.


class PermViewSet(viewsets.ModelViewSet):
    '''
    retrieve:
        返回角色信息
    list:
        返回角色列表
    update:
        更新角色信息
    destroy:
        删除角色
    create:
        创建角色
    partial_update:
        更新角色部分信息
    '''
    queryset = Perm.objects.all()
    serializer_class = PermSerializer
    filterset_class = PermFilter


class PermAssetViewSet(viewsets.GenericViewSet):
    '''
    retrieve:
        返回角色授权资产列表
    update:
        更新角色授权资产列表
    '''
    queryset = Perm.objects.all()
    serializer_class = PermSerializer

    def retrieve(self, request, *args, **kwargs):
        perm_obj = self.get_object()
        queryset = perm_obj.asset.all()
        serializer = AssetSerializer(queryset, many=True)
        data = {
            "count": len(serializer.data),
            "results": serializer.data
        }
        return response.Response(data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        assets = request.data.get("assets", None)
        if not isinstance(assets, list):
            return response.Response(status=status.HTTP_400_BAD_REQUEST)

        asset_objs = []
        for id in assets:
            try:
                asset_obj = Asset.objects.get(pk=id)
                asset_objs.append(asset_obj)
            except:
                pass

        instance.asset.set(asset_objs)
        return response.Response(status=status.HTTP_201_CREATED)


class PermUserViewSet(viewsets.GenericViewSet):
    '''
    retrieve:
        返回角色授权用户列表
    update:
        更新角色授权用户列表
    '''
    queryset = Perm.objects.all()
    serializer_class = PermSerializer

    def retrieve(self, request, *args, **kwargs):
        perm_obj = self.get_object()
        queryset = perm_obj.user.all()
        serializer = UserSerializer(queryset, many=True)
        data = {
            "count": len(serializer.data),
            "results": serializer.data
        }
        return response.Response(data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        users = request.data.get("users", None)
        print(users)
        if not isinstance(users, list):
            return response.Response(status=status.HTTP_400_BAD_REQUEST)

        user_objs = []
        for id in users:
            try:
                user_obj = User.objects.get(pk=id)
                user_objs.append(user_obj)
            except:
                pass

        instance.user.set(user_objs)
        return response.Response(status=status.HTTP_201_CREATED)