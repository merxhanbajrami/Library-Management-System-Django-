from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    points = models.IntegerField(default=0)
    address = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=False)
    def __str__(self):
        return self.name


class Author(models.Model):
    address = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    bio = models.CharField(max_length=2000, default=None)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    available = models.BooleanField()
    category = models.CharField(max_length=200, default='Novel')
    quantity = models.IntegerField(default=1)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Borrow(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    rating = models.IntegerField()

    def __str__(self):
        return self.content

class Message(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    content = models.CharField(max_length=2000)
    marked = models.BooleanField(default=False)

    def __str__(self):
        return self.content

class alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    is_read = models.BooleanField(default=False)
    subject = models.CharField(max_length=100,default=" ")

    def __str__(self):
        return self.content


class Event(models.Model):
    name = models.CharField(max_length=200)
    venue = models.CharField(max_length=200)
    date = models.DateTimeField()
    ended = models.BooleanField(default=False)

    def __str__(self):
        return self.name