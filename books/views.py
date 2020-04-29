from django.http import Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Book, Chapter, Exercise


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
