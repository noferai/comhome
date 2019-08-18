from django.contrib.auth.mixins import AccessMixin


class AdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.raise_exception = True
        if not request.user.is_admin:
            if not request.user.is_superuser:
                return self.handle_no_permission()
        return super(AdminRequiredMixin, self).dispatch(request, *args, **kwargs)
