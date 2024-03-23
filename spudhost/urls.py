"""
URL configuration for spudhost project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from token_auth import urls as token_auth_views
from convos import urls as convos_urls
from groupings import urls as groupings_urls
from lists import urls as lists_urls
from quick_queue import urls as queue_urls
from notes import urls as notes_urls

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('collections/', include(groupings_urls)),
    path('convos/', include(convos_urls)),    
    path('lists/', include(lists_urls)),
    path('notes/', include(notes_urls)),
    path('auth/', include(token_auth_views)),
    path('queue/', include(queue_urls)),
]


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('accounts/', include('allauth.urls')),
#     path('accounts/', include('allauth.socialaccount.urls')),
#     path('apologize/', include(apology_urls)),
#     path('apology/', include(completed_urls)),
#     path('oauth/', include(oauth_urls)),
#     path('u/', include(user_urls)),
# ]
