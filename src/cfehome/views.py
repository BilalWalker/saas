from django.http import HttpResponse
from django.shortcuts import render

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