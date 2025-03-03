from django.http import HttpResponse
from django.shortcuts import render

from visits.models import PageVisit

def home_page_view(request, *args, **kwargs):
    qs = PageVisit.objects.all()
    page_qs = PageVisit.objects.filter(path=request.path)
    my_title = "my Pageee"
    path = request.path
    PageVisit.objects.create(path=request.path)
    my_context = {
        'page_title': my_title,
        'page_visit_count': page_qs.count(),
        'total_visit_count': qs.count(),
    }
    return render(request, 'home.html', my_context)
