from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    subject_name = models.CharField(max_length=128)
    def __str__(self):
        return self.subject_name


class Record(models.Model):
    name = models.CharField(max_length=128)  # in overview
    # price = models.FloatField()
    full_link = models.CharField(max_length=128, default='unknown')
    author = models.CharField(max_length=128, default='unknown')
    pubDate = models.DateField()  # in overview
    record_subjects = models.ManyToManyField(Subject)
    OSTI_id = models.CharField(max_length=64, default='unknown')
    report_num = models.CharField(max_length=64, default='unknown')
    research_org = models.CharField(max_length=256, default='unknown')  # in overview
    sponsor_org = models.CharField(max_length=256, default='unknown')
    resource_type = models.CharField(max_length=64, default='unknown')
    pub_country = models.CharField(max_length=64, default='unknown')   # in overview
    record_description = models.CharField(max_length=1024, default='unknown')
    class META:
        ordering = ['name']
    def __str__(self):
        return self.name


class MySubjectRelations(models.Model):
    child_subject = models.CharField(max_length=128)
    father_subject = models.CharField(max_length=128)
    def __str__(self):
        return self.child_subject


class MyUser(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=16)
    permission = models.IntegerField()
    # TODO: favourite = models.ManyToManyField(Record)

    def __str__(self):
        return self.user.username


class MyNews(models.Model):
    def __str__(self):
        return self.title
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=2048)
    link = models.CharField(max_length=128, default='NULL')
    pub_date = models.DateTimeField('data published', auto_now_add=True)

# TODO: implement a "favourite" function for logged in users.
# TODO:  1.viewbooks.html template: add a "favourite" left side bar; favourite btn in the list
# TODO:  2. views.py: implement the database update and rerender (sidebar & after click)




class Img(models.Model):
    name = models.CharField(max_length = 128)
    desc = models.TextField()
    img = models.ImageField(upload_to = 'image')
    record = models.ForeignKey(Record)

    class META:
        ordering = ['name']

    def __str__(self):
        return self.name


'''
class Book(models.Model):
    name = models.CharField(max_length = 128)
    price = models.FloatField()
    author = models.CharField(max_length = 128)
    pubDate = models.DateField()
    typ = models.CharField(max_length = 128)
'''