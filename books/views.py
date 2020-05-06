from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.forms import ModelForm
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.base import View
from .models import Book, Chapter, Exercise, Author, Solution, Order
from .forms import RegistrationForm, LoginForm, AddBook

### AUTHORIZATION ###
class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'register_view.html', {"form":form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, "Account created successfully for" + user.username )
            return redirect('books:login')
        return render(request, 'register_view.html', {"form": form})

class LoginView(View):
    def get(self, request):
        form = LoginForm
        return render(request, 'login_view.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            auth_user = authenticate(username = username, password = password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('/')
            else:
                messages.info(request, "Username or Password incorrect")

        return render(request, 'login_view.html', {'form': form})

class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')

#### BOOK ####

def book_list(request):
    query_set = Book.objects.all()
    return render(request, 'list_book.html', {'query_set':query_set})

def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    # book = Book.objects.get(slug=slug)
    return render(request, 'detail_book.html', {'book':book})

def chapter_detail(request, book_slug, chapter_number):
    chapter_qs = Chapter.objects.filter(book__slug=book_slug).filter(chapter_number=chapter_number)
    if chapter_qs.exists():
        return render(request, 'detail_chapter.html', {'chapter':chapter_qs[0]})
    return Http404

def exercise_detail(request, book_slug, chapter_number, exercise_number):
    exercise_qs = Exercise.objects.filter(chapter__book__slug=book_slug)\
        .filter(chapter__chapter_number=chapter_number)\
        .filter(exercise_number=exercise_number)
    if exercise_qs.exists():
        return render(request, 'detail_exercise.html', {'exercise':exercise_qs[0]})
    return Http404

### SHOPPING CART

def order_cart_view(request):
    try:
        the_id = request.session['order_id']
    except:
        the_id = None
    if the_id:
        order = Order.objects.get(id=the_id)
        return render(request, 'order_summary.html', {'order': order})
    else:
        empty_message = "Your cart is empty. Please, keep shopping"
        empty = True
        return render(request, 'order_summary.html', { "empty": empty,
                                                  'empty_message': empty_message})

def update_cart(request, book_slug):
    request.session.set_expiry(3000)
    try:
        the_id =request.session['order_id']
    except:
        new_order = Order()
        new_order.save()
        request.session['order_id'] = new_order.id
        the_id = new_order.id
    order = Order.objects.get(id=the_id)

    try:
        book = Book.objects.get(slug=book_slug)
    except Book.DoesNotExist:
        pass

    if not book in order.books.all():
        order.books.add(book)
    else:
        
        order.books.remove(book)

    new_total= 0.00
    for item in order.books.all():
        new_total+= item.price

    request.session['items_total'] = order.books.count()
    order.total = new_total
    order.save()

    return HttpResponseRedirect(reverse('books:view'))


###  CBS CRUD ###
class AddBookView(CreateView):
    form_class = AddBook
    model = Book
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'Create new'
        })
        return context

class UpdateBookView(UpdateView):
    form_class = AddBook
    model = Book
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'Update'
        })
        return context

class BookDeleteView(DeleteView):
    model = Book
    success_url = '/'

###  author

class AddAuthorView(CreateView):
    model = Author
    fields = '__all__'
    success_url = '/'

###  Chapter
class AddChapterView(CreateView):
    model = Chapter
    fields = '__all__'
    success_url = '/'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'Create new'
        })
        return context

class UpdateChapterView(UpdateView):
    model = Chapter
    fields = '__all__'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'Update the'
        })
        return context

class ChapterDeleteView(DeleteView):
    model = Book
    success_url = '/'
    template_name = 'books/book_confirm_delete.html'

### exercise

class AddExerciseView(CreateView):
    model = Exercise
    fields = '__all__'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'Create'
        })
        return context

class UpdateExerciseView(UpdateView):
    model = Exercise
    fields = '__all__'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'Update'
        })
        return context

class ExerciseDeleteView(DeleteView):
    model = Exercise
    success_url = '/'
    template_name = 'books/book_confirm_delete.html'

### solution
class AddSolutionView(CreateView):
    model = Solution
    fields = '__all__'
    success_url = '/'

class UpdateSolutionView(UpdateView):
    model = Solution
    fields = '__all__'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'Update'
        })
        return context

class SolutionDeleteView(DeleteView):
    model = Solution
    success_url = '/'
    template_name = 'books/book_confirm_delete.html'

