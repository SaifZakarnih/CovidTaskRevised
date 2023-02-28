from shortuuid.django_fields import ShortUUIDField
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class User(AbstractUser):
    pass


class Covid19APICountry(models.Model):
    uuid = ShortUUIDField()
    slug = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    iso2 = models.CharField(max_length=100)

    def __str__(self):
        return str(self.country)


class Covid19APICountryUserAssociation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Covid19APICountry, on_delete=models.CASCADE)
    associated_on = models.DateTimeField(default=datetime.now)

    class Meta:
        unique_together = ('user', 'country')

    def __str__(self):
        return str(self.user) + ' ' + str(self.country)


class CountryStatusByDay(models.Model):
    country = models.ForeignKey(Covid19APICountry, on_delete=models.CASCADE)
    date = models.DateTimeField()
    confirmed_cases = models.IntegerField()
    recovered_cases = models.IntegerField()
    deaths_cases = models.IntegerField()
    active_cases = models.IntegerField()

    class Meta:
        unique_together = ('country', 'date')

    def __str__(self):
        return str(self.country)
