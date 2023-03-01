from django.core.management.base import BaseCommand
import requests
from ... import models as covid_models
from django.conf import settings


class Command(BaseCommand):
    help = "This command adds the most recent status of the countries that a user has subscribed to into the database, this command requires the username as an input."

    def add_arguments(self, parser):

        parser.add_argument('user', type=str)

    def handle(self, *args, **options):

        if user := covid_models.User.objects.filter(username=options['user']).first():
            if countries_associations := covid_models.Covid19APICountryUserAssociation.objects.filter(user=user):
                for current_country in countries_associations:
                    country_information = requests.get(f'{settings.API_LINK}/total/dayone/country/{current_country.country.slug}').json()
                    latest_entry = country_information[len(country_information) - 1]
                    preceding_entry = country_information[len(country_information) - 30]
                    if covid_models.CountryStatusByDay.objects.filter(country=current_country.country, date=latest_entry['Date']).exists():
                        self.stdout.write(f'{current_country.country} data for today already exists!')
                    else:
                        covid_models.CountryStatusByDay.objects.create(
                            country=current_country.country,
                            confirmed_cases=(latest_entry['Confirmed'] - preceding_entry['Confirmed']),
                            deaths_cases=(latest_entry['Deaths'] - preceding_entry['Deaths']),
                            active_cases=(latest_entry['Active'] - preceding_entry['Active']),
                            recovered_cases=(latest_entry['Recovered'] - preceding_entry['Recovered']),
                            date=latest_entry['Date']
                        )
                        self.stdout.write(f"Successfully added data for {latest_entry['Country']}!")
