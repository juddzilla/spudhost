from django.urls import path
from .views import (QuickQueueItemView, QuickQueuesView)

urlpatterns = [
    path('', QuickQueuesView.as_view()),
    path('<slug:uuid>/', QuickQueueItemView.as_view()),
]
