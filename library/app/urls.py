from . import views
from django.contrib import admin
from django.urls import path, include
from .views import IndexView

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('register', views.RegisterView.as_view(), name="register"),
    path('login', views.LoginView.as_view(), name="login"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('logout', views.logout, name="logout"),
    path('admin',views.admin,name="admin"),
    path('profile', views.profile, name="profile"),
    path('books/<int:id>', views.my_books, name="my_books"),
    path('settings', views.settings, name="settings"),
    path('books', views.BooksView.as_view(), name="books"),
    path('author/<int:id>', views.author, name="author"),
    path('borrow', views.borrow, name="borrow"),

]
