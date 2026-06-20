# Andromeda Properties - Feature Implementation Plan

## Overview
This document outlines the implementation plan for enhancing the Andromeda Properties website with lead generation, trust-building, advanced search, rich media, SEO, and performance features.

---

## 1. Lead Generation Focus (30% Lead Volume Increase)

### 1.1 "Book a Viewing" Feature Enhancement
**Status:** Partial (PropertyBooking model exists, needs enhancement)

**Tasks:**
- [ ] Enhance PropertyBooking model to support "viewing appointments" (separate from bookings)
- [ ] Add "Book a Viewing" button prominently on property cards and detail pages
- [ ] Create quick booking form modal for instant lead capture
- [ ] Add calendar integration for available viewing slots
- [ ] Email notifications to agents when viewing is booked
- [ ] SMS/WhatsApp confirmation to customers

**Files to Modify:**
- `properties/models.py` - Add ViewingAppointment model
- `properties/forms.py` - Add ViewingAppointmentForm
- `properties/views.py` - Add book_viewing view
- `templates/properties/property_detail.html` - Add "Book a Viewing" button
- `templates/properties/property_list.html` - Add "Book a Viewing" on cards

### 1.2 WhatsApp Integration
**Status:** Not Started

**Tasks:**
- [ ] Add WhatsApp Business API integration or click-to-chat links
- [ ] Add WhatsApp button on property detail pages
- [ ] Pre-fill WhatsApp message with property details
- [ ] Add WhatsApp floating button on all pages
- [ ] Configure WhatsApp number in settings/admin

**Implementation:**
- Add `whatsapp_number` field to settings
- Create WhatsApp link generator: `https://wa.me/{number}?text={message}`
- Add WhatsApp button component to templates

**Files to Create/Modify:**
- `properties/models.py` - Add SiteSettings model with WhatsApp number
- `templates/base.html` - Add floating WhatsApp button
- `templates/properties/property_detail.html` - Add WhatsApp inquiry button
- `static/js/whatsapp.js` - WhatsApp link generation

---

## 2. Trust & Authority Building

### 2.1 "Verified" Badges
**Status:** Not Started

**Tasks:**
- [ ] Add `is_verified` boolean field to Property model
- [ ] Add `is_verified` boolean field to TeamMember model
- [ ] Create verified badge component/icon
- [ ] Display verified badges on property cards and detail pages
- [ ] Display verified badges on agent profiles

**Files to Modify:**
- `properties/models.py` - Add is_verified fields
- `templates/properties/property_list.html` - Show verified badge
- `templates/properties/property_detail.html` - Show verified badge
- `templates/properties/team.html` - Show verified badge
- `static/css/style.css` - Style verified badges

### 2.2 "Last Updated" Timestamps
**Status:** Partial (updated_at exists, needs display)

**Tasks:**
- [ ] Display "Last Updated" timestamp prominently on property listings
- [ ] Show relative time (e.g., "Updated 2 days ago")
- [ ] Add "Last Updated" to property cards
- [ ] Highlight recently updated properties

**Files to Modify:**
- `templates/properties/property_list.html` - Display updated_at
- `templates/properties/property_detail.html` - Display updated_at
- `templates/properties/home.html` - Show "Recently Updated" section

### 2.3 Agent Profiles Enhancement
**Status:** Partial (TeamMember model exists)

**Tasks:**
- [ ] Enhance TeamMember model with:
  - Bio/description field
  - Specializations
  - Years of experience
  - Languages spoken
  - Social media links
  - Agent rating/reviews
- [ ] Create detailed agent profile pages
- [ ] Link agents to their listed properties
- [ ] Add agent contact form
- [ ] Display agent on property detail pages

**Files to Modify:**
- `properties/models.py` - Enhance TeamMember model
- `properties/views.py` - Add agent_detail view
- `templates/properties/team.html` - Enhance agent cards
- `templates/properties/agent_detail.html` - Create new template
- `properties/urls.py` - Add agent_detail URL

---

## 3. Advanced Search

### 3.1 Homepage Hero Search Enhancement
**Status:** Partial (basic search exists, needs price filter)

**Tasks:**
- [ ] Add price range filter (min_price, max_price) to search form
- [ ] Enhance search form with more filters:
  - Price range slider
  - Property size range
  - Number of bathrooms
  - Sale type (For Sale/For Rent)
- [ ] Add search suggestions/autocomplete
- [ ] Make search form more prominent in hero section
- [ ] Add "Advanced Search" link to expanded search page

**Files to Modify:**
- `properties/forms.py` - Add price fields to PropertySearchForm
- `templates/properties/home.html` - Enhance search form
- `properties/views.py` - Update property_list view to handle price filters
- `static/js/search.js` - Add autocomplete functionality

---

## 4. Rich Media & Maps

### 4.1 Video Walkthroughs
**Status:** Not Started

**Tasks:**
- [ ] Add `walkthrough_video` FileField to Property model
- [ ] Add video upload in admin
- [ ] Display video walkthrough on property detail page
- [ ] Add video thumbnail/preview
- [ ] Support YouTube/Vimeo embeds as alternative

**Files to Modify:**
- `properties/models.py` - Add walkthrough_video field
- `templates/properties/property_detail.html` - Add video section
- `properties/admin.py` - Add video field to admin

### 4.2 Floor Plans
**Status:** Not Started

**Tasks:**
- [ ] Create FloorPlan model (multiple floor plans per property)
- [ ] Add floor plan image upload
- [ ] Display floor plans in gallery/carousel on property detail
- [ ] Add floor plan download option
- [ ] Add interactive floor plan viewer (optional)

