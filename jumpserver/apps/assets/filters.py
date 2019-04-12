import django_filters
from django.db.models import Q

from assets.models import Asset, AssetGroup


class AssetFilter(django_filters.FilterSet):
    hostname = django_filters.CharFilter(method='search_hostname')

    def search_hostname(self, qs, name, value):
        return qs.filter(Q(hostname__icontains=value) | Q(ip__icontains=value))

    class Meta:
        model = Asset
        fields = ['hostname']


class AssetGroupFilter(django_filters.FilterSet):
    class Meta:
        model = AssetGroup
        fields = {
            'name': ['icontains']
        }



