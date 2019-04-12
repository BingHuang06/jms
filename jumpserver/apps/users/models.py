from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=32, verbose_name="姓名", help_text="姓名")
    remark = models.CharField(max_length=32, null=True, verbose_name="备注", help_text="备注")

    class Meta:
        db_table = "resources_user"
        ordering = ["id"]

    def __str__(self):
        return "User: <{} {}>".format(self.username, self.name)
