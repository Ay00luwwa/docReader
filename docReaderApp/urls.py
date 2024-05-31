from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.upload_files, name='upload_files'),
    path("", views.handle_uploaded_file, name='handle_upload'),
    path("", views.generate_summary, name='generate_summary'),
]
