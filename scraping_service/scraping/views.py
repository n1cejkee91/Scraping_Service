from django.shortcuts import render
from .models import Vacancy


def home_view(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'scraping/home.html', {'vacancies': vacancies})


def test(request):
    return render(request, 'scraping/test.html')
