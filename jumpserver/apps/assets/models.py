from django.db import models


# Create your models here.


class AssetGroup(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name="资产组名称", help_text="资产组名称")
    remark = models.CharField(max_length=32, null=True, verbose_name="备注", help_text="备注")

    class Meta:
        db_table = "resources_assetgroup"
        ordering = ["id"]

    def __str__(self):
        return "AssetGroup: <{}>".format(self.name)


class Asset(models.Model):
    hostname = models.CharField(max_length=64, verbose_name="主机名", help_text="主机名")
    ip = models.GenericIPAddressField(unique=True, verbose_name="IP地址", help_text="IP地址")
    port = models.IntegerField(verbose_name="端口", default=22, help_text="端口")
    username = models.CharField(max_length=32, verbose_name="远程登陆账号", help_text="远程登陆账号")
    password = models.CharField(max_length=32, verbose_name="远程登陆密码", help_text="远程登陆密码")
    is_active = models.BooleanField(verbose_name="激活", help_text="激活")
    remark = models.CharField(max_length=32, null=True, verbose_name="备注", help_text="备注")
    group = models.ForeignKey(AssetGroup, null=True, verbose_name="资产组", help_text="资产组", on_delete=models.SET_NULL)

    class Meta:
        db_table = "resources_asset"
        ordering = ["id"]

    def __str__(self):
        return "Asset: <{} {}>".format(self.hostname, self.ip)
