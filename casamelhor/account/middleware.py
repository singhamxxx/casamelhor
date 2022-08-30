from django.utils.deprecation import MiddlewareMixin


class HeaderAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'HTTP_AUTHORIZATION' in request.META and request.META['HTTP_AUTHORIZATION']:
            request.META['HTTP_AUTHORIZATION'] = request.META['HTTP_AUTHORIZATION'].split(',')[1]
        elif 'Authorization' in request.META and request.META['Authorization']:
            request.META['Authorization'] = request.META['Authorization'].split(',')[1]
        else:
            pass
