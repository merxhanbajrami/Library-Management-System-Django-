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
    path('borrow/<int:id>', views.borrow, name="borrow"),
    path('return_book/<int:id>', views.return_book, name="return_book"),
    path('manage-books/', views.manage_books, name="manage_books"),
    path('manage-users/', views.manage_users, name="manage_users"),
    path('issued-books/', views.issued, name="issued"),
    path('archived-books/', views.archive, name="archive"),
    path('messages/', views.message, name="messages"),
    path('edit-profile/', views.edit, name="edit"),
    path('read_message/<int:id>', views.read_message, name="read_message"),
    path('alert_user/<int:id>',views.AlertView.as_view(),name="alert"),
    path('reply/<int:id>', views.ReplyView.as_view(), name="reply"),
    path('close/<int:id>', views.close, name="close"),
    path('block/<int:id>', views.block, name="block"),
    path('events', views.event, name="event"),
    path('add-event', views.add_event, name="add_event"),
    path('delete-event/<int:id>', views.delete_event, name="delete_event"),

]
