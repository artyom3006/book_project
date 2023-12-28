from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView
from .forms import BookForm, ReviewForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Book
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.db.models import Q

class BookListView(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/book_list.html'
    login_url = 'account_login'

    
class BookDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'    
    login_url = 'account_login'
    permission_required = 'books.special_status'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        return context
    
class SearchResultsView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/search_results.html'
    
    def get_queryset(self): 
        query = self.request.GET.get('q')
        return Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )

class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book_list')

class AddReviewView(LoginRequiredMixin, FormView):
    form_class = ReviewForm
    template_name = 'books/book_detail.html'
    login_url = 'account_login'

    def form_valid(self, form):
        book_id = self.kwargs['book_id']
        review = form.save(commit=False)
        review.book_id = book_id
        review.author = self.request.user
        review.save()
        return redirect('book_detail', pk=book_id)
    
