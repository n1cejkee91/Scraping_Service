from django.db import models
from autoslug import AutoSlugField


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='Населенный пункт', unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)

    class Meta:
        verbose_name = 'Населенный пункт'
        verbose_name_plural = 'Населенные пункты'

    def __str__(self):
        return self.name


class Professions(models.Model):
    name = models.CharField(max_length=50, verbose_name='Профессия или должность', unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)

    class Meta:
        verbose_name = 'Профессия или должность'
        verbose_name_plural = 'Профессии или должности'

    def __str__(self):
        return self.name
