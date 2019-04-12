from django.db import models

from users.models import User
from assets.models import Asset

# Create your models here.


class Perm(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name="角色名称", help_text="角色名称")
    is_active = models.BooleanField(verbose_name="激活", help_text="激活")
    user = models.ManyToManyField(User, verbose_name="授权用户", help_text="授权用户")
    asset = models.ManyToManyField(Asset, verbose_name="授权资产", help_text="授权资产")
    remark = models.CharField(max_length=32, null=True, verbose_name="备注", help_text="备注")

    class Meta:
        db_table = "resources_perm"
        ordering = ["id"]

    def __str__(self):
        return "Perm: <{}>".format(self.name)
