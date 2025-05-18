import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from google.oauth2 import id_token
from google.auth.transport import requests
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, DetailView

from TrainerAppIvan_BackEnd2.account.forms import AppUserCreationForm, ProfileForm
from TrainerAppIvan_BackEnd2.account.models import AppUser, Profile
from TrainerAppIvan_BackEnd2.program.models import WorkoutPlan

UserModel = get_user_model()


class AccountDetailView(DetailView):
    model = Profile
    template_name = 'account/account-profile.html'
    context_object_name = 'profile'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

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


@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )

        # Extract user info
        user_email = user_data.get("email")

        user = AppUser.objects.filter(email=user_email).first()

        if not user:
            # Create a new user if not found
            user = AppUser.objects.create_user(email=user_email, password=None)
            user.save()
            print('created new user')
        else:
            print(f"Existing user: {user_email}")

    except ValueError:
        return HttpResponse(status=403)

    # Authenticate and log in the user (not working for google oauth, only if user is created manually(TOD0:))

    # user = authenticate(request, email=user_email, password=None)

    if user is not None:
        login(request, user)
        print('logged in')
    else:
        print("Authentication failed")

    # Redirect to the home page
    return redirect('home')


@require_POST
def sign_out(request):
    logout(request)
    return redirect('home')


class AccountRegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)

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
            return redirect('home')

    else:
        form = ProfileForm(instance=profile)

        return render(request, 'account/profile-completion-form.html', {'form': form})
