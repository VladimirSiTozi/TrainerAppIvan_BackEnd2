from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from TrainerAppIvan_BackEnd2.account.models import Profile

UserModel = get_user_model()


class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel


class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('email',)

        widgets = {
            'email': forms.EmailInput(attrs={
                # 'class': 'form-control',
                'placeholder': 'Enter Email address'}
            ),
            'password1': forms.PasswordInput(attrs={
                # 'class': 'form-control',
                'placeholder': 'Enter Password'
            }),
            'password2': forms.PasswordInput(attrs={
                # 'class': 'form-control',
                'placeholder': 'Enter Password'
            })
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', )
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                # 'class': 'datepicker',
                'placeholder': 'Enter Date of Birth',
            }),
            'phone_number': forms.TextInput(attrs={
                # 'class': 'form-control',
                'placeholder': 'Enter Phone Number',

            })
        }
