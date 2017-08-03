from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

@login_required
def home_view(request):
    return render(request, 'index.html', {})

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter