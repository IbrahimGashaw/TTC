from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    Project, Property, PropertyImage, Contact, TeamMember,
    PropertyBooking, ConstructionProgress, ConstructionProgressImage,
    HomePageSettings, SiteSettings, ViewingAppointment, FloorPlan,
    MarketReport, BuyingGuide
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
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'property', 'created_at']
    list_filter = ['created_at', 'gdpr_consent']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at']


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'email', 'phone', 'is_verified', 'years_experience', 'created_at']
    list_filter = ['role', 'is_verified']
    search_fields = ['name', 'email', 'phone']
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'role', 'bio')
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
        (_('Contact Information'), {
            'fields': (
                'company_phone',
                'company_email',
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
        
        fieldsets = (
        (_('Offer Details'), {
            'fields': (
                'title',
                'description',
                'icon',
                'icon_color',
                'badge_type',
                'badge_color',
            )
        }),
        (_('Actions'), {
            'fields': (
                'call_action_text',
                'call_action_url',
                'details_action_text',
                'details_action_url',
            )
        }),
        (_('Settings'), {
            'fields': (
                'is_active',
                'order',
                'start_date',
                'end_date',
            )
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


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
            'fields': ('featured_image', 'pdf_file')
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

