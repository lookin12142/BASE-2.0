# shop/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, OrderViewSet, OrderItemViewSet, CustomerViewSet, MascotaViewSet, EmergencyHistoryListCreate, EmergencyHistoryDetail, product_list
from django.conf.urls.static import static
from django.conf import settings
from .views import create_order
from . import views

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'orderitems', OrderItemViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'mascotas', MascotaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create-order/', create_order, name='create-order'),
    path('emergencies/', EmergencyHistoryListCreate.as_view(), name='emergency-list-create'),
    path('emergencies/<int:pk>/', EmergencyHistoryDetail.as_view(), name='emergency-detail'),
    path('products/', product_list, name='product-list'),
    path('admin/emergencies/', EmergencyHistoryListCreate.as_view(), name='admin-emergency-list-create'),
    path('admin/emergencies/<int:pk>/', EmergencyHistoryDetail.as_view(), name='admin-emergency-detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    