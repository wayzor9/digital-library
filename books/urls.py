from django.urls import path
from .views import book_list, book_detail, chapter_detail, exercise_detail, RegistrationView, LoginView, LogOutView

app_name = 'books'
urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name= 'login'),
    path('logout/', LogOutView.as_view(), name = 'logout'),

    path('', book_list,name = 'book-list'),
    path('<slug>', book_detail , name='book-detail'),
    path('<book_slug>/<int:chapter_number>', chapter_detail, name='chapter-detail'),
    path('<book_slug>/<int:chapter_number>/<int:exercise_number>', exercise_detail, name='exercise-detail'),
]