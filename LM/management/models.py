from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    name = models.CharField(max_length = 128)
    price = models.FloatField()
    author = models.CharField(max_length = 128)
    pubDate = models.DateField()
    typ = models.CharField(max_length = 128)

    class META:
        ordering = ['name']

    def __str__(self):
        return self.name

class MyUser(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length = 16)
    permission = models.IntegerField()
    favourite = models.ManyToManyField(Book)

    def __str__(self):
        return self.user.username

class MySubjectRelations(models.Model):
    father = models.CharField(max_length=128)
    son = models.CharField(max_length=128)

    def __str__(self):
        return self.son


# TODO: implement a "favourite" function for logged in users.
# TODO:  1.viewbooks.html template: add a "favourite" left side bar; favourite btn in the list
# TODO:  2. views.py: implement the database update and rerender (sidebar & after click)




class Img(models.Model):
    name = models.CharField(max_length = 128)
    desc = models.TextField()
    img = models.ImageField(upload_to = 'image')
    book = models.ForeignKey(Book)

    class META:
        ordering = ['name']

    def __str__(self):
        return self.name
