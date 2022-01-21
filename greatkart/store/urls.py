
from django.urls import path
from . import views


urlpatterns = [

    path('', views.store, name='store'),
    path('category/<slug>/', views.store, name='slug'),
    path('category/<slug>/<slug:product_slug>', views.product_detail, name='product_slug'),
    path('search/', views.search, name='search'),

] 
