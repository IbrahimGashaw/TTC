from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.utils.translation import activate, get_language
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import translate_url
from .models import (
    Project, Property, Contact, TeamMember, PropertyBooking, ConstructionProgress,
    HomePageSettings, SiteSettings, ViewingAppointment, MarketReport, BuyingGuide,
    Service, TrainingEvent, EventRegistration, CaseStudy, Testimonial, Partner,
    Milestone, MediaAlbum, WorkingSchedule, Vacancy, VacancyApplication,
)
# PromotionalOffer may not exist
try:
    from .models import PromotionalOffer
except ImportError:
    PromotionalOffer = None
from .forms import (
    ContactForm, PropertyInquiryForm, PropertySearchForm, PropertyBookingForm,
    ViewingAppointmentForm, PropertyNeedRequestForm, EventRegistrationForm,
    VacancyApplicationForm,
)


def home(request):
    homepage_settings = HomePageSettings.load()
    site_settings = SiteSettings.load()

    context = {
        'homepage_settings': homepage_settings,
        'site_settings': site_settings,
        'featured_services': Service.objects.filter(is_active=True, is_featured=True)[:6],
        'services': Service.objects.filter(is_active=True)[:5],
        'upcoming_events': TrainingEvent.objects.filter(is_published=True).order_by('start_date')[:4],
        'testimonials': Testimonial.objects.filter(is_active=True, is_featured=True)[:6],
        'partners': Partner.objects.filter(is_active=True)[:12],
        'case_studies': CaseStudy.objects.filter(is_published=True, is_featured=True)[:3],
        'team_members': TeamMember.objects.all()[:4],
        'stats': {
            'clients_served': 15,
            'years_experience': 10,
            'training_programs': 25,
            'associate_trainers': 20,
        },
    }
    return render(request, 'properties/home.html', context)


def property_list(request):
    properties = Property.objects.filter(status__in=['active', 'new_offer'])
    search_form = PropertySearchForm(request.GET)
    
    # Build dropdown options
    locations = (
        Property.objects.exclude(location__isnull=True)
        .exclude(location__exact='')
        .values_list('location', flat=True)
        .distinct()
        .order_by('location')
    )
    bedroom_options = (
        Property.objects.exclude(bedrooms__isnull=True)
        .values_list('bedrooms', flat=True)
        .distinct()
        .order_by('bedrooms')
    )
    
    if search_form.is_valid():
        if search_form.cleaned_data.get('location'):
            properties = properties.filter(location__icontains=search_form.cleaned_data['location'])
        if search_form.cleaned_data.get('property_type'):
            properties = properties.filter(property_type=search_form.cleaned_data['property_type'])
        if search_form.cleaned_data.get('sale_type'):
            properties = properties.filter(sale_type=search_form.cleaned_data['sale_type'])
        if search_form.cleaned_data.get('min_price'):
            properties = properties.filter(price__gte=search_form.cleaned_data['min_price'])
        if search_form.cleaned_data.get('max_price'):
            properties = properties.filter(price__lte=search_form.cleaned_data['max_price'])
        if search_form.cleaned_data.get('bedrooms'):
            properties = properties.filter(bedrooms=search_form.cleaned_data['bedrooms'])
        if search_form.cleaned_data.get('bathrooms'):
            properties = properties.filter(bathrooms=search_form.cleaned_data['bathrooms'])
        if search_form.cleaned_data.get('status'):
            properties = properties.filter(status=search_form.cleaned_data['status'])
    
    # Check if map view is requested
    view_mode = request.GET.get('view', 'list')
    
    site_settings = SiteSettings.load()
    
    # Get properties with coordinates for map view (before pagination)
    properties_with_coords = properties.filter(
        latitude__isnull=False,
        longitude__isnull=False
    ).exclude(latitude=0, longitude=0)
    
    paginator = Paginator(properties, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'properties': page_obj,
        'search_form': search_form,
        'site_settings': site_settings,
        'view_mode': view_mode,
        'properties_with_coords': properties_with_coords,
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', None),
        'locations': locations,
        'bedroom_options': bedroom_options,
    }
    return render(request, 'properties/property_list.html', context)


