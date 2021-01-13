from datetime import date, datetime

from django.shortcuts import render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.http import HttpResponse
from django.db import transaction
import requests

import xlrd
import pandas as pd
import numpy as np
from xlrd import xldate_as_tuple
import urllib
from io import BytesIO
from PIL import Image

from vueproject import settings
from .models import File,Content,User,Monitor,Picture

def parse(x):
    if x is None or x == '' or pd.isnull(x):
        return False

def parse_fun(x):
    if x is None or x == '':
        return '%s (该值不能为空！)'%x
    else:
        try:
            if not isinstance(x,str):
                return x
            else:
                return '%s (不合法数据类型！)'%x
        except:
            return '%s (不合法数据类型！)'%x

# @require_http_methods(["GET", "POST"])
# @csrf_exempt
def upload(request):
    ret = {}
    ret['row_error'] = None
    if request.method == 'POST':
        print(request.POST.get('extension'))
        print(request.FILES.get('file'))
        file_obj = request.FILES.get('file')
        name = file_obj.name
        size = file_obj.size
        ret['name'] = file_obj.name
        ret['size'] = file_obj.size

        wb = xlrd.open_workbook(filename=file_obj.name, file_contents=file_obj.read())
        table = wb.sheets()[0]
        headers = table.row_values(0)
        print(headers)
        subheaders = ['Product_category', 'Product_name', 'Address', 'Development_unit', 'Customer_manager',
                      'Opening_status', 'Order_time', 'Completion_time', 'Customer_name', 'Quantity_ordered']
        essential_headers = ['Product_name', 'Address']
        checkable = False
        if set(subheaders).issubset(headers):
            col_num = table.ncols
            datas = {}
            for i in range(col_num):
                datas[headers[i]] = table.col_values(i, start_rowx=1)
            df = pd.DataFrame(datas, columns=headers)
            df_bool = df.applymap(parse)
            not_essential_headers = list(
                set(headers).difference(set(essential_headers)))
            df_bool[not_essential_headers] = False
            checkable = not any(df_bool.any().tolist())
            if checkable:
                profile = File()
                profile.name = name
                profile.size = size
                profile.file = file_obj
                profile.save()
                print('path:', profile.file.path)

                file_path = profile.file.path
                ret['status_code'] = 0
                ret['msg'] = '文件预览'
                ret['file_path'] = file_path
                ret['file_path_id'] = profile.id

                rows = table.nrows  # 总行数
                with transaction.atomic():
                    # 获取数据表中的每一行数据写入设计好的数据库表
                    for row in range(1, rows):  # 从1开始是为了去掉表头
                        row_values = table.row_values(row)  # 每一行的数据

                        order_time_Cell = table.cell_value(row, 7)
                        ctype1 = table.cell(row, 7).ctype
                        # ctype =3,为日期
                        if ctype1 == 3:
                            date1 = datetime(*xldate_as_tuple(order_time_Cell, 0))
                            order_time = date1.strftime('%Y-%m-%d')  # (‘%Y/%m/%d %H:%M:%S‘)
                            print(order_time)

                        completion_time_Cell = table.cell_value(row, 8)
                        ctype2 = table.cell(row, 8).ctype
                        if ctype2 == 3:
                            date2 = datetime(*xldate_as_tuple(completion_time_Cell, 0))
                            completion_time = date2.strftime('%Y-%m-%d')  # (‘%Y/%m/%d %H:%M:%S‘)
                            print(completion_time)
                        if ctype2 == 0:
                            completion_time = None

                        Content.objects.create(
                            Product_category=row_values[0],
                            Product_name=row_values[1],
                            Address=row_values[2],
                            Customer_name=row_values[3],
                            Development_unit=row_values[4],
                            Customer_manager=row_values[5],
                            Opening_status=row_values[6],
                            # Order_time=row_values[7],
                            Order_time=order_time,
                            # Completion_time=row_values[8],
                            Completion_time=completion_time,
                            Quantity_ordered=row_values[9]
                        )

            else:
                df['Address'] = df['Address'].map(parse)
                df['Product_name'] = df['Product_name'].map(parse)
                rowIndex_error = np.where(df_bool)[0].tolist()
                row_error = [i + 1 for i in rowIndex_error]
                e = np.where(df_bool)
                cell_error = ['R%sC%s' % (x[0], x[1]) for x in zip(e[0] + 1, e[1] + 1)]
                ret['status_code'] = 1
                ret['msg'] = '文件预览：共发现' + str(len(row_error)) + '处错误！'
                ret['row_error'] = row_error
                ret['cell_error'] = cell_error
            html = df.to_html(index=None, classes='previewtable')
            ret['result'] = html
        else:
            ret['result'] = '错误原因：上传文件必须至少包含 “Product_category,Product_name, Address,Customer_name” 等列，具体格式请查看模板！'
            ret['status_code'] = 1
            ret['msg'] = '错误提示'
        print(ret)
        return JsonResponse(ret, safe=False)

