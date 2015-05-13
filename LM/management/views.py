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
    book_list = Book.objects.all()
    type_list = set()
    for book in book_list:
        type_list.add(book.typ)
    return list(type_list)


def index(req):
    username = req.session.get('username', '')
    if username:
        user = MyUser.objects.get(user__username=username)
    else:
        user = ''
    content = {'active_menu': 'homepage', 'user': user}
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
        return HttpResponseRedirect('/')
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
                return HttpResponseRedirect('/')
            else:
                status = 'not_active'
        else:
            status = 'not_exist_or_passwd_err'
    content = {'active_menu': 'homepage', 'status': status, 'user': ''}
    return render_to_response('login.html', content, context_instance=RequestContext(req))

def get_son_list(current):
    son_list = MySubjectRelations.objects.filter(father=current)
    return list(son_list)

def logout(req):
    auth.logout(req)
    return HttpResponseRedirect('/')


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
        newbook = Book(
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


def viewbook(req):
    # User content
    username = req.session.get('username', '')
    if username != '':
        user = MyUser.objects.get(user__username=username)
    else:
        user = ''
    # check if the depth is 0

    # Roll Back
    # TODO: disable the roll back button when session['-1'] = 0
    if req.GET.get('back', False):
        # TODO: add subject_relation data before test
        req.session['-1'] -= 1
        current_type = req.session.get(str(req.session['-1']), all)
        type_list = [current_type] + get_son_list(current_type)
        book_lst = Book.objects.filter(typ=current_type)
        keywords = ''
        page = 1

    # Step Forward
    else:
        current_type = req.GET.get('record_type', 'all')
        if current_type == 'all':
            # session['0'] is the depth of browsing, which is assigned
            # to zero when browsing the 'all' type
            req.session['-1'] = 0
        req.session['-1'] += 1
        req.session[str(req.session['-1'])] = current_type
        keywords = req.GET.get('keywd', '')
        page = req.GET.get('page', 1)
        type_list = [current_type] + get_son_list(current_type)

        # filtering procedure #
        # filtering by type (subject) #
        if current_type not in type_list:
            book_lst = Book.objects.all()
        else:
            book_lst = Book.objects.filter(typ=current_type)
        book_lst = book_lst.filter(name__contains=keywords)
        if req.POST:
            post = req.POST
            keywords = post.get('keywords', '')
            book_lst = book_lst.filter(name__contains=keywords)
            # book_type = 'all'
        paginator = Paginator(book_lst, 5)
        # page = req.GET.get('page')
        # filtering by page #
        try:
            book_list = paginator.page(page)
        except PageNotAnInteger:
            book_list = paginator.page(1)
        except EmptyPage:
            book_list = paginator.page(paginator.num_pages)
    cannot_back = 1 if req.session['-1'] <=1 else 0
    content = {'user': user, 'active_menu': 'viewbook', 'type_list': type_list,
               'book_type': current_type, 'book_list': book_lst,
               'keywords': keywords, 'currentpage': page,
               'cannot_back': cannot_back
               }

    #return render_to_response('viewbook_new.html', content, context_instance=RequestContext(req))
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
        book = Book.objects.get(pk=Id)
    except:
        return HttpResponseRedirect('/viewbook/')
    img_list = Img.objects.filter(book=book)
    content = {'user': user, 'active_menu': 'viewbook', 'book': book, 'img_list':img_list}
    return render_to_response('detail.html', content)