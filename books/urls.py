from django.urls import path

from .views import BookListView, BookDetailView, BookCreateView, AddReviewView

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('<uuid:pk>', BookDetailView.as_view(), name='book_detail'),
    path('create/', BookCreateView.as_view(), name='book_create'),
     path('<uuid:book_id>/add_review/', AddReviewView.as_view(), name='add_review'),
]