def property_detail(request, slug):
    property = get_object_or_404(Property, slug=slug)
    related_properties = Property.objects.filter(
        Q(project=property.project) | Q(location=property.location),
        status__in=['active', 'new_offer']
    ).exclude(id=property.id)[:4]
    site_settings = SiteSettings.load()
    
    if request.method == 'POST':
        form = PropertyInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.property = property
            inquiry.save()
            messages.success(request, _('Your inquiry has been submitted successfully!'))
            return redirect('site:property_detail', slug=slug)
    else:
        form = PropertyInquiryForm()
    
    context = {
        'property': property,
        'related_properties': related_properties,
        'form': form,
        'site_settings': site_settings,
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', None),
    }
    return render(request, 'properties/property_detail.html', context)


def project_list(request):
    projects = Project.objects.all()
    context = {
        'projects': projects,
    }
    return render(request, 'properties/project_list.html', context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    properties = project.properties.filter(status__in=['active', 'new_offer'])
    progress_updates = ConstructionProgress.objects.filter(project=project).order_by('-update_date')
    
    context = {
        'project': project,
        'properties': properties,
        'progress_updates': progress_updates,
    }
    return render(request, 'properties/project_detail.html', context)


def about(request):
    from .models import AboutPageSettings
    about_settings = AboutPageSettings.load()

    context = {
        'about_settings': about_settings,
        'milestones': Milestone.objects.all(),
        'stats': {
            'clients_served': 15,
            'years_experience': 10,
            'training_programs': 25,
            'associate_trainers': 20,
        },
    }
    return render(request, 'properties/about.html', context)


def team(request):
    team_members = TeamMember.objects.all()
    founders = TeamMember.objects.filter(is_founder=True)
    trainers = TeamMember.objects.filter(role='associate_trainer')
    consultants = TeamMember.objects.filter(role='consultant')
    site_settings = SiteSettings.load()
    context = {
        'team_members': team_members,
        'founders': founders,
        'trainers': trainers,
        'consultants': consultants,
        'site_settings': site_settings,
    }
    return render(request, 'properties/team.html', context)


def team_member_detail(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    site_settings = SiteSettings.load()
    context = {
        'member': member,
        'site_settings': site_settings,
    }
    return render(request, 'properties/team_member_detail.html', context)


def agent_detail(request, agent_id):
    return team_member_detail(request, agent_id)


def service_list(request):
    category = request.GET.get('category', '')
    services = Service.objects.filter(is_active=True)
    if category:
        services = services.filter(category=category)
    context = {
        'services': services,
        'categories': Service.CATEGORY_CHOICES,
        'active_category': category,
    }
    return render(request, 'properties/service_list.html', context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    related = Service.objects.filter(is_active=True, category=service.category).exclude(pk=service.pk)[:3]
    context = {'service': service, 'related_services': related}
    return render(request, 'properties/service_detail.html', context)


def training_events(request):
    from django.utils import timezone
    now = timezone.now()
    upcoming = TrainingEvent.objects.filter(is_published=True, start_date__gte=now).order_by('start_date')
    past = TrainingEvent.objects.filter(is_published=True, start_date__lt=now).order_by('-start_date')[:6]
    context = {
        'upcoming_events': upcoming,
        'past_events': past,
    }
    return render(request, 'properties/training_events.html', context)


def event_detail(request, slug):
    event = get_object_or_404(TrainingEvent, slug=slug, is_published=True)
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            if not event.is_registration_open:
                messages.error(request, _('Registration is closed for this event.'))
            else:
                registration = form.save(commit=False)
                registration.event = event
                registration.gdpr_consent = form.cleaned_data['gdpr_consent']
                registration.status = 'confirmed'
                registration.save()
                messages.success(request, _('You have been registered successfully! We will contact you with details.'))
                return redirect('site:event_detail', slug=slug)
    else:
        form = EventRegistrationForm()
    context = {'event': event, 'form': form}
    return render(request, 'properties/event_detail.html', context)


def event_calendar(request):
    import json
    events = TrainingEvent.objects.filter(is_published=True).order_by('start_date')
    calendar_events = []
    for event in events:
        calendar_events.append({
            'title': event.title,
            'start': event.start_date.isoformat(),
            'end': event.end_date.isoformat(),
            'url': event.get_absolute_url(),
            'color': '#1e5a96',
        })
    context = {
        'events': events,
        'calendar_events_json': json.dumps(calendar_events),
    }
    return render(request, 'properties/event_calendar.html', context)


def vacancy_list(request):
    vacancies = Vacancy.objects.filter(is_published=True)
    open_vacancies = [v for v in vacancies if v.is_application_open]
    closed_vacancies = [v for v in vacancies if not v.is_application_open]
    hr_sourcing_service = Service.objects.filter(category='hr_sourcing', is_active=True).first()
    context = {
        'open_vacancies': open_vacancies,
        'closed_vacancies': closed_vacancies,
        'hr_sourcing_service': hr_sourcing_service,
    }
    return render(request, 'properties/vacancy_list.html', context)


def vacancy_detail(request, slug):
    vacancy = get_object_or_404(Vacancy, slug=slug, is_published=True)
    if request.method == 'POST':
        form = VacancyApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            if not vacancy.is_application_open:
                messages.error(request, _('Applications are closed for this vacancy.'))
            else:
                application = form.save(commit=False)
                application.vacancy = vacancy
                application.gdpr_consent = form.cleaned_data['gdpr_consent']
                application.status = 'pending'
                application.save()
                messages.success(
                    request,
                    _('Your application has been submitted successfully! We will review it and contact you.'),
                )
                return redirect('site:vacancy_detail', slug=slug)
    else:
        form = VacancyApplicationForm()
    context = {'vacancy': vacancy, 'form': form}
    return render(request, 'properties/vacancy_detail.html', context)


def partner_list(request):
    partners = Partner.objects.filter(is_active=True)
    context = {'partners': partners}
    return render(request, 'properties/partner_list.html', context)


def legacy_vacancy_redirect(request, slug):
    return redirect('site:vacancy_detail', slug=slug, permanent=True)


def case_study_list(request):
    case_studies = CaseStudy.objects.filter(is_published=True)
    context = {'case_studies': case_studies}
    return render(request, 'properties/case_study_list.html', context)


def case_study_detail(request, slug):
    case_study = get_object_or_404(CaseStudy, slug=slug, is_published=True)
    context = {'case_study': case_study}
    return render(request, 'properties/case_study_detail.html', context)


def gallery_list(request):
    category = request.GET.get('category', '')
    albums = MediaAlbum.objects.filter(is_published=True)
    if category:
        albums = albums.filter(category__iexact=category)
    categories = MediaAlbum.objects.filter(is_published=True).values_list('category', flat=True).distinct()
    context = {
        'albums': albums,
        'categories': [c for c in categories if c],
        'active_category': category,
    }
    return render(request, 'properties/gallery_list.html', context)


def gallery_detail(request, slug):
    album = get_object_or_404(MediaAlbum, slug=slug, is_published=True)
    context = {'album': album}
    return render(request, 'properties/gallery_detail.html', context)


def market_report_list(request):
    """List all published market reports and generate dynamic reports from property data"""
    from django.db.models import Count, Avg, Max, Min, Q
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    # Get published market reports from database
    reports = MarketReport.objects.filter(is_published=True)
    featured_reports = reports.filter(is_featured=True)[:3]
    categories = MarketReport.objects.filter(is_published=True).values_list('category', flat=True).distinct()
    
    # Generate dynamic market analysis from property database
    active_properties = Property.objects.filter(status__in=['active', 'new_offer'])
    
    # Property statistics for market analysis
    market_stats = {
        'total_properties': active_properties.count(),
        'for_sale_count': active_properties.filter(sale_type='for_sale').count(),
        'for_rent_count': active_properties.filter(sale_type='for_rent').count(),
        'avg_price': active_properties.filter(price__isnull=False).aggregate(Avg('price'))['price__avg'],
        'max_price': active_properties.filter(price__isnull=False).aggregate(Max('price'))['price__max'],
        'min_price': active_properties.filter(price__isnull=False).aggregate(Min('price'))['price__min'],
        'apartments_count': active_properties.filter(property_type='apartment').count(),
        'shops_count': active_properties.filter(property_type='shop').count(),
        'commercial_count': active_properties.filter(property_type='commercial').count(),
        'avg_size': active_properties.aggregate(Avg('size'))['size__avg'],
        'avg_bedrooms': active_properties.filter(bedrooms__gt=0).aggregate(Avg('bedrooms'))['bedrooms__avg'],
        'avg_bathrooms': active_properties.filter(bathrooms__gt=0).aggregate(Avg('bathrooms'))['bathrooms__avg'],
    }
    
    # Location analysis
    location_stats = active_properties.values('location').annotate(
        count=Count('id'),
        avg_price=Avg('price')
    ).order_by('-count')[:10]
    
    # Property type distribution
    type_distribution = active_properties.values('property_type').annotate(
        count=Count('id')
    )
    
    # Recent properties (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_properties = active_properties.filter(created_at__gte=thirty_days_ago).count()
    
    # Filter by category if provided
    category = request.GET.get('category')
    if category:
        reports = reports.filter(category=category)
    
    paginator = Paginator(reports, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    site_settings = SiteSettings.load()
    
    context = {
        'reports': page_obj,
        'featured_reports': featured_reports,
        'categories': categories,
        'current_category': category,
        'site_settings': site_settings,
        'market_stats': market_stats,
        'location_stats': location_stats,
        'type_distribution': type_distribution,
        'recent_properties': recent_properties,
    }
    return render(request, 'properties/market_reports.html', context)


def market_report_detail(request, slug):
    """Detail view for a market report"""
    report = get_object_or_404(MarketReport, slug=slug, is_published=True)
    
    # Increment view count
    report.view_count += 1
    report.save(update_fields=['view_count'])
    
    # Get related reports
    related_reports = MarketReport.objects.filter(
        is_published=True
    ).exclude(id=report.id)[:4]
    
    site_settings = SiteSettings.load()
    
    context = {
        'report': report,
        'related_reports': related_reports,
        'site_settings': site_settings,
    }
    return render(request, 'properties/market_report_detail.html', context)


def buying_guide_list(request):
    """List all published buying guides"""
    guides = BuyingGuide.objects.filter(is_published=True)
    featured_guides = guides.filter(is_featured=True)[:3]
    
    # Filter by category if provided
    category = request.GET.get('category')
    if category:
        guides = guides.filter(category=category)
    
    paginator = Paginator(guides, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    site_settings = SiteSettings.load()
    
    context = {
        'guides': page_obj,
        'featured_guides': featured_guides,
        'current_category': category,
        'site_settings': site_settings,
    }
    return render(request, 'properties/buying_guides.html', context)


def buying_guide_detail(request, slug):
    """Detail view for a buying guide"""
    guide = get_object_or_404(BuyingGuide, slug=slug, is_published=True)
    
    # Increment view count
    guide.view_count += 1
    guide.save(update_fields=['view_count'])
    
    # Get related guides
    related_guides = BuyingGuide.objects.filter(
        is_published=True
    ).exclude(id=guide.id)[:4]
    
    # Get related properties (optional - can be enhanced)
    related_properties = Property.objects.filter(
        status__in=['active', 'new_offer']
    )[:6]
    
    site_settings = SiteSettings.load()
    
    context = {
        'guide': guide,
        'related_guides': related_guides,
        'related_properties': related_properties,
        'site_settings': site_settings,
    }
    return render(request, 'properties/buying_guide_detail.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save(commit=False)
            contact_message.gdpr_consent = form.cleaned_data['gdpr_consent']
            contact_message.save()
            messages.success(
                request,
                _('Thank you! Your message has been sent. Our team will get back to you within 1–2 business days.'),
            )
            return redirect('site:contact')
    else:
        form = ContactForm()

    site_settings = SiteSettings.load()
    context = {
        'form': form,
        'site_settings': site_settings,
        'working_schedule': WorkingSchedule.objects.all(),
    }
    return render(request, 'properties/contact.html', context)


def property_request(request):
    """Page for customers to submit their property needs"""
    if request.method == 'POST':
        form = PropertyNeedRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your property request has been submitted! Our team will contact you soon.'))
            return redirect('site:property_request')
    else:
        form = PropertyNeedRequestForm()
    
    context = {
        'form': form,
    }
    return render(request, 'properties/property_request.html', context)


@login_required
def book_property(request, slug):
    property = get_object_or_404(Property, slug=slug)
    
    if request.method == 'POST':
        form = PropertyBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.property = property
            booking.user = request.user
            booking.status = 'pending'
            booking.save()
            messages.success(request, _('Your booking request has been submitted and is pending approval.'))
            return redirect('site:my_bookings')
    else:
        form = PropertyBookingForm()
    
    context = {
        'property': property,
        'form': form,
    }
    return render(request, 'properties/book_property.html', context)


@login_required
def my_bookings(request):
    bookings = PropertyBooking.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'bookings': bookings,
    }
    return render(request, 'properties/my_bookings.html', context)


@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(PropertyBooking, id=booking_id, user=request.user)
    context = {
        'booking': booking,
    }
    return render(request, 'properties/booking_detail.html', context)


@require_POST
def custom_set_language(request):
    """Custom language switcher that properly handles redirects with prefix_default_language=False"""
    from django.utils.translation import activate
    from django.conf import settings
    
    next_url = request.POST.get('next', '/')
    language = request.POST.get('language')
    
    # Validate language code
    if not language or language not in [lang[0] for lang in settings.LANGUAGES]:
        return redirect(next_url or '/')
    
    # Set the language FIRST (before processing URL)
    activate(language)
    request.session['django_language'] = language
    request.session['language_detected'] = True  # Mark that user has manually selected language
    request.session.modified = True  # Mark session as modified
    request.session.save()  # Ensure session is saved
    
    # Parse the next URL to separate path and query string
    from urllib.parse import urlparse
    
    # Handle both relative and absolute URLs
    if next_url.startswith('http'):
        parsed_url = urlparse(next_url)
        path_without_lang = parsed_url.path
        query_string = parsed_url.query
    else:
        # Relative URL
        if '?' in next_url:
            path_without_lang, query_string = next_url.split('?', 1)
        else:
            path_without_lang = next_url
            query_string = ''
    
    # Get all non-English language prefixes from settings
    lang_prefixes = [lang[0] for lang in settings.LANGUAGES if lang[0] != 'en']
    
    # Remove any existing language prefix from the path
    original_path = path_without_lang
    for lang_prefix in lang_prefixes:
        prefix_pattern = '/' + lang_prefix + '/'
        if path_without_lang.startswith(prefix_pattern):
            # Remove /lang/ prefix (e.g., /am/properties/ -> /properties/)
            path_without_lang = '/' + path_without_lang[len(prefix_pattern):]
            break
        elif path_without_lang == '/' + lang_prefix:
            # Root path with just /lang (e.g., /am -> /)
            path_without_lang = '/'
            break
        elif path_without_lang.startswith('/' + lang_prefix + '?'):
            # Root with query string (e.g., /am?param=value -> /?param=value)
            path_without_lang = '/' + path_without_lang[len(lang_prefix) + 1:]
            break
    
    # Ensure path starts with /
    if not path_without_lang or not path_without_lang.startswith('/'):
        path_without_lang = '/'
    
    # Normalize path (remove double slashes, ensure proper format)
    if len(path_without_lang) > 1:
        parts = [p for p in path_without_lang.split('/') if p]
        path_without_lang = '/' + '/'.join(parts) if parts else '/'
    else:
        path_without_lang = '/'
    
    # Build redirect URL manually (simpler and more reliable with prefix_default_language=False)
    # For English (default), no prefix. For other languages, add prefix.
    if language == 'en':
        # English: no prefix (path without language prefix)
        redirect_path = path_without_lang
    else:
        # Other languages: add prefix
        if path_without_lang == '/':
            redirect_path = '/' + language + '/'
        else:
            # Ensure path starts with / before adding language prefix
            if not path_without_lang.startswith('/'):
                path_without_lang = '/' + path_without_lang
            redirect_path = '/' + language + path_without_lang
    
    # Reconstruct URL with query string
    redirect_url = redirect_path
    if query_string:
        redirect_url += '?' + query_string
    
    # Debug - print to console (can be removed in production)
    print(f"[Language Switch] {language} | Original: {original_path} | Stripped: {path_without_lang} | Redirect: {redirect_url}")
    
    return HttpResponseRedirect(redirect_url)


def book_viewing(request, slug):
    """Quick viewing appointment booking"""
    property = get_object_or_404(Property, slug=slug)
    site_settings = SiteSettings.load()
    
    if request.method == 'POST':
        form = ViewingAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.property = property
            appointment.status = 'pending'
            appointment.save()
            messages.success(request, _('Your viewing appointment request has been submitted! We will contact you soon to confirm.'))
            return redirect('site:property_detail', slug=slug)
    else:
        form = ViewingAppointmentForm()
    
    context = {
        'property': property,
        'form': form,
        'site_settings': site_settings,
    }
    return render(request, 'properties/book_viewing.html', context)
