from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    subject_name = models.CharField(max_length=128)
    def __str__(self):
        return self.subject_name

class Record(models.Model):
    name = models.CharField(max_length=128)  # in overview
    # price = models.FloatField()
    full_link = models.CharField(max_length=128)
    pubDate = models.DateField()  # in overview
    # TODO： important！！！ manytomany field filter
    record_subjects = models.ManyToManyField(Subject)
    OSTI_id = models.CharField(max_length=64)
    report_num = models.CharField(max_length=64)
    research_org = models.CharField(max_length=256)  # in overview
    sponsor_org = models.CharField(max_length=256)
    resource_type = models.CharField(max_length=64)
    pub_country = models.CharField(max_length=64)   # in overview
    record_description = models.CharField(max_length=1024)
    class META:
        ordering = ['name']
    def __str__(self):
        return self.name

class MyUser(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length = 16)
    permission = models.IntegerField()
    # favourite = models.ManyToManyField(Record)

    def __str__(self):
        return self.user.username

class MySubjectRelations(models.Model):
    # child_subject = models.ForeignKey(Subject)
    # father_subject = models.ForeignKey(Subject)
    child_subject = models.CharField(max_length=128)
    father_subject = models.CharField(max_length=128)
    def __str__(self):
        return self.child_subject


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