# Create your views here.
# -*- coding:utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from dc_manager.forms import DingCanForm
from dc_manager.models import DingCan
from dc_manager.models import DingCanPost
import datetime
import time
from django.db.models import Sum, Count
from django.shortcuts import HttpResponse


def dingcan_list(request, template_name='dingcan/dingcan_list.html'):
    today = datetime.date.today()
    dingcans = DingCan.objects.filter(timestamp__startswith=today).order_by('type')
    dingcanpost = DingCanPost.objects.filter(timestamp__startswith=today)
    data = {}
    data['object_list'] = dingcans
    data['dingcanpost'] = dingcanpost
    form = DingCanForm(request.POST or None)
    ip_address = get_client_ip(request)
    current_time = time.mktime(datetime.datetime.now().timetuple())
    stop_time = time.mktime(DingCanPost.objects.get(timestamp__startswith=today).timestamp.timetuple())
    try:
        stop_time = time.mktime(DingCanPost.objects.get(timestamp__startswith=today).timestamp.timetuple())
    except DingCanPost.DoesNotExist:
        stop_time = None

    if stop_time is None:
        return HttpResponse("点餐还未开始")

    if current_time <= stop_time:
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                DingCan.objects.filter(timestamp__startswith=today).get(username=username)
            except DingCan.DoesNotExist:
                form.save()
                return HttpResponse("<script>alert(\"订餐成功\");window.location.assign(\"/dingcan/\")</script>")
            else:
                return HttpResponse("<script>alert(\"你已经点过,请勿反复提交,首页可编辑删除\");"
                                    "window.location.assign(\"/dingcan/\")</script>")
        data['form'] = form
        data['ip_address'] = ip_address
    else:
        return HttpResponse("点餐已结束，请联系前台妹子")
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
    current_time = time.mktime(datetime.datetime.now().timetuple())
    stop_time = time.mktime(DingCanPost.objects.get(timestamp__startswith=today).timestamp.timetuple())
    try:
        stop_time = time.mktime(DingCanPost.objects.get(timestamp__startswith=today).timestamp.timetuple())
    except DingCanPost.DoesNotExist:
        stop_time = None

    if stop_time is None:
        return HttpResponse("点餐还未开始")

    if current_time <= stop_time:
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                DingCan.objects.filter(timestamp__startswith=today).get(username=username)
            except DingCan.DoesNotExist:
                form.save()
                return redirect('dingcan_list')
            else:
                return HttpResponse("你已经点过,请勿反复提交,"
                                    "可返回 <a href=\"http://192.168.1.215:7777/dingcan/\" target=\"_blank\">统计</a>页删除或编辑")
        return render(request, template_name, {'form': form, 'ip_address': ip_address})
    else:
        return HttpResponse("点餐已结束，请联系前台妹子")


def dingcan_update(request, pk, template_name='dingcan/dingcan_form.html'):
    today = datetime.date.today()
    current_time = time.mktime(datetime.datetime.now().timetuple())
    stop_time = time.mktime(DingCanPost.objects.get(timestamp__startswith=today).timestamp.timetuple())
    if current_time <= stop_time:
        dingcan = get_object_or_404(DingCan, pk=pk)
        form = DingCanForm(request.POST or None, instance=dingcan)
        client_ip = get_client_ip(request)
        db_ip = ip = DingCan.objects.filter(id=pk).values_list('ip_address')[0][0]
        if client_ip == db_ip:
            if form.is_valid():
                form.save()
                return redirect('dingcan_list')
            return render(request, template_name, {'form': form, 'ip_address': client_ip})
        else:
            return HttpResponse("你无权修改别人的订餐")
    else:
        return HttpResponse("点餐已结束，请联系前台妹子")


def dingcan_delete(request, pk, template_name='dingcan/dingcan_confirm_delete.html'):
    today = datetime.date.today()
    current_time = time.mktime(datetime.datetime.now().timetuple())
    stop_time = time.mktime(DingCanPost.objects.get(timestamp__startswith=today).timestamp.timetuple())
    if current_time <= stop_time:
        dingcan = get_object_or_404(DingCan, pk=pk)
        client_ip = get_client_ip(request)
        db_ip = DingCan.objects.filter(id=pk).values_list('ip_address')[0][0]
        if db_ip == client_ip:
            if request.method == 'POST':
                dingcan.delete()
                return redirect('dingcan_list')
            return render(request, template_name, {'object': dingcan})
        else:
            return HttpResponse("你无权删除别人的订餐")
    else:
        return HttpResponse("点餐已结束，请联系前台妹子")


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    return ip_address
