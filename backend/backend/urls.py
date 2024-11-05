from django.urls import path, include, re_path
from .views import index

urlpatterns = [
    path("api/", include("api.urls")),
    re_path(r"^.*$", index),
]
