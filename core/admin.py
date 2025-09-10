from django.contrib import admin
from .models import Service, Gallery, Testimonial, Enquiry, FAQ

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'description')
    list_filter = ('category',)
    search_fields = ('title', 'description')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('caption', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('caption',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'review')

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'guest_range', 'date', 'submitted_at')
    list_filter = ('event_type', 'guest_range', 'date')
    search_fields = ('name', 'email', 'phone', 'location')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    search_fields = ('question', 'answer')