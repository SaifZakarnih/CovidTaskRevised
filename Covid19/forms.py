from django import forms
from . import models as covid_models


class UserCountryAssociationAndViewPercentageForm(forms.Form):
    slug = forms.CharField(required=True)

    def clean(self):
        slug = str(self.cleaned_data['slug']).lower()

        # Check if the slug is proper.
        if not covid_models.Covid19APICountry.objects.filter(slug=slug).exists():
            self.add_error('slug', f'Invalid slug "{slug}", please check the available slugs from /list-countries/.')
        self.cleaned_data['slug'] = slug
        return super().clean()


class TopCountriesForm(forms.Form):
    case = forms.CharField(required=True)

    def clean(self):
        case = str(self.cleaned_data['case']).lower()

        # Check if case is proper.
        if case not in ['confirmed', 'deaths']:
            self.add_error('case', f'Invalid case "{case}", please use Confirmed or Deaths.')

        # Fix formatting
        self.cleaned_data['case'] = case
        return super().clean()
