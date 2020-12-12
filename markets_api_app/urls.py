from django.urls import path

from . import views

app_name = 'markets'

urlpatterns = [
    path('markets/', views.MarketApiView.as_view()),
]
