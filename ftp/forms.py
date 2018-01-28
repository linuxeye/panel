# -*- coding: utf-8 -*-
from django import forms

from ftp.models import *

class UserForm(forms.Form):
    name = forms.CharField(label=u'用户名', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=u'密码', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    path = forms.FilePathField(label=u'根目录', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    status = forms.BooleanField(label=u'状态', required=True, initial=True) 
    comment = forms.CharField(label=u'备注', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
