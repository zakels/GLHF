# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    in_game_id = models.CharField(max_length=30, blank=False, unique=True)

    # def as_json(self):
    # 	return dict(
    # 		in_game_id = self.in_game_id
    # 		)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# def create_profile(sender, **kwargs):
# 	if kwargs['created']:
# 		user_profile = Profile.objects.create(user=kwargs['instance'])

# post_save.connect(create_profile, sender=User)