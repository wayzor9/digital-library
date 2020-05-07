from django.contrib import admin
from .models import Author, Book, Chapter, Exercise, Solution, Customer, OrderItem, Order

# Register your models here.

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Exercise)
admin.site.register(Solution)
admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(Order)