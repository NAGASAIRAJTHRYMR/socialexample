# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db import models
import misaka
from groups.models import Group
User=get_user_model()

# Create your models here.
class Post(models.Model):
    user=models.ForeignKey(User,related_name='posts')
    created_at=models.DateTimeField(auto_now=True)
    message=models.TextField()
    message_html=models.TextField(editable=False)
    group=models.ForeignKey(Group,related_name='posts',null=True,blank=True)

    def __str__(self):
        return self.message

    def save(self,*args, **kwargs):
        self.message_html=misaka.html(self.message)
        super(Post,self).save(*args, **kwargs)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('posts:single', kwargs={'username': self.user.username, 'pk': self.pk})

    class Meta:
        ordering=['-created_at']
        unique_together=['user','message']