from __future__ import unicode_literals
from django.db import models

class User(models.Model):
    name = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    date_hired = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

class Wish(models.Model):
    item = models.CharField(max_length = 100)
    added_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "wishes_added")
    wished_by = models.ManyToManyField(User, related_name ="wishes") #this is a list
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)



##ELI'S GUIDANCE FEB 1st 2017

#any User instance can be referenced by the wished_by attribute of many wishes.

#all the wishes added by a particular user "myself" are #addedbyme = myself.wishes_added.all()


#all the wishes that are wished for by a certain user "myself" are:
#mywishes = myself.wishes.all()

#to remove a certain user from the list of people who wish for a certain wish:
#thiswish.wished_by.remove(myself)

#to add same:
#thiswish.wished_by.add(myself)
