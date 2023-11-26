from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import PostModel



class CreatePostForm(forms.ModelForm):

    title = forms.CharField()
    content = forms.CharField(required=False)
    img = forms.ImageField(required=False)
    class Meta:
        model = PostModel
        fields = ('title', 'content', 'img')

    def __init__(self, *args, **kwargs):
        self.user_cache = kwargs.pop('user_cache', None)
        super(CreatePostForm, self).__init__(*args,**kwargs)

    def save(self, commit=True):
        post = super(CreatePostForm, self).save(commit=False)

        if self.user_cache:
            post.user = self.user_cache['user']
        if commit:
            post.save()
        return post