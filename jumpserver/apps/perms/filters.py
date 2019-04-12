import django_filters

from perms.models import Perm


class PermFilter(django_filters.FilterSet):
    class Meta:
        model = Perm
        fields = {
            'name': ['icontains']
        }



