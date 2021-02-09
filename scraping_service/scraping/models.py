from django.db import models


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='Населенный пункт')
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        verbose_name = 'Населенный пункт'
        verbose_name_plural = 'Населенные пункты'

    def __str__(self):
        return self.name
