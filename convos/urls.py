from django.urls import path
from .views import (ConvosView)

urlpatterns = [
    path('', ConvosView.as_view()),
]