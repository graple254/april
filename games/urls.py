from django.urls import path
from .views import *

urlpatterns = [
      path('sudoku/', sudoku, name='sudoku'),
]