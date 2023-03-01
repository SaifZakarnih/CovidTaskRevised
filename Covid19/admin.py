from django.contrib import admin
from . import models as covid_models


class CountyStatusDayAdmin(admin.ModelAdmin):
    list_display = ('country', 'date')
    ordering = ('country', 'date')
    search_fields = ('country__country', 'date')
    list_filter = ('date', ('country', admin.RelatedOnlyFieldListFilter))


admin.site.register(covid_models.Covid19APICountryUserAssociation)
admin.site.register(covid_models.CountryStatusByDay, CountyStatusDayAdmin)
admin.site.register(covid_models.User)
