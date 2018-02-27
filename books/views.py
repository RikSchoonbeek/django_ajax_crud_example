from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import AddBookForm
from .models import Book


def index(request):
    return render(request, 'books/index.html')


def book_list(request):
    data = {}
    context = {}
    context['books'] = Book.objects.all()
    book_list = render_to_string('books/includes/book_list.html',
                                 context,
                                 request=request,)
    data['book_list'] = book_list
    return JsonResponse(data)


def add_book(request):
    data = {}
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = AddBookForm()
    context = {'form': form}
    html_form = render_to_string('books/includes/add_book_form.html',
                                 context,
                                 request=request,
                                 )
    data['html_form'] = html_form
    return JsonResponse(data)


def delete_book(request, book_pk):
    data = {}
    book = get_object_or_404(Book, pk=book_pk)
    book.delete()
    data['book_deleted'] = True
    return JsonResponse(data)
