from django.shortcuts import render
from rest_framework import viewsets, response
from users.models import User
from assets.models import Asset

# Create your views here.


class StatisticInfo(viewsets.ViewSet):
    '''
    list:
        获取用户和资产统计信息信息
    '''
    def list(self, request, *args, **kwargs):
        user_count = User.objects.count()
        asset_count = Asset.objects.count()
        data = {
            'user_count': user_count,
            'asset_count': asset_count
        }
        return response.Response(data)