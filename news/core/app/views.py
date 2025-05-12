from django.shortcuts import render
from .models import Info


def news_view(request):
    info = Info.objects.all()

    return render(request=request, template_name='app/index.html', context={'info': info})


def news_detail(request, pk):
    info = Info.objects.get(id=pk)

    return render(request=request, template_name='app/detail.html', context={'info': info})


