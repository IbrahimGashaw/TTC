from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.home, name='home'),
    path('properties/', views.property_list, name='property_list'),
    path('properties/<slug:slug>/', views.property_detail, name='property_detail'),
    path('properties/<slug:slug>/book/', views.book_property, name='book_property'),
    path('properties/<slug:slug>/viewing/', views.book_viewing, name='book_viewing'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('about/', views.about, name='about'),
    path('team/', views.team, name='team'),
    path('team/<int:agent_id>/', views.agent_detail, name='agent_detail'),
    path('contact/', views.contact, name='contact'),
    path('property-request/', views.property_request, name='property_request'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('market-reports/', views.market_report_list, name='market_report_list'),
    path('market-reports/<slug:slug>/', views.market_report_detail, name='market_report_detail'),
    path('buying-guides/', views.buying_guide_list, name='buying_guide_list'),
    path('buying-guides/<slug:slug>/', views.buying_guide_detail, name='buying_guide_detail'),
]

