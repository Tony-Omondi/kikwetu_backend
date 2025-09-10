from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.core.mail import EmailMessage
from .models import Service, Gallery, Testimonial, Enquiry, FAQ
from .serializers import ServiceSerializer, GallerySerializer, TestimonialSerializer, EnquirySerializer, FAQSerializer
import logging
import smtplib  # Added missing import



# Configure logging
logger = logging.getLogger(__name__)

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            return [AllowAny()]
        return [IsAdminUser()]

class EnquiryViewSet(viewsets.ModelViewSet):
    queryset = Enquiry.objects.all()
    serializer_class = EnquirySerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [AllowAny()]
        return [IsAdminUser()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'data': serializer.data,
            'email_sent': result['email_sent'],
            'enquiry_id': result['enquiry_id']
        }, status=201, headers=headers)

    def perform_create(self, serializer):
        enquiry = serializer.save()
        email_sent = True  # Track if both emails succeed

        # Prepare common email content
        subject = f"New Enquiry from {enquiry.name}"
        message = (
            f"New enquiry received:\n\n"
            f"Name: {enquiry.name}\n"
            f"Email: {enquiry.email}\n"
            f"Phone: {enquiry.phone}\n"
            f"Event Type: {enquiry.get_event_type_display()}\n"
            f"Date: {enquiry.date}\n"
            f"Location: {enquiry.location}\n"
            f"Guest Range: {enquiry.get_guest_range_display()}\n"
            f"Message: {enquiry.message or 'No message provided'}\n"
            f"Submitted At: {enquiry.submitted_at}"
        )

        # Admin notification
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
        except (BadHeaderError, smtplib.SMTPAuthenticationError, smtplib.SMTPException) as e:
            logger.error(f"Failed to send admin email for enquiry {enquiry.id}: {str(e)}")
            email_sent = False

        # Enquirer confirmation email
        confirmation_subject = "Thank You for Your Enquiry"
        confirmation_message = (
            f"Dear {enquiry.name},\n\n"
            f"Thank you for reaching out to us! We have received your enquiry, and our team will get back to you shortly. Below are the details you submitted:\n\n"
            f"Name: {enquiry.name}\n"
            f"Email: {enquiry.email}\n"
            f"Phone: {enquiry.phone}\n"
            f"Event Type: {enquiry.get_event_type_display()}\n"
            f"Date: {enquiry.date}\n"
            f"Location: {enquiry.location}\n"
            f"Guest Range: {enquiry.get_guest_range_display()}\n"
            f"Message: {enquiry.message or 'No message provided'}\n"
            f"Submitted At: {enquiry.submitted_at}\n\n"
            f"We look forward to assisting you with your event!\n"
            f"Best regards,\n"
            f"The Kikwetu Team"
        )
        try:
            send_mail(
                subject=confirmation_subject,
                message=confirmation_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[enquiry.email],
                fail_silently=False,
            )
        except (BadHeaderError, smtplib.SMTPAuthenticationError, smtplib.SMTPException) as e:
            logger.error(f"Failed to send confirmation email to {enquiry.email} for enquiry {enquiry.id}: {str(e)}")
            email_sent = False

        return {'enquiry_id': enquiry.id, 'email_sent': email_sent}

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]