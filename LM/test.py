import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'LM.settings'
'''
A mapping object representing the string environment. For example, environ['HOME']
is the pathname of your home directory (on some platforms), a
nd is equivalent to getenv("HOME") in C.
'''
__author__ = 'WangZhe'
from management.models import Subject, MySubjectRelations
from management.views import filter_by_all_subjects

'''
Without adding the following 2 lines, calling
test_filter_by_all_subjects('Electrical Engineering') will
raise "django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet."
'''
import django
django.setup()

def setup_subjects_from_subject_relations():
    all_relations = list(MySubjectRelations.objects.all())
    child_subjects = {i.child_subject for i in all_relations}
    father_subjects = {i.father_subject for i in all_relations}
    all_subjects_set = child_subjects | father_subjects
    all_subjects = [i for i in all_subjects_set]
    for i in range(len(all_subjects)):
        Subject.objects.create(subject_name=all_subjects[i])

def test_filter_by_all_subjects(subject):
    a = filter_by_all_subjects(subject)
    print(a)

test_filter_by_all_subjects('Ocean Engineering')
