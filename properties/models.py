from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Project(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('properties:project_detail', kwargs={'slug': self.slug})

    @property
    def property_count(self):
        return self.properties.count()


class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('apartment', _('Apartment')),
        ('shop', _('Shop')),
        ('commercial', _('Commercial')),
    ]

    STATUS_CHOICES = [
        ('active', _('Active')),
        ('new_offer', _('New Offer')),
        ('sold', _('Sold')),
        ('booked', _('Booked')),
        ('on_hold', _('On Hold')),
    ]

    SALE_TYPE_CHOICES = [
        ('for_sale', _('For Sale')),
        ('for_rent', _('For Rent')),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, default='apartment')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    sale_type = models.CharField(max_length=20, choices=SALE_TYPE_CHOICES, default='for_sale')
    
    # Property details
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    size = models.DecimalField(max_digits=10, decimal_places=2, help_text="Size in square meters")
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    
    # Location
    address = models.CharField(max_length=300)
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        help_text=_('Latitude for map display (e.g., 9.1450)'),
        verbose_name=_('Latitude')
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        help_text=_('Longitude for map display (e.g., 38.7614)'),
        verbose_name=_('Longitude')
    )
    
    # Images
    main_image = models.ImageField(upload_to='properties/', blank=True, null=True)
    
    # Video Walkthrough
    walkthrough_video = models.FileField(
        upload_to='properties/videos/',
        blank=True,
        null=True,
        help_text=_('Video walkthrough of the property (MP4 recommended)'),
        verbose_name=_('Video Walkthrough')
    )
    walkthrough_video_url = models.URLField(
        blank=True,
        null=True,
        help_text=_('YouTube or Vimeo video URL (alternative to uploaded video)'),
        verbose_name=_('Video URL')
    )
    
    # Virtual Tour
    virtual_tour_image = models.ImageField(
        upload_to='properties/virtual_tours/',
        blank=True,
        null=True,
        help_text=_('360-degree panoramic image for virtual tour (equirectangular format recommended)'),
        verbose_name=_('Virtual Tour Image')
    )
    virtual_tour_url = models.URLField(
        blank=True,
        null=True,
        help_text=_('External virtual tour URL (e.g., Matterport, Kuula, etc.)'),
        verbose_name=_('Virtual Tour URL')
    )
    
    # Additional info
    featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(
        default=False,
        help_text=_('Mark property as verified for trust building'),
        verbose_name=_('Verified')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('properties:property_detail', kwargs={'slug': self.slug})
    
    def get_display_image(self):
        """Get the main image or first available image"""
        if self.main_image:
            return self.main_image
        # Try to get the first PropertyImage
        first_image = self.images.first()
        if first_image:
            return first_image.image
        return None


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/images/')
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']


class Contact(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='inquiries')
    created_at = models.DateTimeField(auto_now_add=True)
    gdpr_consent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Contact from {self.name}"


class TeamMember(models.Model):
    ROLE_CHOICES = [
        ('sales_officer', 'Sales Officer'),
        ('sales_agent', 'Sales Agent'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    whatsapp_number = models.CharField(
        max_length=20,
        blank=True,
        help_text=_('WhatsApp number with country code (e.g., +251912345678)'),
        verbose_name=_('WhatsApp Number')
    )
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(
        default=False,
        help_text=_('Mark agent as verified'),
        verbose_name=_('Verified')
    )
    years_experience = models.IntegerField(
        default=0,
        help_text=_('Years of experience in real estate'),
        verbose_name=_('Years of Experience')
    )
    languages = models.CharField(
        max_length=200,
        blank=True,
        help_text=_('Languages spoken (comma-separated, e.g., English, Amharic, Arabic)'),
        verbose_name=_('Languages')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.get_role_display()}"


class PropertyBooking(models.Model):
    """Model for booking/holding properties with approval workflow"""
    STATUS_CHOICES = [
        ('pending', _('Pending Approval')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
        ('expired', _('Expired')),
        ('completed', _('Completed')),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings', verbose_name=_('Property'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='property_bookings', verbose_name=_('User'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name=_('Status'))
    
    # Booking period
    start_date = models.DateTimeField(verbose_name=_('Start Date'))
    end_date = models.DateTimeField(verbose_name=_('End Date'))
    
    # Customer information
    full_name = models.CharField(max_length=200, verbose_name=_('Full Name'))
    email = models.EmailField(verbose_name=_('Email'))
    phone = models.CharField(max_length=20, verbose_name=_('Phone'))
    id_number = models.CharField(max_length=50, blank=True, verbose_name=_('ID Number'))
    
    # Additional information
    notes = models.TextField(blank=True, verbose_name=_('Notes'))
    admin_notes = models.TextField(blank=True, verbose_name=_('Admin Notes'))
    
    # Approval tracking
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                    related_name='approved_bookings', verbose_name=_('Approved By'))
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Approved At'))
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Property Booking')
        verbose_name_plural = _('Property Bookings')

    def __str__(self):
        return f"{self.property.title} - {self.full_name} ({self.get_status_display()})"

    def is_active(self):
        """Check if booking is currently active"""
        from django.utils import timezone
        return (self.status == 'approved' and 
                self.start_date <= timezone.now() <= self.end_date)

    def is_expired(self):
        """Check if booking has expired"""
        from django.utils import timezone
        return self.end_date < timezone.now() and self.status == 'approved'


class FloorPlan(models.Model):
    """Floor plans for properties"""
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='floor_plans',
        verbose_name=_('Property')
    )
    image = models.ImageField(
        upload_to='properties/floor_plans/',
        verbose_name=_('Floor Plan Image')
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        help_text=_('e.g., "Ground Floor", "First Floor", "Unit Layout"'),
        verbose_name=_('Title')
    )
    description = models.TextField(
        blank=True,
        help_text=_('Description of this floor plan'),
        verbose_name=_('Description')
    )
    order = models.IntegerField(
        default=0,
        help_text=_('Display order (lower numbers appear first)'),
        verbose_name=_('Order')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = _('Floor Plan')
        verbose_name_plural = _('Floor Plans')
    
    def __str__(self):
        if self.title:
            return f"{self.property.title} - {self.title}"
        return f"{self.property.title} - Floor Plan {self.order + 1}"


class MarketReport(models.Model):
    """Market reports and analysis for SEO and content marketing"""
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    slug = models.SlugField(unique=True, verbose_name=_('Slug'))
    excerpt = models.TextField(
        max_length=500,
        blank=True,
        help_text=_('Short summary for listings'),
        verbose_name=_('Excerpt')
    )
    content = models.TextField(verbose_name=_('Content'))
    featured_image = models.ImageField(
        upload_to='market_reports/',
        blank=True,
        null=True,
        verbose_name=_('Featured Image')
    )
    pdf_file = models.FileField(
        upload_to='market_reports/pdfs/',
        blank=True,
        null=True,
        help_text=_('Optional PDF download'),
        verbose_name=_('PDF File')
    )
    category = models.CharField(
        max_length=100,
        blank=True,
        help_text=_('e.g., "Q1 2025", "Annual Report", "Market Analysis"'),
        verbose_name=_('Category')
    )
    tags = models.CharField(
        max_length=300,
        blank=True,
        help_text=_('Comma-separated tags for SEO'),
        verbose_name=_('Tags')
    )
    is_published = models.BooleanField(default=True, verbose_name=_('Published'))
    is_featured = models.BooleanField(default=False, verbose_name=_('Featured'))
    view_count = models.IntegerField(default=0, verbose_name=_('View Count'))
    publication_date = models.DateField(verbose_name=_('Publication Date'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    
    class Meta:
        ordering = ['-publication_date', '-created_at']
        verbose_name = _('Market Report')
        verbose_name_plural = _('Market Reports')
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('properties:market_report_detail', kwargs={'slug': self.slug})
    
    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []


class BuyingGuide(models.Model):
    """Buying guides for SEO and content marketing"""
    CATEGORY_CHOICES = [
        ('first_time_buyer', _('First-Time Buyer')),
        ('investment', _('Investment Guide')),
        ('financing', _('Financing Guide')),
        ('legal', _('Legal Guide')),
        ('tips', _('Tips & Advice')),
        ('other', _('Other')),
    ]
    
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    slug = models.SlugField(unique=True, verbose_name=_('Slug'))
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='tips',
        verbose_name=_('Category')
    )
    excerpt = models.TextField(
        max_length=500,
        blank=True,
        help_text=_('Short summary for listings'),
        verbose_name=_('Excerpt')
    )
    content = models.TextField(verbose_name=_('Content'))
    featured_image = models.ImageField(
        upload_to='buying_guides/',
        blank=True,
        null=True,
        verbose_name=_('Featured Image')
    )
    tags = models.CharField(
        max_length=300,
        blank=True,
        help_text=_('Comma-separated tags for SEO'),
        verbose_name=_('Tags')
    )
    is_published = models.BooleanField(default=True, verbose_name=_('Published'))
    is_featured = models.BooleanField(default=False, verbose_name=_('Featured'))
    view_count = models.IntegerField(default=0, verbose_name=_('View Count'))
    publication_date = models.DateField(verbose_name=_('Publication Date'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    
    class Meta:
        ordering = ['-publication_date', '-created_at']
        verbose_name = _('Buying Guide')
        verbose_name_plural = _('Buying Guides')
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('properties:buying_guide_detail', kwargs={'slug': self.slug})
    
    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []


class ConstructionProgress(models.Model):
    """Model for tracking construction progress updates"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='progress_updates', 
                                verbose_name=_('Project'))
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    
    # Progress tracking
    progress_percentage = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Progress Percentage'),
        help_text=_('Progress from 0 to 100%')
    )
    
    # Date information
    update_date = models.DateField(verbose_name=_('Update Date'))
    
    # Images
    image = models.ImageField(upload_to='construction_progress/', blank=True, null=True, 
                              verbose_name=_('Image'))
    
    # Status
    is_published = models.BooleanField(default=True, verbose_name=_('Published'))
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        ordering = ['-update_date', '-created_at']
        verbose_name = _('Construction Progress')
        verbose_name_plural = _('Construction Progress Updates')

    def __str__(self):
        return f"{self.project.name} - {self.title} ({self.progress_percentage}%)"


class ConstructionProgressImage(models.Model):
    """Additional images for construction progress updates"""
    progress = models.ForeignKey(ConstructionProgress, on_delete=models.CASCADE, 
                                 related_name='images', verbose_name=_('Progress Update'))
    image = models.ImageField(upload_to='construction_progress/images/', verbose_name=_('Image'))
    caption = models.CharField(max_length=200, blank=True, verbose_name=_('Caption'))
    order = models.IntegerField(default=0, verbose_name=_('Order'))

    class Meta:
        ordering = ['order']
        verbose_name = _('Progress Image')
        verbose_name_plural = _('Progress Images')

    def __str__(self):
        return f"{self.progress.title} - Image {self.order + 1}"


class HomePageSettings(models.Model):
    """Singleton model for homepage settings including hero video"""
    # Hero Section Video
    hero_video = models.FileField(
        upload_to='videos/homepage/',
        blank=True,
        null=True,
        help_text=_('Video file for homepage hero section (MP4 recommended)'),
        verbose_name=_('Hero Video')
    )
    hero_video_poster = models.ImageField(
        upload_to='images/homepage/',
        blank=True,
        null=True,
        help_text=_('Poster image shown before video loads'),
        verbose_name=_('Video Poster Image')
    )
    hero_video_enabled = models.BooleanField(
        default=True,
        help_text=_('Enable/disable video background'),
        verbose_name=_('Video Enabled')
    )
    
    # Hero Section Text
    hero_title = models.CharField(
        max_length=200,
        default='MAKE YOUR NEXT MOVE WITH US',
        verbose_name=_('Hero Title')
    )
    hero_subtitle = models.CharField(
        max_length=200,
        default='ANDROMEDA PROPERTIES',
        verbose_name=_('Hero Subtitle')
    )
    hero_description = models.TextField(
        max_length=500,
        default='Discover the latest real estate in Ethiopia on Andromeda Properties',
        blank=True,
        verbose_name=_('Hero Description')
    )
    hero_button_text = models.CharField(
        max_length=50,
        default='Explore Properties',
        verbose_name=_('Hero Button Text')
    )
    
    # Fallback to static video if no video uploaded
    use_static_video = models.BooleanField(
        default=True,
        help_text=_('Use static video (video104.mp4) if no video is uploaded'),
        verbose_name=_('Use Static Video Fallback')
    )
    static_video_path = models.CharField(
        max_length=200,
        default='videos/video104.mp4',
        help_text=_('Path to static video file (relative to static folder)'),
        verbose_name=_('Static Video Path')
    )
    
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    
    class Meta:
        verbose_name = _('Homepage Settings')
        verbose_name_plural = _('Homepage Settings')
    
    def __str__(self):
        return 'Homepage Settings'
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists (singleton pattern)
        self.pk = 1
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Prevent deletion - just reset to defaults
        pass
    
    @classmethod
    def load(cls):
        """Get or create the singleton instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
    def get_video_url(self):
        """Get the video URL - prefer uploaded video, fallback to static path"""
        if self.hero_video_enabled:
            if self.hero_video:
                return self.hero_video.url
            elif self.use_static_video:
                # Return static path - template will use {% static %} tag
                return self.static_video_path
        return None
    
    def get_video_is_static(self):
        """Check if video is from static files (not uploaded)"""
        return self.hero_video_enabled and not self.hero_video and self.use_static_video
    
    def get_poster_url(self):
        """Get the poster image URL"""
        if self.hero_video_poster:
            return self.hero_video_poster.url
        # Return static path - template will use {% static %} tag
        return 'images/header-realestate.svg'
    
    def get_poster_is_static(self):
        """Check if poster is from static files (not uploaded)"""
        return not self.hero_video_poster


class SiteSettings(models.Model):
    """Site-wide settings including WhatsApp integration"""
    # WhatsApp Settings
    whatsapp_number = models.CharField(
        max_length=20,
        blank=True,
        help_text=_('WhatsApp Business number with country code (e.g., +251912345678)'),
        verbose_name=_('WhatsApp Number')
    )
    whatsapp_default_message = models.CharField(
        max_length=500,
        default='Hello! I am interested in your properties.',
        help_text=_('Default message for WhatsApp inquiries'),
        verbose_name=_('Default WhatsApp Message')
    )
    whatsapp_enabled = models.BooleanField(
        default=True,
        help_text=_('Enable WhatsApp floating button'),
        verbose_name=_('WhatsApp Enabled')
    )
    
    # Contact Information
    company_phone = models.CharField(max_length=20, blank=True, verbose_name=_('Company Phone'))
    company_email = models.EmailField(blank=True, verbose_name=_('Company Email'))
    
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    
    class Meta:
        verbose_name = _('Site Settings')
        verbose_name_plural = _('Site Settings')
    
    def __str__(self):
        return 'Site Settings'
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists (singleton pattern)
        self.pk = 1
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Prevent deletion
        pass
    
    @classmethod
    def load(cls):
        """Get or create the singleton instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
    def get_whatsapp_url(self, message=None, property_title=None):
        """Generate WhatsApp click-to-chat URL"""
        if not self.whatsapp_number:
            return None
        
        # Clean phone number (remove spaces, dashes, etc.)
        phone = self.whatsapp_number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        # Build message
        if property_title:
            msg = f"Hello! I'm interested in: {property_title}. {message or self.whatsapp_default_message}"
        else:
            msg = message or self.whatsapp_default_message
        
        # URL encode message
        from urllib.parse import quote
        encoded_msg = quote(msg)
        
        return f"https://wa.me/{phone}?text={encoded_msg}"


class AboutPageSettings(models.Model):
    """Singleton model for about page settings including video"""
    # Video Settings
    about_video = models.FileField(
        upload_to='videos/about/',
        blank=True,
        null=True,
        help_text=_('Video file for about page (MP4 recommended)'),
        verbose_name=_('About Page Video')
    )
    about_video_url = models.URLField(
        blank=True,
        null=True,
        help_text=_('External video URL (YouTube, Vimeo, etc.)'),
        verbose_name=_('Video URL')
    )
    about_video_poster = models.ImageField(
        upload_to='images/about/',
        blank=True,
        null=True,
        help_text=_('Poster image shown before video loads'),
        verbose_name=_('Video Poster Image')
    )
    about_video_enabled = models.BooleanField(
        default=True,
        help_text=_('Enable/disable video display'),
        verbose_name=_('Video Enabled')
    )
    
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    
    class Meta:
        verbose_name = _('About Page Settings')
        verbose_name_plural = _('About Page Settings')
    
    def __str__(self):
        return 'About Page Settings'
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists (singleton pattern)
        self.pk = 1
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Prevent deletion - just reset to defaults
        pass
    
    @classmethod
    def load(cls):
        """Get or create the singleton instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class ViewingAppointment(models.Model):
    """Model for property viewing appointments (quick lead capture)"""
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    ]
    
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='viewing_appointments',
        verbose_name=_('Property')
    )
    
    # Customer Information
    full_name = models.CharField(max_length=200, verbose_name=_('Full Name'))
    email = models.EmailField(verbose_name=_('Email'))
    phone = models.CharField(max_length=20, verbose_name=_('Phone'))
    whatsapp_number = models.CharField(
        max_length=20,
        blank=True,
        help_text=_('WhatsApp number if different from phone'),
        verbose_name=_('WhatsApp Number')
    )
    
    # Appointment Details
    preferred_date = models.DateField(verbose_name=_('Preferred Date'))
    preferred_time = models.TimeField(verbose_name=_('Preferred Time'))
    notes = models.TextField(blank=True, verbose_name=_('Additional Notes'))
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status')
    )
    
    # Agent Assignment
    assigned_agent = models.ForeignKey(
        TeamMember,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='viewing_appointments',
        verbose_name=_('Assigned Agent')
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Viewing Appointment')
        verbose_name_plural = _('Viewing Appointments')
    
    def __str__(self):
        return f"{self.property.title} - {self.full_name} ({self.get_status_display()})"

