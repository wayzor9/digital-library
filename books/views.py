from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from django.views.generic.base import View
from .models import Book, Chapter, Exercise
from .forms import RegistrationForm, LoginForm

class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'register_view.html', {"form":form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            user.set_password('password1')
            user.save()
            messages.success(request, "Created account for " + username)
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

