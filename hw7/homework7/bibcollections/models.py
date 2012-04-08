#database models

from django.db import models
from django.contrib.auth.models import User

#Collection model for file pointer and collection name
class Bibcollection(models.Model):
    name = models.CharField(max_length=200)
    #author = models.ForeignKey(User)
    bibfile = models.FileField(upload_to='documents/%y/%m/%d')

#Model for properties of individual articles
class Article(models.Model):
    collection = models.ForeignKey(Bibcollection)
    collection_name = models.CharField(max_length=200)
    itemtype = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    year = models.CharField(max_length=200)
    tag = models.CharField(max_length=200)
    volume = models.CharField(max_length=200)
    pages = models.CharField(max_length=200)
    journal = models.CharField(max_length=200)
