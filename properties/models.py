from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


def sync_media_type(instance):
    """Set media_type from whichever file or URL was uploaded."""
    if instance.image and not instance.video_file and not instance.video_url:
        instance.media_type = 'image'
    elif (instance.video_file or instance.video_url) and not instance.image:
        instance.media_type = 'video'


def embed_video_url(url):
    """Convert YouTube/Vimeo watch URLs to embed URLs."""
    if not url:
        return None
    url = url.strip()
    if 'youtube.com/watch' in url and 'v=' in url:
        video_id = url.split('v=')[1].split('&')[0]
        return f'https://www.youtube.com/embed/{video_id}'
    if 'youtu.be/' in url:
        video_id = url.rstrip('/').split('/')[-1].split('?')[0]
        return f'https://www.youtube.com/embed/{video_id}'
    if 'vimeo.com/' in url:
        video_id = url.rstrip('/').split('/')[-1].split('?')[0]
        return f'https://player.vimeo.com/video/{video_id}'
    return url


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
        return reverse('site:project_detail', kwargs={'slug': self.slug})

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
        ('for_sale', _('Financed with bank')),
        ('for_rent', _('Non financed with bank')),
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
        return reverse('site:property_detail', kwargs={'slug': self.slug})
    
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


class PropertyNeedRequest(models.Model):
    """Customers can submit their property requirement"""
    PROPERTY_TYPE_CHOICES = Property.PROPERTY_TYPE_CHOICES
    SALE_TYPE_CHOICES = Property.SALE_TYPE_CHOICES

    full_name = models.CharField(max_length=150, verbose_name=_('Full Name'))
    email = models.EmailField(verbose_name=_('Email'))
    phone = models.CharField(max_length=30, verbose_name=_('Phone'), blank=True)
    whatsapp_number = models.CharField(max_length=30, verbose_name=_('WhatsApp Number'), blank=True)
    preferred_location = models.CharField(max_length=200, verbose_name=_('Preferred Location'), blank=True)
    property_type = models.CharField(
        max_length=30,
        choices=PROPERTY_TYPE_CHOICES,
        verbose_name=_('Property Type'),
        blank=True
    )
    sale_type = models.CharField(
        max_length=30,
        choices=SALE_TYPE_CHOICES,
        verbose_name=_('Sale/Payment Type'),
        blank=True
    )
    bedrooms_min = models.IntegerField(null=True, blank=True, verbose_name=_('Min Bedrooms'))
    bedrooms_max = models.IntegerField(null=True, blank=True, verbose_name=_('Max Bedrooms'))
    bathrooms_min = models.IntegerField(null=True, blank=True, verbose_name=_('Min Bathrooms'))
    bathrooms_max = models.IntegerField(null=True, blank=True, verbose_name=_('Max Bathrooms'))
    budget_min = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name=_('Min Budget (ETB)'))
    budget_max = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name=_('Max Budget (ETB)'))
    size_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_('Min Size (m²)'))
    size_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_('Max Size (m²)'))
    move_in_timeline = models.CharField(max_length=100, blank=True, verbose_name=_('Preferred Move-in Timeline'))
    notes = models.TextField(blank=True, verbose_name=_('Additional Notes'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Submitted At'))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Property Need Request')
        verbose_name_plural = _('Property Need Requests')

    def __str__(self):
        return f"{self.full_name} - {self.preferred_location or 'No location'}"

class TeamMember(models.Model):
    ROLE_CHOICES = [
        ('founder', _('Founder & Manager')),
        ('deputy_manager', _('Deputy Manager')),
        ('associate_trainer', _('Associate Trainer')),
        ('consultant', _('Consultant')),
        ('sales_officer', _('Sales Officer')),
        ('sales_agent', _('Business Development Officer')),
        ('other', _('Other')),
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
        help_text=_('Mark team member as verified'),
        verbose_name=_('Verified')
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        help_text=_('Professional title or designation'),
        verbose_name=_('Title')
    )
    credentials = models.TextField(
        blank=True,
        help_text=_('Degrees, certifications, and professional credentials'),
        verbose_name=_('Credentials')
    )
    is_founder = models.BooleanField(default=False, verbose_name=_('Founder'))
    order = models.IntegerField(default=0, verbose_name=_('Display Order'))
    years_experience = models.IntegerField(
        default=0,
        help_text=_('Years of professional experience'),
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
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('site:team_member_detail', kwargs={'pk': self.pk})


class PropertyBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='property_bookings', null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    id_number = models.CharField(max_length=50, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_bookings')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.property.title} - {self.full_name} ({self.get_status_display()})"


class FloorPlan(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='floor_plans')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='properties/floor_plans/')
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.property.title} - {self.title}"


class MarketReport(models.Model):
    CATEGORY_CHOICES = [
        ('market_analysis', _('Market Analysis')),
        ('price_trends', _('Price Trends')),
        ('location_insights', _('Location Insights')),
        ('investment_advice', _('Investment Advice')),
        ('general', _('General')),
    ]

    title = models.CharField(max_length=200, verbose_name=_('Title'))
    slug = models.SlugField(unique=True, verbose_name=_('Slug'))
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='general',
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
        upload_to='market_reports/',
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
        verbose_name = _('Market Report')
        verbose_name_plural = _('Market Reports')
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('site:market_report_detail', kwargs={'slug': self.slug})
    
    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []


class BuyingGuide(models.Model):
    CATEGORY_CHOICES = [
        ('tips', _('Buying Tips')),
        ('financing', _('Financing')),
        ('legal', _('Legal Advice')),
        ('investment', _('Investment Guide')),
        ('general', _('General')),
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
        return reverse('site:buying_guide_detail', kwargs={'slug': self.slug})
    
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
    progress_percentage = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Progress Percentage')
    )
    update_date = models.DateField(verbose_name=_('Update Date'))
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
    progress = models.ForeignKey(ConstructionProgress, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='construction_progress/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.progress.title} - Image {self.order}"


class HomePageSettings(models.Model):
    """Singleton model for homepage settings"""
    # Hero Video
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
        default='Guiding your Success, Every step of the way!',
        verbose_name=_('Hero Title')
    )
    hero_subtitle = models.CharField(
        max_length=200,
        default='TEAM TRAINING AND CONSULTANCY SERVICE PLC',
        verbose_name=_('Hero Subtitle')
    )
    hero_description = models.TextField(
        max_length=500,
        default='Specialized training, consultancy, and human resource sourcing solutions tailored to enhance organizational effectiveness and employee development.',
        blank=True,
        verbose_name=_('Hero Description')
    )
    hero_button_text = models.CharField(
        max_length=50,
        default='Explore Our Services',
        verbose_name=_('Hero Button Text')
    )
    hero_button_url = models.CharField(
        max_length=200,
        default='/services/',
        verbose_name=_('Hero Button URL')
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
        return 'images/team-training-logo.jpg'
    
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
        default='Hello! I am interested in your training and consultancy services.',
        help_text=_('Default message for WhatsApp inquiries'),
        verbose_name=_('Default WhatsApp Message')
    )
    whatsapp_enabled = models.BooleanField(
        default=True,
        help_text=_('Enable WhatsApp floating button'),
        verbose_name=_('WhatsApp Enabled')
    )
    
    # Contact Information
    company_name = models.CharField(
        max_length=200,
        default='Team Training and Consultancy Service PLC',
        verbose_name=_('Company Name')
    )
    company_tagline = models.CharField(
        max_length=200,
        default='Guiding your Success, Every step of the way!',
        verbose_name=_('Company Tagline')
    )
    company_phone = models.CharField(max_length=50, blank=True, verbose_name=_('Company Phone'))
    company_phone_secondary = models.CharField(max_length=50, blank=True, verbose_name=_('Secondary Phone'))
    company_email = models.EmailField(blank=True, verbose_name=_('Company Email'))
    company_address = models.CharField(max_length=300, blank=True, verbose_name=_('Company Address'))
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True,
        help_text=_('Latitude for map (e.g., 8.5400)'),
        verbose_name=_('Latitude')
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True,
        help_text=_('Longitude for map (e.g., 39.2700)'),
        verbose_name=_('Longitude')
    )
    
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
    
    def get_whatsapp_url(self, message=None, subject=None, property_title=None):
        """Generate WhatsApp click-to-chat URL"""
        if not self.whatsapp_number:
            return None
        
        # Clean phone number (remove spaces, dashes, etc.)
        phone = self.whatsapp_number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        # Build message
        inquiry_subject = subject or property_title
        if inquiry_subject:
            msg = f"Hello! I'd like to inquire about: {inquiry_subject}. {message or self.whatsapp_default_message}"
        else:
            msg = message or self.whatsapp_default_message
        
        # URL encode message
        from urllib.parse import quote
        encoded_msg = quote(msg)
        
        return f"https://wa.me/{phone}?text={encoded_msg}"


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


