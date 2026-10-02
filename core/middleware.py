from django.utils.timezone import now

class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # We only update if the user has a profile
            if hasattr(request.user, 'perfil'):
                request.user.perfil.ultima_actividad = now()
                request.user.perfil.save(update_fields=['ultima_actividad'])
        
        response = self.get_response(request)
        return response
