#!/usr/bin/env python3
# coding: utf-8

import os
import django
import argparse

os.environ['DJANGO_SETTINGS_MODULE'] = 'jumpserver.jms.settings'
django.setup()

from users.models import User

def create_admin(password, email, name):
    try:
        User.objects.create_superuser("admin", email, password, name=name)
        return True
    except:
        return False


def main():
    parser = argparse.ArgumentParser(
        prog="createsuperuser",
        description="创建jms管理员账号admin"
    )

    parser.add_argument('password', help='管理员密码')
    parser.add_argument('email', help='管理员邮箱')
    parser.add_argument("name", nargs='?', help='管理员姓名', default="管理员")

    args = parser.parse_args()
    ret = create_admin(args.password, args.email, args.name)
    if ret:
        print("管理员创建成功")
    else:
        print("管理员创建失败")


if __name__ == '__main__':
    main()
