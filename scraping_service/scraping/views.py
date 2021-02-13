from django.shortcuts import render
from .models import Vacancy
from .forms import FindForm


def home_view(request):
    vacancies = Vacancy.objects.all()

    form = FindForm(request.GET)
    city = request.GET.get('city')
    profession = request.GET.get('profession')
    if city or profession:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if profession:
            _filter['profession__slug'] = profession
        vacancies = Vacancy.objects.filter(**_filter)
        return render(request, 'scraping/home.html', {'vacancies': vacancies, 'form': form})

    return render(request, 'scraping/home.html', {'vacancies': vacancies, 'form': form})


def test(request):
    return render(request, 'scraping/test.html')
