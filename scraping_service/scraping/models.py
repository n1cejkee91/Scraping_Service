import jsonfield
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=255, verbose_name='Населенный пункт', unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        verbose_name = 'Населенный пункт'
        verbose_name_plural = 'Населенные пункты'

    def __str__(self):
        return self.name


class Languages(models.Model):
    name = models.CharField(max_length=255, verbose_name='Язык программирования', unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Название вакансии')
    company = models.CharField(max_length=250, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание вакансии')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    language = models.ForeignKey('Languages', on_delete=models.CASCADE, verbose_name='Язык программирования')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вакансия(ю)'
        verbose_name_plural = 'Вакансии'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title


class Errors(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = jsonfield.JSONField()

    class Meta:
        verbose_name = 'Ошибка(у)'
        verbose_name_plural = 'Ошибки'

    def __str__(self):
        return str(self.timestamp)


def default_urls():
    return {'work': '', 'rabota': '', 'dou': '', 'djinni': ''}


class Url(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    language = models.ForeignKey('Languages', on_delete=models.CASCADE, verbose_name='Язык программирования')
    url_data = jsonfield.JSONField(default=default_urls)

    class Meta:
        unique_together = ('city', 'language')
