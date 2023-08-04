from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import SignupAPIView, LoginAPIView, UserViewSet, IncidentViewSet

router = SimpleRouter()
router.register('users', UserViewSet)
router.register('incidents', IncidentViewSet)

urlpatterns = [
    path('signup', SignupAPIView.as_view(), name="sign up POST"),
    path('login', LoginAPIView.as_view(), name="log in POST"),
]

urlpatterns += router.urls
