from rest_framework.routers import DefaultRouter

from utils.views import StatisticInfo

util_router = DefaultRouter()

util_router.register('statisticinfo', StatisticInfo, base_name='statisticinfo')
