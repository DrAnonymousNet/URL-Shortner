from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework import routers

from api.views import LinkViewSet, RedirectView, UserRegisterView

router = routers.DefaultRouter(trailing_slash=False)
router.register('links', LinkViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token),
    path('users/', UserRegisterView.as_view(), name="user-create"),
    path('<str:str>', RedirectView.as_view(), name="redirect-view")
]
