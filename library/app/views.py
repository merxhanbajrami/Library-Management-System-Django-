from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib import messages
from .models import *
from .forms import *
from django.db.models import Count
import datetime
from datetime import timedelta


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
        form = LoginForm
        return render(request, 'login.html', context={'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = User.objects.filter(username=username)
            if username == 'admin':
                return redirect('admin')
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
        #books = Book.objects.all().group_by("category")
        #books = Book.objects.all().order_by("category")

        politics = Book.objects.filter(category='Politics')
        science = Book.objects.filter(category='Science')
        philosophy = Book.objects.filter(category='Philosophy')
        novel = Book.objects.filter(category='Novel')
        astronomy = Book.objects.filter(category='Astronomy')
        psychology = Book.objects.filter(category='Psychology')
        self_improvement = Book.objects.filter(category='Self improvement')

        context = {
            'books': [
                {'category' : 'Politics', 'books' : politics, 'color' : 'blue'},
                {'category' : 'Novel', 'books' : novel,'color':'red'},
                {'category' : 'Science', 'books' : science,'color':'yellow'},
                {'category': 'Astronomy', 'books': astronomy, 'color': 'lightgreen'},
                {'category': 'Philosophy', 'books': philosophy, 'color': 'lightpink'},
                {'category': 'Psychology', 'books': psychology, 'color': 'lightgrey'},
                {'category': 'Self improvement', 'books': self_improvement, 'color': 'darkgrey'},

            ]
        }
        return render(request, 'books.html', context=context)

    def post(self, request):
        return render(request, 'books.html')


def dashboard(request):
    user = User.objects.filter(username=request.session.get('username')).first()
    result = Borrow.objects.filter(user=user)
    messages = []
    for r in result:
        book = Book.objects.filter(id=r.book_id).first()
        return_date = r.date + timedelta(days=20)
        diff = return_date.day - datetime.datetime.now().day
        if diff >= 0:
            message = {
                'message': "You have " + str(diff) + " days to return the book " + book.title,
                'type': 1
            }
            messages.append(message)
        else:
            message = {
                'message': "You have succesfully read the book " + book.title,
                'type': 2
            }
            messages.append(message)

    context = {
        'messages': messages
    }
    return render(request, 'base.html', context=context)


def return_book(request, id):
    book = Book.objects.filter(id=id).first()
    b = Borrow.objects.filter(book=book).delete()
    return redirect('dashboard')


def author(request, id):
    author = Author.objects.filter(id=id).first()
    books = Book.objects.filter(author_id=id)
    context = {
        'author': author,
        'books': books,
    }
    return render(request, 'author.html', context=context)


def borrow(request, id):
    if not request.session.get('is_logged_in'):
        return redirect('login')
    user = User.objects.filter(username=request.session.get('username')).first()
    book = Book.objects.filter(id=id).first()
    if book.quantity <= 0:
        book.available = 0

    # borrowing
    if book.available == 1:
        book.quantity = book.quantity - 1
        borrows = Borrow.objects.create(date=datetime.datetime.now(), user=user, book=book)
    else:
        return HttpResponse("Book is not available")

    return redirect('dashboard')


def profile(request):
    user = User.objects.filter(username=request.session.get('username')).first()
    context = {
        'user': user
    }
    return render(request, 'profile.html', context=context)


def my_books(request, id):
    user = User.objects.filter(id=id).first()
    result = Borrow.objects.filter(user=user)
    books = []
    for r in result:
        book = Book.objects.filter(id=r.book_id).first()
        author = Author.objects.filter(id=book.author_id).first()
        borrowed_date = r.date
        return_date = r.date
        data = {
            'book': book,
            'author': author,
            'borrow_date': borrowed_date,
            'return_date': return_date + timedelta(days=20)
        }
        books.append(data)
    # return HttpResponse(books)
    context = {
        'books': books,
        'user': user,
        'result': result
    }
    return render(request, 'my_books.html', context=context)


def logout(request):
    del (request.session['username'])
    del (request.session['is_logged_in'])
    return redirect('index')


def settings(request):
    return render(request, 'settings.html')

def admin(request):
    m = Message.objects.filter(marked=False).count()
    books = Book.objects.all().count()
    context = {
        'length': m,
        'total_books':books,
    }
    return render(request, 'admin_dashboard.html', context=context)


def manage_books(request):
    books = Book.objects.all()
    context = {
        'books': books,
    }
    return render(request, 'admin_books.html', context=context)


def manage_users(request):
    users = User.objects.all()
    data = []
    for u in users:
        if not u.username == 'admin':
            data.append(u)
    context = {
        'users': data,
    }
    return render(request, 'admin_users.html', context=context)


def issued(request):
    result = Borrow.objects.all()
    books = []
    for r in result:
        book = Book.objects.filter(id=r.book_id).first()
        author = Author.objects.filter(id=book.author_id).first()
        user = User.objects.filter(id=r.user_id).first()
        borrowed_date = r.date
        return_date = r.date
        data = {
            'user':user,
            'book': book,
            'author': author,
            'borrow_date': borrowed_date,
            'return_date': return_date + timedelta(days=20)
        }
        if return_date <= datetime.datetime.now().date():
            books.append(data)
    context = {
        'books': books,
    }
    return render(request, 'admin_issued.html', context=context)


def archive(request):
    result = Borrow.objects.all()
    books = []
    for r in result:
        book = Book.objects.filter(id=r.book_id).first()
        author = Author.objects.filter(id=book.author_id).first()
        user = User.objects.filter(id=r.user_id).first()
        borrowed_date = r.date
        return_date = r.date
        data = {
            'user':user,
            'book': book,
            'author': author,
            'borrow_date': borrowed_date,
            'return_date': return_date + timedelta(days=20)
        }
        books.append(data)

    context = {
        'books': books,
    }
    return render(request, 'admin_archive.html',context=context)


def message(request):
    unread = Message.objects.filter(marked=False).all()

    all = Message.objects.filter(marked=True).order_by("marked")

    context = {
        'unread': unread,
        'all': all
    }
    return render(request, 'admin_messages.html', context=context)

def read_message(request,id):
    message = Message.objects.filter(id=id).update(marked=True)
    return redirect('messages')

def edit(request):
    return render(request, 'admin_edit.html')
