from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    id = models.UUIDField( # new
        primary_key=True,
        db_index=True,
        default=uuid.uuid4,
        editable=False)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cover = models.ImageField(upload_to='covers/', blank=True)
    
    class Meta: # new
        permissions = [
            ("special_status", "Can read all books"),
        ]
            
    def __str__(self):
        return self.title
    
    def get_absolute_url(self): 
        return reverse('book_detail', kwargs={'pk': str(self.pk)})
    
class Review(models.Model):
    book = models.ForeignKey(
        Book, 
        on_delete = models.CASCADE,
        related_name = 'reviews',
    )
    review = models.CharField(max_length = 255)
    author = models.ForeignKey(
        get_user_model(), 
        on_delete = models.CASCADE,
    )
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, default=0)
    
    def stars_display(self):
        full_stars = '⭐' * self.rating
        empty_stars = '' * (10 - self.rating)
        rate = self.rating
        return f'{full_stars}{empty_stars}({rate}/10)'
    
    def __str__(self):
        return self.review