# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField

# Create your models here.

class Book(models.Model):
    isbn = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=128)
    memo = JSONField(default={}, dump_kwargs={'ensure_ascii': False})

    def __str__(self):
        return self.title
