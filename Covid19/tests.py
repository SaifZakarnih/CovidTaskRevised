import pdb

import django.test
from . import models as covid_models
from . import forms as covid_forms


class ImportTestCase(django.test.TestCase):

    def test_correct_scenario(self):
        response = self.client.post('/api/v2/import-countries/')
        self.assertEquals(response.status_code, 409)

    def test_incorrect_url(self):
        response = self.client.post('/api/v2/import-count/')
        self.assertEquals(response.status_code, 404)

    def test_incorrect_method(self):
        response = self.client.get('/api/v2/import-countries/')
        self.assertEquals(response.status_code, 405)


class PercentageTestCase(django.test.TestCase):
    slug = 'south-africa'
    invalid_slug = 'south'

    def test_form_valid(self):
        form = covid_forms.PercentageForm(data={'slug': self.slug})
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = covid_forms.PercentageForm(data={'slug': self.invalid_slug})
        self.assertFalse(form.is_valid())

    def test_form_empty(self):
        form = covid_forms.PercentageForm()
        self.assertFalse(form.is_bound)

    def test_form_empty_slug(self):
        form = covid_forms.PercentageForm(data={'slug': ''})
        self.assertFalse(form.is_valid())

    def test_form_none_slug(self):
        form = covid_forms.PercentageForm(data={'slug': None})
        self.assertFalse(form.is_valid())


class SubscribeTestCase(django.test.TestCase):

    username = 'testuesr'
    password = '123'
    email = 'test@user.com'
    existing_slug = 'south-africa'
    new_slug = 'united-states'

    def setUp(self):
        self.user = covid_models.User.objects.create(username=self.username, password=self.password, email=self.email)

    def test_existing_id(self):
        country_id = covid_models.Covid19APICountry.objects.filter(slug=self.existing_slug).values_list('id', flat=True)
        response = self.client.post('/api/v2/subscribe/', data={'user_id': self.user.pk, 'country': country_id})
        self.assertEquals(response.status_code, 302)

    def test_new_id(self):
        country_id = covid_models.Covid19APICountry.objects.filter(slug=self.new_slug).values_list('id', flat=True)
        response = self.client.post('/api/v2/subscribe/', data={'user_id': self.user.pk, 'country': country_id})
        self.assertEquals(response.status_code, 302)

    def test_wrong_id(self):
        country_id = 500
        response = self.client.post('/api/v2/subscribe/', data={'user_id': self.user.pk, 'country': country_id})
        self.assertEquals(response.status_code, 302)


class TopCountriesTestCase(django.test.TestCase):

    def test_form_valid(self):
        form = covid_forms.TopCountriesForm(data={'case': 'confirmed'})
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = covid_forms.TopCountriesForm(data={'case': 'invalid'})
        self.assertFalse(form.is_valid())

    def test_form_empty_case(self):
        form = covid_forms.TopCountriesForm(data={'case': ''})
        self.assertFalse(form.is_valid())

    def test_form_none_case(self):
        form = covid_forms.TopCountriesForm(data={'case': None})
        self.assertFalse(form.is_valid())

    def test_correct_scenario(self):
        response = self.client.post('/api/v2/top/', data={'case': 'confirmed'})
        self.assertEquals(response.status_code, 302)
