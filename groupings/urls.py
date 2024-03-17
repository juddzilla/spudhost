from django.urls import path
from .views import (GroupingsView)

urlpatterns = [
    path('', GroupingsView.as_view()),
]