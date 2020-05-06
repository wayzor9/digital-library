from django.urls import path

from .views import (book_list, book_detail, chapter_detail,
                    exercise_detail, RegistrationView, LoginView,
                    LogOutView, AddBookView, AddAuthorView, AddChapterView,
                    AddExerciseView, AddSolutionView, UpdateBookView, BookDeleteView,
                    UpdateChapterView, ChapterDeleteView, UpdateExerciseView,
                    ExerciseDeleteView, UpdateSolutionView, SolutionDeleteView, update_cart, order_cart_view)


app_name = 'books'

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name= 'login'),
    path('logout/', LogOutView.as_view(), name = 'logout'),

    path('', book_list,name = 'book-list'),
    path('<slug>', book_detail , name='book-detail'),
    path('<book_slug>/<int:chapter_number>', chapter_detail, name='chapter-detail'),
    path('<book_slug>/<int:chapter_number>/<int:exercise_number>', exercise_detail, name='exercise-detail'),

    path('add_book/', AddBookView.as_view(), name='add-book'),
    path('add_author/', AddAuthorView.as_view(), name='add-author'),
    path('add_chapter/', AddChapterView.as_view(), name='add-chapter'),
    path('add_exercise/', AddExerciseView.as_view(), name= 'add-exercise'),
    path('add_solution/', AddSolutionView.as_view(), name='add-solution'),

    path('update_book/<slug>/', UpdateBookView.as_view(), name='update-book'),
    # path('add_author/', AddAuthorView.as_view(), name='add-author'),
    path('chapter_update/<int:pk>/', UpdateChapterView.as_view(), name='update-chapter'),
    path('exercise_update/<int:pk>/', UpdateExerciseView.as_view(), name= 'update-exercise'),
    path('solution_update/<int:pk>/', UpdateSolutionView.as_view(), name='update-solution'),

    path('delete_book/<slug>/', BookDeleteView.as_view(), name='delete-book'),
    path('delete_chapter/<int:pk>/', ChapterDeleteView.as_view(), name='delete-chapter'),
    path('delete_exercise/<int:pk>/', ExerciseDeleteView.as_view(), name='delete-exercise'),
    path('delete_solution/<int:pk>/', SolutionDeleteView.as_view(), name='delete-solution'),

    path('order_cart_view/', order_cart_view, name='view'),
    path('update_cart/<book_slug>/', update_cart, name='update-order')
]
