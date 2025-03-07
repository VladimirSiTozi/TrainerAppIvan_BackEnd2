from django.views.generic import TemplateView


class AccountDetailView(TemplateView):
    template_name = 'account/account-details.html'


class AccountLoginView(TemplateView):
    template_name = 'account/login.html'


class AccountRegisterView(TemplateView):
    template_name = 'account/register.html'

