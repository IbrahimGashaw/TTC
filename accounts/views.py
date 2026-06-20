from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('site:home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, 'Login successful!')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    # Allow GET for convenience (delegates to POST). POST is still preferred.
    http_method_names = ["get", "post", "options"]

    def get(self, request, *args, **kwargs):
        # Delegate GET to post so direct GET requests also log the user out.
        return self.post(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'You have been logged out.')
        return super().dispatch(request, *args, **kwargs)


class CustomPasswordResetView(PasswordResetView):
    """Custom password reset view that uses namespaced URLs"""
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    
    def form_valid(self, form):
        """
        Override form_valid to use namespaced URL for password_reset_confirm
        """
        from django.contrib.sites.shortcuts import get_current_site
        from django.contrib.auth.tokens import default_token_generator
        from django.contrib.auth import get_user_model
        from django.core.mail import send_mail
        from django.template.loader import render_to_string
        
        User = get_user_model()
        email = form.cleaned_data["email"]
        current_site = get_current_site(self.request)
        site_name = current_site.name
        domain = current_site.domain
        use_https = self.request.is_secure()
        protocol = 'https' if use_https else 'http'
        
        email_field_name = User.get_email_field_name()
        for user in form.get_users(email):
            user_email = getattr(user, email_field_name)
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Build the reset URL using namespaced URL name
            reset_url = reverse('accounts:password_reset_confirm', kwargs={
                'uidb64': uidb64,
                'token': token
            })
            
            context = {
                'email': user_email,
                'domain': domain,
                'site_name': site_name,
                'uid': uidb64,
                'user': user,
                'token': token,
                'protocol': protocol,
                'url': f"{protocol}://{domain}{reset_url}",
            }
            
            # Render email templates
            subject = render_to_string(self.subject_template_name, context)
            subject = ''.join(subject.splitlines())  # Remove any line breaks
            message = render_to_string(self.email_template_name, context)
            
            send_mail(
                subject,
                message,
                None,  # Use DEFAULT_FROM_EMAIL
                [user_email],
                fail_silently=False,
            )
        
        return super().form_valid(form)
    
    def get_success_url(self):
        """Override to ensure we use the namespaced URL"""
        return reverse_lazy('accounts:password_reset_done')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Custom password reset confirm view that uses namespaced URLs"""
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')
    
    def get_success_url(self):
        """Override to ensure we use the namespaced URL"""
        return reverse_lazy('accounts:password_reset_complete')

