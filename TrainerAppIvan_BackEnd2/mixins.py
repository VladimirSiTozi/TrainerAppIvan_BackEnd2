class ProfileContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'object') and hasattr(self.object, 'user'):
            context['profile'] = self.object.user.profile
        return context