def getLngLat(address):
    base = "http://api.map.baidu.com/geocoding/v3/?address=" + address + '&region=武汉' + "&output=json&ak=pcjTtBjhEjxY2xWXxKe1XwvuSg4vkh95"
    response = requests.get(base)
    answer = response.json()
    # print(answer)
    # print(answer['result'])
    lng = answer['result']['location']['lng']
    lat = answer['result']['location']['lat']
    return lng, lat

def showMap(request):
    if request.method == 'POST':
        userName = request.POST.get('userName')
        projectStatus = request.POST.get('projectStatus')
        beginDate_str = request.POST.get('beginDate')
        # beginDate = date(*map(int, beginDate_str.split('-')))
        endDate_str = request.POST.get('endDate')
        # endDate = date(*map(int, endDate_str.split('-')))

        search_dict = dict()
        if userName:
            search_dict['Customer_manager'] =userName
        if projectStatus:
            search_dict['Opening_status'] = projectStatus
        if beginDate_str:
            beginDate = date(*map(int, beginDate_str.split('-')))
            search_dict['Order_time__gte'] = beginDate
        if endDate_str :
            endDate = date(*map(int, endDate_str.split('-')))
            search_dict['Order_time__lte'] = endDate

        user_list = []
        user_dates = Content.objects.filter(**search_dict)
        for user in user_dates:
            json_dict = {}
            address1 = user.Address
            address = "湖北省武汉市" + address1
            # print(type(address))
            lng, lat = getLngLat(address)
            json_dict['lng'] = lng
            json_dict['lat'] = lat
            json_dict['showFlag'] = False
            json_dict['address'] = address
            json_dict['prodect_name'] = user.Product_name
            json_dict['status'] = user.Opening_status
            json_dict['customer_manager'] = user.Customer_manager
            user_list.append(json_dict)

            # print(lng,lat)

        # print(userName)
        # print(beginDate)
        # print(type(beginDate))
        # print(user_list)
        # print(Content.objects.filter(Customer_name="陈晓琴"))
        return JsonResponse(user_list,safe=False)

def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    print(username)
    print(password)
    try:
        user = User.objects.get(username=username)
    except:
        date = {'flag': 'no', "msg" : "no to user"}
        return JsonResponse({'request':date})
    if password == user.password:
        date_msg = "登陆成功"
        date_flag = "yes"
        print("成功")
    else:
        date_msg = "密码输入错误"
        date_flag = "no"
    date = {'flag': date_flag,'msg': date_msg}
    return JsonResponse({'request': date})

def addData(request):
    if request.method=='POST':
        num = int(request.POST.get('Serial_number'))
        pc = request.POST.get('Product_category')
        pn = request.POST.get('Product_name')
        ad = request.POST.get('Address')
        cn = request.POST.get('Customer_name')
        du = request.POST.get('Development_unit')
        cm = request.POST.get('Customer_manager')
        os = request.POST.get('Opening_status')
        ot = request.POST.get('Order_time')
        ct = request.POST.get('Completion_time')
        qo = request.POST.get('Quantity_ordered')
        # print(num)
        # print(type(num))

        ret = {}
        if pc=='' or pn=='' or ad=='' or cn=='' or du=='' or cm=='' or os=='' or qo=='':
            ret['success'] = False
            ret['msg'] = "注意：除完工日期外，其他项不能为空"
        if os == "未完工":
            if ct != '':
                ret['success'] = False
                ret['msg'] = "注意：未完工项目无完工日期"
            else:
                if num == 0:
                    con = Content.objects.create(
                        Product_category=pc,
                        Product_name=pn,
                        Address=ad,
                        Customer_name=cn,
                        Development_unit=du,
                        Customer_manager=cm,
                        Opening_status=os,
                        Order_time=ot,
                        Completion_time=None,
                        Quantity_ordered=qo
                    )
                    ret['success'] = True
                    ret['msg'] = "保存成功"
                    ret['id'] = con.id
                    # print(con.id)
                else:
                    con = Content.objects.filter(id=num).update(
                        Product_category=pc,
                        Product_name=pn,
                        Address=ad,
                        Customer_name=cn,
                        Development_unit=du,
                        Customer_manager=cm,
                        Opening_status=os,
                        Order_time=ot,
                        Completion_time=None,
                        Quantity_ordered=qo
                    )
                    ret['success'] = True
                    ret['msg'] = "保存成功"
        if os == "已完工":
            if ct == '':
                ret['success'] = False
                ret['msg'] = "注意：已完工项目请填写完工日期"
            else:
                ot = date(*map(int, ot.split('-')))
                ct = date(*map(int, ct.split('-')))
                print(ot)
                if ot > ct:
                    ret['success'] = False
                    ret['msg'] = "注意：完工日期应大于订单日期"
                else:
                    if num == 0:
                        con = Content.objects.create(
                            Product_category=pc,
                            Product_name=pn,
                            Address=ad,
                            Customer_name=cn,
                            Development_unit=du,
                            Customer_manager=cm,
                            Opening_status=os,
                            Order_time=ot,
                            Completion_time=ct,
                            Quantity_ordered=qo
                        )
                        ret['success'] = True
                        ret['msg'] = "保存成功"
                        ret['id'] = con.id
                    else:
                        con = Content.objects.filter(id=num).update(
                            Product_category=pc,
                            Product_name=pn,
                            Address=ad,
                            Customer_name=cn,
                            Development_unit=du,
                            Customer_manager=cm,
                            Opening_status=os,
                            Order_time=ot,
                            Completion_time=ct,
                            Quantity_ordered=qo
                        )
                        ret['success'] = True
                        ret['msg'] = "保存成功"
        return JsonResponse(ret, safe=False)
        # return JsonResponse({'success': True})