**Files to Create/Modify:**
- `properties/models.py` - Add FloorPlan model
- `templates/properties/property_detail.html` - Add floor plans section
- `properties/admin.py` - Add FloorPlanInline

### 4.3 Interactive Maps with Amenities
**Status:** Not Started

**Tasks:**
- [ ] Integrate Google Maps or Mapbox
- [ ] Add latitude/longitude fields to Property model
- [ ] Display property location on map
- [ ] Show nearby amenities (schools, hospitals, shops, restaurants)
- [ ] Add map view toggle on property list page
- [ ] Add "View on Map" button on property cards

**Implementation:**
- Use Google Maps JavaScript API or Mapbox GL JS
- Add Places API for nearby amenities
- Store property coordinates in database

**Files to Modify:**
- `properties/models.py` - Add latitude, longitude fields
- `templates/properties/property_detail.html` - Add map section
- `templates/properties/property_list.html` - Add map view
- `static/js/maps.js` - Map initialization and amenities
- `ttcs_site/settings.py` - Add Google Maps API key

---

## 5. SEO & Content

### 5.1 Market Reports Hub
**Status:** Not Started

**Tasks:**
- [ ] Create MarketReport model:
  - Title, slug, content
  - Publication date
  - Featured image
  - PDF download option
  - Category/tags
- [ ] Create market reports list page
- [ ] Create market report detail page
- [ ] Add SEO meta tags
- [ ] Add social sharing buttons
- [ ] Add related reports section

**Files to Create:**
- `properties/models.py` - Add MarketReport model
- `properties/views.py` - Add market_report_list, market_report_detail views
- `templates/properties/market_reports.html` - List page
- `templates/properties/market_report_detail.html` - Detail page
- `properties/urls.py` - Add market report URLs

### 5.2 Buying Guides Section
**Status:** Not Started

**Tasks:**
- [ ] Create BuyingGuide model (similar to MarketReport)
- [ ] Create buying guides list page
- [ ] Create buying guide detail page
- [ ] Add categories (First-time buyer, Investment, etc.)
- [ ] Add related properties section
- [ ] Optimize for SEO with proper headings, meta descriptions

**Files to Create:**
- `properties/models.py` - Add BuyingGuide model
- `properties/views.py` - Add buying_guide views
- `templates/properties/buying_guides.html` - List page
- `templates/properties/buying_guide_detail.html` - Detail page

---

## 6. Performance Optimization (PageSpeed 90+)

### 6.1 Mobile-First Design
**Status:** Partial (Bootstrap responsive, needs optimization)

**Tasks:**
- [ ] Audit current mobile experience
- [ ] Optimize touch targets (min 44x44px)
- [ ] Improve mobile navigation
- [ ] Optimize images for mobile (responsive images)
- [ ] Test on real devices
- [ ] Fix mobile-specific layout issues

**Files to Modify:**
- `static/css/style.css` - Mobile optimizations
- `templates/base.html` - Mobile navigation
- All templates - Responsive image tags

### 6.2 PageSpeed Optimization
**Status:** Not Started

**Tasks:**
- [ ] Image optimization:
  - Convert to WebP format
  - Add lazy loading
  - Implement responsive images (srcset)
  - Compress images
- [ ] CSS optimization:
  - Minify CSS
  - Remove unused CSS
  - Critical CSS inlining
- [ ] JavaScript optimization:
  - Minify JS
  - Defer non-critical JS
  - Remove unused JS
- [ ] Caching:
  - Browser caching headers
  - CDN setup (optional)
- [ ] Font optimization:
  - Preload fonts
  - Use font-display: swap
- [ ] Database queries:
  - Optimize queries (select_related, prefetch_related)
  - Add database indexes

**Files to Modify:**
- `ttcs_site/settings.py` - Caching, compression
- `static/css/style.css` - Optimize
- `static/js/main.js` - Optimize
- All templates - Add lazy loading, optimize images
- `properties/views.py` - Optimize queries

---

## Implementation Priority

### Phase 1 (High Priority - Lead Generation)
1. WhatsApp Integration
2. "Book a Viewing" Enhancement
3. Verified Badges
4. Last Updated Timestamps

### Phase 2 (Medium Priority - User Experience)
5. Advanced Search (Price Filter)
6. Video Walkthroughs
7. Floor Plans
8. Agent Profile Enhancement

### Phase 3 (Long-term - SEO & Growth)
9. Interactive Maps
10. Market Reports Hub
11. Buying Guides
12. Performance Optimization

---

## Technical Requirements

### External Services/APIs Needed:
- Google Maps API (for maps and amenities)
- WhatsApp Business API (optional, or use click-to-chat)
- Image optimization service (or local tools)

### Django Packages to Consider:
- `django-crispy-forms` - Better form rendering
- `django-ckeditor` - Rich text editor for content
- `django-compressor` - CSS/JS compression
- `django-imagekit` - Image processing
- `django-extensions` - Development utilities

---

## Success Metrics

- **Lead Generation:** 30% increase in inquiries/bookings
- **Trust:** Verified badges on 80%+ of properties
- **Search:** 50%+ users use advanced search
- **Media:** 60%+ properties have video/floor plans
- **SEO:** Top 10 rankings for key terms
- **Performance:** PageSpeed score 90+ on mobile and desktop

---

## Notes

- All features should be i18n compatible (support multiple languages)
- Maintain backward compatibility with existing data
- Test thoroughly before deployment
- Consider user feedback during development
- Document API endpoints if creating REST APIs

