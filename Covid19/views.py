import django.views.generic
import rest_framework.generics
from django.contrib import messages
from django.http import HttpResponseRedirect
import requests
import django.urls
from django.conf import settings
from rest_framework.views import APIView

from . import models as covid_models
from . import forms as covid_forms


class ImportCountries(APIView):

    def post(self, request, *args, **kwargs):
        countries = requests.get(f'{settings.API_LINK}/countries').json()

        for current_country in countries:
            covid_models.Covid19APICountry.objects.get_or_create(slug=current_country['Slug'], country=current_country['Country'], iso2=current_country['ISO2'])

        return rest_framework.views.Response('Countries imported successfully!', status=200)


class GetCountries(rest_framework.generics.ListAPIView):
    template_name = 'Covid19/views/list.html'

    def get_queryset(self):
        return covid_models.Covid19APICountry.objects.values('slug', 'country').order_by('country')


class UserCountryAssociation(django.views.generic.CreateView):
    model = covid_models.Covid19APICountryUserAssociation
    fields = ['country']
    template_name = 'Covid19/views/subscribe.html'

    def post(self, request, *args, **kwrags):
        user = covid_models.User.objects.get(id=1)
        country = covid_models.Covid19APICountry.objects.get(id=request.POST['country'])
        if covid_models.Covid19APICountryUserAssociation.objects.filter(user=user, country=country).exists():
            messages.error(self.request, f'{user} is already subscribed to {country}')
        else:
            covid_models.Covid19APICountryUserAssociation.objects.create(user=user, country=country)
            messages.success(self.request, f'{user} successfully subscribed to {country}')
        return HttpResponseRedirect(self.request.path_info)


class ViewPercentage(django.views.generic.FormView):
    form_class = covid_forms.UserCountryAssociationAndViewPercentageForm
    template_name = 'Covid19/views/percentage.html'
    pattern_name = 'percentage'

    def get_success_url(self):
        return django.urls.reverse_lazy(self.pattern_name)

    def form_valid(self, form):
        country_details = requests.get(f'{settings.API_LINK}/total/dayone/country/{form.cleaned_data["slug"]}').json()
        country_details = country_details[(len(country_details) - 1)]
        try:
            percentage = (country_details['Deaths'] / country_details['Confirmed']) * 100
        except ZeroDivisionError:
            messages.error(self.request, 'Division by Zero!')
            return super().form_valid(form)

        messages.success(self.request, f'{country_details["Country"]} Deaths to Confirmed is {percentage}%!')
        return super().form_valid(form)


class TopCountries(django.views.generic.FormView):
    form_class = covid_forms.TopCountriesForm
    template_name = 'Covid19/views/top.html'
    pattern_name = 'top'

    def get_success_url(self):
        return django.urls.reverse_lazy(self.pattern_name)

    def form_valid(self, form):
        max_values = []
        country_dictionary = {}
        queryset = covid_models.Covid19APICountryUserAssociation.objects.values_list('country__slug', flat=True).distinct()
        for slug in queryset:
            country_information = requests.get(f'{settings.API_LINK}/total/dayone/country/{slug}/status/{form.cleaned_data["case"]}').json()
            country_information = country_information[len(country_information) - 1]
            country_dictionary['Country'] = country_information['Country']
            country_dictionary[form.cleaned_data['case']] = country_information['Cases']
            max_values.append(country_dictionary)
            country_dictionary = {}
        max_values = sorted(max_values, key=lambda key: key[form.cleaned_data["case"]], reverse=True)
        messages.success(self.request, message=max_values[:3])
        return super().form_valid(form)
