from django.urls import path
from .views import (ListsView)

urlpatterns = [
    path('', ListsView.as_view()),
]