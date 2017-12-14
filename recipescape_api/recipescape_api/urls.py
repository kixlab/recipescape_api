"""recipescape_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from tagger_api import urls as tagger_urls
from recipe_api import urls as recipe_urls
from mturk_scraper import urls as scraper_urls
from recipescape_api.views import FacebookLogin, GoogleLogin

urlpatterns = [
    # url(r'^$', home_view, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^rest-auth/google/$', GoogleLogin.as_view(), name='goog_login'),
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^tagger/', include(tagger_urls)),
    url(r'^recipe/', include(recipe_urls)),
    url(r'^scraper/', include(scraper_urls)),
    url(r'^accounts/', include('allauth.urls')),
]
