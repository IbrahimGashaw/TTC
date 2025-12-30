// Soft UI Dashboard Django - Main JavaScript for Andromeda Properties

// Prevent loading of corrupted or non-existent video files
document.addEventListener('DOMContentLoaded', function() {
    // Fix for header-video.webm errors - remove any cached references
    const videos = document.querySelectorAll('video');
    videos.forEach(function(video) {
        // Remove any webm sources that might cause errors
        const sources = video.querySelectorAll('source[src*="header-video.webm"], source[src*=".webm"]');
        sources.forEach(function(source) {
            source.remove();
        });
        
        // Add error handler to hide video if it fails to load
        video.addEventListener('error', function(e) {
            console.log('Video load error:', e);
            // If all sources fail, hide the video and show poster image
            if (video.readyState === 4 && video.error) {
                video.style.display = 'none';
                const poster = video.getAttribute('poster');
                if (poster && video.parentElement) {
                    const img = document.createElement('img');
                    img.src = poster;
                    img.style.width = '100%';
                    img.style.height = '100%';
                    img.style.objectFit = 'cover';
                    img.style.position = 'absolute';
                    img.style.top = '0';
                    img.style.left = '0';
                    img.style.zIndex = '-1';
                    video.parentElement.appendChild(img);
                }
            }
        }, true);
    });
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Form validation
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Soft UI Dashboard - Animate cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.property-card, .project-card, .blog-card, .team-card, .card').forEach(card => {
        observer.observe(card);
    });

    // EstateAgency - Navbar scroll effect
    const navbar = document.querySelector('.navbar-estateagency');
    if (navbar) {
        window.addEventListener('scroll', function() {
            const currentScroll = window.pageYOffset;
            if (currentScroll > 10) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // Search form enhancement
    const searchForm = document.querySelector('.search-section form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Searching...';
                submitBtn.disabled = true;
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 2000);
            }
        });
    }

    // Property inquiry form enhancement
    const inquiryForm = document.querySelector('form[method="post"]');
    if (inquiryForm && inquiryForm.querySelector('input[name="phone"]')) {
        inquiryForm.addEventListener('submit', function(e) {
            const phoneInput = this.querySelector('input[name="phone"]');
            if (phoneInput && phoneInput.value) {
                const phoneRegex = /^[\d\s\-\+\(\)]+$/;
                if (!phoneRegex.test(phoneInput.value)) {
                    e.preventDefault();
                    alert('Please enter a valid phone number');
                    phoneInput.focus();
                    return false;
                }
            }
        });
    }

    // Back to top button - Soft UI Dashboard Style
    const backToTopBtn = document.createElement('button');
    backToTopBtn.innerHTML = '<i class="bi bi-arrow-up"></i>';
    backToTopBtn.className = 'btn btn-primary rounded-circle position-fixed';
    backToTopBtn.style.display = 'none';
    backToTopBtn.style.zIndex = '1000';
    backToTopBtn.style.width = '50px';
    backToTopBtn.style.height = '50px';
    backToTopBtn.style.bottom = '2rem';
    backToTopBtn.style.right = '2rem';
    backToTopBtn.style.boxShadow = '0 8px 15px rgba(94, 114, 228, 0.4)';
    backToTopBtn.setAttribute('aria-label', 'Back to top');
    document.body.appendChild(backToTopBtn);

    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.style.display = 'flex';
            backToTopBtn.style.alignItems = 'center';
            backToTopBtn.style.justifyContent = 'center';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });

    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Language switcher - let custom view handle redirect logic
    const languageForm = document.getElementById('language-form');
    const languageSelect = document.getElementById('language-select');
    
    if (languageForm && languageSelect) {
        // Update redirect path before form submission
        function updateRedirectPath() {
            const nextInput = document.getElementById('language-next');
            if (nextInput) {
                // Get current full path with query string
                const currentPath = window.location.pathname;
                const queryString = window.location.search;
                const fullPath = currentPath + queryString;
                const selectedLang = languageSelect.value;
                
                // Set the next parameter - custom view will handle prefix stripping/adding
                nextInput.value = fullPath;
                
                console.log('Language switch:', {
                    currentPath: currentPath,
                    selectedLang: selectedLang,
                    redirectPath: fullPath
                });
                
                return true;
            }
            return false;
        }
        
        // Handle language change - update path before submit
        languageSelect.addEventListener('change', function(e) {
            if (updateRedirectPath()) {
                console.log('Submitting language form...');
                // Form will submit via onchange attribute
            }
        });
        
        // Also handle form submission to ensure path is set
        languageForm.addEventListener('submit', function(e) {
            updateRedirectPath();
        });
        
        // Initialize on page load
        updateRedirectPath();
    }
    
    // Google Language Detection and Auto-Translation Support
    (function() {
        // Detect browser language
        const browserLang = navigator.language || navigator.userLanguage;
        const langCode = browserLang.split('-')[0].toLowerCase();
        
        // Check if Google Translate is already active
        const checkGoogleTranslate = function() {
            if (window.google && window.google.translate) {
                // Google Translate is available
                console.log('Google Translate detected');
            }
        };
        
        // Initialize Google Translate widget (optional - can be enabled if needed)
        // Uncomment to enable Google Translate widget
        /*
        window.googleTranslateElementInit = function() {
            new google.translate.TranslateElement({
                pageLanguage: 'en',
                includedLanguages: 'en,am,ar,fr',
                layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
                autoDisplay: false
            }, 'google_translate_element');
        };
        */
        
        // Auto-detect language on first visit (if not already set)
        const storedLang = localStorage.getItem('preferred_language');
        const sessionLang = document.documentElement.lang || 'en';
        
        if (!storedLang && langCode && langCode !== sessionLang) {
            // Browser language differs from current page language
            // The middleware will handle redirect on server side
            console.log('Browser language detected:', langCode, 'Current:', sessionLang);
        }
        
        // Store user's language preference
        if (languageSelect) {
            languageSelect.addEventListener('change', function() {
                localStorage.setItem('preferred_language', this.value);
            });
        }
        
        // Restore user's language preference on next visit (if middleware doesn't redirect)
        if (storedLang && storedLang !== sessionLang) {
            console.log('Restoring preferred language:', storedLang);
        }
    })();

    // Promotional Offers Carousel Slider
    const offersContainer = document.getElementById('offersSliderContainer');
    const offersToggleBtn = document.getElementById('offersToggleBtn');
    const offersCarouselCard = document.getElementById('offersCarouselCard');
    const offersCloseBtn = document.getElementById('offersCloseBtn');
    const offersBackdrop = document.getElementById('offersBackdrop');
    const offersCarousel = document.getElementById('offersCarousel');
    const offerItems = document.querySelectorAll('.offer-item');
    const offerIndicators = document.querySelectorAll('.offers-indicator');
    const offersActionBtns = document.querySelectorAll('.offers-action-btn');
    
    let currentSlide = 0;
    let slideInterval = null;
    const SLIDE_DURATION = 5000; // 5 seconds per slide
    
    // Function to open carousel
    function openCarousel() {
        if (offersCarouselCard) {
            offersCarouselCard.classList.add('show');
            if (offersToggleBtn) {
                offersToggleBtn.classList.add('hidden');
            }
            startCarousel();
            updateActionButtons(currentSlide);
        }
    }
    
    // Function to close carousel
    function closeCarousel() {
        if (offersCarouselCard) {
            offersCarouselCard.classList.remove('show');
            if (offersToggleBtn) {
                offersToggleBtn.classList.remove('hidden');
            }
            stopCarousel();
        }
    }
    
    // Toggle offers carousel
    if (offersToggleBtn && offersCarouselCard) {
        offersToggleBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            openCarousel();
        });
        
        // Close button
        if (offersCloseBtn) {
            offersCloseBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                closeCarousel();
            });
        }
    }
    
    // Carousel functionality
    function showSlide(index) {
        if (offerItems.length === 0) return;
        
        // Reset all slides
        offerItems.forEach(item => item.classList.remove('active'));
        offerIndicators.forEach(indicator => indicator.classList.remove('active'));
        
        // Show current slide
        currentSlide = index % offerItems.length;
        if (offerItems[currentSlide]) {
            offerItems[currentSlide].classList.add('active');
        }
        if (offerIndicators[currentSlide]) {
            offerIndicators[currentSlide].classList.add('active');
        }
        
        // Update action buttons
        updateActionButtons(currentSlide);
    }
    
    function nextSlide() {
        showSlide(currentSlide + 1);
    }
    
    function startCarousel() {
        stopCarousel(); // Clear any existing interval
        if (offerItems.length > 1) {
            slideInterval = setInterval(nextSlide, SLIDE_DURATION);
        }
    }
    
    function stopCarousel() {
        if (slideInterval) {
            clearInterval(slideInterval);
            slideInterval = null;
        }
    }
    
    // Indicator clicks
    offerIndicators.forEach((indicator, index) => {
        indicator.addEventListener('click', function() {
            stopCarousel();
            showSlide(index);
            startCarousel();
        });
    });
    
    // Update action buttons based on current slide
    function updateActionButtons(slideIndex) {
        const offersActions = document.getElementById('offersActions');
        if (!offersActions) return;
        
        // Hide all action button groups
        const actionGroups = offersActions.querySelectorAll('.offer-actions-content');
        actionGroups.forEach(group => group.classList.add('d-none'));
        
        // Show current slide's action buttons
        const currentActionGroup = offersActions.querySelector(`[data-offer-index="${slideIndex}"]`);
        if (currentActionGroup) {
            currentActionGroup.classList.remove('d-none');
        }
    }
    
    // Initialize carousel if offers are available
    if (offerItems.length > 0) {
        showSlide(0);
        // Auto-start carousel after a delay
        setTimeout(function() {
            if (offersCarouselCard && offersCarouselCard.classList.contains('show')) {
                startCarousel();
            }
        }, 1000);
    }
    
    // Pause carousel on hover
    if (offersCarouselCard) {
        offersCarouselCard.addEventListener('mouseenter', function() {
            stopCarousel();
        });
        
        offersCarouselCard.addEventListener('mouseleave', function() {
            if (offersCarouselCard.classList.contains('show')) {
                startCarousel();
            }
        });
    }
});
