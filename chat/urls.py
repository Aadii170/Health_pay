# urls.py
# Django view-based URL routing for rendering templates

from django.urls import path
from . import views

# Define routes for serving pages
urlpatterns = [
    path('<str:group_name>/', views.index, name='chatroom'),  # Pass group_name to template
]
# This allows dynamic rendering of chat rooms based on group_name in the URL