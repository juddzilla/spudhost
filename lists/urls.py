from django.urls import path
from .views import (ListView, ListsView, ListItemView)

urlpatterns = [
    path('', ListsView.as_view()),
    path('<slug:id>/', ListView.as_view()),
    path('<slug:id>/items/<slug:item_id>/', ListItemView.as_view()),
]