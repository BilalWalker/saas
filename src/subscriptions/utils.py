from typing import Any
from django.core.management.base import BaseCommand
from django.db.models import Q

from customers.models import Customer
from subscriptions.models import UserSubscription, Subscription, SubscriptionStatus
import helpers.billing

def refresh_active_users_subscription(
        user_ids=None,
        active_only=True,
        days_left=0,
        days_ago=0,
        day_start=0,
        day_end=0,
        verbose=False
    ):
    qs = UserSubscription.objects.all()
    if active_only:
        qs = qs.by_active_trialing()
    if user_ids is not None:
        qs = qs.by_user_ids(user_ids=user_ids)
    if days_ago > 0:
        qs = qs.by_days_ago(days_ago=days_ago)
    if days_left > 0:
        qs = qs.by_days_left(days_left=days_left)
    if day_start > 0 and day_end > 0:
        qs = qs.by_range(day_start=day_start, day_end=day_end)    
    # qs = qs.filter(active_qs_lookup).filter(user_id__in=user_ids)
    # active_qs = qs.filter(status=SubscriptionStatus.ACTIVE)
    # trialing_qs = qs.filter(status=SubscriptionStatus.TRIALING)
    # qs = (active_qs | trialing_qs)
    complete_count = 0
    qs_count = qs.count()
    for obj in qs:
        if verbose:
            print("Updating user", obj.user, obj.subscription, obj.current_period_end)
        if obj.stripe_id:
            sub_data = helpers.billing.get_subscription(obj.stripe_id, raw=False)
            for k, v in sub_data.items():
                setattr(obj, k, v)
            obj.save()
            complete_count += 1
    return complete_count == qs_count

def clear_dangling_subs():
    qs = Customer.objects.filter(stripe_id__isnull=False)
    for customer_obj in qs:
        user = customer_obj.user
        customer_stripe_id = user.customer.stripe_id
        print(f"Sync {user} - {customer_stripe_id} subs and remove old ones")
        subs = helpers.billing.get_customer_active_subscriptions(customer_stripe_id)
        for sub in subs:
            existing_user_subs_qs = UserSubscription.objects.filter(stripe_id__iexact=f"{sub.id}".strip())
            if existing_user_subs_qs.exists():
                continue
            helpers.billing.cancel_subscription(sub.id, reason="Dangling active subscription", cancel_at_period_end=False)
            print(sub.id, existing_user_subs_qs.exists())

def sync_subs_group_permissions():
    qs = Subscription.objects.filter(active=True)
    for obj in qs:
        # print(obj.groups.all())
        subscription_perms = obj.permissions.all()
        for group in obj.groups.all():
            group.permissions.set(subscription_perms)
            # for perm in obj.permissions.all():
            #     group.permissions.add(perm)
        # print(obj.permissions.all())
