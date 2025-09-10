from django.db import models

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('corporate', 'Corporate Events'),
        ('social', 'Social Gatherings'),
        ('special', 'Special Occasions'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=100)  # e.g., "Weddings", "AGMs"
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='services/', blank=True, null=True)  # New image field

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption or f"Image {self.id}"

    class Meta:
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    review = models.TextField()
    rating = models.PositiveIntegerField(default=5)  # 1-5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.rating} stars)"

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

class Enquiry(models.Model):
    EVENT_CHOICES = [
        ('corporate', 'Corporate Event'),
        ('wedding', 'Wedding'),
        ('birthday', 'Birthday'),
        ('burial', 'Burial'),
        ('other', 'Other'),
    ]

    GUEST_RANGES = [
        ('0-100', '0 - 100 Guests'),
        ('100-200', '100 - 200 Guests'),
        ('200-500', '200 - 500 Guests'),
        ('500-1000', '500 - 1000 Guests'),
        ('1000+', '1000+ Guests'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES, default='other')
    date = models.DateField()
    location = models.CharField(max_length=200)
    guest_range = models.CharField(max_length=20, choices=GUEST_RANGES, default='0-100')
    message = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enquiry from {self.name} ({self.event_type}) - {self.guest_range}"

    class Meta:
        verbose_name = "Enquiry"
        verbose_name_plural = "Enquiries"

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"