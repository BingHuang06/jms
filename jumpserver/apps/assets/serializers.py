from rest_framework import serializers

from assets.models import Asset, AssetGroup


class AssetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=32, write_only=True,  label="远程登陆密码", help_text="远程登陆密码")

    class Meta:
        model = Asset
        fields = "__all__"

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)
        if password:
            instance.password = password
        instance.hostname = validated_data.get('hostname', instance.hostname)
        instance.ip = validated_data.get('ip', instance.ip)
        instance.port = validated_data.get('port', instance.port)
        instance.username = validated_data.get('username', instance.username)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.remark = validated_data.get('remark', instance.remark)
        instance.group = validated_data.get('group', instance.group)
        instance.save()
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        group = ret.get('group')
        if group:
            ret["group"] = {
                "id": instance.group.id,
                "name": instance.group.name
            }
        return ret


class AssetSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ("id", "hostname", "group")

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        group = ret.get('group')
        if group:
            ret["group"] = instance.group.name
        return ret



class AssetGroupSerializer(serializers.ModelSerializer):
    asset_count = serializers.SerializerMethodField(read_only=True)
    assets = serializers.ListField(help_text="关联资产列表")

    class Meta:
        model = AssetGroup
        fields = "__all__"

    def get_asset_count(self, row):
        return row.asset_set.count()

    def create(self, validated_data):
        assets = validated_data.pop('assets')

        asset_objs = []
        for id in assets:
            try:
                asset_obj = Asset.objects.get(pk=id)
                asset_objs.append(asset_obj)
            except:
                pass

        instance = AssetGroup.objects.create(**validated_data)
        instance.asset_set.set(asset_objs)

        return instance

    def update(self, instance, validated_data):
        assets = validated_data.pop('assets')

        asset_objs = []
        for id in assets:
            try:
                asset_obj = Asset.objects.get(pk=id)
                asset_objs.append(asset_obj)
            except:
                pass

        instance.name = validated_data.get('name', instance.name)
        instance.remark = validated_data.get('remark', instance.remark)
        instance.asset_set.set(asset_objs)

        instance.save()
        return instance

    def to_representation(self, instance):
        assets = AssetSimpleSerializer(instance.asset_set.all(), many=True)
        ret = {
            "id": instance.id,
            "name": instance.name,
            "remark": instance.remark,
            "asset_count": self.get_asset_count(instance),
            "assets": assets.data
        }
        return ret
