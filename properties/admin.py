from django.contrib import admin, messages
from django.http import Http404
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .admin_export import (
    ExportMixin,
    CONTACT_EXPORT,
    EVENT_REGISTRATION_EXPORT,
    SERVICE_EXPORT,
    TRAINING_EVENT_EXPORT,
    TEAM_MEMBER_EXPORT,
    TESTIMONIAL_EXPORT,
    CASE_STUDY_EXPORT,
    PARTNER_EXPORT,
    MILESTONE_EXPORT,
    WORKING_SCHEDULE_EXPORT,
    VACANCY_EXPORT,
    VACANCY_APPLICATION_EXPORT,
)
from .event_export import EXPORTERS, export_registrations
from .vacancy_export import EXPORTERS as VACANCY_EXPORTERS, export_applications
from .media_bulk_upload import add_bulk_media_to_album
from .models import (
    Project, Property, PropertyImage, Contact, TeamMember,
    PropertyBooking, ConstructionProgress, ConstructionProgressImage,
    HomePageSettings, SiteSettings, ViewingAppointment, FloorPlan,
    MarketReport, BuyingGuide, Service, TrainingEvent, EventRegistration,
    CaseStudy, CaseStudyTimeline, Testimonial, Partner, Milestone,
    Vacancy, VacancyApplication,
    MediaAlbum, MediaItem, WorkingSchedule, ServiceMedia, CaseStudyMedia, EventMedia,
)
# PromotionalOffer and AboutPageSettings may not exist - check models.py
try:
    from .models import PromotionalOffer
except ImportError:
    PromotionalOffer = None

try:
    from .models import AboutPageSettings
except ImportError:
    AboutPageSettings = None

try:
    from .models import PropertyNeedRequest
except ImportError:
    PropertyNeedRequest = None

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


class FloorPlanInline(admin.TabularInline):
    model = FloorPlan
    extra = 1
    fields = ('title', 'image', 'description', 'order')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'property_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'location']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'property_type', 'status', 'bedrooms', 'bathrooms', 'size', 'featured', 'is_verified', 'has_coordinates', 'updated_at']
    list_filter = ['property_type', 'status', 'sale_type', 'featured', 'is_verified', 'project']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description', 'location', 'address']
    inlines = [PropertyImageInline, FloorPlanInline]
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('project', 'title', 'slug', 'description')
        }),
        (_('Property Details'), {
            'fields': ('property_type', 'status', 'sale_type', 'bedrooms', 'bathrooms', 'size', 'price')
        }),
        (_('Location'), {
            'fields': ('location', 'address', 'latitude', 'longitude'),
            'description': 'Enter address and location. Latitude and longitude can be added manually or use the geocoding command: python manage.py geocode_properties --all'
        }),
        (_('Media'), {
            'fields': ('main_image', 'walkthrough_video', 'walkthrough_video_url')
        }),
        (_('Settings'), {
            'fields': ('featured', 'is_verified')
        }),
    )
    
    def has_coordinates(self, obj):
        """Check if property has coordinates"""
        return bool(obj.latitude and obj.longitude)
    has_coordinates.boolean = True
    has_coordinates.short_description = 'Has Coordinates'


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'alt_text', 'order']
    list_filter = ['property']


@admin.register(Contact)
class ContactAdmin(ExportMixin, admin.ModelAdmin):
    export_config = CONTACT_EXPORT
    list_display = ['name', 'email', 'phone', 'subject', 'created_at', 'gdpr_consent']
    list_filter = ['subject', 'created_at', 'gdpr_consent']
    search_fields = ['name', 'last_name', 'email', 'phone', 'message']
    readonly_fields = ['created_at']
    exclude = ['property']
    fieldsets = (
        (_('Contact Details'), {
            'fields': ('name', 'last_name', 'email', 'phone', 'subject'),
        }),
        (_('Message'), {
            'fields': ('message', 'gdpr_consent', 'created_at'),
        }),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(ExportMixin, admin.ModelAdmin):
    export_config = TEAM_MEMBER_EXPORT
    list_display = ['name', 'title', 'role', 'is_founder', 'email', 'years_experience', 'order']
    list_filter = ['role', 'is_founder', 'is_verified']
    search_fields = ['name', 'email', 'phone', 'title']
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'title', 'role', 'is_founder', 'bio', 'credentials', 'order')
        }),
        (_('Contact Information'), {
            'fields': ('email', 'phone', 'whatsapp_number')
        }),
        (_('Professional Details'), {
            'fields': ('years_experience', 'languages', 'is_verified')
        }),
        (_('Media'), {
            'fields': ('image',)
        }),
    )


