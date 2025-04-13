from typing import Any
from django.core.management.base import BaseCommand

from customers.models import Customer
from subscriptions import utils as subs_utils
import helpers.billing

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--clear-dangling", action="store_true", default=False)

    def handle(self, *args: Any, **options: Any):
        # python manage.py sync_user_subs --clear-dangling
        print(options)
        clear_dangling = options.get("clear_dangling")
        if clear_dangling:
            print("Clearing dangling subs")
            subs_utils.clear_dangling_subs()
        else:
            print("Sync active subs")
            done = subs_utils.refresh_active_users_subscription(active_only=True, verbose=True)
            if done:
                print("Done")