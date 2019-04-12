from django.shortcuts import render
from rest_framework import viewsets, response, mixins

from assets.models import Asset, AssetGroup
from assets.serializers import AssetSerializer, AssetGroupSerializer, AssetSimpleSerializer
from assets.filters import AssetFilter, AssetGroupFilter


# Create your views here.


class AssetViewSet(viewsets.ModelViewSet):
    '''
    retrieve:
        返回指定资产信息
    list:
        返回资产列表
    update:
        更新资产信息
    destroy:
        删除资产
    create:
        创建资产
    partial_update:
        更新资产部分信息
    '''
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    filterset_class = AssetFilter


class AssetGroupViewSet(viewsets.ModelViewSet):
    '''
    retrieve:
        返回指定资产组信息
    list:
        返回资产组列表
    update:
        更新资产组信息
    destroy:
        删除资产组
    create:
        创建资产组
    partial_update:
        更新资产组部分信息
    '''
    queryset = AssetGroup.objects.all()
    serializer_class = AssetGroupSerializer
    filterset_class = AssetGroupFilter


class GroupAssetListViewSet(viewsets.GenericViewSet):
    '''
    retrieve:
        返回资产组关联资产列表
    '''
    queryset = AssetGroup.objects.all()
    serializer_class = AssetGroupSerializer

    def retrieve(self, request, *args, **kwargs):
        group_obj = self.get_object()
        queryset = group_obj.asset_set.all()
        serializer = AssetSerializer(queryset, many=True)
        data = {
            "count": len(serializer.data),
            "results": serializer.data
        }
        return response.Response(data)


class AssetListViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    '''
    list:
        返回资产列表，不分页
    '''
    queryset = Asset.objects.all()
    serializer_class = AssetSimpleSerializer
    pagination_class = None


class AssetGroupListViewSet(mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    '''
    list:
        返回资产组列表，不分页
    '''
    queryset = AssetGroup.objects.all()
    serializer_class = AssetGroupSerializer
    pagination_class = None
