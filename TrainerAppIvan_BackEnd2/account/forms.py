import random

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.text import slugify

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
        exclude = ('user', 'slug', 'is_profile_complete')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'placeholder': 'Enter Date of Birth',
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Enter Phone Number',
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Enter First Name',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Enter Last Name',
            }),
            'preferred_social_media': forms.Select(attrs={
                'id': 'social'
            }),
            'social_media_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Social Media URL (e.g., https://www.instagram.com/yourprofile)',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Force these fields to be required
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

        for field_name, field in self.fields.items():
            if field.required:
                field.label = f"{field.label}*"

    def clean(self):
        cleaned_data = super().clean()
        # Add any global clean logic here if needed
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Generate slug if not set
        if not instance.slug:
            base_slug = slugify(f"{instance.first_name}-{instance.last_name}")

            def generate_slug_int():
                random_int = random.randint(1000, 9999)
                return f"{base_slug}-{random_int}"

            slug = generate_slug_int()
            while Profile.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
                slug = generate_slug_int()

            instance.slug = slug

        instance.is_profile_complete = True

        if commit:
            instance.save()
        return instance
