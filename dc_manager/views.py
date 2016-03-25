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
    dingcans = DingCan.objects.filter(timestamp__startswith=today).order_by('type')
    dingcanpost = DingCanPost.objects.filter(timestamp__startswith=today)
    data = {}
    data['object_list'] = dingcans
    data['dingcanpost'] = dingcanpost
    return render(request, template_name, data)


def admin_display(request, template_name='dingcan/admin_display.html'):
    today = datetime.date.today()
    dingcans = DingCan.objects.filter(timestamp__startswith=today).order_by('type')
    price_sum = DingCan.objects.filter(timestamp__startswith=today).aggregate(Sum('price'))
    count_id = DingCan.objects.filter(timestamp__startswith=today).aggregate(Count('id'))
    data ={}
    data['object_list'] = dingcans
    data['price_sum'] = price_sum['price__sum']
    data['count_id'] = count_id['id__count']
    return render(request, template_name, data)


def dingcan_create(request, template_name='dingcan/dingcan_form.html'):
    today = datetime.date.today()
    form = DingCanForm(request.POST or None)
    ip_address = get_client_ip(request)
    if form.is_valid():
        username = form.cleaned_data['username']
        try:
            DingCan.objects.filter(timestamp__startswith=today).get(username=username)
        except DingCan.DoesNotExist:
            form.save()
            return redirect('dingcan_list')
        else:
            return HttpResponse("你已经点过,请勿反复提交，"
                                "可返回 <a href=\"http://127.0.0.1:8000/dingcan/\" target=\"_blank\">统计</a>页删除或编辑")
    return render(request, template_name, {'form': form, 'ip_address': ip_address})


def dingcan_update(request, pk, template_name='dingcan/dingcan_form.html'):
    dingcan = get_object_or_404(DingCan, pk=pk)
    form = DingCanForm(request.POST or None, instance=dingcan)
    ip_address = get_client_ip(request)
    ip = DingCan.objects.filter(id=pk).values_list('ip_address')[0][0]
    if ip == ip_address:
        if form.is_valid():
            form.save()
            return redirect('dingcan_list')
        return render(request, template_name, {'form': form, 'ip_address': ip_address})
    else:
        return HttpResponse("你无权修改别人的订餐")


def dingcan_delete(request, pk, template_name='dingcan/dingcan_confirm_delete.html'):
    dingcan = get_object_or_404(DingCan, pk=pk)
    ip_address = get_client_ip(request)
    ip = DingCan.objects.filter(id=pk).values_list('ip_address')[0][0]
    if ip == ip_address:
        if request.method == 'POST':
            dingcan.delete()
            return redirect('dingcan_list')
        return render(request, template_name, {'object': dingcan, 'ip_address': ip_address})
    else:
        return HttpResponse("你无权删除别人的订餐")


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')

    return ip_address



