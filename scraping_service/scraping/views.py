from django.core.paginator import Paginator
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
    context = {'city': city, 'language': language, 'form': form}
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language
        vacancies = Vacancy.objects.filter(**_filter)
        paginator = Paginator(vacancies, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['vacancies'] = page_obj
    return render(request, 'scraping/list.html', context)


def test(request):
    return render(request, 'scraping/test.html')