def delData(request):
    if request.method == 'POST':
        ret = {}
        con_id = request.POST.get('Serial_number')
        # print(con_id)
        if not con_id:
            ret['success'] = False
            ret['msg'] = '需要删除的数据不存在'
        else:
            Content.objects.filter(id=con_id).delete()
            ret['success'] = True
            ret['msg'] = "删除成功"
        return JsonResponse(ret, safe=False)

def uploadMonitor(request):
    ret = {}
    ret['row_error'] = None
    if request.method=='POST':
        file_obj = request.FILES.get('file')
        name = file_obj.name
        size = file_obj.size
        ret['name'] = file_obj.name
        ret['size'] = file_obj.size
        ret['msg'] = '上传成功！'

        wb = xlrd.open_workbook(filename=file_obj.name, file_contents=file_obj.read())
        table = wb.sheets()[0]
        headers = table.row_values(0)

        profile = File()
        profile.name = name
        profile.size = size
        profile.file = file_obj
        profile.save()
        print('path:', profile.file.path)

        rows = table.nrows
        for row in range(1, rows):
            row_values = table.row_values(row)
            Monitor.objects.create(
                Region = row_values[1],
                Monitor_points = row_values[2],
                Longitude = row_values[3],
                Latitude = row_values[4],
            )
    return JsonResponse(ret,safe=False)

def showMonitor(request):
    if request.method=='POST':
        region = request.POST.get('area')

        if region == '':
            monitor_data = Monitor.objects.filter()
        else:
            monitor_data = Monitor.objects.filter(Region=region)

        mon_list = []
        for m in monitor_data:
            mon_dic = {}
            mon_dic['Region'] = m.Region
            mon_dic['Monitor_points'] = m.Monitor_points
            mon_dic['lng'] = m.Longitude
            mon_dic['lat'] = m.Latitude
            mon_dic['showFlag'] = False

            # pic_data = Picture.objects.filter(pic_name=m.Monitor_points)[0]
            # path = pic_data.pic_path
            head_path = 'http://127.0.0.1:8000/media/pic_folder/'+ format(urllib.request.quote(str(m.Monitor_points),'utf-8'))+'.jpg'
            response = requests.get(head_path)
            image = Image.open(BytesIO(response.content),'r')
            img_size = image.size
            mon_dic['Image_path'] = head_path
            mon_dic['width'] = img_size[0]
            mon_dic['height'] = img_size[1]
            print(head_path)
            print(img_size[0])

            mon_list.append(mon_dic)

        return JsonResponse(mon_list, safe=False)

def uploadImage(request):
    ret = {}
    if request.method=='POST':
        pic_obj = request.FILES.get('file')
        new_pic = Picture()
        name = pic_obj.name
        size = pic_obj.size
        print(size)

        ret['name'] = name
        ret['msg'] = '上传成功'
        new_pic.pic_name = name
        new_pic.pic_size = size
        new_pic.pic_path = pic_obj
        print(new_pic.pic_path)
        new_pic.save()

        return JsonResponse(ret,safe=False)
