
from django.shortcuts import render, redirect
from .models import User,Wish
import bcrypt
import re
from django.contrib import messages
# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    # User.objects.all().delete()
    # Wish.objects.all().delete()
    # allusers = User.objects.all()
    # print "here is the list of all users:"
    # for u in allusers:
    #     print "---------"
    #     print u.id
    #     print u.username
    #     print u.password
    #     print u.date_hired
    #     print "---------"
    # allwishes = Wish.objects.all()
    # print "here is the list of all wishes:"
    # for w in allwishes:
    #     print "---------"
    #     print w.id
    #     print w.item
    #     print w.added_by
    #     print w.wished_by
    #     print "---------"
    return render(request, "belt3/index.html")


def register(request):
    if request.method != 'POST':
        print("You have gotten to this page by invalid means!")
        return redirect('/')
    wrong = False
    name = request.POST['name'].lower()
    username = request.POST['username']
    password = request.POST['password'].encode()
    confirm_password = request.POST['confirm_password'].encode()
    date_hired= request.POST['date_hired']
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    if len(name) <3 :
        wrong = True
        messages.warning(request, "Name must be at least 3 characters!")
    if len(username) <3:
        wrong = True
        messages.warning(request, "Username must be at least 3 characters!")
    if len(password) < 8:
        wrong = True
        messages.warning(request, "Password must be at least 8 characters!")
    if password != confirm_password:
        wrong = True
        messages.warning(request, "Your passwords must match!")
    if len(name)>3 and not name.isalpha():
        wrong = True
        messages.warning(request, "Name must consist of letters ONLY!")
    if len(date_hired)<1:
        wrong = True
        messages.warning(request, "Date Hired can't be left blank!")
    if wrong:
        return redirect('/')
    else:
        messages.success(request, "Registration successful! ")
        request.session['name']=name
        request.session['username'] = username
        User.objects.create(name = name, username = username, date_hired = date_hired, password= hashed)
        thisperson_list = User.objects.filter(username=username, date_hired=date_hired)
        request.session['user_id'] = thisperson_list[0].id
        return redirect('/success')

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    username_list = User.objects.filter(username=username)
    if username_list:
        hashed = username_list[0].password
        if bcrypt.hashpw(password.encode(), hashed.encode()) == hashed.encode():
            request.session['user_id'] = username_list[0].id
            request.session['name'] = username_list[0].name
            return redirect('/success')
        else:
            messages.warning(request, "Password does not match username!")
            return redirect('/')
    else:
        messages.warning(request, "Username not recognized!")
        return redirect('/')

def success(request):
    me = User.objects.get(id = request.session['user_id'])
    mywishes = Wish.objects.filter(wished_by = me)
    mywishes_ids = mywishes.values_list('id')
    otherwishes = Wish.objects.exclude(id__in=mywishes_ids)
    context = {
        "mywishes": mywishes,
        "otherwishes": otherwishes,
            }
    return render (request, "belt3/dashboard.html", context)

def addwish(request,wish_id):
    me = User.objects.get(id = request.session['user_id'])
    thiswish = Wish.objects.get(id=wish_id)
    thiswish.wished_by.add(me)
    print "-----> just created a new wish object"
    return redirect('/success')

def additem(request):
    return render (request, "belt3/wish_items_create.html")

def removewish(request,wish_id):
    thiswish = Wish.objects.get(id = wish_id)
    me = User.objects.get(id = request.session['user_id'])
    thiswish.wished_by.remove(me)
    return redirect('/success')

def showitem(request,wish_id):
    thiswish = Wish.objects.get(id=wish_id)
    print "thiswish is",thiswish.id,"which is the item", thiswish.item, "and is wished by",thiswish.wished_by.name
    wishers = thiswish.wished_by.all()
    print wishers
    context = {
        "thiswish": thiswish,
        "wishers": wishers,
        }
    return render (request, "belt3/wish_items.html", context)

def createwish(request):
    wish_text = request.POST['new_wish']
    me = User.objects.get(id = request.session['user_id'])
    Wish.objects.create(item = wish_text, added_by = me) #the wished_by field is a LIST to which you must ADD
    print "just created a new wish item"
    return redirect ('/success')

def deletewish(request, wish_id):
    thisthing = Wish.objects.get(id = wish_id)
    thisthing.delete()

def logout(request):
    del request.session['user_id']
    return redirect('/')
