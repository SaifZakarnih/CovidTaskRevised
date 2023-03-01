from django.urls import path
from . import views as covid_views

urlpatterns = [
    path('import-countries/', covid_views.ImportCountries.as_view(), name='import'),
    path('list-countries/', covid_views.GetCountries.as_view(), name='list'),
    path('subscribe/', covid_views.UserCountryAssociation.as_view(), name='subscribe'),
    path('percentage/', covid_views.ViewPercentage.as_view(), name='percentage'),
    path('top/', covid_views.TopCountries.as_view(), name='top'),
]
