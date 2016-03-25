# -*- coding: utf-8 -*-

from django import forms
from models import DingCan
import datetime


class DingCanForm(forms.ModelForm):
    username = forms.CharField(label=u'用户名', error_messages={'required': u'认真点，还想吃饭吗?'})
    food = forms.CharField(label=u'吃点啥?', error_messages={'required': u'你不填,我怎么知道你吃什么?'})
    type = forms.CharField(label=u'上还是下?', error_messages={'required': u'嗨,别想歪了,这个得填'})
    organization = forms.CharField(label=u'部门', error_messages={'required': u'前台妹子很想认识你?'})
    price = forms.FloatField(label=u'价格', error_messages={'required': u'你鸡不鸡，这个要用来合计总价地，得填！'})
    timestamp = forms.DateTimeField(label=u'当前时间', initial=datetime.datetime.now)
    ip_address = forms.IPAddressField(label=u'IP地址')

    class Meta:
        model = DingCan
        fields = '__all__'

