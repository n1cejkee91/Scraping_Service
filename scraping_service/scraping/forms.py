from django import forms
from .models import City, Professions


class FindForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name='slug', required=False,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    profession = forms.ModelChoiceField(queryset=Professions.objects.all(), to_field_name='slug', required=False,
                                        widget=forms.Select(attrs={'class': 'form-control'}))
