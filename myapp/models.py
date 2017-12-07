# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
<<<<<<< HEAD
from jsonfield import JSONField
=======
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
>>>>>>> f37822d68501b265bc5c8fb7236337b1eeb09248

# api_form = "?api_key="
# api_key = api_form + "RGAPI-cc796626-90e8-4f70-ac34-f9e41e7a40ca"
# Create your models here.

<<<<<<< HEAD
class Book(models.Model):
    isbn = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=128)
    memo = JSONField(default={}, dump_kwargs={'ensure_ascii': False})

    def __str__(self):
        return self.title
=======
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    in_game_id = models.CharField(max_length=30, blank=False, unique=False)
    account_id = models.BigIntegerField(default=0, unique=False)
    summoner_id = models.BigIntegerField(default=0, unique=False)
    follow_list = models.TextField(null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

>>>>>>> f37822d68501b265bc5c8fb7236337b1eeb09248
