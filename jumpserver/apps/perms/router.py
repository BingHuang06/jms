from rest_framework.routers import DefaultRouter

from perms.views import PermViewSet, PermAssetViewSet, PermUserViewSet

perm_router = DefaultRouter()

perm_router.register('perms', PermViewSet, base_name='perms')
perm_router.register('permassets', PermAssetViewSet, base_name='permassets')
perm_router.register('permusers', PermUserViewSet, base_name='permusers')
