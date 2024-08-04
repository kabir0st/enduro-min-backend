from django.urls import include, path
from rest_framework.routers import SimpleRouter
from users.api.auth import forget_password, reset_password
from users.api.users import RegisterUserBaseAPI, UserBaseAPI
from users.api.settings import SettingsAPI

router = SimpleRouter()

router.register('settings', SettingsAPI)
router.register('', UserBaseAPI, basename='Users')

urlpatterns = [
    path('register/', RegisterUserBaseAPI.as_view()),
    path('password/reset/', reset_password),
    path('password/forget/', forget_password),
    path('', include(router.urls)),
]
