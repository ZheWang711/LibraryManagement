from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *

# TODO: this function seems unused
def get_type_list():
    book_list = Record.objects.all()
    type_list = set()
    for book in book_list:
        type_list.add(book.record_subjects)
    return list(type_list)


def index(req):
    username = req.session.get('username', '')
    if username:
        user = MyUser.objects.get(user__username=username)
    else:
        user = ''
    latest_news = MyNews.objects.all().order_by('-pub_date')[0:3]

    content = {'active_menu': 'homepage', 'user': user, 'latest_news': latest_news}
    return render_to_response('index.html', content)


def signup(req):
    # if req.session.get('username', ''):
    #     return HttpResponseRedirect('/')

    status = ''
    if req.POST:
        post = req.POST
        passwd = post.get('passwd', '')
        repasswd = post.get('repasswd', '')
        if passwd != repasswd:
            status = 're_err'
        else:
            username = post.get('username', '')
            if User.objects.filter(username=username):
                status = 'user_exist'
            else:
                email = post.get('email', '')
                newuser = User.objects.create_user(username=username, password=passwd, email=email)
                newuser.save()
                new_myuser = MyUser(user=newuser, nickname=post.get('nickname'), permission=1)
                new_myuser.save()
                status = 'success'
    content = {'active_menu': 'homepage', 'status': status, 'user': ''}
    return render_to_response('signup.html', content, context_instance=RequestContext(req))


