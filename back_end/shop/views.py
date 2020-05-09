from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.db.models import Q
from .models import *
import json


def get_all_item(request):
    if request.method == 'GET':
        res_obj = {
            'status': 'success',
            'items': []
        }
        all_item = get_list_or_404(Item)
        for item in all_item:
            res_obj['items'].append({
                'id': item.item_id,
                'name': item.item_name,
                'price': item.price,
            })
        # print(res_obj)

        return JsonResponse(res_obj)


def get_item_info(request, item_id):
    if request.method == 'GET':
        res_obj = {
            'status': 'success'
        }
        item_info = get_object_or_404(Item, pk=item_id)
        res_obj['item'] = {
            'id': item_info.item_id,
            'name': item_info.item_name,
            'price': item_info.price,
            'inventory': item_info.stockinfo.inventory,
            'description': item_info.description
        }
        # print(res_obj)

        return JsonResponse(res_obj)


def get_item_type(request):
    if request.method == 'GET':
        res_obj = {
            'status': 'success',
            'type': []
        }
        all_type = get_list_or_404(ItemType)
        for item_type in all_type:
            res_obj['type'].append({
                'id': item_type.typeid,
                'name': item_type.typename
            })
        # print(res_obj)

        return JsonResponse(res_obj)


def get_item_from_type(request, type_id):
    if request.method == 'GET':
        res_obj = {
            'status': 'success',
            'items': []
        }
        items = Item.objects.filter(typeid__typeid=type_id)
        for item in items:
            res_obj['items'].append({
                'id': item.item_id,
                'name': item.item_name,
                'price': item.price,
                'description': item.description
            })
        # print(res_obj)

        return JsonResponse(res_obj)

        
def cart(request):
    if request.method == 'GET':
        res_obj = {
            'status': 'success',
            'items': []
        }
        user = request.GET.get('user')
        with connection.cursor() as cursor:
            sql = 'SELECT item_id, item_name, price, amount, inventory ' \
                  'FROM Cart NATURAL JOIN Item NATURAL JOIN StockInfo ' \
                  'WHERE username = %s ' \
                  'ORDER BY update_time DESC'
            cursor.execute(sql, [user])
            items = cursor.fetchall()
            for item in items:
                res_obj['items'].append({
                    'id': item[0],
                    'name': item[1],
                    'price': item[2],
                    'amount': item[3],
                    'inventory': item[4]
                })

        # print(res_obj)
        return JsonResponse(res_obj)
    elif request.method == 'POST':
        info = json.loads(request.body)
        user = get_object_or_404(UserInfo, username__username=info['user'])
        item = get_object_or_404(Item, pk=info['item_id'])
        try:
            cart_item = Cart.objects.get(username=user, item_id=item)
            cart_item.amount += info['amount']
            cart_item.save()
        except Cart.DoesNotExist:
            Cart.objects.create(amount=info['amount'], username=user, item_id=item)

        res_obj = {
            'status': 'success',
            'message': '已添加到购物车'
        }
        return JsonResponse(res_obj)


def update_cart_item(request):
    update_info = json.loads(request.body)
    res_obj = {
        'status': 'success'
    }
    with connection.cursor() as cursor:
        sql = 'UPDATE Cart ' \
              'SET amount = %s ' \
              'WHERE username = %s AND item_id = %s'
        cursor.execute(sql, [update_info['amount'], update_info['user'], update_info['item_id']])
        return JsonResponse(res_obj)


def delete_cart_item(request):
    delete_info = json.loads(request.body)
    if __delete_cart_item(delete_info):
        res_obj = {
            'status': 'success',
            'message': '删除成功'
        }
    else:
        res_obj = {
            'status': 'danger',
            'message': '删除失败'
        }
    return JsonResponse(res_obj)


def __delete_cart_item(delete_info: dict) -> bool:
    try:
        with connection.cursor() as cursor:
            sql = 'DELETE FROM Cart ' \
                  'WHERE username = %s AND item_id = %s'
            cursor.execute(sql, [delete_info['user'], delete_info['item_id']])
            return True
    except:
        return False


def get_order(request):
    if request.method == 'GET':
        username = request.GET.get('user')
        user = get_object_or_404(UserInfo, username__username=username)
        order_list = Order.objects.filter(username=user).order_by('-create_time')
        status = {
            0: '待支付',
            1: '待发货',
            2: '已发货',
            3: '已完成',
            4: '已取消',
            5: '已退款',
            6: '已退货'
        }
        orders = []
        for order in order_list:
            orders.append({
                'id': order.order_id,
                'price': order.summary_price,
                'status': status[order.status]
            })

        res_obj = {
            'status': 'success',
            'orders': orders
        }
        # print(orders)
        return JsonResponse(res_obj)

    elif request.method == 'POST':
        details = json.loads(request.body)
        user = get_object_or_404(UserInfo, username__username=details['user'])
        order = Order.objects.create(username=user)
        items = details['items']
        summary_money = 0
        for item in items:
            try:
                item_info = Item.objects.get(pk=item['id'])
                item_info.stockinfo.inventory -= item['amount']
                item_info.stockinfo.save()
                summary_money += item_info.price * item['amount']
                OrderDetails.objects.create(order_id=order,
                                            item_id=item_info.item_id,
                                            item_name=item_info.item_name,
                                            price=item_info.price,
                                            amount=item['amount'])
                Cart.objects.get(username=user, item_id=item_info).delete()
            except Item.DoesNotExist:
                res_obj = {
                    'status': 'danger',
                    'message': '不存在该商品'
                }

        order.summary_price = summary_money
        order.save()

        res_obj = {
            'status': 'success'
        }

        return JsonResponse(res_obj)


def login(request):
    if request.method == 'POST':
        user_dict = json.loads(request.body)
        res_obj = {
            'status': 'success',
            'is_valid': False
        }
        try:
            user = Account.objects.get(pk=user_dict['username'])
            if user.password == user_dict['password']:
                res_obj['is_valid'] = True
            else:
                res_obj['message'] = '用户名或密码错误！'
        except Account.DoesNotExist:
            res_obj['message'] = '用户不存在！'

        return JsonResponse(res_obj)
