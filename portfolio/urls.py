from django.urls import path
from . import views

urlpatterns = [
    path('', views.informacje, name='informacje'),
    path('o-mnie/', views.o_mnie, name='o_mnie'),
    path('portfolio/', views.portfolio_view, name='portfolio'),
    path('portfolio/<slug:slug>/', views.portfolio_view, name='portfolio_category'),
    path('kontakt/', views.kontakt, name='kontakt'),
]
