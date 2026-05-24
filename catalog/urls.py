from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')

urlpatterns = [
    # Auth routes
    path('auth/register', views.register, name='auth-register'),
    path('auth/login', views.login, name='auth-login'),
    path('auth/logout', views.logout, name='auth-logout'),
    # CRUD routes (via router)
    path('', include(router.urls)),
]
