# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile

#from myapp.models import Book
#admin.site.register(Book)
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'is_staff', 'get_id', 'get_sum_id' , 'get_acc_id', 'get_list_follow')
    list_select_related = ('profile', )

    def get_id(self, instance):
        return instance.profile.in_game_id
    get_id.short_description = 'In-Game ID'

    def get_acc_id(self, instance):
        return instance.profile.account_id
    get_acc_id.short_description = 'Account ID'

    def get_sum_id(self, instance):
        return instance.profile.summoner_id
    get_sum_id.short_description = 'Summoner ID'

    def get_list_follow(self, instance):
        return instance.profile.follow_list
    get_list_follow.short_description = 'Follow List'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
