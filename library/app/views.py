from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib import messages
from .models import *
from .forms import *


# Create your views here.

class IndexView(View):
    def get(self, request):
        form = ContactForm()
        context = {
            'form': form
        }
        return render(request, 'index.html', context=context)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
        form = ContactForm()
        context = {
            'form': form
        }
        return render(request, 'index.html', context=context)


class LoginView(View):
    def get(self, request):
        if request.session.get('is_logged_in'):
            return redirect('dashboard')
        else:
            form = LoginForm
            return render(request, 'login.html', context={'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = User.objects.filter(username=username)
            if user:
                if user[0].password == password:
                    request.session['is_logged_in'] = True
                    request.session['username'] = username
                    return redirect('dashboard')
                else:
                    messages.add_message(request, messages.ERROR, 'Password is incorrect!')
            else:
                messages.add_message(request, messages.ERROR, 'This username doesnt exist')

        return render(request, 'login.html', context={'form': form})


class RegisterView(View):
    def get(self, request):
        if request.session.get('is_logged_in'):
            return redirect('dashboard')
        else:
            form = RegisterForm()
            return render(request, 'register.html', context={'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        password = request.POST['password']
        conifrm_password = request.POST['confirm_password']
        username = request.POST['username']
        users = User.objects.all()
        for user in users:
            if user.username == username:
                messages.add_message(request, messages.ERROR, 'Username already exists')
                return render(request, 'register.html', context={'form': form})
        if password == conifrm_password:
            if form.is_valid():
                form.save()
            request.session['is_logged_in'] = True
            request.session['username'] = username
            return redirect('dashboard')
        else:
            messages.add_message(request, messages.INFO, 'Passwords dont match!')
            return render(request, 'register.html', context={'form': form})


class BooksView(View):
    def get(self, request):
        politics = Book.objects.filter(category='Politics')
        science = Book.objects.filter(category='Science')
        philosophy = Book.objects.filter(category='Philosophy')
        novel = Book.objects.filter(category='Novel')
        astronomy = Book.objects.filter(category='Astronomy')
        psychology = Book.objects.filter(category='Psychology')
        self_improvement = Book.objects.filter(category='Self improvement')
        context = {
            'politics': politics,
            'science': science,
            'philosophy': philosophy,
            'novel':novel,
            'psychology':psychology,
            'astronomy':astronomy,
            'self_improvement':self_improvement
        }
        return render(request, 'books.html', context=context)

    def post(self, request):
        return render(request, 'books.html')


def dashboard(request):
    user = User.objects.filter(username=request.session.get('username')).first()
    context = {
        'user': user
    }
    return render(request, 'base.html', context=context)


def author(request, id):
    author = Author.objects.filter(id=id).first()
    books = Book.objects.filter(author_id=id)
    context = {
        'author': author,
        'books': books,
    }
    return render(request, 'author.html', context=context)


def borrow(request):
    return HttpResponse('BORROWING')


def profile(request):
    user = User.objects.filter(username=request.session.get('username')).first()
    context = {
        'user': user
    }
    return render(request, 'profile.html', context=context)


def my_books(request, id):
    user = User.objects.filter(id=id).first()
    books = Borrow.objects.filter(user=user.id)
    context = {
        'books': books,
    }
    return render(request, 'my_books.html', context=context)


def logout(request):
    del (request.session['username'])
    del (request.session['is_logged_in'])
    return redirect('index')


def settings(request):
    return render(request, 'settings.html')


def admin(request):
    return render(request, 'admin.html')
