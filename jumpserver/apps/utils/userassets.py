# coding: utf-8

from perms.models import Perm


def get_user_assets(user):
    assets = set()
    perms = Perm.objects.filter(user=user)
    for perm in perms:
        if not perm.is_active:
            continue
        for asset in perm.asset.iterator():
            if not asset.is_active:
                continue
            assets.add(asset)
    return assets
