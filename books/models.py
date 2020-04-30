from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User


class Customer(models.Model):
    books = models.ManyToManyField('Book')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def book_list(self):
        return self.books.all()

def post_signup_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        Customer.objects.get_or_create(user=instance)
        print(f"CREATE CUSTOMER ---> {instance}")

post_save.connect(post_signup_user_receiver, User)

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    slug = models.SlugField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    authors = models.ManyToManyField(Author)
    title = models.CharField(max_length=100)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=16)
    slug = models.SlugField()
    cover = models.ImageField()
    price = models.FloatField()

    def __str__(self):
        return f'{self.title}'

    def get_url(self):
        return reverse("books:book-detail", kwargs={
            'slug': self.slug})

class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter_number = models.IntegerField()
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse ("books:chapter-detail", kwargs={
            'book_slug' : self.book.slug,
            'chapter_number' : self.chapter_number})

class Exercise(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    exercise_number = models.IntegerField()
    page_number = models.IntegerField()
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse("books:exercise-detail", kwargs={
            'book_slug': self.chapter.book.slug,
            'chapter_number': self.chapter.chapter_number,
            'exercise_number' :self.exercise_number
        })


class Solution(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    image = models.ImageField()
    solution_number = models.IntegerField()


    def __str__(self):
        return f'{self.exercise.title} {self.pk}'