def login(req):
    if req.session.get('username', ''):
        return HttpResponseRedirect('/OE/')
    status = ''
    if req.POST:
        post = req.POST
        username = post.get('username', '')
        password = post.get('passwd', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(req, user)
                req.session['username'] = username
                return HttpResponseRedirect('/OE/')
            else:
                status = 'not_active'
        else:
            status = 'not_exist_or_passwd_err'
    content = {'active_menu': 'homepage', 'status': status, 'user': ''}
    return render_to_response('login.html', content, context_instance=RequestContext(req))

def get_son_list(current):
    son_list = MySubjectRelations.objects.filter(father_subject=current)
    return [i.child_subject for i in son_list]

def logout(req):
    auth.logout(req)
    return HttpResponseRedirect('/OE/')

# current subject name
def get_all_son_set(current, result_set):
    son = MySubjectRelations.objects.filter(father_subject=current)
    son_list = [i.child_subject for i in son]
    result_set |= set(son_list)
    if not son_list:
        return
    else:
        for i in son_list:
            get_all_son_set(i, result_set)
        return

# current subject name
def filter_by_all_subjects(current_subject):
    result_set = set()
    get_all_son_set(current_subject, result_set)
    result_list = list(result_set) + [current_subject]
    # Default record subject is multiple
    subject_objects = [Subject.objects.get(subject_name=i) for i in result_list]
    records = Record.objects.filter(record_subjects__in=subject_objects).distinct()
    return records


def record_subject_to_char(record):
    subject_object_list = record.record_subjects.all()
    charlist= [i.subject_name for i in subject_object_list]
    return charlist

def setpasswd(req):
    username = req.session.get('username', '')
    if username != '':
        user = MyUser.objects.get(user__username=username)
    else:
        return HttpResponseRedirect('/login/')
    status = ''
    if req.POST:
        post = req.POST
        if user.user.check_password(post.get('old', '')):
            if post.get('new', '') == post.get('new_re', ''):
                user.user.set_password(post.get('new', ''))
                user.user.save()
                status = 'success'
            else:
                status = 're_err'
        else:
            status = 'passwd_err'
    content = {'user': user, 'active_menu': 'homepage', 'status': status}
    return render_to_response('setpasswd.html', content, context_instance=RequestContext(req))


# TODO: implement the addbook view function
'''
def addbook(req):
    username = req.session.get('username', '')
    if username != '':
        user = MyUser.objects.get(user__username=username)
    else:
        return HttpResponseRedirect('/login/')
    if user.permission < 2:
        return HttpResponseRedirect('/')
    status = ''
    if req.POST:
        post = req.POST
        newbook = Record(
            name=post.get('name', ''),
            author=post.get('author', ''),
            typ=post.get('typ', ''),
            price=post.get('price', ''),
            pubDate=post.get('pubdate', ''),
            )
        newbook.save()
        status = 'success'
    content = {'user': user, 'active_menu': 'addbook', 'status': status}
    return render_to_response('addbook.html', content, context_instance=RequestContext(req))
'''

def viewbook(req):
    # User content
    username = req.session.get('username', '')
    if username != '':
        user = MyUser.objects.get(user__username=username)
    else:
        user = ''
    # check if the depth is 0

    # Roll Back
    back_to = req.GET.get('back', '')
    if back_to != '':
        i = 0
        for j in range(int(req.session.get('-1') + 1)):
            if req.session.get(str(i), '') == back_to:
                break
            i += 1
        back_step = int(req.session['-1']) - i
        if back_step:
            req.session['-1'] -= int(back_step)
            current_subject = req.session.get(str(req.session['-1']), 'all')
            if current_subject != 'all':
                subject_list = [current_subject] + get_son_list(current_subject)
                # TODO: a DFS before the following step
                # record_list = Record.objects.filter(record_subjects=current_subject)
                record_list = filter_by_all_subjects(current_subject=current_subject)
                keywords = ''
                page = 1
            else:
                record_list = Record.objects.all()
                keywords = ''
                page = 1
                # TODO: the outermost subject -- OE
                subject_list = Subject.objects.filter(subject_name='Ocean Engineering')

    # Step Forward
    if back_to == '':
        current_subject = req.GET.get('record_type', 'all')
        if current_subject == 'all':
            # session['0'] is the depth of browsing, which is assigned
            # to zero when browsing the 'all' type
            req.session['-1'] = 0
        if req.GET.get('forward', 0) and current_subject != req.session.get(str(req.session.get('-1')), ''):
            req.session['-1'] += 1
        req.session[str(req.session['-1'])] = current_subject
        keywords = req.GET.get('keywd', '')
        page = req.GET.get('page', 1)
        subject_list = [current_subject] + get_son_list(current_subject)

        # filtering procedure #
        # filtering by type (subject) #

        # if current_subject not in subject_list:
        if current_subject == 'all' or current_subject not in subject_list:
            record_list = Record.objects.all()
        else:
            # record_list = Record.objects.filter(record_subjects=current_subject)
            record_list = filter_by_all_subjects(current_subject=current_subject)
        record_list = record_list.filter(name__contains=keywords)
        if req.POST:
            post = req.POST
            keywords = post.get('keywords', '')
            record_list = record_list.filter(name__contains=keywords)
            # book_type = 'all'
        paginator = Paginator(record_list, 5)
        # page = req.GET.get('page')
        # filtering by page #
        try:
            record_list = paginator.page(page)
        except PageNotAnInteger:
            record_list = paginator.page(1)
        except EmptyPage:
            record_list = paginator.page(paginator.num_pages)
    # cannot_back = 1 if req.session['-1'] <= 1 else 0

    browse_depth = int(req.session['-1'])
    browse_history = [(browse_depth-i, req.session[str(i)]) for i in range(1, int(req.session['-1'])+1)]
    content = {'user': user, 'active_menu': 'viewbook', 'subject_list': subject_list,
               'book_type': current_subject, 'record_list': record_list,
               'keywords': keywords, 'currentpage': page,
               # 'cannot_back': cannot_back,
               'browse_history': browse_history, 'browse_depth': browse_depth
               }

    # return render_to_response('viewbook_new.html', content, context_instance=RequestContext(req))
    return render(req, 'viewbook_new.html', content)


def detail(req, record_id):
    username = req.session.get('username', '')
    if username != '':
        user = MyUser.objects.get(user__username=username)
    else:
        user = ''
    Id = record_id  # need refract----------------------------------------
    if Id == '':
        return HttpResponseRedirect('/viewbook/')
    try:
        record = Record.objects.get(pk=Id)
    except:
        return HttpResponseRedirect('/viewbook/')
    # TODO: delete things about image
    # img_list = Img.objects.filter(record=record)
    # content = {'user': user, 'active_menu': 'viewbook', 'record': record, 'img_list':img_list}
    record_subjects = record_subject_to_char(record)
    content = {'user': user, 'active_menu': 'viewbook', 'record': record, 'record_subjects': record_subjects}
    return render_to_response('detail.html', content)