import django_filters
from django.db.models import Q

from users.models import User


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(method='search_username')

    def search_username(self, qs, name, value):
        return qs.filter(Q(username__icontains=value) | Q(name__icontains=value))

    class Meta:
        model = User
        fields = ['username']


