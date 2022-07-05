from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.authtoken import views
from rest_framework import routers

from api.views import LinkViewSet, RedirectView, UserRegisterView, index
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

schema_view = get_schema_view(
   openapi.Info(
      title="GoWithEase API",
      default_version='v1',
      description="GoWithEase API description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
   authentication_classes=[JWTAuthentication]
)


router = routers.DefaultRouter()
router.register('links', LinkViewSet)

app_name = "api"

urlpatterns_v1 = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
       path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path('', include(router.urls)),
    
]



urlpatterns = [
   path("", index, name="index"),
    path('admin/', admin.site.urls),
    re_path(r'^v1/', include((urlpatterns_v1,"api"), namespace="v1")),
    path('<str:str>', RedirectView.as_view(), name="redirect-view")

]

