from django.urls import path,re_path
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import ProductListAPIView


schema_view = get_schema_view(
    openapi.Info(
        title="Your Api Decumation",
        default_version= ' v1',
        description='Api documantination for you project',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='your@gmail.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('',views.index,name='index'), 
    re_path(r'^swagger(?P<format>\.json|\.yml)$',schema_view.without_ui(cache_timeout=0),name='schema-json'),
    path('swagger/',schema_view.with_ui('swagger',cache_timeout=0),name='schema-swagger-ui'),
    path('product/',ProductListAPIView.as_view(), name="product-list")
    
]