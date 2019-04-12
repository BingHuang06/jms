from rest_framework import serializers

from perms.models import Perm


class PermSerializer(serializers.ModelSerializer):
    user_count = serializers.SerializerMethodField(read_only=True)
    asset_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Perm
        fields = ("id", "name", "is_active", "remark", "user_count", "asset_count")

    def get_user_count(self, row):
        return row.user.count()

    def get_asset_count(self, row):
        return row.asset.count()
