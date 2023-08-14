from .models import *
from django.db.models import Max
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


def getTable():
  tables=Table.objects.all()
  table=tables.filter(available=True).first()
  if table == None:
    table=Table.objects.create(name="New Table", location="New Location", available=True)

  table.available=False
  table.save()
  return table

def getGroupId(requser):
    user=User.objects.get(id=requser.id)
    try:
        groupName=Group.objects.get(user=user)
        groupid=groupName.id
    except Group.DoesNotExist:
        groupid=0
    return groupid

def loadFeedback(order, questions):
    if Feedback.objects.filter(order=order).count() == 0:
      for question in questions:
        feedback=Feedback.objects.create(order=order, question=question, answer='')
        feedback.save()
      
      

    feedbacks=Feedback.objects.filter(order=order)
    return feedbacks