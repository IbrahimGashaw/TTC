from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'site'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.service_list, name='service_list'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('training/', views.training_events, name='training_events'),
    path('training/calendar/', views.event_calendar, name='event_calendar'),
    path('training/<slug:slug>/', views.event_detail, name='event_detail'),
    path('showcases/', views.case_study_list, name='case_study_list'),
    path('showcases/<slug:slug>/', views.case_study_detail, name='case_study_detail'),
    path('team/', views.team, name='team'),
    path('team/<int:pk>/', views.team_member_detail, name='team_member_detail'),
    path('team/consultant/<int:agent_id>/', views.agent_detail, name='agent_detail'),
    path('gallery/', views.gallery_list, name='gallery_list'),
    path('gallery/<slug:slug>/', views.gallery_detail, name='gallery_detail'),
    path('contact/', views.contact, name='contact'),
    # Redirect legacy real-estate URLs to relevant TTCS pages
    path('properties/', RedirectView.as_view(pattern_name='site:service_list', permanent=False), name='property_list'),
    path('properties/<slug:slug>/', RedirectView.as_view(pattern_name='site:service_list', permanent=False), name='property_detail'),
    path('properties/<slug:slug>/book/', RedirectView.as_view(pattern_name='site:contact', permanent=False), name='book_property'),
    path('properties/<slug:slug>/viewing/', RedirectView.as_view(pattern_name='site:contact', permanent=False), name='book_viewing'),
    path('projects/', RedirectView.as_view(pattern_name='site:case_study_list', permanent=False), name='project_list'),
    path('projects/<slug:slug>/', RedirectView.as_view(pattern_name='site:case_study_list', permanent=False), name='project_detail'),
    path('property-request/', RedirectView.as_view(pattern_name='site:contact', permanent=False), name='property_request'),
    path('bookings/', RedirectView.as_view(url='/', permanent=False), name='my_bookings'),
    path('bookings/<int:booking_id>/', RedirectView.as_view(url='/', permanent=False), name='booking_detail'),
    path('market-reports/', RedirectView.as_view(pattern_name='site:case_study_list', permanent=False), name='market_report_list'),
    path('market-reports/<slug:slug>/', RedirectView.as_view(pattern_name='site:case_study_list', permanent=False), name='market_report_detail'),
    path('buying-guides/', RedirectView.as_view(pattern_name='blog:blog_list', permanent=False), name='buying_guide_list'),
    path('buying-guides/<slug:slug>/', RedirectView.as_view(pattern_name='blog:blog_list', permanent=False), name='buying_guide_detail'),
]
