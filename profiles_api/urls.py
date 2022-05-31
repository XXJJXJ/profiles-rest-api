from django.urls import path

from profiles_api import views

## This will be for "webserver_url/api/..."
## the "api/" will bring us here
## here we can continue to redirect into more directories
urlpatterns = [
    path("hello-view/", views.HelloApiView.as_view()),
]
## needs localhost:8000/api/hello-view/ to work, localhost:8000/api/ does not work anymore
