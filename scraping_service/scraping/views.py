from django.shortcuts import render
from .models import Vacancy
from .forms import FindForm


def home_view(request):
    form = FindForm(request.GET)

    return render(request, 'scraping/home.html', {'form': form})


def list_view(request):
    form = FindForm(request.GET)
    city = request.GET.get('city')
    language = request.GET.get('language')
    vacancies = []
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language
        vacancies = Vacancy.objects.filter(**_filter)
    return render(request, 'scraping/list.html', {'vacancies': vacancies, 'form': form})


def test(request):
    return render(request, 'scraping/test.html')
