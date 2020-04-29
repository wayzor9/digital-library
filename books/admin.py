from django.contrib import admin
from .models import Author, Book, Chapter, Exercise, Solution
# Register your models here.

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Exercise)
admin.site.register(Solution)

