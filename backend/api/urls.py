from django.urls import path, include

urlpatterns = [
    path("query/", include("api.urls")),
]
