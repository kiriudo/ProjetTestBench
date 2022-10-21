from django.urls import path
from . import views
app_name = 'reworking'
urlpatterns = [
    path('', views.ProductSearch,name='search'),
]