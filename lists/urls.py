from django.urls import path
from .views import (ListView, ListsView, ListItemView, ListItemsView)

urlpatterns = [
    path('', ListsView.as_view()),
    path('<slug:uuid>/', ListView.as_view()),
    path('<slug:uuid>/items/', ListItemsView.as_view()),
    path('<slug:uuid>/item/<slug:item_id>/', ListItemView.as_view()),
]