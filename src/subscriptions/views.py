from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from subscriptions.models import SubscriptionPrice, UserSubscription
import helpers.billing

@login_required
def user_subscription_view(request):
    user_sub_obj, created = UserSubscription.objects.get_or_create(user=request.user)
    # sub_data = user_sub_obj.serialize()
    if request.method == "POST":
        print("refresh sub")
        if user_sub_obj.stripe_id:
            sub_data = helpers.billing.get_subscription(user_sub_obj.stripe_id, raw=False)
            for k, v in sub_data.items():
                setattr(user_sub_obj, k, v)
            user_sub_obj.save()
        return redirect(user_sub_obj.get_absolute_url())
    return render(request, 'subscriptions/user_detail_view.html', {"subscription": user_sub_obj})


# Create your views here.
def subscription_price_view(request, interval="month"):
    qs = SubscriptionPrice.objects.filter(featured=True)
    inv_mo = SubscriptionPrice.IntervalChoices.MONTHLY
    inv_yr = SubscriptionPrice.IntervalChoices.YEARLY

    object_list = qs.filter(interval=inv_mo)
    url_path_name = "pricing_interval"
    mo_url = reverse(url_path_name, kwargs={"interval": inv_mo})
    yr_url = reverse(url_path_name, kwargs={"interval": inv_yr})
    print(yr_url)
    active = inv_mo
    if interval == inv_yr:
        active = inv_yr
        object_list = qs.filter(interval=inv_yr)
    return render(request, "subscriptions/pricing.html", {
        "object_list": object_list,
        "mo_url": mo_url,
        "yr_url": yr_url,
        "active": active
    })