from rest_framework.routers import DefaultRouter

from assets.views import AssetViewSet, AssetGroupViewSet, GroupAssetListViewSet, AssetListViewSet, AssetGroupListViewSet

asset_router = DefaultRouter()

asset_router.register('assets', AssetViewSet, base_name='assets')
asset_router.register('assetgroups', AssetGroupViewSet, base_name='assetgroups')
asset_router.register('groupassets', GroupAssetListViewSet, base_name='groupassets')
asset_router.register('assetlists', AssetListViewSet, base_name='assetlists')
asset_router.register('assetgrouplists', AssetGroupListViewSet, base_name='assetgrouplists')
