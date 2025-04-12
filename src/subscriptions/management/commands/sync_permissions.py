from typing import Any
from django.core.management.base import BaseCommand

from subscriptions.models import Subscription

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        qs = Subscription.objects.filter(active=True)
        for obj in qs:
            # print(obj.groups.all())
            subscription_perms = obj.permissions.all()
            for group in obj.groups.all():
                group.permissions.set(subscription_perms)
                # for perm in obj.permissions.all():
                #     group.permissions.add(perm)
            # print(obj.permissions.all())