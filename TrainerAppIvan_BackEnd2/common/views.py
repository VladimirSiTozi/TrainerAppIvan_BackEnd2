from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.conf import settings

from TrainerAppIvan_BackEnd2.common.froms import ContactForm
from TrainerAppIvan_BackEnd2.product.models import Product


class HomePageView(TemplateView):
    template_name = 'common/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['first_products'] = Product.objects.filter(is_active=True, category='Martial Arts').order_by('-created_at')[:3]
        context['second_products'] = Product.objects.filter(is_active=True, category='Gym').order_by('-created_at')[:3]
        print(context)
        return context


class CoachingPageView(TemplateView):
    template_name = 'common/coaching.html'


class ArticlePageView():
    template_name = 'common/articles.html'


class ContactMeView(TemplateView):
    template_name = 'common/contact-me.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success'] = kwargs.get('success')
        context['error'] = kwargs.get('error')
        context['form_data'] = kwargs.get('form_data', {})
        return context

    def post(self, request, *args, **kwargs):

        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        theme = request.POST.get('theme')
        message = request.POST.get('message')

        if not (first_name and last_name and email and theme and message):
            return self.render_to_response(
                self.get_context_data(
                    error="*Please fill in all required fields.",
                    form_data=request.POST
                )
            )

        subject = f"Contact Form filled - Theme: {theme} - Message from {first_name} {last_name}"
        full_message = f"""
            From: {first_name} {last_name} Email:<{email}>
            
            Subject: {theme}
            
            Message: {message}
            """

        send_mail(
            subject,
            full_message,
            settings.EMAIL_HOST_USER,
            ['ivanthebear.contact@gmail.com'],
            fail_silently=False,
        )

        return self.render_to_response(
            self.get_context_data(success="Your message has been sent successfully!")
        )


class AboutUsView(TemplateView):
    template_name = 'common/about-us.html'

