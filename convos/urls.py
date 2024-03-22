from django.urls import path
from .views import (ConvoView, ConvosView)

urlpatterns = [
    path('', ConvosView.as_view()),
    path('<slug:uuid>/', ConvoView.as_view()),
]