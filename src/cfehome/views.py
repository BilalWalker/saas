from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from pathlib import Path

from visits.models import PageVisit

this_dir = Path(__file__).resolve().parent

def home_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        print(request.user.is_authenticated, request.user)
    return about_view(request, *args, **kwargs)

def about_view(request, *args, **kwargs):
    qs = PageVisit.objects.all()
    page_qs = PageVisit.objects.filter(path=request.path)
    try:
        percent = (page_qs.count() * 100.0) / qs.count()
    except:
        percent = 0

    my_title = "my Pageee"
    path = request.path
    PageVisit.objects.create(path=request.path)
    my_context = {
        'page_title': my_title,
        'page_visit_count': page_qs.count(),
        'percent': percent,
        'total_visit_count': qs.count(),
    }
    return render(request, 'home.html', my_context)

VALID_CODE = "abc123"

def pw_protected_view(request, *args, **kwargs):
    is_allowed = request.session.get('protected_page_allowed') or 0
    print(request.session.get('protected_page_allowed'), type(request.session.get('protected_page_allowed')))
    if request.method == "POST":
        user_pw_sent = request.POST.get("code") or None
        if user_pw_sent == VALID_CODE:
            is_allowed = 1
            request.session['protected_page_allowed'] = is_allowed
            
    if is_allowed:
        return render(request, "protected/view.html", {})
    return render(request, "protected/entry.html", {})

@login_required
def user_only_view(request, *args, **kwargs):
    return render(request, "protected/user-only.html", {})