class ConstructionProgressImageInline(admin.TabularInline):
    model = ConstructionProgressImage
    extra = 1


@admin.register(PropertyBooking)
class PropertyBookingAdmin(admin.ModelAdmin):
    list_display = ['property', 'full_name', 'email', 'phone', 'status', 'start_date', 'end_date', 'created_at']
    list_filter = ['status', 'start_date', 'end_date', 'created_at']
    search_fields = ['full_name', 'email', 'phone', 'property__title']
    readonly_fields = ['created_at', 'updated_at', 'approved_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (_('Property & User'), {
            'fields': ('property', 'user')
        }),
        (_('Booking Information'), {
            'fields': ('status', 'start_date', 'end_date')
        }),
        (_('Customer Information'), {
            'fields': ('full_name', 'email', 'phone', 'id_number')
        }),
        (_('Notes'), {
            'fields': ('notes', 'admin_notes')
        }),
        (_('Approval'), {
            'fields': ('approved_by', 'approved_at')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['approve_bookings', 'reject_bookings']
    
    def approve_bookings(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(status='pending').update(
            status='approved',
            approved_by=request.user,
            approved_at=timezone.now()
        )
        self.message_user(request, _('{} bookings approved.').format(updated))
    approve_bookings.short_description = _('Approve selected bookings')
    
    def reject_bookings(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, _('{} bookings rejected.').format(updated))
    reject_bookings.short_description = _('Reject selected bookings')


@admin.register(ConstructionProgress)
class ConstructionProgressAdmin(admin.ModelAdmin):
    list_display = ['project', 'title', 'progress_percentage', 'update_date', 'is_published', 'created_at']
    list_filter = ['is_published', 'update_date', 'project']
    search_fields = ['title', 'description', 'project__name']
    prepopulated_fields = {}
    inlines = [ConstructionProgressImageInline]
    date_hierarchy = 'update_date'


@admin.register(ConstructionProgressImage)
class ConstructionProgressImageAdmin(admin.ModelAdmin):
    list_display = ['progress', 'caption', 'order']
    list_filter = ['progress__project']


@admin.register(HomePageSettings)
class HomePageSettingsAdmin(admin.ModelAdmin):
    """Admin for homepage settings - singleton pattern"""
    def has_add_permission(self, request):
        # Only allow one instance
        try:
            return not HomePageSettings.objects.exists()
        except:
            # Table doesn't exist yet (during migrations)
            return True
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False
    
    fieldsets = (
        (_('Hero Video Settings'), {
            'fields': (
                'hero_video_enabled',
                'hero_video',
                'hero_video_poster',
                'use_static_video',
                'static_video_path',
            )
        }),
        (_('Hero Text Content'), {
            'fields': (
                'hero_title',
                'hero_subtitle',
                'hero_description',
                'hero_button_text',
                'hero_button_url',
            )
        }),
        (_('Metadata'), {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['updated_at']


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Admin for site settings - singleton pattern"""
    def has_add_permission(self, request):
        try:
            return not SiteSettings.objects.exists()
        except:
            return True
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    fieldsets = (
        (_('WhatsApp Integration'), {
            'fields': (
                'whatsapp_enabled',
                'whatsapp_number',
                'whatsapp_default_message',
            )
        }),
        (_('Social Media'), {
            'fields': (
                'facebook_url',
                'telegram_url',
                'youtube_url',
            )
        }),
        (_('Company Information'), {
            'fields': (
                'company_name',
                'company_tagline',
                'company_phone',
                'company_phone_secondary',
                'company_email',
                'company_address',
                'latitude',
                'longitude',
            )
        }),
        (_('Metadata'), {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['updated_at']


# @admin.register(PromotionalOffer)  # Commented out if model doesn't exist
if PromotionalOffer is not None:
    @admin.register(PromotionalOffer)
    class PromotionalOfferAdmin(admin.ModelAdmin):
        """Admin for promotional offers"""
        list_display = ['title', 'badge_type', 'is_active', 'order', 'start_date', 'end_date', 'created_at']
        list_filter = ['is_active', 'badge_type', 'icon', 'start_date', 'end_date']
        search_fields = ['title', 'description']
        list_editable = ['order', 'is_active']


if PropertyNeedRequest is not None:
    @admin.register(PropertyNeedRequest)
    class PropertyNeedRequestAdmin(admin.ModelAdmin):
        list_display = ['full_name', 'preferred_location', 'property_type', 'sale_type', 'budget_min', 'budget_max', 'created_at']
        list_filter = ['property_type', 'sale_type', 'created_at']
        search_fields = ['full_name', 'email', 'phone', 'preferred_location', 'notes']
        readonly_fields = ['created_at']
        fieldsets = (
            (_('Contact'), {
                'fields': ('full_name', 'email', 'phone', 'whatsapp_number')
            }),
            (_('Preferences'), {
                'fields': ('preferred_location', 'property_type', 'sale_type', 'move_in_timeline')
            }),
            (_('Bedrooms / Bathrooms'), {
                'fields': (
                    ('bedrooms_min', 'bedrooms_max'),
                    ('bathrooms_min', 'bathrooms_max'),
                )
            }),
            (_('Budget & Size'), {
                'fields': (
                    ('budget_min', 'budget_max'),
                    ('size_min', 'size_max'),
                )
            }),
            (_('Notes'), {
                'fields': ('notes',)
            }),
            (_('Meta'), {
                'fields': ('created_at',),
                'classes': ('collapse',)
            }),
        )


# @admin.register(AboutPageSettings)  # Commented out if model doesn't exist
if AboutPageSettings:
    @admin.register(AboutPageSettings)
    class AboutPageSettingsAdmin(admin.ModelAdmin):
        """Admin for about page settings - singleton pattern"""
        def has_add_permission(self, request):
            # Only allow one instance
            try:
                return not AboutPageSettings.objects.exists()
            except:
                # Table doesn't exist yet (during migrations)
                return True
        
        def has_delete_permission(self, request, obj=None):
            # Prevent deletion
            return False
        
        fieldsets = (
            (_('Video Settings'), {
                'fields': (
                    'about_video_enabled',
                    'about_video',
                    'about_video_url',
                    'about_video_poster',
                )
            }),
        )
        
        readonly_fields = ['updated_at']


@admin.register(ViewingAppointment)
class ViewingAppointmentAdmin(admin.ModelAdmin):
    list_display = ['property', 'full_name', 'email', 'phone', 'preferred_date', 'preferred_time', 'status', 'created_at']
    list_filter = ['status', 'preferred_date', 'created_at', 'assigned_agent']
    search_fields = ['full_name', 'email', 'phone', 'property__title']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'preferred_date'
    
    fieldsets = (
        (_('Property & Agent'), {
            'fields': ('property', 'assigned_agent')
        }),
        (_('Customer Information'), {
            'fields': ('full_name', 'email', 'phone', 'whatsapp_number')
        }),
        (_('Appointment Details'), {
            'fields': ('preferred_date', 'preferred_time', 'notes')
        }),
        (_('Status'), {
            'fields': ('status',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['confirm_appointments', 'mark_completed', 'cancel_appointments']
    
    def confirm_appointments(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='confirmed')
        self.message_user(request, _('{} appointments confirmed.').format(updated))
    confirm_appointments.short_description = _('Confirm selected appointments')
    
    def mark_completed(self, request, queryset):
        updated = queryset.filter(status__in=['pending', 'confirmed']).update(status='completed')
        self.message_user(request, _('{} appointments marked as completed.').format(updated))
    mark_completed.short_description = _('Mark as completed')
    
    def cancel_appointments(self, request, queryset):
        updated = queryset.exclude(status='cancelled').update(status='cancelled')
        self.message_user(request, _('{} appointments cancelled.').format(updated))
    cancel_appointments.short_description = _('Cancel selected appointments')


@admin.register(FloorPlan)
class FloorPlanAdmin(admin.ModelAdmin):
    list_display = ['property', 'title', 'order']
    list_filter = ['property']
    search_fields = ['property__title', 'title', 'description']
    list_editable = ['order']


@admin.register(MarketReport)
class MarketReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_published', 'is_featured', 'publication_date', 'view_count', 'created_at']
    list_filter = ['is_published', 'is_featured', 'category', 'publication_date', 'created_at']
    search_fields = ['title', 'content', 'excerpt', 'tags', 'category']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publication_date'
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    
    fieldsets = (
        (_('Content'), {
            'fields': ('title', 'slug', 'excerpt', 'content', 'category', 'tags')
        }),
        (_('Media'), {
            'fields': ('featured_image',)
        }),
        (_('Settings'), {
            'fields': ('is_published', 'is_featured', 'publication_date')
        }),
        (_('Statistics'), {
            'fields': ('view_count',),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BuyingGuide)
class BuyingGuideAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_published', 'is_featured', 'publication_date', 'view_count', 'created_at']
    list_filter = ['is_published', 'is_featured', 'category', 'publication_date', 'created_at']
    search_fields = ['title', 'content', 'excerpt', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publication_date'
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    
    fieldsets = (
        (_('Content'), {
            'fields': ('title', 'slug', 'category', 'excerpt', 'content', 'tags')
        }),
        (_('Media'), {
            'fields': ('featured_image',)
        }),
        (_('Settings'), {
            'fields': ('is_published', 'is_featured', 'publication_date')
        }),
        (_('Statistics'), {
            'fields': ('view_count',),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class CaseStudyTimelineInline(admin.TabularInline):
    model = CaseStudyTimeline
    extra = 1


class MediaItemInline(admin.TabularInline):
    model = MediaItem
    extra = 1
    min_num = 0
    fields = ('title', 'image', 'video_file', 'video_url', 'caption', 'media_type', 'order')
    verbose_name = _('Gallery item')
    verbose_name_plural = _('Album items (edit titles/order below, or use bulk upload above)')


class ServiceMediaInline(admin.StackedInline):
    model = ServiceMedia
    extra = 3
    min_num = 0
    fields = ('title', 'image', 'video_file', 'video_url', 'caption', 'media_type', 'order')


class CaseStudyMediaInline(admin.StackedInline):
    model = CaseStudyMedia
    extra = 3
    min_num = 0
    fields = ('title', 'image', 'video_file', 'video_url', 'caption', 'media_type', 'order')


class EventMediaInline(admin.StackedInline):
    model = EventMedia
    extra = 3
    min_num = 0
    fields = ('title', 'image', 'video_file', 'video_url', 'caption', 'media_type', 'order')


@admin.register(Service)
class ServiceAdmin(ExportMixin, admin.ModelAdmin):
    export_config = SERVICE_EXPORT
    list_display = ['title', 'category', 'is_featured', 'is_active', 'order']
    list_filter = ['category', 'is_featured', 'is_active']
    list_editable = ['is_featured', 'is_active', 'order']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'short_description']
    inlines = [ServiceMediaInline]
    fieldsets = (
        (_('Service Details'), {
            'fields': ('title', 'slug', 'category', 'icon', 'short_description', 'full_description', 'image')
        }),
        (_('Display'), {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )


@admin.register(TrainingEvent)
class TrainingEventAdmin(ExportMixin, admin.ModelAdmin):
    export_config = TRAINING_EVENT_EXPORT
    list_display = ['title', 'event_type', 'start_date', 'location', 'registration_count', 'is_published', 'is_featured']
    list_filter = ['event_type', 'is_published', 'is_featured']
    list_editable = ['is_published', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'location']
    date_hierarchy = 'start_date'
    readonly_fields = ['export_participants_links']
    fieldsets = (
        (_('Event Details'), {
            'fields': ('title', 'slug', 'event_type', 'short_description', 'description', 'featured_image')
        }),
        (_('Schedule & Location'), {
            'fields': ('start_date', 'end_date', 'location', 'venue', 'registration_deadline')
        }),
        (_('Registration'), {
            'fields': ('max_participants', 'brochure', 'export_participants_links'),
            'description': _('Download registered participants for this event in Excel, CSV, Word, or PDF.'),
        }),
        (_('Publishing'), {
            'fields': ('is_published', 'is_featured')
        }),
    )
    inlines = [EventMediaInline]

    @admin.display(description=_('Registrations'))
    def registration_count(self, obj):
        total = obj.registrations.count()
        confirmed = obj.registrations.filter(status='confirmed').count()
        return f'{confirmed}/{total}'

    @admin.display(description=_('Export participants'))
    def export_participants_links(self, obj):
        if not obj or not obj.pk:
            return _('Save this event first to export participants.')
        links = []
        labels = {
            'xlsx': _('Excel (.xlsx)'),
            'csv': _('CSV (.csv)'),
            'docx': _('Word (.docx)'),
            'pdf': _('PDF (.pdf)'),
        }
        for file_format, label in labels.items():
            url = reverse(
                'admin:properties_trainingevent_export_participants',
                args=[obj.pk, file_format],
            )
            links.append(format_html('<a class="button" href="{}">{}</a>', url, label))
        return mark_safe(' &nbsp;|&nbsp; '.join(str(link) for link in links))

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/export-participants/<str:file_format>/',
                self.admin_site.admin_view(self.export_participants_view),
                name='properties_trainingevent_export_participants',
            ),
        ]
        return custom_urls + urls

    def export_participants_view(self, request, object_id, file_format):
        if file_format not in EXPORTERS:
            raise Http404(_('Unsupported export format.'))

        event = self.get_object(request, object_id)
        if event is None:
            raise Http404(_('Event not found.'))

        queryset = event.registrations.all()
        status = request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        return export_registrations(queryset, file_format, event=event)


@admin.register(EventRegistration)
class EventRegistrationAdmin(ExportMixin, admin.ModelAdmin):
    export_config = EVENT_REGISTRATION_EXPORT
    list_display = ['full_name', 'event', 'email', 'organization', 'status', 'created_at']
    list_filter = ['status', 'event', 'created_at']
    search_fields = ['full_name', 'email', 'organization']


@admin.register(CaseStudy)
class CaseStudyAdmin(ExportMixin, admin.ModelAdmin):
    export_config = CASE_STUDY_EXPORT
    list_display = ['title', 'client_name', 'industry', 'is_featured', 'is_published']
    list_filter = ['is_featured', 'is_published', 'industry']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CaseStudyTimelineInline, CaseStudyMediaInline]


@admin.register(Testimonial)
class TestimonialAdmin(ExportMixin, admin.ModelAdmin):
    export_config = TESTIMONIAL_EXPORT
    list_display = ['client_name', 'organization', 'rating', 'is_featured', 'is_active']
    list_filter = ['is_featured', 'is_active', 'rating']


@admin.register(Partner)
class PartnerAdmin(ExportMixin, admin.ModelAdmin):
    export_config = PARTNER_EXPORT
    list_display = ['name', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'order']
    fields = ('name', 'logo', 'website', 'description', 'is_active', 'order')


@admin.register(Vacancy)
class VacancyAdmin(ExportMixin, admin.ModelAdmin):
    export_config = VACANCY_EXPORT
    list_display = [
        'title', 'department', 'employment_type', 'application_deadline',
        'application_count_display', 'is_published', 'is_featured',
    ]
    list_filter = ['employment_type', 'is_published', 'is_featured']
    list_editable = ['is_published', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'department', 'location']
    readonly_fields = ['export_applicants_links']
    fieldsets = (
        (_('Position Details'), {
            'fields': ('title', 'slug', 'department', 'location', 'employment_type', 'short_description', 'description', 'requirements'),
        }),
        (_('Application Period'), {
            'fields': ('application_open_at', 'application_deadline', 'max_applications', 'export_applicants_links'),
            'description': _('Control when applicants can apply and export received applications.'),
        }),
        (_('Publishing'), {
            'fields': ('is_published', 'is_featured'),
        }),
    )

    @admin.display(description=_('Applications'))
    def application_count_display(self, obj):
        return obj.application_count

    @admin.display(description=_('Export applicants'))
    def export_applicants_links(self, obj):
        if not obj or not obj.pk:
            return _('Save this vacancy first to export applicants.')
        links = []
        labels = {
            'xlsx': _('Excel (.xlsx)'),
            'csv': _('CSV (.csv)'),
            'docx': _('Word (.docx)'),
            'pdf': _('PDF (.pdf)'),
        }
        for file_format, label in labels.items():
            url = reverse(
                'admin:properties_vacancy_export_applicants',
                args=[obj.pk, file_format],
            )
            links.append(format_html('<a class="button" href="{}">{}</a>', url, label))
        return mark_safe(' &nbsp;|&nbsp; '.join(str(link) for link in links))

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/export-applicants/<str:file_format>/',
                self.admin_site.admin_view(self.export_applicants_view),
                name='properties_vacancy_export_applicants',
            ),
        ]
        return custom_urls + urls

    def export_applicants_view(self, request, object_id, file_format):
        if file_format not in VACANCY_EXPORTERS:
            raise Http404(_('Unsupported export format.'))

        vacancy = self.get_object(request, object_id)
        if vacancy is None:
            raise Http404(_('Vacancy not found.'))

        queryset = vacancy.applications.all()
        status = request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return export_applications(queryset, file_format, vacancy=vacancy)


@admin.register(VacancyApplication)
class VacancyApplicationAdmin(ExportMixin, admin.ModelAdmin):
    export_config = VACANCY_APPLICATION_EXPORT
    list_display = ['full_name', 'vacancy', 'email', 'phone', 'status', 'created_at']
    list_filter = ['status', 'vacancy', 'created_at']
    search_fields = ['full_name', 'email', 'phone', 'vacancy__title']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(Milestone)
class MilestoneAdmin(ExportMixin, admin.ModelAdmin):
    export_config = MILESTONE_EXPORT
    list_display = ['year', 'title', 'order']


@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'album', 'media_type', 'order']
    list_filter = ['album', 'media_type']
    search_fields = ['title', 'caption', 'album__title']
    list_editable = ['order']
    fields = ('album', 'title', 'image', 'video_file', 'video_url', 'caption', 'media_type', 'order')


@admin.register(MediaAlbum)
class MediaAlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'item_count', 'is_published', 'order']
    list_filter = ['category', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [MediaItemInline]
    change_form_template = 'admin/properties/mediaalbum/change_form.html'

    @admin.display(description=_('Items'))
    def item_count(self, obj):
        return obj.items.count()

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        files = request.FILES.getlist('bulk_photos')
        if not files:
            return
        created = add_bulk_media_to_album(form.instance, files)
        if created:
            self.message_user(
                request,
                _('%(count)d file(s) added to the album.') % {'count': created},
                messages.SUCCESS,
            )
        else:
            self.message_user(
                request,
                _('No supported image or video files were uploaded.'),
                messages.WARNING,
            )


@admin.register(WorkingSchedule)
class WorkingScheduleAdmin(ExportMixin, admin.ModelAdmin):
    export_config = WORKING_SCHEDULE_EXPORT
    list_display = ['get_day_of_week_display', 'open_time', 'close_time', 'is_closed']


# Unregister legacy real-estate models from admin (not used on TTCS website)
_LEGACY_ADMIN_MODELS = [
    Project, Property, PropertyImage, PropertyBooking,
    ConstructionProgress, ConstructionProgressImage,
    ViewingAppointment, FloorPlan, MarketReport, BuyingGuide,
]
if PromotionalOffer is not None:
    _LEGACY_ADMIN_MODELS.append(PromotionalOffer)
if PropertyNeedRequest is not None:
    _LEGACY_ADMIN_MODELS.append(PropertyNeedRequest)

for _legacy_model in _LEGACY_ADMIN_MODELS:
    try:
        admin.site.unregister(_legacy_model)
    except admin.sites.NotRegistered:
        pass

