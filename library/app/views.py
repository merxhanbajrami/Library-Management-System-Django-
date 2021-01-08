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
            if user:
                if user[0].password == password:
                    request.session['is_logged_in'] = True
                    request.session['username'] = username
                    if user[0].is_admin:
                        return redirect('admin')
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
        # books = Book.objects.all().group_by("category")
        # books = Book.objects.all().order_by("category")

        politics = Book.objects.filter(category='Politics')
        science = Book.objects.filter(category='Science')
        philosophy = Book.objects.filter(category='Philosophy')
        novel = Book.objects.filter(category='Novel')
        astronomy = Book.objects.filter(category='Astronomy')
        psychology = Book.objects.filter(category='Psychology')
        self_improvement = Book.objects.filter(category='Self improvement')

        context = {
            'books': [
                {'category': 'Politics', 'books': politics, 'color': 'lightblue'},
                {'category': 'Novel', 'books': novel, 'color': 'lightdark'},
                {'category': 'Science', 'books': science, 'color': 'lightyellow'},
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
    if user.is_admin:
        return redirect('admin')
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

    admin_messages = alert.objects.filter(user=user, is_read=False).all()
    events = Event.objects.filter(ended=False).all()
    my_events=[]
    for e in events:
        if datetime.datetime.now().day - e.date.day >= 0:
            e.ended = 1
        else:
            my_events.append(e)
    context = {
        'messages': messages,
        'user': user,
        'admin_messages': admin_messages,
        'events':my_events,
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
    users = User.objects.all().count()
    borrowed = Borrow.objects.all().count()
    user = User.objects.filter(username='admin').first()
    inbox = alert.objects.filter(user=user, is_read=False)
    sender = None
    if len(inbox) > 0:
        list = alert.objects.filter(subject=inbox[0].subject).all()
        for s in list:
            user = User.objects.filter(id=s.user_id).first()
            if user.username != 'admin':
                sender = user
                break
    members = User.objects.all()
    context = {
        'total_books': books,
        'total_users': users,
        'total_issued': borrowed,
        'inbox': inbox,
        'sender': sender,
        'total_inbox': len(inbox),
        'users': members,
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
            'user': user,
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
            'user': user,
            'book': book,
            'author': author,
            'borrow_date': borrowed_date,
            'return_date': return_date + timedelta(days=20)
        }
        books.append(data)

    context = {
        'books': books,
    }
    return render(request, 'admin_archive.html', context=context)


def message(request):
    unread = Message.objects.filter(marked=False).all()

    all = Message.objects.filter(marked=True).order_by("marked")

    context = {
        'unread': unread,
        'all': all
    }
    return render(request, 'admin_messages.html', context=context)


def read_message(request, id):
    message = Message.objects.filter(id=id).update(marked=True)
    return redirect('messages')


def edit(request):
    return render(request, 'admin_edit.html')


class AlertView(View):
    def get(self, request, id):
        user = User.objects.filter(id=id).first()
        context = {
            'user': user,
        }
        return render(request, 'admin_alert.html', context=context)

    def post(self, request, id):
        subject = request.POST['subject']
        content = request.POST['content']
        user = User.objects.filter(id=id).first()
        a = alert.objects.create(user=user, subject=subject, content=content, is_read=False)
        return redirect('admin')


def close(request, id):
    a = alert.objects.filter(id=id).update(is_read=True)
    return redirect('admin')


class ReplyView(View):
    def get(self, request, id):
        user = User.objects.filter(username=request.session.get('username')).first()
        case = alert.objects.filter(id=id).first()
        context = {
            'case': case,
            'user': user,
        }
        return render(request, 'user_reply.html', context=context)

    def post(self, request, id):
        c = alert.objects.filter(id=id).first()
        case = alert.objects.filter(id=id).update(is_read=True)
        content = request.POST['content']
        user = User.objects.filter(username='admin').first()
        a = alert.objects.create(user=user, subject=c.subject, content=content, is_read=False)
        return redirect("dashboard")


def event(request):
    events = Event.objects.filter(ended=False).all()
    my_events=[]
    for e in events:
        if datetime.datetime.now().day - e.date.day >= 0:
            e.ended = 1
        else:
            my_events.append(e)

    context = {
        'events': my_events
    }
    return render(request, 'admin_events.html', context=context)

def delete_event(request,id):
    event = Event.objects.filter(id=id).delete()
    return redirect('event')

def add_event(request):
    if request.method == "POST":
        name = request.POST.get('name')
        venue = request.POST.get('venue')
        date_time = request.POST.get('time')
        event = Event.objects.create(name=name, venue=venue, date=date_time, ended=False)
    return redirect('event')


def block(requset, id):
    User.objects.filter(id=id).delete()
    return redirect('manage_users')
