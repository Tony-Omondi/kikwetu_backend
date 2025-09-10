from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, GalleryViewSet, TestimonialViewSet, EnquiryViewSet, FAQViewSet, CustomObtainAuthToken

router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'gallery', GalleryViewSet)
router.register(r'testimonials', TestimonialViewSet)
router.register(r'enquiries', EnquiryViewSet)
router.register(r'faqs', FAQViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', CustomObtainAuthToken.as_view(), name='api_login'),
]