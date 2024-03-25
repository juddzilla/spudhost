from django.urls import path
from .views import (GroupingView, GroupingsView)

urlpatterns = [
    path('', GroupingsView.as_view()),
    path('<slug:uuid>/', GroupingView.as_view()),
]