class PromotionalOffer(models.Model):
    """Model for promotional offers displayed in floating carousel"""
    BADGE_TYPE_CHOICES = [
        ('hot_deal', _('Hot Deal')),
        ('new', _('New')),
        ('limited', _('Limited')),
        ('sale', _('Sale')),
    ]
    
    ICON_CHOICES = [
        ('target', _('Target')),
        ('money', _('Money')),
        ('gift', _('Gift')),
        ('star', _('Star')),
        ('tag', _('Tag')),
    ]
    
    ICON_COLOR_CHOICES = [
        ('primary', _('Primary')),
        ('success', _('Success')),
        ('danger', _('Danger')),
        ('warning', _('Warning')),
        ('info', _('Info')),
    ]
    
    BADGE_COLOR_CHOICES = [
        ('primary', _('Primary')),
        ('success', _('Success')),
        ('danger', _('Danger')),
        ('warning', _('Warning')),
        ('info', _('Info')),
    ]
    
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    icon = models.CharField(
        max_length=20,
        choices=ICON_CHOICES,
        default='star',
        verbose_name=_('Icon')
    )
    icon_color = models.CharField(
        max_length=20,
        choices=ICON_COLOR_CHOICES,
        default='primary',
        verbose_name=_('Icon Color')
    )
    badge_type = models.CharField(
        max_length=20,
        choices=BADGE_TYPE_CHOICES,
        default='new',
        verbose_name=_('Badge Type')
    )
    badge_color = models.CharField(
        max_length=20,
        choices=BADGE_COLOR_CHOICES,
        default='danger',
        verbose_name=_('Badge Color')
    )
    
    # Actions
    call_action_text = models.CharField(
        max_length=100,
        blank=True,
        help_text=_('Text for call action button (e.g., "Call Now")'),
        verbose_name=_('Call Action Text')
    )
    call_action_url = models.CharField(
        max_length=200,
        blank=True,
        help_text=_('Phone number or URL for call action (e.g., "tel:+251912345678" or URL)'),
        verbose_name=_('Call Action URL')
    )
    details_action_text = models.CharField(
        max_length=100,
        blank=True,
        help_text=_('Text for details action button (e.g., "View Details")'),
        verbose_name=_('Details Action Text')
    )
    details_action_url = models.URLField(
        blank=True,
        null=True,
        help_text=_('URL for details action (e.g., property detail page)'),
        verbose_name=_('Details Action URL')
    )
    
    # Scheduling
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    order = models.IntegerField(
        default=0,
        help_text=_('Display order (lower numbers appear first)'),
        verbose_name=_('Order')
    )
    start_date = models.DateField(
        blank=True,
        null=True,
        help_text=_('Start date for the offer (leave blank for immediate start)'),
        verbose_name=_('Start Date')
    )
    end_date = models.DateField(
        blank=True,
        null=True,
        help_text=_('End date for the offer (leave blank for no expiration)'),
        verbose_name=_('End Date')
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = _('Promotional Offer')
        verbose_name_plural = _('Promotional Offers')
    
    def __str__(self):
        return self.title
    
    def is_valid(self):
        """Check if offer is currently valid based on dates"""
        from django.utils import timezone
        today = timezone.localdate()
        
        if not self.is_active:
            return False
        
        if self.start_date and self.start_date > today:
            return False
        
        if self.end_date and self.end_date < today:
            return False
        
        return True
    
    def get_call_url(self):
        """Get the call URL, adding tel: prefix if it's a phone number"""
        if not self.call_action_url:
            return None
        
        # If it starts with tel: or http:// or https://, return as is
        if self.call_action_url.startswith(('tel:', 'http://', 'https://')):
            return self.call_action_url
        
        # If it looks like a phone number, add tel: prefix
        if self.call_action_url.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            return f"tel:{self.call_action_url}"
        
        # Otherwise, assume it's a URL and add https://
        return f"https://{self.call_action_url}"


class AboutPageSettings(models.Model):
    """Singleton model for about page video settings"""
    # Video Settings
    about_video_enabled = models.BooleanField(
        default=True,
        help_text=_('Enable/disable video on about page'),
        verbose_name=_('Video Enabled')
    )
    about_video = models.FileField(
        upload_to='videos/about/',
        blank=True,
        null=True,
        help_text=_('Video file for about page (MP4 recommended)'),
        verbose_name=_('About Video')
    )
    about_video_url = models.URLField(
        blank=True,
        null=True,
        help_text=_('YouTube or Vimeo video URL (alternative to uploaded video)'),
        verbose_name=_('Video URL')
    )
    about_video_poster = models.ImageField(
        upload_to='images/about/',
        blank=True,
        null=True,
        help_text=_('Poster image shown before video loads'),
        verbose_name=_('Video Poster Image')
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
        # Prevent deletion
        pass
    
    @classmethod
    def load(cls):
        """Get or create the singleton instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Service(models.Model):
    CATEGORY_CHOICES = [
        ('management_consultancy', _('Management Consultancy')),
        ('strategic_leadership', _('Strategic Leadership')),
        ('hr_sourcing', _('HR Sourcing')),
        ('investment', _('Investment')),
        ('organizational_development', _('Organizational Development')),
    ]

    title = models.CharField(max_length=200, verbose_name=_('Title'))
    slug = models.SlugField(unique=True, verbose_name=_('Slug'))
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name=_('Category'))
    short_description = models.TextField(max_length=500, verbose_name=_('Short Description'))
    full_description = models.TextField(verbose_name=_('Full Description'))
    icon = models.CharField(
        max_length=50,
        default='bi-briefcase',
        help_text=_('Bootstrap icon class (e.g., bi-briefcase)'),
        verbose_name=_('Icon')
    )
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name=_('Image'))
    is_featured = models.BooleanField(default=False, verbose_name=_('Featured'))
    order = models.IntegerField(default=0, verbose_name=_('Display Order'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('site:service_detail', kwargs={'slug': self.slug})


class TrainingEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ('training', _('Training Program')),
        ('workshop', _('Workshop')),
        ('seminar', _('Seminar')),
        ('conference', _('Conference')),
        ('consultancy', _('Consultancy Session')),
    ]

    title = models.CharField(max_length=200, verbose_name=_('Title'))
    slug = models.SlugField(unique=True, verbose_name=_('Slug'))
    event_type = models.CharField(max_length=30, choices=EVENT_TYPE_CHOICES, default='training')
    description = models.TextField(verbose_name=_('Description'))
    short_description = models.TextField(max_length=500, blank=True, verbose_name=_('Short Description'))
    start_date = models.DateTimeField(verbose_name=_('Start Date'))
    end_date = models.DateTimeField(verbose_name=_('End Date'))
    location = models.CharField(max_length=200, verbose_name=_('Location'))
    venue = models.CharField(max_length=200, blank=True, verbose_name=_('Venue'))
    max_participants = models.IntegerField(default=50, verbose_name=_('Max Participants'))
    registration_deadline = models.DateTimeField(blank=True, null=True, verbose_name=_('Registration Deadline'))
    brochure = models.FileField(
        upload_to='brochures/',
        blank=True,
        null=True,
        help_text=_('Downloadable brochure (PDF)'),
        verbose_name=_('Brochure')
    )
    featured_image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name=_('Featured Image'))
    is_published = models.BooleanField(default=True, verbose_name=_('Published'))
    is_featured = models.BooleanField(default=False, verbose_name=_('Featured'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_date']
        verbose_name = _('Training Event')
        verbose_name_plural = _('Training Events')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('site:event_detail', kwargs={'slug': self.slug})

    @property
    def is_registration_open(self):
        from django.utils import timezone
        now = timezone.now()
        if self.registration_deadline and now > self.registration_deadline:
            return False
        if now > self.start_date:
            return False
        return self.registered_count < self.max_participants

    @property
    def registered_count(self):
        return self.registrations.filter(status='confirmed').count()

    @property
    def spots_remaining(self):
        return max(0, self.max_participants - self.registered_count)


class EventRegistration(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('cancelled', _('Cancelled')),
    ]

    event = models.ForeignKey(TrainingEvent, on_delete=models.CASCADE, related_name='registrations')
    full_name = models.CharField(max_length=200, verbose_name=_('Full Name'))
    email = models.EmailField(verbose_name=_('Email'))
    phone = models.CharField(max_length=30, verbose_name=_('Phone'))
    organization = models.CharField(max_length=200, blank=True, verbose_name=_('Organization'))
    job_title = models.CharField(max_length=200, blank=True, verbose_name=_('Job Title'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Event Registration')
        verbose_name_plural = _('Event Registrations')

    def __str__(self):
        return f"{self.full_name} - {self.event.title}"


class CaseStudy(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    slug = models.SlugField(unique=True, verbose_name=_('Slug'))
    client_name = models.CharField(max_length=200, verbose_name=_('Client Name'))
    industry = models.CharField(max_length=100, blank=True, verbose_name=_('Industry'))
    challenge = models.TextField(verbose_name=_('Challenge'))
    solution = models.TextField(verbose_name=_('Solution'))
    results = models.TextField(verbose_name=_('Results'))
    excerpt = models.TextField(max_length=500, blank=True, verbose_name=_('Excerpt'))
    featured_image = models.ImageField(upload_to='case_studies/', blank=True, null=True, verbose_name=_('Featured Image'))
    project_start = models.DateField(blank=True, null=True, verbose_name=_('Project Start'))
    project_end = models.DateField(blank=True, null=True, verbose_name=_('Project End'))
    is_featured = models.BooleanField(default=False, verbose_name=_('Featured'))
    is_published = models.BooleanField(default=True, verbose_name=_('Published'))
    order = models.IntegerField(default=0, verbose_name=_('Display Order'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = _('Case Study')
        verbose_name_plural = _('Case Studies')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('site:case_study_detail', kwargs={'slug': self.slug})


class CaseStudyTimeline(models.Model):
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE, related_name='timeline')
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    date = models.DateField(verbose_name=_('Date'))
    order = models.IntegerField(default=0, verbose_name=_('Order'))

    class Meta:
        ordering = ['order', 'date']
        verbose_name = _('Case Study Timeline')
        verbose_name_plural = _('Case Study Timelines')

    def __str__(self):
        return f"{self.case_study.title} - {self.title}"


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100, verbose_name=_('Client Name'))
    organization = models.CharField(max_length=200, blank=True, verbose_name=_('Organization'))
    position = models.CharField(max_length=100, blank=True, verbose_name=_('Position'))
    content = models.TextField(verbose_name=_('Testimonial'))
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True, verbose_name=_('Photo'))
    rating = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('Rating')
    )
    is_featured = models.BooleanField(default=False, verbose_name=_('Featured'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    order = models.IntegerField(default=0, verbose_name=_('Display Order'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = _('Testimonial')
        verbose_name_plural = _('Testimonials')

    def __str__(self):
        return f"{self.client_name} - {self.organization}"


class Partner(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    logo = models.ImageField(upload_to='partners/', blank=True, null=True, verbose_name=_('Logo'))
    website = models.URLField(blank=True, verbose_name=_('Website'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    order = models.IntegerField(default=0, verbose_name=_('Display Order'))

    class Meta:
        ordering = ['order', 'name']
        verbose_name = _('Partner')
        verbose_name_plural = _('Partners')

    def __str__(self):
        return self.name


class Milestone(models.Model):
    year = models.CharField(max_length=20, verbose_name=_('Year'))
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    order = models.IntegerField(default=0, verbose_name=_('Display Order'))

    class Meta:
        ordering = ['order', 'year']
        verbose_name = _('Milestone')
        verbose_name_plural = _('Milestones')

    def __str__(self):
        return f"{self.year} - {self.title}"


class MediaAlbum(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    slug = models.SlugField(unique=True, verbose_name=_('Slug'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    cover_image = models.ImageField(upload_to='gallery/covers/', blank=True, null=True, verbose_name=_('Cover Image'))
    category = models.CharField(max_length=100, blank=True, verbose_name=_('Category'))
    is_published = models.BooleanField(default=True, verbose_name=_('Published'))
    order = models.IntegerField(default=0, verbose_name=_('Display Order'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = _('Media Album')
        verbose_name_plural = _('Media Albums')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('site:gallery_detail', kwargs={'slug': self.slug})


class MediaItem(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', _('Image')),
        ('video', _('Video')),
    ]

    album = models.ForeignKey(MediaAlbum, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200, blank=True, verbose_name=_('Title'))
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    image = models.ImageField(
        upload_to='gallery/images/',
        blank=True,
        null=True,
        verbose_name=_('Image'),
        help_text=_('Recommended: 1200×800px or larger, JPG/PNG/WebP'),
    )
    video_file = models.FileField(
        upload_to='gallery/videos/',
        blank=True,
        null=True,
        verbose_name=_('Video File'),
        help_text=_('MP4 or WebM video upload'),
    )
    video_url = models.URLField(
        blank=True,
        verbose_name=_('Video URL'),
        help_text=_('YouTube or Vimeo link (alternative to uploaded video)'),
    )
    caption = models.CharField(max_length=300, blank=True, verbose_name=_('Caption'))
    order = models.IntegerField(default=0, verbose_name=_('Order'))

    class Meta:
        ordering = ['order']
        verbose_name = _('Media Item')
        verbose_name_plural = _('Media Items')

    def __str__(self):
        return self.title or f"Media in {self.album.title}"

    def save(self, *args, **kwargs):
        sync_media_type(self)
        super().save(*args, **kwargs)

    def get_embed_video_url(self):
        return embed_video_url(self.video_url)


class ServiceMedia(models.Model):
    MEDIA_TYPE_CHOICES = MediaItem.MEDIA_TYPE_CHOICES

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='media_items')
    title = models.CharField(max_length=200, blank=True, verbose_name=_('Title'))
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    image = models.ImageField(upload_to='services/gallery/', blank=True, null=True, verbose_name=_('Image'))
    video_file = models.FileField(upload_to='services/videos/', blank=True, null=True, verbose_name=_('Video File'))
    video_url = models.URLField(blank=True, verbose_name=_('Video URL'))
    caption = models.CharField(max_length=300, blank=True, verbose_name=_('Caption'))
    order = models.IntegerField(default=0, verbose_name=_('Order'))

    class Meta:
        ordering = ['order']
        verbose_name = _('Service Media')
        verbose_name_plural = _('Service Media')

    def __str__(self):
        return self.title or f'{self.service.title} media'

    def save(self, *args, **kwargs):
        sync_media_type(self)
        super().save(*args, **kwargs)

    def get_embed_video_url(self):
        return embed_video_url(self.video_url)


class CaseStudyMedia(models.Model):
    MEDIA_TYPE_CHOICES = MediaItem.MEDIA_TYPE_CHOICES

    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE, related_name='media_items')
    title = models.CharField(max_length=200, blank=True, verbose_name=_('Title'))
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    image = models.ImageField(upload_to='case_studies/gallery/', blank=True, null=True, verbose_name=_('Image'))
    video_file = models.FileField(upload_to='case_studies/videos/', blank=True, null=True, verbose_name=_('Video File'))
    video_url = models.URLField(blank=True, verbose_name=_('Video URL'))
    caption = models.CharField(max_length=300, blank=True, verbose_name=_('Caption'))
    order = models.IntegerField(default=0, verbose_name=_('Order'))

    class Meta:
        ordering = ['order']
        verbose_name = _('Case Study Media')
        verbose_name_plural = _('Case Study Media')

    def __str__(self):
        return self.title or f'{self.case_study.title} media'

    def save(self, *args, **kwargs):
        sync_media_type(self)
        super().save(*args, **kwargs)

    def get_embed_video_url(self):
        return embed_video_url(self.video_url)


class EventMedia(models.Model):
    MEDIA_TYPE_CHOICES = MediaItem.MEDIA_TYPE_CHOICES

    event = models.ForeignKey(TrainingEvent, on_delete=models.CASCADE, related_name='media_items')
    title = models.CharField(max_length=200, blank=True, verbose_name=_('Title'))
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    image = models.ImageField(upload_to='events/gallery/', blank=True, null=True, verbose_name=_('Image'))
    video_file = models.FileField(upload_to='events/videos/', blank=True, null=True, verbose_name=_('Video File'))
    video_url = models.URLField(blank=True, verbose_name=_('Video URL'))
    caption = models.CharField(max_length=300, blank=True, verbose_name=_('Caption'))
    order = models.IntegerField(default=0, verbose_name=_('Order'))

    class Meta:
        ordering = ['order']
        verbose_name = _('Event Media')
        verbose_name_plural = _('Event Media')

    def __str__(self):
        return self.title or f'{self.event.title} media'

    def save(self, *args, **kwargs):
        sync_media_type(self)
        super().save(*args, **kwargs)

    def get_embed_video_url(self):
        return embed_video_url(self.video_url)


class WorkingSchedule(models.Model):
    DAY_CHOICES = [
        (0, _('Monday')),
        (1, _('Tuesday')),
        (2, _('Wednesday')),
        (3, _('Thursday')),
        (4, _('Friday')),
        (5, _('Saturday')),
        (6, _('Sunday')),
    ]

    day_of_week = models.IntegerField(choices=DAY_CHOICES, unique=True, verbose_name=_('Day'))
    open_time = models.TimeField(blank=True, null=True, verbose_name=_('Open Time'))
    close_time = models.TimeField(blank=True, null=True, verbose_name=_('Close Time'))
    is_closed = models.BooleanField(default=False, verbose_name=_('Closed'))

    class Meta:
        ordering = ['day_of_week']
        verbose_name = _('Working Schedule')
        verbose_name_plural = _('Working Schedules')

    def __str__(self):
        if self.is_closed:
            return f"{self.get_day_of_week_display()} - Closed"
        return f"{self.get_day_of_week_display()} {self.open_time}-{self.close_time}"
