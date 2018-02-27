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


def add_book(request, book_pk=None):
    data = {}
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            data['form_is_valid'] = True
            if book_pk:
                # If book_pk: get book, update and save
                book = get_object_or_404(Book, pk=book_pk)
                book.title = form.cleaned_data['title']
                book.author = form.cleaned_data['author']
                book.save()
            else:
                # Else: just save
                form.save()
        # Form not valid
        else:
            data['form_is_valid'] = False
    else:
        context = {}
        if book_pk:
            book = get_object_or_404(Book, pk=book_pk)
            # Instantiate form with initialized data from book
            form = AddBookForm(initial={'title': book.title,
                                        'author': book.author,})
            # Generate context with form and book_pk to create correct action url
            context['form'] = form
            context['book_pk'] = book_pk
            # render_to_string the form
            html_form = render_to_string('books/includes/update_book_form.html',
                                         context,
                                         request=request,
                                         )
        else:
            form = AddBookForm()
            context['form'] = form
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
