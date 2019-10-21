from django.urls import path

from . import views


urlpatterns = [
    path("", views.index),
    path("files/", views.get_file),
    path("sign/", views.sign_file),
    path("success/", views.uploaded),
    path("upload/", views.file_upload),
]
