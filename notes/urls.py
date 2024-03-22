from django.urls import path
from .views import (NoteView, NotesView)

urlpatterns = [
    path('', NotesView.as_view()),
    path('<slug:uuid>/', NoteView.as_view()),
]
