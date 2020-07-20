from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.base import View

from .models import Book, Chapter, Exercise, Author, Solution, OrderItem, Order
from .forms import RegistrationForm, LoginForm, AddBook


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'register_view.html', {"form": form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, "Account created successfully for " + user.username )
            return redirect('books:login')
        return render(request, 'register_view.html', {"form": form})


class LoginView(View):
    def get(self, request):
        form = LoginForm
        return render(request, 'login_view.html', {'form': form})

    def post(self, request):
        next = request.GET.get('next')
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            auth_user = authenticate(username = username, password = password)
            if auth_user is not None:
                login(request, auth_user)
                if next:
                    return redirect(next)
                return redirect('/')
            else:
                messages.info(request, "Username or Password incorrect")

        return render(request, 'login_view.html', {'form': form})


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


OWNED = 'owned'
IN_CART = 'in_cart'
NOT_IN_CART = 'not_in_cart'


def check_book_relationship(request, book):
    if book in request.user.customer.book_list():
        return OWNED
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        order_item_qs = OrderItem.objects.filter(book=book)
        if order_item_qs.exists():
            order_item = order_item_qs[0]
            if order_item in order.items.all():
                return IN_CART
    return NOT_IN_CART


def book_list(request):
    list_of_books = Book.objects.all()
    paginator = Paginator(list_of_books, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'list_book.html', {'page_obj': page_obj})


def book_list2(request):
    query_set = Book.objects.all()
    return render(request, 'list_book.html', {'query_set': query_set})


@login_required
def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    check_book_status = check_book_relationship(request, book)
    return render(request, 'detail_book.html', {'book': book, 'check_book_status': check_book_status})


@login_required
def chapter_detail(request, book_slug, chapter_number):
    chapter_qs = Chapter.objects.filter(book__slug=book_slug)\
        .filter(chapter_number=chapter_number)
    chapter = chapter_qs[0]
    check_book_status = check_book_relationship(request, chapter.book)
    if chapter_qs.exists():
        return render(request, 'detail_chapter.html',
                      {'chapter': chapter, 'check_book_status': check_book_status})
    return Http404


@login_required
def exercise_detail(request, book_slug, chapter_number, exercise_number):
    exercise_qs = Exercise.objects.filter(chapter__book__slug=book_slug)\
        .filter(chapter__chapter_number=chapter_number)\
        .filter(exercise_number=exercise_number)
    exercise = exercise_qs[0]
    check_book_status = check_book_relationship(request, exercise.chapter.book)
    if exercise_qs.exists():
        return render(request, 'detail_exercise.html',
                      {'exercise': exercise, 'check_book_status': check_book_status})
    return Http404


@login_required
def add_to_cart(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)
    order_item, created = OrderItem.objects.get_or_create(book=book)
    order, created = Order.objects.get_or_create(user=request.user, is_ordered=False)
    order.items.add(order_item)
    order.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def remove_from_cart(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)
    order_item = get_object_or_404(OrderItem, book=book)
    order = Order.objects.get(user=request.user, is_ordered=False)
    order.items.remove(order_item)
    order.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def summary_view(request):
    order, created = Order.objects.get_or_create(user=request.user)
    return render(request, 'order_summary.html', {'order': order})


class AddBookView(CreateView):
    form_class = AddBook
    model = Book
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'add new book'
        })
        return context


class UpdateBookView(UpdateView):
    form_class = AddBook
    model = Book
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update the book'
        })
        return context


class BookDeleteView(DeleteView):
    model = Book
    success_url = '/'


class AddAuthorView(CreateView):
    model = Author
    fields = '__all__'
    success_url = '/'
    template_name = 'books/book_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'add new author'
        })
        return context


class AddChapterView(CreateView):
    model = Chapter
    fields = '__all__'
    success_url = '/'
    template_name = 'books/book_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'add new chapter'
        })
        return context


class UpdateChapterView(UpdateView):
    model = Chapter
    fields = '__all__'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update the chapter'
        })
        return context


class ChapterDeleteView(DeleteView):
    model = Book
    success_url = '/'
    template_name = 'books/book_confirm_delete.html'


class AddExerciseView(CreateView):
    model = Exercise
    fields = '__all__'
    success_url = '/'
    template_name = 'books/book_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'add new exercise'
        })
        return context


class UpdateExerciseView(UpdateView):
    model = Exercise
    fields = '__all__'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update the exercise'
        })
        return context


class ExerciseDeleteView(DeleteView):
    model = Exercise
    success_url = '/'
    template_name = 'books/book_confirm_delete.html'


class AddSolutionView(CreateView):
    model = Solution
    fields = '__all__'
    success_url = '/'
    template_name = 'books/book_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'add new solution'
        })
        return context


class UpdateSolutionView(UpdateView):
    model = Solution
    fields = '__all__'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update the solution'
        })
        return context


class SolutionDeleteView(DeleteView):
    model = Solution
    success_url = '/'
    template_name = 'books/book_confirm_delete.html'
