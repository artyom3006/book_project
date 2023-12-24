from django.contrib import admin
from .models import Book, Review

class ReviewInLine(admin.TabularInline):
    model = Review
    
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "price",)
    inlines = [
        ReviewInLine,
    ]

admin.site.register(Book, BookAdmin)