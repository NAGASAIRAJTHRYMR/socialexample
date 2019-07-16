# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DetailView, ListView, RedirectView
from django.views import generic
from models import Group, GroupMember
from . import models

class CreateGroup(LoginRequiredMixin,CreateView):
    fields=('name','description')
    model=Group

class SingleGroup(DetailView):
    model=Group

class ListGroups(ListView):
    model=Group

class JoinGroup(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self,*args, **kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args, **kwargs):
        group=get_object_or_404(Group,slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except IntegrityError:
            messages.warning(self.request,('Warning already a member.'))
        else:
            messages.success(self.request,'You are now a member.')
        return super(JoinGroup,self).get(request,*args, **kwargs)

class LeaveGroup(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self,*args, **kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
        
    def get(self,request,*args, **kwargs):
        try:
            membership=models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')
            ).get()
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request,'Sorry you are not in this group.')
        else:
            membership.delete()
            messages.success(self.request,'You have left the group')
        return super(LeaveGroup,self).get(request,*args, **kwargs)