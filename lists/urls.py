from django.urls import path
from .views import (ListView, ListsView, ListItemView, ListItemsView)

urlpatterns = [
    path('', ListsView.as_view()),
    path('<slug:id>/', ListView.as_view()),
    path('<slug:id>/items/', ListItemsView.as_view()),
    path('<slug:id>/item/<slug:item_id>/', ListItemView.as_view()),
]