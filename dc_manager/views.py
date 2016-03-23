# Create your views here.
# -*- coding:utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from dc_manager.forms import DingCanForm
from dc_manager.models import DingCan
from dc_manager.models import DingCanPost
import datetime
from django.db.models import Sum, Count
from django.shortcuts import HttpResponse


def dingcan_list(request, template_name='dingcan/dingcan_list.html'):
    today = datetime.date.today()
    dingcans = DingCan.objects.filter(timestamp__startswith=today)
    dingcanpost = DingCanPost.objects.filter(timestamp__startswith=today)
    data = {}
    data['object_list'] = dingcans
    data['dingcanpost'] = dingcanpost
    return render(request, template_name, data)


def admin_display(request, template_name='dingcan/admin_display.html'):
    today = datetime.date.today()
    dingcans = DingCan.objects.filter(timestamp__startswith=today)
    price_sum = DingCan.objects.filter(timestamp__startswith=today).aggregate(Sum('price'))
    count_id = DingCan.objects.filter(timestamp__startswith=today).aggregate(Count('id'))
    #print count_id['id__count']
    #print price_sum['price__sum']
    data ={}
    data['object_list'] = dingcans
    data['price_sum'] = price_sum['price__sum']
    data['count_id'] = count_id['id__count']
    return render(request, template_name, data)


def dingcan_create(request, template_name='dingcan/dingcan_form.html'):
    today = datetime.date.today()
    form = DingCanForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        try:
            DingCan.objects.filter(timestamp__startswith=today).get(username=username)
        except DingCan.DoesNotExist:
            form.save()
            return redirect('dingcan_list')
        else:
            return HttpResponse("你已经点过,请勿反复提交，可返回统计页删除或编辑")

    return render(request, template_name, {'form': form})


def dingcan_update(request, pk, template_name='dingcan/dingcan_form.html'):
    dingcan = get_object_or_404(DingCan, pk=pk)
    form = DingCanForm(request.POST or None, instance=dingcan)
    if form.is_valid():
        form.save()
        return redirect('dingcan_list')
    return render(request, template_name, {'form': form})


def dingcan_delete(request, pk, template_name='dingcan/dingcan_confirm_delete.html'):
    dingcan = get_object_or_404(DingCan, pk=pk)
    if request.method == 'POST':
        dingcan.delete()
        return redirect('dingcan_list')
    return render(request, template_name, {'object': dingcan})
