import os

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from google.oauth2 import id_token
from google.auth.transport import requests
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from TrainerAppIvan_BackEnd2.account.models import AppUser


class AccountDetailView(TemplateView):
    template_name = 'account/account-details.html'


class AccountLoginView(TemplateView):
    template_name = 'account/login.html'


class GoogleView(TemplateView):
    template_name = 'account/google_sign_in.html'

@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    print('Inside')
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )

        # Extract user info
        user_email = user_data.get("email")

        print(f"User Email: {user_email}")

        user = AppUser.objects.filter(email=user_email).first()

        if not user:
            # Create a new user if not found
            user = AppUser.objects.create_user(email=user_email, password=None)
            user.save()
            print(f"Created new user: {user_email}")
        else:
            print(f"Existing user: {user_email}")

    except ValueError:
        return HttpResponse(status=403)

    user = authenticate(request, email=user_email, password=None)
    if user is not None:
        login(request, user)
        print(f"Logged in user: {user_email}")
    else:
        print("Authentication failed")

    # In a real app, I'd also save any new user here to the database.
    # You could also authenticate the user here using the details from Google (https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in)
    request.session['user_data'] = user_data

    return redirect('home')

def sign_out(request):
    del request.session['user_data']
    return redirect('home')


class AccountRegisterView(TemplateView):
    template_name = 'account/register.html'

