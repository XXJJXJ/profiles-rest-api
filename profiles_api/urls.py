from django.urls import path, include # include is for ViewSet

# for ViewSet
from rest_framework.routers import DefaultRouter

from profiles_api import views

# for ViewSet
router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
# Register profile viewset
router.register('profile', views.UserProfileViewSet)
router.register('feed', views.UserProfileFeedViewSet)

## This will be for "webserver_url/api/..."
## the "api/" will bring us here
## here we can continue to redirect into more directories
urlpatterns = [
    path("hello-view/", views.HelloApiView.as_view()),
    path('login/', views.UserLoginApiView.as_view()),
    path('', include(router.urls)), # for ViewSet
]
## needs localhost:8000/api/hello-view/ to work, localhost:8000/api/ does not work anymore

