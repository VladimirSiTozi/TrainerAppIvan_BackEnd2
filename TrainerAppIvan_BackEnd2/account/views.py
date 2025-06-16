import os

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from google.oauth2 import id_token
from google.auth.transport import requests
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView

from TrainerAppIvan_BackEnd2 import settings
from TrainerAppIvan_BackEnd2.account.forms import AppUserCreationForm, ProfileForm
from TrainerAppIvan_BackEnd2.account.models import AppUser, Profile
from TrainerAppIvan_BackEnd2.mixins import StaffRequiredMixin
from TrainerAppIvan_BackEnd2.program.models import WorkoutPlan, ExerciseTemplate

UserModel = get_user_model()


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'account/profile-details.html'
    context_object_name = 'profile'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def dispatch(self, request, *args, **kwargs):
        # Call get_object early to access the profile
        profile = self.get_object()

        # Check if the current user is the profile owner or a staff member
        if profile.user != request.user and not request.user.is_staff:
            raise PermissionDenied("You are not allowed to view this profile.")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = self.get_object()
        current_user = profile.user
        context['current_user'] = current_user

        workout_plans = WorkoutPlan.objects.filter(user=self.request.user).all()
        context['workout_plans'] = workout_plans
        return context


class AccountNutritionView(TemplateView):
    template_name = 'programs/training-plan.html'


class AccountLoginView(LoginView):
    template_name = 'account/login.html'


class GoogleView(TemplateView):
    template_name = 'account/google_sign_in.html'


# Google Login and Registration
@csrf_exempt
def auth_receiver(request):
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )

        # Extract user info from request
        user_email = user_data.get("email")
        user_created = False

        # Check for existing user
        user = AppUser.objects.filter(email=user_email).first()

        # Create a new user if not found
        if not user:
            user = AppUser.objects.create_user(email=user_email, password=None)
            user.save()
            user_created = True

    except ValueError:
        return HttpResponse(status=403)

    # Send email to the admin about new user registration
    if user_created:
        admin_subject = f"New user registered: {user_email}"
        admin_body = f"""
        A new user has registered through the Google Authentication in your application:

        Email: {user_email}
        Registration Time: {timezone.now()} UTC
        
        Registration Method: Google Authentication
        """

        admin_email = EmailMultiAlternatives(
            subject=admin_subject,
            body=admin_body,
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],
        )
        admin_email.send()

        # Send welcome email to the new user
        user_subject = "Welcome to Our App!"
        user_body = f"""
            Hi there,
            
            Thank you for registering with our application! We're excited to have you on board.
            
            Get started by completing your profile to unlock all features.
            
            If you have any questions, please don't hesitate to contact us.
            
            Best regards,
            The Team
            """

        user_email = EmailMultiAlternatives(
            subject=user_subject,
            body=user_body,
            from_email=settings.EMAIL_HOST_USER,
            to=[user_email],
        )
        user_email.send()

    if user is not None:
        login(request, user)

    return redirect('complete-profile')


@require_POST
def sign_out(request):
    logout(request)
    return redirect('home')


# Custom User Registration
class AccountRegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('complete-profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)

        # Send admin notification email
        admin_subject = f"New user registered: {user.email}"
        admin_body = f"""
                A new user has registered through the Custom Registration Form in your application:

                Email: {user.email}
                Registration Time: {timezone.now()} UTC

                Registration Method: Custom Form
                """

        admin_email = EmailMultiAlternatives(
            subject=admin_subject,
            body=admin_body,
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],
        )
        admin_email.send()

        # Optional: Send welcome email to the user
        user_subject = "Welcome to Our Platform!"
        user_body = f"""
                Hi there,

                Thank you for registering with us through our website!

                Please complete your profile to get started.

                Best regards,
                The Team
                """

        user_email = EmailMultiAlternatives(
            subject=user_subject,
            body=user_body,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email],
        )
        user_email.send()

        return response


@login_required
def complete_profile(request):
    profile = request.user.profile

    if profile.is_profile_complete:
        return redirect('home')

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()

            # Send email to admin
            admin_subject = f"Profile completed: {request.user.email}"
            admin_body = f"""
            User: {request.user.profile.first_name} {request.user.profile.last_name} 
            Email: {request.user.email} 
            has completed their profile:

            Completion Time: {timezone.now()}

            You can view the profile in admin panel.
            """

            admin_email = EmailMultiAlternatives(
                subject=admin_subject,
                body=admin_body,
                from_email=settings.EMAIL_HOST_USER,
                to=[settings.EMAIL_HOST_USER],
            )
            admin_email.send()

            # Send confirmation email to user
            user_subject = "Your profile in IvanTheBear is now complete!"
            user_body = f"""
            Dear {request.user.email},

            Thank you for completing your profile on our platform. 

            You now have full access to all features.

            If you have any questions, please contact our support team.

            Best regards,
            The Team
            """

            user_email = EmailMultiAlternatives(
                subject=user_subject,
                body=user_body,
                from_email=settings.EMAIL_HOST_USER,
                to=[request.user.email],
            )
            user_email.send()

            return redirect('home')

    else:
        form = ProfileForm(instance=profile)

        return render(request, 'account/profile-completion-form.html', {'form': form})


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'account/profile-completion-form.html'

    def get_object(self, queryset=None):
        # If user is staff, allow editing any profile by slug
        if self.request.user.is_staff:
            return get_object_or_404(Profile, slug=self.kwargs['slug'])
        # Otherwise, only allow editing their own profile
        return self.request.user.profile

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect('account-detail', slug=self.request.user.profile.slug)


@staff_member_required
def staff_user_search(request):
    query = request.GET.get('q', '')
    user_results = []
    profile_results = []

    if query:
        user_results = AppUser.objects.filter(
            Q(email__icontains=query)
        )

        profile_results = Profile.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    context = {
        'user_results': user_results,
        'profile_results': profile_results,
        'query': query
    }

    return render(request, 'account/users-search.html', context)


class AdminHubView(StaffRequiredMixin, TemplateView):
    template_name = 'account/admin-hub.html'


class UsersListView(StaffRequiredMixin, ListView):
    model = AppUser
    template_name = 'account/users-list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return AppUser.objects.all().order_by('email')

